---
title: '生化研讨室 第12期：轮状病毒 NSP3 与宿主翻译竞争'
date: 2021-01-01
permalink: /posts/2021/01/seminar-12-rotavirus-nsp3-translation/
tags:
  - 生化研讨室
  - Virology
  - Translation
  - mRNA
---

*#Shionari的生化研讨室# 比较硬的一些病毒学的东西（2015）*

![](/images/blog/seminar-room/seminar-12-fig1.png)

mRNA 的翻译过程需要 5' cap 和 3' poly A tail，他们分别对应的结合蛋白是 eIF4E 和 PABP，再经过支架蛋白 eIF4G 连接，并募集转录前起始复合物（PIC）然后开始翻译。5' cap 和 3' poly A tail 在此过程中缺一不可。其中 3' poly A tail 上的 PABP 起码帮助了 cap-tail 环形结构的形成。

轮状病毒的 mRNA（下称 R-RNA）就不太一样，只有 5' cap 但没有 3' poly A，取而代之的是 3' 的 GACC 序列。虽然但是，他这病毒的 mRNA 仍然可以与细胞 mRNA 竞争有限的翻译机器。

感染轮状病毒后，在 R-RNA 稳定度不变的情况下，R-RNA 翻译水平上升，pA-RNA 翻译减少。看到这个现象，他们就开始考虑一种病毒蛋白叫 nsp3 的作用（之前报道过它能抑制宿主蛋白合成）。之前是这么认为的：nsp3 利用了 eIF4G 上 PABP 的结合位置，且对 4G 的亲和力比 PABP 更强。这使得感染过程中 PABP 被迫逃离了 eIF4G，翻译所必须的 PIC 也无法组装，宿主蛋白合成速率就下降了。

实验发现额外少量表达 nsp3 的细胞（注意此细胞未被感染）中 R-RNA 翻译的确提升了（一百多倍），但意外的是 N-RNA（非 polyA，非轮状病毒的 mRNA）和 pA-RNA 也有所提升（2-3 倍）。这一方面说明了 nsp3 参与提升 R-RNA 的合成，另一方面 N/pA-RNA 翻译的提升又仿佛与普通感染时的情况不同：nsp3 可能在此处起到了代替 PABP-polyA 的作用。

进一步生化实验 co-IP 发现：含 4G-BD 的 nsp3 阻碍了 eIF4G 与 PABP 的结合位点（这是正如同预期的），但是同时也稳定了 eIF4E-eIF4G 的相互作用（new!），所以作者推断非轮状病毒的 RNA（N/pA-RNA）在 nsp3 影响下翻译也会提升。

那究竟是什么在轮状病毒感染时抑制了宿主的蛋白合成呢？不能简单认为是 nsp3 使得 PIC 组装过程受阻，而是感染过程中大量的病毒 mRNA "中和"了翻译起始因子们，使他们无法再接触宿主 polyA mRNA。说到底，是 nsp3 促进病毒 mRNA 翻译所导致的。

适者生存。
