# 学习补全与删除：集合语义引导的掩码精修

## 摘要

当粗掩码遗漏物体主体或混入大块背景时，分割精修需要重新确定目标范围，并同时完成前景补全与多余区域删除。本文提出集合语义引导的双方向掩码精修方法，将这两类纠错直接编码到过程监督中。我们的关键观察是，粗掩码与真实掩码的并集和交集分别对应完成初始补全、完成初始删除的参考状态。结合初始与最终掩码，四个锚点构成以补全和删除进度为坐标的参考曲面。我们在统一距离尺度下解析计算两方向的区间平均修正，使各自的监督目标与合成更新精确对应。区域—细节预测器结合全图上下文与原生分辨率残差，执行大范围区域修正和局部轮廓调整。

## 1. 引言

粗掩码中的主体遗漏、背景混入和邻近物体粘连，会直接改变目标的覆盖范围。修正这些错误，需要精修模型结合图像重新判断哪些区域属于目标。粗掩码在此承担着双重角色：它帮助模型定位目标，其中错误的区域判断又需要被修正。恢复完整目标因此涉及两类相反的操作：补回遗漏的前景，删除多余的区域。两类操作可以同时出现在同一目标上，并分别作用于物体内部、附属结构和外部轮廓。

已有方法通过多尺度预测、细粒度特征与稀疏位置修正改善掩码质量[3,8,10,22]，通过离散去噪学习粗到精的转换[20]，或借助SAM的提示机制重新预测目标[11,12,19]。QuBER与Phoenix还将错误类别、对抗扰动和对比学习引入精修训练[1,9]。补全与删除需要在不同位置执行不同的区域修正，而最终掩码给出的是两类操作共同完成后的结果。我们为它们分别构造参考状态，将各自的纠错职责直接写入监督，并描述两类操作处于不同进度时应执行的更新。

我们的关键观察是，这些状态可以直接由粗掩码与真实掩码的集合关系得到。设两者分别为$C$和$Y$，并集$C\cup Y$补齐全部初始遗漏，同时保留原有前景；交集$C\cap Y$清除全部初始多余，同时保留共同前景。二者与$C$、$Y$共同构成四个锚点，对应初始状态、完成补全、完成删除和最终目标。以两类操作的进度为坐标，四个锚点将一对掩码展开为二维纠错过程：沿一个方向学习补入前景，沿另一个方向学习删除多余，两者共同推进至目标掩码。已有标注由此提供了具有操作含义的过程监督，无需额外标注中间步骤。

基于这一观察，我们提出集合语义引导的双方向掩码精修方法。四个锚点被转换为统一尺度下的截断符号距离场，并通过双线性插值构成参考曲面。集合包含关系赋予两个参考方向明确的前景增减含义；曲面的解析形式则给出任意进度区间上的平均修正。两个方向分别学习对应的修正，再按各自的进度跨度合成为下一状态。模型在参考状态上学习方向场，并通过自身预测状态上的递归训练完成连续纠错。

为将这些修正落实到图像中，我们构建共享双方向目标的区域—细节预测器。区域分支结合冻结的DINOv2-S表征[17]与当前掩码状态，判断需要补回或清除的整体范围；细节分支在原生分辨率窗口中预测残差，校正轮廓与细小结构的位置。两者共同形成每次更新的补全场和删除场，将目标范围的判断与像素位置的调整纳入同一纠错过程。该过程由总参数量为33.24M的模型直接执行。


本文的主要贡献如下：

- **将掩码标注转化为具有操作语义的过程监督。** 利用粗掩码与真实掩码的并集、交集构建四锚点参考，为补全与删除建立可分别设定的进度坐标。
- **构造可解析的双方向区间目标。** 对补全与删除分别计算有限进度内的平均修正，并通过跨度加权精确合成参考位移；区域场与原生细节残差共同预测两类修正。
- **从显著区域偏差中恢复目标。** 在四个基准的困难输入上取得相对增益，并在VOC整体评测中同时提高区域与边界精度；监督对照和方向干预揭示了对应的纠错分工。![[Pasted image 20261022002237.png]]

## 2. 相关工作

## 3. 方法

