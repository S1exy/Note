#### Attention is all you need

没了解过`Transformer`可以先看: https://arxiv.org/abs/1706.03762, 

视频教程的话可以看https://www.bilibili.com/video/BV1pu411o7BE/?spm_id_from=333.337.search-card.all.click&vd_source=f91e0f7fbde4d038587b6116f2b0357e

接着可以了解一下`Bert`: https://arxiv.org/abs/1810.04805

视频教程: https://www.bilibili.com/video/BV1PL411M7eQ/?spm_id_from=333.337.search-card.all.click&vd_sour

后面可以再看一下`Llama`, `Qwen`, `Deepseek`这系列开源模型, 了解一下他们各自的不同和优化手段, 这些不是必看, 但是很有帮助

对这些有初步了解就可以自己尝试搭建一个`LLM`, 具体可以参考下面这些项目:

https://github.com/datawhalechina/happy-llm.git

https://github.com/jingyaogong/minimind.git

做完之后你可以思考这些问题:

- 什么是Transformer, 大致的架构是什么样
- 不同位置编码和注意力机制的差异
- 为什么Decoder-only架构能成为主流
- `prefill`和`decoder`阶段的差异

后续感兴趣也可以了解一些`post-training`相关的工作



#### 推理加速

这块是`ASC`比赛的热点, 毕竟比赛还是聚焦高性能计算的.

主要包括几个方面: 

- **模型量化**: INT8/INT4量化, KV Cache量化, 了解PTQ和QAT的区别
- **算子优化**: Flash Attention, Paged Attention等高效注意力机制(详见下方详细展开)
- **并行策略**: Tensor Parallelism, Pipeline Parallelism, Data Parallelism
- **推理框架**: 
  - vLLM: https://github.com/vllm-project/vllm
  - TensorRT-LLM: https://github.com/NVIDIA/TensorRT-LLM
  - SGLang: https://github.com/sgl-project/sglang
  - DeepSpeed-Inference: https://github.com/microsoft/DeepSpeed
- **KV Cache优化**: PagedAttention, Continuous Batching
- **Speculative Decoding**: 投机采样加速生成

推荐阅读:
- Flash Attention论文: https://arxiv.org/abs/2205.14135
- vLLM论文: https://arxiv.org/abs/2309.06180
- Speculative Decoding: https://arxiv.org/abs/2211.17192

实践:
1. 使用vLLM部署一个开源模型,对比不同配置下的吞吐量和延迟
2. 简单实现以下kv-cache, 了解其工作原理
3. 对比不同量化方案对模型性能的影响

思考问题:
- PagedAttention如何解决KV Cache的内存碎片问题
- Continuous Batching相比Static Batching的优势
- 不同并行策略适用的场景和权衡
- Speculative Decoding的加速原理和适用条件



#### 算子优化

深入CUDA/C++层面的算子优化对ASC比赛很关键,但比较难上手,建议有一定基础后再看:

- **CUDA编程基础**:
  - GPU架构理解: SM, Warp, Thread Block
  - 内存层次: Global/Shared/Register Memory
  - 内存访问优化: Coalesced Access, Bank Conflict
  - 同步与通信: `__syncthreads()`, warp-level primitives
  - Tensor Core利用

- **PyTorch自定义算子**:
  - **Pybind11 + CUDA**: 完全控制的CUDA kernel实现
    - 编写CUDA kernel (.cu文件)
    - 使用pybind11绑定到Python
    - setup.py配置编译参数
  - **Torch C++ Extension**: JIT即时编译,适合快速原型
  - **Triton**: 用Python DSL写GPU kernel,更易上手

- **Flash Attention原理**:
  - Tiling技术: 分块计算减少HBM访问
  - Online Softmax: 避免存储完整attention矩阵
  - Kernel Fusion: 融合多个操作减少内存往返
  - Recomputation: backward时重算而非存储

- **性能分析工具**:
  - NVIDIA Nsight Systems/Compute
  - PyTorch Profiler
  - 关注指标: 带宽利用率、Occupancy

推荐阅读:
- CUDA编程指南: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
- PyTorch C++ Extension教程: https://pytorch.org/tutorials/advanced/cpp_extension.html
- Triton教程: https://triton-lang.org/main/getting-started/tutorials/index.html
- 近100行代码的flashattention实现: https://github.com/tspeterkim/flash-attention-minimal.git

实践:
1. 实现简单的CUDA kernel(矩阵乘法/elementwise ops)
2. 使用Triton实现LayerNorm并对比性能
3. 阅读Flash Attention源码
4. 用profiler分析模型瓶颈并尝试优化

