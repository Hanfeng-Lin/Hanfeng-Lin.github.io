---
title: '生化研讨室 第11期：LACE——蛋白特定 Lys 位点的酰基化修饰'
date: 2020-12-23
permalink: /posts/2020/12/seminar-11-lace-site-specific-acylation/
tags:
  - 生化研讨室
  - Chemical Biology
  - Ubiquitination
  - Protein Engineering
---

*#Shionari的生化研讨室# 蛋白特定 Lys 位点的酰基化修饰【施工中】*

上个月的 Nature Chemistry 上登载了一篇介绍如何对蛋白特定位点（绝大部分是赖氨酸 Lys）进行酰基化修饰的研究。

![](/images/blog/seminar-room/seminar-11-fig1.png)

蛋白质酰基化在生化层面上起到不少关键作用，其中包括了泛素化（26S 蛋白酶体降解，作用位点识别，复合体组装等）和 SUMO 化（定位，DNA 修复等）。然而，目前还没有很好的办法来操控这些过程，让他们只在特定位点发生反应，而一个蛋白若有多个这种位点，就很难将他们分开独立进行研究。

他们组利用人体内天然存在的 E2-SUMO 偶联酶 Ubc9，加上他们设计的 probe，构建出了用一步法在蛋白特定 Lys 位点添加酰化基团的系统，取名为 LACE。选择 Ubc9 的原因，是因为它能够不依赖 E3 就对 SUMO motif 进行识别和反应。至于这个 probe 怎么设计的，是参照 ATP 活化后的 E1-Ubl 而模仿的硫酯类中间体，其中的肽段试了多种 SUMO 亚型但效果都不太好，而用泛素末端的肽段（LRLRGG）效果反而出乎意料的好。最后的 probe 就变成了图 2 左边那个样子。

![](/images/blog/seminar-room/seminar-11-fig2.png)

识别修饰位点（被酰化的位置，称为 LACE tag）最少有 4 个连续的氨基酸：ΨKXD/E，其中 Ψ 表示疏水 aa，D/E 表示酸性 aa，X 表示任意。LACE tag 可以在 N 端，C 端，或者中间位置。如果存在多个符合条件的位点则都可以被修饰。

到这里为止都只是尝试在特定位点加上泛素末端的各种小肽段，并用荧光团检验反应特性。成功之后，他们下面就开始尝试能不能用这个方法对目的蛋白添加整个泛素。首先要准备 2-巯基乙烷磺酸泛素作为酰基供体，并在目的蛋白的特定 Lys 周围通过点突变方法构建表达含 LACE tag 的重组蛋白。对 α 突触核蛋白（帕金森病中的致病蛋白，存在多个单泛素化位点）的实验可以看到，反应只在构建好 LACE tag 的 Lys96 或 Lys102 上发生，证明了这一系统的有效性，同时也为某些蛋白的泛素修饰研究提供的格外简便的研究方法。

![](/images/blog/seminar-room/seminar-11-fig3.png)

【写给自己：如果以后要研究泛素相关功能记得回来精读这篇文章】
