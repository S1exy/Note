# 语义引导的双方向掩码精修


# 1. 引言

粗掩码中的大块漏分与误分会改变目标的范围：物体主体或附属结构可能被遗漏，背景和邻近物体也可能被并入前景。面对这类错误，分割精修需要依据图像重新判断区域归属，同时补回缺失前景、清除多余区域。粗掩码在这一过程中既提供了目标线索，也携带需要被纠正的区域判断。如何利用这些线索，从存在显著区域偏差的初始预测中恢复完整、精细的目标，是本文研究的核心问题。

已有研究通过多尺度预测、细粒度特征融合和稀疏位置修正提高掩码质量[3,8,10,22]。SegRefiner 以条件离散去噪建模粗到精的转换[20]，SAMRefiner 与 PromptMoE 借助 SAM 从粗掩码及图像中构造提示，引导目标恢复[11,12,19]。QuBER 通过边界错误分类指导修正[1]，Phoenix 利用对抗扰动与对比学习增强精修训练[9]。本文从纠错动作出发，将补全与删除的职责直接写入过程监督。最终掩码给出了正确的目标区域，而两类修正在不同位置发生，也可以处于不同的完成阶段。为它们分别建立参考进度，可以让训练目标明确描述各个阶段应执行的修正位置与幅度。

粗掩码与真实掩码的并集、交集为这种监督提供了直接构造。设两者分别为 (C) 和 (Y)，并集 (C\cup Y) 补入全部初始遗漏，同时保留粗掩码中的原有区域；交集 (C\cap Y) 清除全部初始多余，同时保留二者的共同前景。二者与 (C)、(Y) 共同构成四个锚点，分别表示初始状态、完成补全、完成删除，以及两类修正均完成的状态。以补全和删除的进度为两个坐标，这四个锚点便能描述两类操作分别推进的参考过程。由此，一对已有掩码标注即可提供具有明确纠错含义的过程监督，无需额外标注中间修正步骤。

基于这一构造，我们提出集合语义引导的双方向掩码精修方法。我们将四个锚点转换为统一距离尺度下的截断符号距离场，并通过双线性插值建立二维参考曲面。集合包含关系使参考补全方向对应前景增加，参考删除方向对应前景减少。利用曲面的解析形式，我们进一步计算给定进度区间上的平均修正目标，监督模型预测两类方向场，再按各自的进度跨度合成状态更新。模型在参考状态和自身递归产生的状态上学习后续修正，从而将补全、删除及其联合执行纳入同一精修过程。

大范围区域恢复需要目标整体形态与图像上下文，精确定位轮廓和细小结构则需要局部空间信息。为此，我们构建共享双方向目标的区域—细节预测器。区域分支结合冻结的 DINOv 2-S 表征[17]与掩码状态，判断需要恢复或清除的整体范围；细节分支在原生分辨率窗口中预测局部残差，调整边界与细小结构。两者共同生成每次更新的补全场与删除场，使区域判断和局部定位服务于同一纠错目标。整个模型包含 33.24 M 参数，直接从图像与粗掩码预测修正场。

在 BIG、VOC、ECSSD 和 MSRA-B 的真实粗掩码上，本方法表现出突出的区域恢复能力。对于初始 IoU 处于 (10%, 50%) 的困难输入，相较于相同输入下的 PromptMoE，四个数据集的精修后平均 IoU 分别提高 19.04、16.30、15.29 和 13.01 个百分点。在 VOC 整体精修评测中，本方法的 IoU 与 BIoU 分别高出 PromptMoE 3.35 和 2.72 个百分点，同时提高目标区域与边界质量。同结构参考监督对照和方向场干预进一步表明，四锚点监督在提高精修质量的同时，使两个预测场形成了明确的补全与删除分工。

本文的主要贡献如下：

- 提出面向区域纠错的四锚点参考过程，利用粗掩码与真实掩码的并集、交集，为补全和删除建立各自的参考进度，将已有区域标注转化为具有操作语义的过程监督。
    
- 构建解析的双方向区间监督与区域—细节预测器，使全局区域判断和原生局部残差共同执行补全与删除，兼顾大范围区域恢复和精细轮廓定位。
    
- 在四个数据集的困难粗掩码上，相对 PromptMoE 取得 13.01 至 19.04 个百分点的精修后平均 IoU 优势，并在 VOC 整体评测中同时提升区域与边界精度，验证了集合语义过程监督对目标恢复的有效性。
## 2. 相关工作

*本节暂留，后续补充。*

## 3. 方法
![[Pasted image 20261021205827.png]]