思考问题:
- Flash Attention如何同时降低显存和提升速度
- 什么场景适合用Triton vs 手写CUDA
- Kernel Fusion的收益



#### 分布式推理

推理加速中的并行策略较为重要, 这里详细讲一下. 

大模型推理需要多卡甚至多机协作，掌握分布式推理技术是ASC比赛的关键, 但这部分比较难, 而且难以实践, 建议最后看:

- **PyTorch分布式通信原语**:
  - `torch.distributed`基础: init_process_group, barrier等
  - 集合通信操作:
    - `all_reduce`: 聚合所有进程的数据(求和/平均等)
    - `all_gather`: 收集所有进程的数据
    - `broadcast`: 从一个进程广播数据到所有进程
    - `reduce_scatter`: 聚合后分发不同部分到各进程
    - `send/recv`: 点对点通信
  - Process Group管理和多种backend(NCCL/Gloo/MPI)
  
- **张量并行(Tensor Parallelism)**:
  - 模型权重按张量维度切分到多个GPU
  - 适合单机多卡场景
  - 需要在layer间插入通信操作(all-reduce, all-gather等)
  - Megatron-LM的实现方式
  
- **流水线并行(Pipeline Parallelism)**:
  - 模型按层切分到多个GPU/节点
  - 适合层数多、深度大的模型
  - Micro-batch切分减少bubble time
  - GPipe、PipeDream等实现
  
- **序列并行(Sequence Parallelism)**:
  - 将输入序列切分到多个设备
  - 适合长序列推理场景
  - 需要处理attention的跨设备依赖
  
- **混合并行策略**:
  - TP + PP组合
  - 根据网络拓扑和模型特点选择策略
  - 通信与计算的overlap优化

推荐阅读:
- PyTorch分布式教程: https://pytorch.org/tutorials/beginner/dist_overview.html
- Megatron-LM论文: https://arxiv.org/abs/1909.08053
- GPipe论文: https://arxiv.org/abs/1811.06965
- Sequence Parallelism: https://arxiv.org/abs/2105.13120

实践这块没有多机环境可以用docker模拟:
1. 使用`torch.distributed`实现简单的多卡模型推理
2. 手动实现Tensor Parallelism的Linear层(需要插入all-reduce)
3. 使用vLLM的`--tensor-parallel-size`参数进行多卡推理并分析性能
4. 编写脚本测试不同通信原语的带宽和延迟

思考问题:
- Tensor Parallelism中哪些操作需要通信,通信量是多少
- Pipeline Parallelism的bubble time如何优化
- 如何根据模型大小和硬件配置选择并行策略
- NCCL的Ring All-Reduce算法原理
- 如何测量和优化跨节点通信延迟





#### 系统和性能调优

ASC比赛中系统层面的优化也很重要:

- **性能分析工具**:
  - NVIDIA Nsight Systems/Compute
  - PyTorch Profiler
- **内存优化**:
  - 显存分析和优化
  - CPU-GPU数据传输优化
  - 内存池管理
- **计算优化**:
  - CUDA kernel优化基础
  - Tensor Core利用
  - IO优化(数据加载)
  
- **分布式系统配置**:
  - NCCL环境变量调优(NCCL_DEBUG, NCCL_IB_*)
  - InfiniBand/RoCE网络配置
  - 网络拓扑感知的进程分配
  - 多机通信优化

推荐资源:
- CUDA编程指南: https://docs.nvidia.com/cuda/cuda-c-programming-guide/

- NCCL文档: https://docs.nvidia.com/deeplearning/nccl/

- PyTorch性能调优: https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html

- 内存管理: https://github.com/jemalloc/jemalloc/wiki/getting-started

  



#### 资源

**重要论文**:
- Transformer: https://arxiv.org/abs/1706.03762
- Flash Attention: https://arxiv.org/abs/2205.14135
- vLLM (PagedAttention): https://arxiv.org/abs/2309.06180
- Megatron-LM: https://arxiv.org/abs/1909.08053

**开源项目**:

- Hugging Face Transformers: https://github.com/huggingface/transformers
- vLLM: https://github.com/vllm-project/vllm
- TensorRT-LLM: https://github.com/NVIDIA/TensorRT-LLM
- DeepSpeed: https://github.com/microsoft/DeepSpeed
- Flash Attention: https://github.com/Dao-AILab/flash-attention

**学习资源**:

- 大模型学习资料整合: https://github.com/liguodongiot/llm-action.git
- 一个简单的推理框架实践: https://github.com/GeeeekExplorer/nano-vllm.git
