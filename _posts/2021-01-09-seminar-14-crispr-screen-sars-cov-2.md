---
title: '生化研讨室 第14期：CRISPR 筛选寻找新冠的宿主因子'
date: 2021-01-09
permalink: /posts/2021/01/seminar-14-crispr-screen-sars-cov-2/
tags:
  - 生化研讨室
  - SARS-CoV-2
  - CRISPR
  - Functional Genomics
---

*#Shionari的生化研讨室# CRISPR 文库筛选发现新冠的宿主因子*

为了寻找对人流行 CoV（SARS-CoV-1/2，MERS-CoV）响应的细胞生存因子，研究人员选用了猴 Vero E6 细胞（易感，内源表达 ACE2 和 DPP4，且可引发细胞病变方便后期筛选）进行了全基因组 CRISPR 筛选。

大致原理就是准备了一系列配对到整个基因组各处的 sgRNA（大约 8w 条，4x 覆盖率），用 CRISPR 系统进行随机敲除。一旦敲掉了那些病毒感染或者致病所依赖的关键蛋白质，那么这些细胞就能存活下来。之后再对这些细胞基因组 DNA 进行测序，寻找缺失了哪些关键蛋白。（注意此处还包含了 1k 多条非特异性的对照 sgRNA，用来控制 FDR = 0.03）

不出意外，ACE2 位于抵抗性基因序列中排名第一位，CTSL（编码组织蛋白酶 L）也出现了。TMPRSS2 倒是没有出现，提示这个可能不是 CoV2 引发细胞死亡的胞内方式，也可能是功能上的赘余。

通过筛选，他们发现了一个潜在的促进病毒感染（pro-viral）的基因，HMGB1-like。HMGB1 本身是一个核蛋白，平时乖乖结合着 DNA，但在应激状态下会迁移到胞质并分泌，起到了警报素（alarmin）的功能。那么这个东西呢，在表达 CoV1 和 CoV2 的 Spike 蛋白的假病毒中有，但 MERS 中没有中发现富集。这就说明这个蛋白很可能是 SARS 特异性的细胞反应因子。通过验证实验敲除了这个基因后，可以避免细胞感染后死亡，并可以减缓病毒繁殖。当在培养液中加入这种蛋白时，却没有效果，说明了这种蛋白的作用是来自细胞内部而不是外部的（不是 alarmin 效果）。

通过比较正常细胞与 CRISPR 筛选中的 HMGB1 敲除细胞中的差异表达基因，发现了在已筛选出来的促病毒基因中，只有 ACE2，CTSL 和它自己本身表达降低。再通过 ChIP-seq 和 ATAC-seq，发现了缺陷株的 ACE2 基因 TSS 位置后面的 H3K27 乙酰化水平（增强子活化的标志）显著降低，且 ACE2 基因座的染色体可及性降低的趋势。

至此，砸完这么多钱，他们终于发现了一条新的调控 ACE2 表达水平的通路，并且能够影响 CoV2 的易感性。

![](/images/blog/seminar-room/seminar-14-fig1.png)

![](/images/blog/seminar-room/seminar-14-fig2.png)

![](/images/blog/seminar-room/seminar-14-fig3.png)