给定图像$I\in\mathbb{R}^{H\times W\times3}$及上游掩码$S\in[0,1]^{H\times W}$，我们的目标是预测精修后的二值掩码$\widehat C$。记$C=\mathbf1[S\geq0.5]$为粗前景集合，$Y$为训练标注，$\Omega$为原图像素域。方法包含三个相互衔接的部分：集合关系定义参考曲面，解析区间目标监督两个修正方向，区域—细节预测器根据图像与当前状态执行更新。

### 3.1. 四锚点语义参考过程

**集合状态与距离表示。** 我们以$U=C\cup Y$和$J=C\cap Y$分别表示补全参考与删除参考。$U\setminus C=Y\setminus C$恰为初始遗漏前景，$C\setminus J=C\setminus Y$恰为初始多余前景。两个中间状态由同一对掩码直接确定，分别保留另一类尚未完成的纠错需求。

为连续描述状态变化，我们采用前景为正的截断符号距离场。对集合$A\subseteq\Omega$，定义

$$
s_\rho(A)(x)=
\operatorname{clip}_{[-1,1]}
\left(\frac{d(x,A^{c})-d(x,A)}{\rho}\right),
\qquad \rho=\frac{\max(H,W)}{64},
\tag{1}
$$

其中$d(x,A)$为最近像素距离，$A^c$表示$\Omega$内的补集；空集和全图分别映射为常数$-1$和$+1$。同一图像的四个锚点共用$\rho$，局部窗口也沿用原图中的距离值。这样，全局预测与局部修正具有相同的数值单位。

**二维参考曲面。** 记$c=s_\rho(C)$、$u=s_\rho(U)$、$j=s_\rho(J)$和$y=s_\rho(Y)$。令$a,b\in[0,1]$分别表示补全和删除的参考进度，构造

$$
\Phi(a,b)=(1-a)(1-b)c+a(1-b)u+(1-a)bj+aby.
\tag{2}
$$

曲面的四个角依次满足$\Phi(0,0)=c$、$\Phi(1,0)=u$、$\Phi(0,1)=j$和$\Phi(1,1)=y$。内部状态是距离表示空间中的插值场，其零阈值对应当前参考前景。改变两个坐标，可以得到补全与删除处于不同进度的训练状态。

**参考方向的操作含义。** 集合包含关系在共同距离尺度下给出逐像素不等式$j\leq c\leq u$和$j\leq y\leq u$。因此，

$$
\begin{aligned}
\partial_a\Phi(a,b)&=(1-b)(u-c)+b(y-j)\geq0,\\
\partial_b\Phi(a,b)&=(1-a)(j-c)+a(y-u)\leq0.
\end{aligned}
\tag{3}
$$

固定$b$并增加$a$，参考前景不会缩小；固定$a$并增加$b$，参考前景不会扩大。若$C\subseteq Y$，则$j=c$、$u=y$，参考删除场恒为零；若$Y\subseteq C$，参考补全场恒为零。两种错误同时存在时，每个方向的幅度还取决于另一方向的进度。上述性质规定了参考监督的含义，并通过方向回归传递给预测器。

### 3.2. 解析的双方向区间监督

瞬时方向描述局部进度变化，一次实际更新则需要跨越有限区间。借鉴区间平均场的建模思想[5]，我们为任意起点$p=(a_0,b_0)$和终点$q=(a_1,b_1)$构造平均修正目标，其中$0\leq p\leq q\leq1$按坐标成立。记$\Delta a=a_1-a_0$、$\Delta b=b_1-b_0$，连接路径为$\gamma(t)=p+t(q-p)$，区间中点为$(\bar a,\bar b)=(p+q)/2$。两个目标定义为

$$
\begin{aligned}
V_+^{p\rightarrow q}
&=\int_0^1\partial_a\Phi(\gamma(t))\,dt
 =(1-\bar b)(u-c)+\bar b(y-j),\\
V_-^{p\rightarrow q}
&=\int_0^1\partial_b\Phi(\gamma(t))\,dt
 =(1-\bar a)(j-c)+\bar a(y-u).
\end{aligned}
\tag{4}
$$

由于$\Phi$为双线性函数，两个偏导沿$\gamma$均为$t$的一次函数，故区间平均可以由中点精确计算。对$\Phi(\gamma(t))$应用链式法则并积分，得到

$$
\Phi(q)-\Phi(p)
=\Delta a\,V_+^{p\rightarrow q}
+\Delta b\,V_-^{p\rightarrow q}.
\tag{5}
$$

因此，两个方向目标与完整参考位移严格对应。即使某一坐标跨度为零，式（4）的目标仍有定义，合成时该方向的贡献由跨度置零。这里的方向指纠错进度，场值表示每单位相应进度引起的像素距离值变化。

预测器以图像、初始掩码及当前状态$z$为条件，输出$\widehat V_+$与$\widehat V_-$：