给定图像$I\in\mathbb R^{H\times W\times3}$和上游软掩码$S\in[0,1]^{H\times W}$，我们学习将粗前景$C=\mathbf1[S\geq0.5]$修正为目标掩码。记训练标注为$Y$，原图像素域为$\Omega$。方法首先从$(C,Y)$构造补全与删除的参考状态，再将状态间的变化写成两个可监督的区间场。区域—细节预测器根据图像、当前状态和请求区间预测这些场，并迭代更新掩码。

![[Pasted image 20261021205827.png]]

**图1．由集合关系定义纠错，再由图像预测修正。** 粗掩码$C$、并集$C\cup Y$、交集$C\cap Y$与真实掩码$Y$构成四个参考锚点。补全和删除进度分别沿两个坐标推进，解析区间目标监督两类方向场。区域预测与原生窗口残差在同一距离尺度下合成，形成每次掩码更新。

### 3.1. 用四个锚点定义补全与删除

**从集合关系得到操作状态。** 定义补全参考$U=C\cup Y$和删除参考$J=C\cap Y$。其中，$U\setminus C=Y\setminus C$恰为全部初始遗漏；$C\setminus J=C\setminus Y$恰为全部初始多余。到达$U$意味着补全完成、删除尚待执行；到达$J$意味着删除完成、补全尚待执行。四个状态因此把两类纠错的完成阶段分别确定下来。

**在共同距离尺度上连接状态。** 我们以截断符号距离场连续表示区域，约定前景为正。对$A\subseteq\Omega$，定义

$$
s_\rho(A)(x)=
\operatorname{clip}_{[-1,1]}
\left(\frac{d(x,A^c)-d(x,A)}{\rho}\right),
\qquad \rho=\frac{\max(H,W)}{64},
\tag{1}
$$

其中$d(x,A)$表示到集合$A$的最近像素距离，$A^c$为$\Omega$内的补集；空集和全图分别映射为常数$-1$与$+1$。同一图像的四个锚点及局部窗口共用原图距离尺度，使区域预测和细节残差具有相同单位。

记$c=s_\rho(C)$、$u=s_\rho(U)$、$j=s_\rho(J)$、$y=s_\rho(Y)$。以$a,b\in[0,1]$分别表示补全和删除进度，构造双线性参考曲面

$$
\Phi(a,b)=(1-a)(1-b)c+a(1-b)u+(1-a)bj+aby.
\tag{2}
$$

其四个角满足$\Phi(0,0)=c$、$\Phi(1,0)=u$、$\Phi(0,1)=j$和$\Phi(1,1)=y$。内部状态为距离表示空间中的插值场，以零为阈值给出参考前景。两个坐标可以分别改变，使同一掩码对提供不同补全、删除进度下的训练状态。

**参考方向具有确定的纠错含义。** 集合包含关系在共同距离尺度下给出$j\leq c\leq u$与$j\leq y\leq u$。因此，

$$
\begin{aligned}
\partial_a\Phi(a,b)&=(1-b)(u-c)+b(y-j)\geq0,\\
\partial_b\Phi(a,b)&=(1-a)(j-c)+a(y-u)\leq0.
\end{aligned}
\tag{3}
$$

固定删除进度并推进补全，参考前景单调不减；固定补全进度并推进删除，参考前景单调不增。纯漏分时$C\subseteq Y$，有$j=c$、$u=y$，参考删除场恒为零；纯误分时$Y\subseteq C$，参考补全场恒为零。两类错误并存时，每个方向的幅度随另一方向的进度变化。

### 3.2. 将参考过程转化为一次可学习的更新

一次掩码更新需要跨越有限进度。我们借鉴区间平均场的建模思想[5]，直接监督这一跨度内的平均修正。设起点$p=(a_0,b_0)$、终点$q=(a_1,b_1)$，且$0\leq p\leq q\leq1$按坐标成立。记$\Delta a=a_1-a_0$、$\Delta b=b_1-b_0$，连接路径为$\gamma(t)=p+t(q-p)$，中点为$(\bar a,\bar b)=(p+q)/2$。两个区间目标为

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

