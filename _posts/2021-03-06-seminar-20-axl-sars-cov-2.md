---
title: '生化研讨室 第20期：AXL——新冠的另一个候选受体'
date: 2021-03-06
permalink: /posts/2021/03/seminar-20-axl-sars-cov-2/
tags:
  - 生化研讨室
  - SARS-CoV-2
  - Receptor
  - Virology
---

*#Shionari的生化研讨室# 不知道写啥了就随便写写新冠吧（AXL）*

虽然大众可能觉得对新冠的受体位点研究的已经差不多了，但其实有很多候选才刚刚通过高通量筛选被发现，并没有对他们做详细可靠的功能验证。举个简单例子，大家都知道 ACE2 是新冠的受体，但单细胞测序结果表明，ACE2 在多种人体器官里的表达水平其实很低，尤其是呼吸系统。但新冠主要攻击的就是肺上皮细胞，这一与现实相反的现象恰恰说明了存在着某些人体内广泛分布的别的关键受体。此外，很多现有的中和抗体也都不是结合 Spike 的 RBD 区的，说明存在着其他关键的宿主受体结合到 Spike 上的其他位点。

**如何寻找？(TAP-MS 技术)**

在肺细胞系中表达标签化的 Spike 蛋白，分离出膜蛋白和可溶蛋白后，用 strep 珠孵育后洗脱，再用 S 蛋白珠孵育 + 清洗 + 跑胶，把每个条带单独切下用 trypsin 消化后跑 LC-MS/MS，从而获得单个蛋白身份。因为会有很多非特异性结合所以要设置对照蛋白（这里他们用的是甲流的 HA），筛到 22 个候选者。然后依次用分子对接，MD，和 MM/PBSA 寻找最高亲和力的结合构象，结果有三个：AXL，EGFR，以及 LDLR。

实验验证 AXL 和 Spike 能在 HEK293T 和 H1299 细胞中结合，结合界面不同于 ACE2 结合的 S-RBD，是在 S 的 NTD 上。考虑到 AXL 与 ACE2/TMPRSS2 在肺和气管中不会共表达，AXL 在感染时起到的作用可以说是不依赖 ACE2 的。敲除或敲低 AXL 后则会减弱 SARS-CoV-2 感染 H1299 细胞。体外过表达 AXL 与过表达 ACE2 都会以相似程度促进 SARS-CoV-2 感染。可溶性的人重组 AXL 可以减少感染 H1299，而给予重组 ACE2 却不能，这说明 AXL 介导病毒进入可以不依赖于 ACE2，也侧面反映了两者与 Spike 结合并不占用同一表位。

通过对 COVID19 病人的气管肺泡灌洗液中的单细胞测序数据进行分析，发现 AXL 阳性的细胞相比阴性细胞更易受 CoV-2 攻击。从而进一步证实了 AXL 在感染中起到的作用。

![](/images/blog/seminar-room/seminar-20-fig1.png)

![](/images/blog/seminar-room/seminar-20-fig2.png)

![](/images/blog/seminar-room/seminar-20-fig3.png)