$$
\begin{aligned}
(\widehat V_+,\widehat V_-)
&=F_\theta(I,S,c,z,p,q),\\
T_\theta(z;p,q)
&=z+\Delta a\,\widehat V_+
       +\Delta b\,\widehat V_-.
\end{aligned}
\tag{6}
$$

我们直接用式（4）分别监督两个输出，并同时约束式（6）的合成状态。这样，每个分支具有确定的参考目标，状态损失则检验两类修正的联合结果。不同起止进度共享同一预测器，区间跨度通过条件输入和更新权重共同参与计算。

### 3.3. 区域—细节预测器

**区域修正。** 图像与掩码首先缩放到$448\times448$。冻结的DINOv2-S/14编码器[17]提供第3、6、9和12层图像特征，卷积分支从RGB与软掩码$S$提取空间信息。投影和逐级融合得到通道数为192、分辨率分别为$112^2$、$56^2$和$28^2$的特征。当前状态$z$、初始场$c$与$S$共同编码为状态特征；四个起止坐标及其正弦、余弦编码映射为128维区间条件。

补全与删除分支从共享特征出发，分别加入方向嵌入，经三层跨尺度特征读取与分支交互后输出区域场$G_+$、$G_-$及非负修正需求$N_+$、$N_-$。每层采用六个读取头，每头在三个尺度上分别读取四个学习位置；两个方向通过共享交互特征交换信息。区域场双线性插值到原图网格，形成临时更新

$$
\widetilde z=z+\Delta a\,G_++\Delta b\,G_-.
\tag{7}
$$

**原生窗口残差。** 为补充区域场在局部位置的修正，我们在原图上使用$256\times256$窗口，并以约128像素间距构造候选中心。对于候选网格单元$k$，定义方向$d\in\{+,-\}$的需求评分为$\Delta_d\operatorname{MaxPool}_k(N_d)$，其中$\Delta_+=\Delta a$、$\Delta_-=\Delta b$。每个方向依次选择至多三个高分位置并去重；剩余名额用于空间覆盖，训练时随机抽取，推理时按固定均匀位置补齐。每次更新最多使用八个窗口。

局部编码—解码器接收窗口RGB、两倍范围的图像上下文，以及同位置的$(z,c,S,G_+,G_-,\widetilde z)$。扩大的上下文缩放为$256\times256$，状态与输出保持原生像素网格。对应的区域语义特征注入局部瓶颈，区间条件调制局部计算，最终输出两通道残差$r_{k,+}$和$r_{k,-}$。重叠窗口通过Hann权重融合：

$$
R_d(x)=
\frac{\sum_k w_k(x)r_{k,d}(x)}
{\max\{\sum_k w_k(x),\epsilon\}},
\qquad
\widehat V_d(x)=G_d(x)+R_d(x).
\tag{8}
$$

其中$w_k$为窗口内的二维可分离权重，窗口外取零；一维Hann权重下限为0.05，$\epsilon=10^{-6}$。未覆盖位置的残差为零。区域场与局部残差共同估计式（4）的两个方向目标，并通过式（6）执行一次更新。

### 3.4. 参考监督与递归训练

**参考状态上的监督。** 对采样区间$(p,q)$，令$z=\Phi(p)$，记$V=(V_+,V_-)$、$\widehat V=(\widehat V_+,\widehat V_-)$。以$M$表示有效标注区域。对具有$D$个通道的量$X$，定义加权平均$\langle X\rangle_M=\sum_{x,d}M(x)X_d(x)/\max\{D\sum_xM(x),1\}$。方向与状态损失为

$$
\begin{aligned}
\mathcal L_{\mathrm{field}}
&=\left\langle(\widehat V-V)^2\right\rangle_M,\\
\mathcal L_{\mathrm{state}}
&=\left\langle
\left|T_\theta(\Phi(p);p,q)-\Phi(q)\right|
\right\rangle_M.
\end{aligned}
\tag{9}
$$

包含无效标注时，我们以有效像素的最近邻标签延拓$Y$用于距离计算，并以$M$限定损失区域。粗掩码距离场$c$始终由输入掩码单独计算。

区域场、局部残差与需求预测还接受相应的辅助监督。设$\mathcal A$为到需求网格的区域平均池化，定义有效区域归一化算子

$$
\mathcal A_M(X)=
\frac{\mathcal A(XM)}{\max\{\mathcal A(M),10^{-8}\}},
\qquad M_\ell=\mathcal A(M).
\tag{10}
$$

记$G=(G_+,G_-)$、$R=(R_+,R_-)$，残差目标为$R^*=V-\operatorname{sg}(G)$，其中$\operatorname{sg}$表示停止梯度；$P$表示所选窗口覆盖的原图区域。三个辅助项为

$$
\begin{aligned}
\mathcal L_{\mathrm{region}}
&=\left\langle
  \big(\mathcal A_M(G)-\mathcal A_M(V)\big)^2
  \right\rangle_{M_\ell},\\