由于$\Phi$为双线性函数，两个偏导沿$\gamma$均为$t$的一次函数，区间平均可由中点精确计算。沿路径积分得到

$$
\Phi(q)-\Phi(p)
=\Delta a\,V_+^{p\rightarrow q}
+\Delta b\,V_-^{p\rightarrow q}.
\tag{5}
$$

式（5）把两个纠错目标与完整参考位移直接联系起来：每个场表达单位进度内的距离值变化，对应跨度决定该方向在本次更新中的贡献。单轴区间中，未推进方向的贡献由零跨度消去。

预测器根据图像、初始掩码、当前状态$z$及区间条件输出两类修正：

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

式（4）分别监督两个输出，式（5）对应的状态目标监督其合成结果。因此，方向回归学习各自的纠错职责，状态回归学习它们如何共同完成这一步更新。不同起止进度共享同一预测器。

### 3.3. 在区域与细节尺度上执行同一修正

大块区域的归属需要全图上下文，轮廓和细小结构的位置需要原生像素信息。我们使两种尺度的预测共同回归式（4）的方向目标。

**区域场确定整体修正范围。** 区域分支以$448\times448$输入提取冻结的DINOv2-S/14表征[17]，并融合RGB、软掩码$S$、初始场$c$和当前状态$z$。起止进度经编码后作为区间条件，调制补全与删除两个共享视觉特征的分支。经过跨尺度读取和分支交互，模型预测区域场$G_+$、$G_-$，以及两类非负修正需求$N_+$、$N_-$。区域场被插值到原图网格，形成临时状态$\widetilde z=z+\Delta aG_++\Delta bG_-$，为局部预测提供整体修正后的参照。

**原生残差校正局部位置。** 细节分支根据修正需求选择原图窗口，每次更新最多处理八个$256\times256$窗口。每个窗口同时接收原生RGB、扩大两倍的图像上下文、同位置的$(z,c,S,G_+,G_-,\widetilde z)$、区域语义特征和区间条件，并输出两方向残差$r_{k,+}$、$r_{k,-}$。重叠窗口以Hann权重$w_k$融合：

$$
R_d(x)=
\frac{\sum_k w_k(x)r_{k,d}(x)}
{\max\{\sum_k w_k(x),\epsilon\}},
\qquad
\widehat V_d(x)=G_d(x)+R_d(x),
\quad d\in\{+,-\}.
\tag{7}
$$

窗口外的权重与未覆盖位置的残差均为零。区域场承担整体判断，局部残差在相同距离单位下补充位置修正，二者通过式（6）共同更新当前状态。网络配置与窗口选择规则见附录A.1。

### 3.4. 学习参考动作与递归纠错

训练同时覆盖具有解析目标的参考状态和模型自身产生的预测状态。前者确定两个方向应学习的修正，后者使模型在连续更新中完成目标恢复。

**参考状态监督。** 对采样区间$(p,q)$，令$z=\Phi(p)$，记$V=(V_+,V_-)$与$\widehat V=(\widehat V_+,\widehat V_-)$。以$\langle\cdot\rangle_M$表示有效标注区域$M$内的通道平均，核心目标为

$$
\begin{aligned}
\mathcal L_{\mathrm{field}}
&=\left\langle(\widehat V-V)^2\right\rangle_M,\\
\mathcal L_{\mathrm{state}}
&=\left\langle
\left|T_\theta(\Phi(p);p,q)-\Phi(q)\right|
\right\rangle_M.
\end{aligned}
\tag{8}
$$

区域场回归低分辨率方向目标，细节分支回归区域场尚未解释的残差，需求分支学习残差的空间分布。参考监督写为

$$
\mathcal L_{\mathrm{ref}}
=\mathcal L_{\mathrm{field}}+\mathcal L_{\mathrm{state}}
+0.25(\mathcal L_{\mathrm{region}}+\mathcal L_{\mathrm{detail}})
+0.1\mathcal L_{\mathrm{need}}.
\tag{9}
$$

**预测状态递归。** 从$z_0=c$出发，令$p_k=(k/K,k/K)$，连续执行

$$
z_{k+1}=T_\theta(z_k;p_k,p_{k+1}),
\qquad k=0,\ldots,K-1.
\tag{10}
$$

