
原图：

![image.png](https://gitee.com/Slexy/picture/raw/master/20251129180204516.png)

![image.png](https://gitee.com/Slexy/picture/raw/master/20251129180217980.png)


## 实验1
[xugao97/AttentionDistillation: [CVPR 2025] Attention Distillation: A Unified Approach to Visual Characteristics Transfer](https://github.com/xugao97/AttentionDistillation)
![image.png](https://gitee.com/Slexy/picture/raw/master/20251129173154841.png)
上面是第一次试验采用的参数网格进行的实验
![image.png](https://gitee.com/Slexy/picture/raw/master/20251129173241885.png)

根据出来的结果修改了网格参数为：

![image.png](https://gitee.com/Slexy/picture/raw/master/20251129180114262.png)


![image.png](https://gitee.com/Slexy/picture/raw/master/20251129180055560.png)


![image.png](https://gitee.com/Slexy/picture/raw/master/20251129183814591.png)




![D:\Code\experiment\AttentionDistillation-main\AttentionDistillation-main\results\comprehensive_grid.png](file:///d%3A/Code/experiment/AttentionDistillation-main/AttentionDistillation-main/results/comprehensive_grid.png)


基于之前做的实验来说，我们可以得到一个比较简单的分析：
1. 从学习率的角度来分析的话，我们可以从每一组进行分析。在低 step 的组别里面，我们可以看到，学习率的提高很明显的促进了图像的风格迁移，但是在学习率高的组别里面学习率过高反倒会让图片出现一些细节性的偏差，例如出现一些莫名其妙的噪点色块等
2. 其次从纵向来进行对比的话，我们可以看见就是 weight 可以有效的控制图像，使其风格化，越高的 weight 保留的 content 信息就越完整，越不会让风格图中的东西泄露进结果图中，但是同时也带来问题就是，content 图像中的颜色可能会误入结果中，比如背景的紫色，但是风格图是一个素描图像，这也是一个可以去优化的问题？之前 **使用的 adain**  是不是就可以去解决这个问题
3. 还有从上面我们可以看到，人物的头发其实是重灾区，他可能会出现书架的样子，当 weight 大于 0.7 的时候可能才会有更好的表达结果
4. 很显然的从图像中的对比我们可以发现越往右下肯定是图像的结果会更好
5. 不过不论是哪一个参数即使是左上角最差的，我们也可以看到大致的结构轮廓是有保存下来的

## 实验 2


[Neural Style Transfer - a Hugging Face Space by georgescutelnicu](https://huggingface.co/spaces/georgescutelnicu/neural-style-transfer)

![image.png](https://gitee.com/Slexy/picture/raw/master/20251130195759099.png)

结果并不是很好并且在网站上其实没有提供任何的可以调整参数的位置 


[Flux Style Shaping - a Hugging Face Space by multimodalart](https://huggingface.co/spaces/multimodalart/flux-style-shaping)

![image.png](https://gitee.com/Slexy/picture/raw/master/20251130230001048.png)




[InstantStyle - a Hugging Face Space by InstantX](https://huggingface.co/spaces/InstantX/InstantStyle)

scale =1

![image.png](https://gitee.com/Slexy/picture/raw/master/20251212113432895.png)


scale = 0.7

![image.png](https://gitee.com/Slexy/picture/raw/master/20251212113559208.png)

这个似乎不太行.....