\mathcal L_{\mathrm{detail}}
&=\left\langle(R-R^*)^2\right\rangle_{MP},\\
N^*&=\operatorname{MaxPool}(|R^*|M),\\
\mathcal L_{\mathrm{need}}
&=\left\langle
 \left|\log(1+N)-\log(1+\operatorname{sg}(N^*))\right|
 \right\rangle_{M_\ell}.
\end{aligned}
\tag{11}
$$

MaxPool逐方向产生与$N$同分辨率的需求目标。区域项约束整体修正，细节项在已覆盖位置学习尚未由区域场解释的残差，需求项学习这些残差的空间分布。参考监督合成为

$$
\begin{aligned}
\mathcal L_{\mathrm{ref}}
={}&\mathcal L_{\mathrm{field}}+\mathcal L_{\mathrm{state}}\\
&+0.25(\mathcal L_{\mathrm{region}}+\mathcal L_{\mathrm{detail}})
+0.1\mathcal L_{\mathrm{need}}.
\end{aligned}
\tag{12}
$$

**预测状态上的递归监督。** 实际推理从模型自己的预测状态继续更新。为使训练覆盖这一过程，我们另从$z_0=c$出发，沿$p_k=(k/K,k/K)$执行$K$次更新：

$$
z_{k+1}=T_\theta(z_k;p_k,p_{k+1}),
\qquad k=0,\ldots,K-1.
\tag{13}
$$

全部更新参与反向传播。令$Q_K=\sigma(z_K/0.1)$，终态同时接受距离、像素分类与区域重叠监督：

$$
\begin{aligned}
\mathcal L_{\mathrm{end}}
={}&\langle|z_K-y|\rangle_M
+\langle\operatorname{BCELogits}(z_K/0.1,Y)\rangle_M\\
&+1-
\frac{2\sum_x M(x)Q_K(x)Y(x)+1}
{\sum_x M(x)Q_K(x)+\sum_x M(x)Y(x)+1}.
\end{aligned}
\tag{14}
$$

对中间预测状态，使用同进度参考场进行对齐：

$$
\mathcal L_{\mathrm{inter}}=
\begin{cases}
\displaystyle\frac{1}{K-1}
\sum_{k=1}^{K-1}\langle|z_k-\Phi(p_k)|\rangle_M,
&K>1,\\
0,&K=1.
\end{cases}
\tag{15}
$$

最终目标为

$$
\mathcal L=
\mathcal L_{\mathrm{ref}}
+\mathcal L_{\mathrm{end}}
+0.25\mathcal L_{\mathrm{inter}}.
\tag{16}
$$

区间采样以20%、40%、20%和20%的比例覆盖原点、终点、单轴与内部区间。终点类中的一半样本进一步使起点的两个坐标围绕共同均值反向偏移，增加两类纠错进度不一致的状态。递归训练在前两轮使用$K=1$，此后从$\{1,2,3,4\}$中均匀采样$K$。参考分支学习具有解析目标的方向更新，递归分支学习在实际预测状态上完成目标恢复，两者共享全部预测参数。

### 3.5. 推理

推理首先编码图像与初始掩码，并在后续更新中复用图像特征。从$z_0=c$出发，我们固定采用三个对角区间，依次使用$p_k=(k/3,k/3)$、$k=0,1,2,3$，按照式（13）更新状态。每一步根据当前$z_k$与相应区间重新预测区域场、需求位置及局部残差，最终输出

$$
\widehat C(x)=\mathbf1[z_3(x)>0].
\tag{17}
$$

推理条件由图像、上游掩码、当前预测状态和预设进度构成。四锚点与解析区间目标用于训练监督；部署时直接由同一预测器完成三次区域—细节更新，输出原生分辨率掩码。该实现共33.24M参数，其中11.19M参与训练，其余为冻结的视觉编码器。

## 4. 实验

我们围绕整体精修性能、显著区域错误的恢复，以及参考监督形成的修正行为展开评估。总体比较采用BIG与VOC，区域恢复分析进一步覆盖ECSSD和MSRA-B；同结构监督对照与固定模型干预用于检验方法中的参考构造和空间细化。

### 4.1. 实验设置

**数据与粗掩码。** 我们沿用PromptMoE[19]的任务清单与来源划分。BIG[3]和VOC[4]分别包含283和5408项图像—目标—coarse任务，采用DeepLabV3-ResNet101、FCN-ResNet50[15]及LR-ASPP-MobileNetV3-Large[7]三种输入。各来源对应的任务数列于表1。ECSSD[21]与MSRA-B[14]使用RMBG-1.4和BiRefNet-matting[23]两种来源，分别有2000和10000项任务，用于下文明确范围的区域恢复分析。