全部更新参与反向传播。终态损失$\mathcal L_{\mathrm{end}}$结合距离回归、二值交叉熵与Dice损失，使最终预测恢复目标区域；中间损失$\mathcal L_{\mathrm{inter}}$将各步预测与同进度参考场$\Phi(p_k)$对齐。总目标为

$$
\mathcal L=
\mathcal L_{\mathrm{ref}}
+\mathcal L_{\mathrm{end}}
+0.25\mathcal L_{\mathrm{inter}}.
\tag{11}
$$

参考区间覆盖原点、终点、单轴与内部状态，包括补全和删除进度不同的情况；递归训练覆盖一至四次更新。两类训练共享全部预测参数。完整损失定义与采样配置见附录A.2。

### 3.5. 推理

推理从$z_0=c$开始，采用三个对角区间，令$p_k=(k/3,k/3)$，按式（10）逐步更新。每一步根据当前状态重新预测区域场、修正需求与局部残差，图像特征在三步间复用。最终输出原生分辨率掩码

$$
\widehat C(x)=\mathbf1[z_3(x)>0].
\tag{12}
$$

四锚点提供训练目标，推理根据图像、上游掩码与当前状态直接生成修正场。模型总参数量为33.24M，其中11.19M参与训练，其余为冻结的视觉编码器。

## 4. 实验


### 4.1. 实验设置

**数据与输入。** BIG[3]与VOC[4]分别包含283和5408项图像—目标—粗掩码任务，输入来自DeepLabV3-ResNet101、FCN-ResNet50[15]和LR-ASPP-MobileNetV3-Large[7]。ECSSD[21]与MSRA-B[14]分别包含2000和10000项任务，输入来自RMBG-1.4与BiRefNet-matting[23]。整体精修在BIG与VOC的三种来源上评价；困难输入恢复覆盖四个数据集。

**训练与推理。** 模型在VOC训练划分的1464张图像、6510项配对任务上学习，采用AdamW[16]，初始学习率为$2\times10^{-4}$，有效批量为16。整体精修与困难输入评测统一使用$448\times448$全局输入、每步最多八个原生窗口与三步推理。

**比较与指标。** 比较方法包括CascadePSP[3]、SegRefiner-HR[20]、DualSight[18]、SAMRefiner[12]和PromptMoE-Full[19]。IoU和对称BIoU均在原图网格上计算。困难输入表按任务求均值，整体精修表先按来源求均值，再对来源等权平均。


### 4.2. 跨上游预测的区域与边界提升

**VOC三个来源同时提升。** 本方法在VOC的三种上游输入上均取得比较方法中最高的IoU与BIoU（表2(a)）。来源平均达到77.97%和73.19%，分别超过PromptMoE 3.35和2.72个百分点。FCN与LR-ASPP的输入IoU分别为62.35%和64.77%，精修后达到77.31%和78.35%；三个来源的最终IoU均超过77%。同一模型由此将不同上游预测转化为完整度和边界质量均更高的掩码。

**BIG上的原生分辨率精修。** 在BIG上，本方法获得87.38%的IoU与81.84%的BIoU，分别高于PromptMoE 0.75和0.83个百分点；LR-ASPP来源上的两项指标均为表中最高值（表2(b)）。模型以33.24M总参数实现了这些恢复与细化结果。

**表2．VOC与BIG上的整体精修。** 每格为IoU / BIoU（%），粗体标出各列各指标的最高值。括号为任务数，参数量单位为M；†为PromptMoE公开CSV中的报告值。

**（a）VOC：三种上游来源的区域与边界指标

