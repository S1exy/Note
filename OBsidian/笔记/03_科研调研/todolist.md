
- [ ] 部署 aaai 这篇论文到本地：
	- [x] 下载数据集
	- [ ] 下载代码
- [ ] 阅读相关文献找一些思路：
	- [x] PD-UniST: Prompt-Driven Universal Model for Unpaired H&E-to-IHC Stain Tran（MICCAI 2025）
	- [ ] SCSA: A Plug-and-Play Semantic Continuous-Sparse Attention for Arbitrary Semantic Style Transfer（cvpr 2025）
	- [x] Style Injection in Diffusion: A Training-free Approach for Adapting Large-scale Diffusion Models for Style Transfer（cvpr 2024）
	- [x] DiffStain: Conditioned Diffusion-Based Semantic Virtual Staining with Mask Guidance（miccai 2024）
	- [x] **CoCoDiff: Correspondence-Consistent Diffusion Model for Fine-grained Style Transfer（iclr 2026）**
	- [ ] FreCaS: Efficient Higher-Resolution Image Generation via Frequency-aware Cascaded Sampling（iclr 2026）
	- [ ] StyleStudio: Text-Driven Style Transfer with Selective Control of Style Elements（cvpr 2025）
	- [ ] MagicStain: High-Fidelity Pathology Image Virtual Staining via Guided Single-Step Diffusion（iclr 2026）
	- [ ] PST-diff
	- [ ] 













学长给的一些建议：
1. 前置模型的问题，还有替换主干模型
2. 还有加速的问题，现实意义（

1， aaai 复现 （加速 deepcache，前置瓶颈，分割）
2，coco 复现+论文


提示词 1：
```
你是一位以严苛、精准著称的资深学术审稿人，熟悉计算机科学领域顶级会议的评审标准。你的职责是作为守门员，确保只有在理论创新、实验严谨性和逻辑自洽性上均达到最高标准的研究才能被接收。

1. 评审基调：

- 默认态度：

- 拒绝客套：省略所有无关痛痒的赞美，直接切入核心缺陷。你的目标是帮作者发现可能导致拒稿的致命伤，而不是让作者开心。2. 审查维度：

- 原创性：该工作是实质性的突破还是边际增量？如果是后者，直接指出。

- 严谨性：数学推导是否有跳跃？实验对比是否公平（Baseline 是否齐全）？消融实验是否充分支撑了核心主张？

- 一致性：引言中声称的贡献在实验部分是否真的得到了验证？

请你对我之前的想法进行评判 并写以下内容：

1.审稿报告：

2.具体的修改建议
```

提示词 2：
```
你是一位以严苛、精准著称的资深学术审稿人，熟悉计算机科学领域顶级会议的评审标准。你的职责是作为守门员，确保只有在理论创新、实验严谨性和逻辑自洽性上均达到最高标准的研究才能被接收。

请你根据你之前输出的报告 去帮我修改我的整体plan

```



目前想去做的方向，想先完成主要思路的验证，等待 aaaibaseline 实验的跑完
下面是大纲：
[[审查报告及大致方案]]