**训练与推理。** 模型在VOC训练划分的1464张图像、6510项配对任务上学习。优化器为AdamW[16]，初始学习率为$2\times10^{-4}$，权重衰减为0.01，有效批量为16；采用两轮预热与按150轮预算设置的余弦调度。每五轮在VOC验证划分的1449张图像、6444项任务上评价，按来源等权IoU选择EMA模型，主表使用第55轮检查点。VOC主表的5408项任务为该验证划分中的对齐子集。本文方法统一采用448全局输入、最多八个256原生窗口与三步推理。

**比较方法与评价指标。** 我们比较CascadePSP[3]、SegRefiner-HR[20]、DualSight[18]、SAMRefiner[12]和PromptMoE-Full[19]。SegRefiner-HR采用PromptMoE公开CSV的报告值并标记为†；其余方法在共享输入上运行，各自保留对应推理配置。所有指标在原图网格上计算。IoU采用全图二值区域重叠，对称BIoU沿用PromptMoE实现：以膨胀与腐蚀的异或构造边界带，使用半径$r=\max(1,\lfloor0.02\sqrt{H^2+W^2}\rfloor)$的方形结构元。表1先在来源内求任务均值，再对来源等权平均；表2及诊断分析采用各自任务集合内的算术均值。

### 4.2. 不同上游预测的整体精修结果

表1展示两套基准在不同coarse来源下的结果。本文方法在VOC三个来源上均取得表中最高的IoU与BIoU，来源平均达到77.97和73.19，分别比PromptMoE高3.35和2.72个百分点。对于FCN与LR-ASPP输入，IoU由62.35和64.77提升至77.31和78.35，说明恢复收益能够出现在不同上游预测中。

**表1．BIG与VOC上的整体精修结果。** 每格为IoU / BIoU（%），粗体标出各列各指标的最高值。括号为任务数，参数量单位为M。

**（a）BIG。**

| 方法 | 参数（M） | DeepLabV3（97） | FCN（96） | LR-ASPP（90） | 来源平均 |
|---|---:|---:|---:|---:|---:|
| Coarse | — | 84.05 / 76.50 | 74.35 / 65.67 | 76.36 / 68.18 | 78.25 / 70.12 |
| CascadePSP[3] | 67.68 | 87.04 / 79.89 | 80.74 / 73.46 | 81.92 / 75.87 | 83.23 / 76.40 |
| SegRefiner-HR†[20] | 119.05 | **89.80** / **84.71** | **87.68** / **82.41** | 85.91 / 80.75 | **87.80** / **82.62** |
| DualSight[18] | 641.09 | 82.94 / 75.54 | 80.29 / 73.42 | 81.33 / 74.11 | 81.52 / 74.36 |
| SAMRefiner[12] | 641.09 | 85.99 / 80.64 | 84.07 / 78.24 | 85.18 / 79.95 | 85.08 / 79.61 |
| PromptMoE[19] | 1932.88 | 88.22 / 82.72 | 84.89 / 79.25 | 86.77 / 81.07 | 86.63 / 81.01 |
| 本文方法 | 33.24 | 87.44 / 81.84 | 87.64 / 82.04 | **87.06** / **81.64** | 87.38 / 81.84 |

**（b）VOC。**

| 方法 | 参数（M） | DeepLabV3（1846） | FCN（1869） | LR-ASPP（1693） | 来源平均 |
|---|---:|---:|---:|---:|---:|
| Coarse | — | 73.07 / 66.32 | 62.35 / 57.54 | 64.77 / 56.38 | 66.73 / 60.08 |
| CascadePSP[3] | 67.68 | 73.21 / 64.94 | 65.61 / 59.85 | 66.49 / 57.63 | 68.44 / 60.81 |
| SegRefiner-HR†[20] | 119.05 | 65.83 / 59.67 | 61.15 / 56.64 | 61.63 / 54.78 | 62.87 / 57.03 |
| DualSight[18] | 641.09 | 72.83 / 69.40 | 68.19 / 65.25 | 69.54 / 64.48 | 70.19 / 66.38 |
| SAMRefiner[12] | 641.09 | 76.46 / 72.20 | 71.65 / 68.36 | 73.26 / 68.97 | 73.79 / 69.84 |
| PromptMoE[19] | 1932.88 | 77.49 / 73.02 | 72.29 / 69.05 | 74.08 / 69.33 | 74.62 / 70.47 |
| 本文方法 | 33.24 | **78.25** / **73.60** | **77.31** / **72.88** | **78.35** / **73.09** | **77.97** / **73.19** |

### 4.3. 显著区域错误的恢复