| 方法 | 参数（M） | DeepLabV3（1846） | FCN（1869） | LR-ASPP（1693） | 来源平均 |
|---|---:|---:|---:|---:|---:|
| 粗掩码 | — | 73.07 / 66.32 | 62.35 / 57.54 | 64.77 / 56.38 | 66.73 / 60.08 |
| CascadePSP[3] | 67.68 | 73.21 / 64.94 | 65.61 / 59.85 | 66.49 / 57.63 | 68.44 / 60.81 |
| SegRefiner-HR†[20] | 119.05 | 65.83 / 59.67 | 61.15 / 56.64 | 61.63 / 54.78 | 62.87 / 57.03 |
| DualSight[18] | 641.09 | 72.83 / 69.40 | 68.19 / 65.25 | 69.54 / 64.48 | 70.19 / 66.38 |
| SAMRefiner[12] | 641.09 | 76.46 / 72.20 | 71.65 / 68.36 | 73.26 / 68.97 | 73.79 / 69.84 |
| PromptMoE[19] | 1932.88 | 77.49 / 73.02 | 72.29 / 69.05 | 74.08 / 69.33 | 74.62 / 70.47 |
| 本文方法 | 33.24 | **78.25** / **73.60** | **77.31** / **72.88** | **78.35** / **73.09** | **77.97** / **73.19** |

**（b）BIG：区域恢复与原生分辨率细化**

| 方法 | 参数（M） | DeepLabV3（97） | FCN（96） | LR-ASPP（90） | 来源平均 |
|---|---:|---:|---:|---:|---:|
| 粗掩码 | — | 84.05 / 76.50 | 74.35 / 65.67 | 76.36 / 68.18 | 78.25 / 70.12 |
| CascadePSP[3] | 67.68 | 87.04 / 79.89 | 80.74 / 73.46 | 81.92 / 75.87 | 83.23 / 76.40 |
| SegRefiner-HR†[20] | 119.05 | **89.80** / **84.71** | **87.68** / **82.41** | 85.91 / 80.75 | **87.80** / **82.62** |
| DualSight[18] | 641.09 | 82.94 / 75.54 | 80.29 / 73.42 | 81.33 / 74.11 | 81.52 / 74.36 |
| SAMRefiner[12] | 641.09 | 85.99 / 80.64 | 84.07 / 78.24 | 85.18 / 79.95 | 85.08 / 79.61 |
| PromptMoE[19] | 1932.88 | 88.22 / 82.72 | 84.89 / 79.25 | 86.77 / 81.07 | 86.63 / 81.01 |
| 本文方法 | 33.24 | 87.44 / 81.84 | 87.64 / 82.04 | **87.06** / **81.64** | 87.38 / 81.84 |


### 4.3. 从显著区域偏差中恢复目标

**困难粗掩码的恢复。** 在四个数据集初始 IoU 处于 $[10\%,50\%)$ 的全部已有任务上，本方法的精修后 IoU 均超过 PromptMoE，优势达到 13.01 至 19.04 个百分点，边界质量也同时提高（表 1）。BIG 上的平均 IoU 从 33.93%恢复至 70.68%，VOC 上从 31.47%恢复至 62.38%。在来自不同图像分布与上游模型的 ECSSD 和 MSRA-B 输入上，平均 IoU 优势分别为 15.29 和 13.01 个百分点。四个基准一致的提升表明，该纠错过程能够在初始目标范围显著失准时恢复前景。

**表 1．困难粗掩码上的目标恢复。** 所有输入的初始 IoU 位于 $[10\%,50\%)$。每格为 IoU / BIoU（%），$\Delta$ 为本文方法相对同输入 PromptMoE 的百分点差。

| 数据集 | 任务数 | 粗掩码 | PromptMoE | 本文方法 | ΔIoU / ΔBIoU |
|---|---:|---:|---:|---:|---:|
| BIG | 38 | 33.93 / 41.44 | 51.64 / 53.08 | **70.68 / 71.47** | +19.04 / +18.38 |
| VOC | 1111 | 31.47 / 40.84 | 46.09 / 52.36 | **62.38 / 67.66** | +16.30 / +15.29 |
| ECSSD | 212 | 32.74 / 22.11 | 43.60 / 41.48 | **58.89 / 50.08** | +15.29 / +8.60 |
| MSRA-B | 1744 | 30.91 / 19.30 | 35.78 / 30.76 | **48.79 / 39.04** | +13.01 / +8.28 |