**困难输入。** 为考察初始区域偏差较大时的恢复能力，我们取各数据集中初始IoU位于$[10\%,50\%)$的全部已有任务，以共享输入上的PromptMoE作为对照。表2中，本文方法在四个数据集上均取得更高的精修后IoU与BIoU，IoU优势为13.01至19.04个百分点。BIG与VOC的平均输入IoU分别为33.93和31.47，本文方法将其恢复至70.68和62.38。ECSSD与MSRA-B上的对应结果进一步表明，这一困难输入恢复能力能够出现在不同的粗掩码来源和图像分布中。

**表2．初始IoU位于$[10\%,50\%)$的任务上的区域恢复。** 每格为IoU / BIoU（%），$\Delta$表示本文方法相对PromptMoE的百分点差。所有数值均在表中对应的相同任务集合上计算。

| 数据集 | 任务数 | Coarse | PromptMoE | 本文方法 | ΔIoU / ΔBIoU |
|---|---:|---:|---:|---:|---:|
| BIG | 38 | 33.93 / 41.44 | 51.64 / 53.08 | **70.68 / 71.47** | +19.04 / +18.38 |
| VOC | 1111 | 31.47 / 40.84 | 46.09 / 52.36 | **62.38 / 67.66** | +16.30 / +15.29 |
| ECSSD | 212 | 32.74 / 22.11 | 43.60 / 41.48 | **58.89 / 50.08** | +15.29 / +8.60 |
| MSRA-B | 1744 | 30.91 / 19.30 | 35.78 / 30.76 | **48.79 / 39.04** | +13.01 / +8.28 |

**目标内部的遗漏。** 区域恢复还应覆盖目标内部的缺失。我们在第4.4节定义的固定诊断集上，以$FN_{\mathrm{in}}=\{x\in Y\setminus C:d(x,Y^c)>\rho\}$表示远离GT边界的初始漏分，其中$\rho=\max(H,W)/64$。在具有这类错误的166项任务上，本文方法的逐任务平均恢复率为72.73%，PromptMoE为46.45%，提高26.28个百分点。该结果说明，本方法的有效修正能够到达目标内部，而不仅体现为紧邻GT轮廓的位置调整。

### 4.4. 参考监督与纠错行为分析

**参考构造的作用。** 我们保持预测器结构、输入与损失形式一致，将中间参考锚点替换为$m=(c+y)/2$。相应参考曲面退化为$\Phi_{\mathrm{mid}}(a,b)=c+\frac{a+b}{2}(y-c)$，两个方向的解析目标均为$(y-c)/2$。表3(a)比较两种监督在第45轮、完整VOC6444任务上的三步结果。四锚点参考相较中点参考提高0.48 IoU和1.17 BIoU，支持利用集合关系组织中间参考状态。

**方向是否体现操作分工。** 我们从初始IoU位于$[10\%,80\%)$的任务中，按数据集、来源与初始错误类型分层，每层按固定哈希顺序选取至多八项，得到223项、193张原图的诊断集。记$FN=Y\setminus C$、$FP=C\setminus Y$为初始错误集合；$|FN|\geq2|FP|$为漏分主导，$|FP|\geq2|FN|$为多分主导，其余为混合错误。对每项任务，在$p=(0,0)$、$q=(1,1)$的一次调用中预测两个场，再固定这两个输出，分别只保留补全场或删除场合成掩码。

对输出$\widehat C$，统计$|\widehat C\cap FN|/|FN|$与$|\widehat C^c\cap FP|/|FP|$，分别衡量原有漏分的修复和原有多分的清除。表3(b)显示，四锚点模型的补全场主要作用于FN，删除场主要作用于FP；中点参考的两个分支则呈现相近的修正比例。这将参考状态中的操作含义与模型实际执行的方向行为联系起来。

**表3．监督构造、方向行为与原生细节分析。** (a)为相同轮次的监督对照；(b)为一次调用内固定预测场的干预；(c)为固定E55权重的三步推理模块干预。

**（a）同结构、同轮次参考监督对照：VOC6444，E45。**

| 参考监督 | IoU ↑ | BIoU ↑ |
|---|---:|---:|
| 中点参考 | 72.42 | 68.34 |
| 四锚点参考 | **72.90** | **69.52** |

**（b）方向场干预：固定223项诊断任务。**

| 参考监督 | 单独保留的方向 | FN修复率 | FP清除率 |
|---|---|---:|---:|
| 四锚点 | 补全场 | 64.88 | 1.75 |
| 四锚点 | 删除场 | 1.41 | 55.56 |
| 中点 | 分支1 | 21.05 | 24.93 |
| 中点 | 分支2 | 21.97 | 25.49 |

修复率为逐任务平均百分比。FN和FP统计分别包含200和221项非零初始错误任务；两种模型使用相同任务及分母。四锚点模型采用E55，中点模型采用E45。

**（c）原生细节残差：同一223项诊断任务，三步推理。**

| 固定模型的推理设置 | IoU ↑ | BIoU ↑ |
|---|---:|---:|
| 仅区域场 | 66.36 | 64.57 |
| 区域场＋原生细节残差 | **68.26** | **66.78** |

**原生细节的作用。** 在同一诊断集上，我们保持E55参数与输入不变，分别执行仅区域场更新和完整区域—细节更新。启用细节残差后，IoU与BIoU分别提高1.90和2.22个百分点，说明局部原生证据能够进一步改善同一纠错过程的输出。

![图1：固定同次预测场的方向干预](D:/Code/codex/10.8/outputs/paper_intro_method_20261021/assets/direction_intervention.png)

**图1．补全与删除的定性干预。** 从左至右为图像、coarse、仅补全、仅删除、联合更新与GT。绿色、橙色和粉色分别表示正确前景、漏分和多分，图中数值在原图网格上计算。三个样例展示漏分、多分与混合错误下的方向作用；两个场均来自同一次完整区间调用。玻璃杯的两类错误同时存在，单独补全或删除的IoU分别为94.30和67.16，联合更新达到98.32。

## 参考文献

[1] Seunghyeok Back, Sangbeom Lee, Kangmin Kim, Joosoon Lee, Sungho Shin, Jemo Maeng, and Kyoobin Lee. [High-Quality Unknown Object Instance Segmentation via Quadruple Boundary Error Refinement](https://ieeexplore.ieee.org/document/11127393). In *IEEE International Conference on Robotics and Automation (ICRA)*, pages 13574–13581, 2025.

[2] Lea Bogensperger, Dominik Narnhofer, Alexander Falk, Konrad Schindler, and Thomas Pock. [FlowSDF: Flow Matching for Medical Image Segmentation Using Distance Transforms](https://link.springer.com/article/10.1007/s11263-025-02373-y). *International Journal of Computer Vision*, 133(7):4864–4876, 2025.

[3] Ho Kei Cheng, Jihoon Chung, Yu-Wing Tai, and Chi-Keung Tang. [CascadePSP: Toward Class-Agnostic and Very High-Resolution Segmentation via Global and Local Refinement](https://openaccess.thecvf.com/content_CVPR_2020/html/Cheng_CascadePSP_Toward_Class-Agnostic_and_Very_High-Resolution_Segmentation_via_Global_and_CVPR_2020_paper.html). In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 8890–8899, 2020.

[4] Mark Everingham, Luc Van Gool, Christopher K. I. Williams, John Winn, and Andrew Zisserman. [The Pascal Visual Object Classes (VOC) Challenge](https://link.springer.com/article/10.1007/s11263-009-0275-4). *International Journal of Computer Vision*, 88(2):303–338, 2010.

[5] Zhengyang Geng, Mingyang Deng, Xingjian Bai, Zico Kolter, and Kaiming He. [Mean Flows for One-step Generative Modeling](https://papers.neurips.cc/paper_files/paper/2025/hash/6d13e085b79d454da5910e4ca82a3d9d-Abstract-Conference.html). *Advances in Neural Information Processing Systems*, 38:75460–75482, 2025.

[6] Kaiming He, Georgia Gkioxari, Piotr Dollár, and Ross Girshick. [Mask R-CNN](https://openaccess.thecvf.com/content_iccv_2017/html/He_Mask_R-CNN_ICCV_2017_paper.html). In *Proceedings of the IEEE International Conference on Computer Vision (ICCV)*, pages 2961–2969, 2017.

[7] Andrew Howard, Mark Sandler, Grace Chu, Liang-Chieh Chen, Bo Chen, Mingxing Tan, Weijun Wang, Yukun Zhu, Ruoming Pang, Vijay Vasudevan, Quoc V. Le, and Hartwig Adam. [Searching for MobileNetV3](https://openaccess.thecvf.com/content_ICCV_2019/html/Howard_Searching_for_MobileNetV3_ICCV_2019_paper.html). In *Proceedings of the IEEE/CVF International Conference on Computer Vision*, pages 1314–1324, 2019.

[8] Lei Ke, Martin Danelljan, Xia Li, Yu-Wing Tai, Chi-Keung Tang, and Fisher Yu. [Mask Transfiner for High-Quality Instance Segmentation](https://openaccess.thecvf.com/content/CVPR2022/html/Ke_Mask_Transfiner_for_High-Quality_Instance_Segmentation_CVPR_2022_paper.html). In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 4412–4421, 2022.

[9] Beomyoung Kim and Sung Ju Hwang. [Learning from Adversity: Semantic-Aware Mask Refinement Through Adversarial Perturbation](https://link.springer.com/chapter/10.1007/978-3-032-37520-9_5). In *Computer Vision—ECCV 2026*, LNCS 17022, pages 75–92, 2026.

[10] Alexander Kirillov, Yuxin Wu, Kaiming He, and Ross Girshick. [PointRend: Image Segmentation As Rendering](https://openaccess.thecvf.com/content_CVPR_2020/html/Kirillov_PointRend_Image_Segmentation_As_Rendering_CVPR_2020_paper.html). In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 9799–9808, 2020.

[11] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollár, and Ross Girshick. [Segment Anything](https://openaccess.thecvf.com/content/ICCV2023/html/Kirillov_Segment_Anything_ICCV_2023_paper.html). In *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, pages 4015–4026, 2023.

[12] Yuqi Lin, Hengjia Li, Wenqi Shao, Zheng Yang, Jun Zhao, Xiaofei He, Ping Luo, and Kaipeng Zhang. [SAMRefiner: Taming Segment Anything Model for Universal Mask Refinement](https://proceedings.iclr.cc/paper_files/paper/2025/hash/90800f46f84381b7891e1378ee850013-Abstract-Conference.html). In *International Conference on Learning Representations (ICLR)*, 2025.

[13] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. [Flow Matching for Generative Modeling](https://openreview.net/forum?id=PqvMRDCJT9t). In *International Conference on Learning Representations (ICLR)*, 2023.

[14] Tie Liu, Zejian Yuan, Jian Sun, Jingdong Wang, Nanning Zheng, Xiaoou Tang, and Heung-Yeung Shum. [Learning to Detect a Salient Object](https://doi.org/10.1109/TPAMI.2010.70). *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 33(2):353–367, 2011.

[15] Jonathan Long, Evan Shelhamer, and Trevor Darrell. [Fully Convolutional Networks for Semantic Segmentation](https://openaccess.thecvf.com/content_cvpr_2015/html/Long_Fully_Convolutional_Networks_2015_CVPR_paper.html). In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 3431–3440, 2015.

[16] Ilya Loshchilov and Frank Hutter. [Decoupled Weight Decay Regularization](https://openreview.net/forum?id=Bkg6RiCqY7). In *International Conference on Learning Representations (ICLR)*, 2019.

[17] Maxime Oquab, Timothée Darcet, Théo Moutakanni, et al. [DINOv2: Learning Robust Visual Features without Supervision](https://openreview.net/forum?id=a68SUt6zFt). *Transactions on Machine Learning Research*, 2024.

[18] Stephen Price, Kiran Judd, Kyle Tsaknopoulos, Rodica Neamtu, and Danielle L. Cote. [DualSight: multi-stage instance segmentation framework for improved precision](https://www.nature.com/articles/s41598-025-09642-3). *Scientific Reports*, 15(1):27521, 2025.

[19] Stephen Price, Danielle L. Cote, and Elke A. Rundensteiner. [PromptMoE: A Segmentation Refinement Framework Leveraging Mixture of Experts for Improved Prompting](https://openaccess.thecvf.com/content/CVPR2026/html/Price_PromptMoE_A_Segmentation_Refinement_Framework_Leveraging_Mixture_of_Experts_for_CVPR_2026_paper.html). In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 6325–6335, 2026.

[20] Mengyu Wang, Henghui Ding, Jun Hao Liew, Jiajun Liu, Yao Zhao, and Yunchao Wei. [SegRefiner: Towards Model-Agnostic Segmentation Refinement with Discrete Diffusion Process](https://proceedings.neurips.cc/paper_files/paper/2023/hash/fc0cc55dca3d791c4a0bb2d8ddeefe4f-Abstract-Conference.html). *Advances in Neural Information Processing Systems*, 36:79761–79780, 2023.

[21] Qiong Yan, Li Xu, Jianping Shi, and Jiaya Jia. [Hierarchical Saliency Detection](https://openaccess.thecvf.com/content_cvpr_2013/html/Yan_Hierarchical_Saliency_Detection_2013_CVPR_paper.html). In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, pages 1155–1162, 2013.

[22] Gang Zhang, Xin Lu, Jingru Tan, Jianmin Li, Zhaoxiang Zhang, Quanquan Li, and Xiaolin Hu. [RefineMask: Towards High-Quality Instance Segmentation With Fine-Grained Features](https://openaccess.thecvf.com/content/CVPR2021/html/Zhang_RefineMask_Towards_High-Quality_Instance_Segmentation_With_Fine-Grained_Features_CVPR_2021_paper.html). In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 6861–6869, 2021.

[23] Peng Zheng, Dehong Gao, Deng-Ping Fan, Li Liu, Jorma Laaksonen, Wanli Ouyang, and Nicu Sebe. [Bilateral Reference for High-Resolution Dichotomous Image Segmentation](https://doi.org/10.26599/AIR.2024.9150038). *CAAI Artificial Intelligence Research*, 3:9150038, 2024.