**修正深入目标内部。** 在具有目标内部遗漏的 166 项诊断任务中，本方法恢复了平均 72.73%的内部漏分，PromptMoE 为 46.45%，相差 26.28 个百分点。这里将内部遗漏定义为
$FN_{\mathrm{in}}=\{x\in Y\setminus C:d(x,Y^c)>\rho\}$，
其中 $\rho=\max(H,W)/64$；恢复率为精修后进入前景的初始内部漏分占比，按任务平均。诊断任务的构成见第 4.4 节。该结果直接体现了对目标主体缺失的恢复能力，与困难输入上的区域 IoU 提升相对应。

### 4.4. 集合参考形成补全与删除分工

![[Pasted image 20261022000158.png]]

**语义参考提高精修质量。** 四锚点参考在同结构、同轮次对照中同时提高区域与边界指标（表3(a)）。对照保持预测器、输入和损失形式一致，将两个中间锚点替换为$m=(c+y)/2$，得到
$\Phi_{\mathrm{mid}}(a,b)=c+\frac{a+b}{2}(y-c)$。
此时两方向的解析目标均为$(y-c)/2$。在VOC全部6444项验证任务的第45轮三步结果中，四锚点使IoU从72.42%提高至72.90%，BIoU从68.34%提高至69.52%。

**预测场学到了不同的纠错职责。** 固定同次调用产生的两个方向场后，单独施加补全场可恢复64.88%的初始漏分，单独施加删除场可清除55.56%的初始误分；它们在另一类初始错误上的修正比例分别为1.75%和1.41%（表3(b)）。中点参考的两个分支则产生相近的混合修正。两种监督对应的行为差异表明，四锚点的操作含义进入了模型实际执行的修正。


**原生细节继续提高区域与边界质量。** 在同一诊断集上，保持模型参数不变，加入原生细节残差后，三步精修的IoU由66.36%提高至68.26%，BIoU由64.57%提高至66.78%（表3(c)）。区域场完成整体修正，局部残差继续提高同一纠错过程的空间精度。

**表3．参考语义、方向行为与细节修正。** (a)保持结构、输入、损失形式及训练轮次一致；(b)固定同次完整区间调用的预测场；(c)固定模型参数，改变推理中是否合成原生残差。

**（a）参考监督对照：

| 参考监督 | IoU（%）↑ | BIoU（%）↑ |
|---|---:|---:|
| 中点参考 | 72.42 | 68.34 |
| 四锚点参考 | **72.90** | **69.52** |

**（b）方向场干预：223项诊断任务。**

| 参考监督 | 单独施加的方向 | FN修复率（%） | FP清除率（%） |
|---|---|---:|---:|
| 四锚点 | 补全场 | 64.88 | 1.75 |
| 四锚点 | 删除场 | 1.41 | 55.56 |
| 中点 | 分支1 | 21.05 | 24.93 |
| 中点 | 分支2 | 21.97 | 25.49 |

修复率为逐任务平均。FN与FP统计分别包含200和221项具有对应初始错误的任务，两种模型使用相同任务与分母。四锚点采用第55轮模型，中点采用第45轮模型。

**（c）原生细节残差：同一诊断集，第55轮固定模型，三步推理。**

| 推理设置 | IoU（%）↑ | BIoU（%）↑ |
|---|---:|---:|
| 区域场 | 66.36 | 64.57 |
| 区域场＋原生细节残差 | **68.26** | **66.78** |



**图2．两类修正共同恢复目标。** 从左至右为图像、粗掩码、补全更新、删除更新、联合更新与真实掩码。绿色、橙色和粉色分别表示正确前景、漏分和误分，数值在原图网格上计算。三个样例对应漏分、多分与混合错误，两个方向场来自同一次完整区间调用。玻璃杯同时存在两类错误，单独补全、单独删除与联合更新的IoU分别为94.30%、67.16%与98.32%，展示两类修正的互补作用。

## 5. 结论

本文将掩码精修表示为补全与删除两个协同执行的过程。粗掩码与真实掩码的并集、交集提供中间参考，解析区间目标将其转化为两类可分别学习的修正，区域场与原生细节残差共同完成目标恢复。在四个基准的困难输入上，本方法相较PromptMoE取得13.01至19.04个百分点的平均IoU增益，并在VOC的三种上游预测上同时提升区域与边界质量。方向场干预进一步表明，模型学习到了补回遗漏与清除多余的明确分工。

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

