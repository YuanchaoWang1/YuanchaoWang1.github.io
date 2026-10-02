# Content provenance and editorial notes

核对日期：2026-09-08。

## 个人资料

姓名、NYU 职位、Duke 学位、教育与工作经历、竞赛和审稿服务来自原仓库：

- [原主页内容](https://github.com/JohnnyWyc/JohnnyWyc.github.io/blob/master/_pages/about.md)
- [原主页配置与个人链接](https://github.com/JohnnyWyc/JohnnyWyc.github.io/blob/master/_config.yml)

照片沿用原站 `images/ChatGPT_Image_影棚.png`。邮箱沿用原站公开的 `yuanchao.wang@nyu.edu`。

当前 GitHub 账号与站点仓库已确认为 `yuanchaowang1` 和 `YuanchaoWang1/YuanchaoWang1.github.io`；原仓库链接仅作为内容来源记录保留。

简介采用用户本轮补充的研究轨迹：环境层面的分布偏移、环境内异质性、样本可靠性，以及学生模型动态生成的训练分布。首页按 OOD-TV-IRM、ECTR、ShellOOD、CROSS 顺序给出简要介绍。

## 论文与 CROSS 占位

| 条目 | 首轮处理 | 依据 |
| --- | --- | --- |
| OOD-TV-IRM | ICLR 2025 | 附件首页、[arXiv](https://arxiv.org/abs/2502.19665) |
| ECTR | arxiv 2026 | 用户指定标签；[arXiv](https://arxiv.org/abs/2601.22944) |
| ShellOOD | arxiv 2025 | 用户指定标签；[公开版本](https://arxiv.org/abs/2511.13539)仍题为 BootOOD |
| Attention & decision trees | arxiv 2021 | 附件 arXiv:2110.03879v1，未显示已确认的正式出版会议或期刊 |
| CROSS | arxiv 2026；暂无公开链接 | 用户指定标签与作者名单；未提供公开论文链接 |

ECTR 原主页的作者顺序与公开 arXiv 元数据不同。根据用户确认，当前顺序为：Yuanchao Wang, Tianqi Zhong, Fengnan Li, Zhao-Rong Lai。ShellOOD 作者按用户要求仅保留 Yuanchao Wang, Tian Qin。

四个 Paper 链接均指向公开的论文入口。附件供方法理解和重新绘图使用，未将匿名投稿 PDF 放入站点目录。ShellOOD 的链接标签明确为 Earlier paper (BootOOD)，Project overview 链接进入当前项目介绍。

CROSS 全名为 **CROSS: Verified Peer Corrections for Robust On-Policy Self-Distillation**。题目与简介已纳入 Publications 和 Projects；作者按 2026-10-02 用户指定顺序展示：Yuanchao Wang, Jinnuo Liu, Yifan Li, Hongyi Wen。方法图使用用户提供的 `Cross091002.png`。Publications 按用户最新要求显示 `arxiv 2026`，目前未提供对应公开链接。

## 示意图的事实范围

2026-09-26，CROSS、OOD-TV-IRM、ECTR、ShellOOD 和 Attention 的示意图均使用用户提供的素材；ECTR 图片由 `ECTR_iclr2027.pdf` 的单页以 2 倍分辨率渲染为 PNG。

ShellOOD 图片随后更新为 `ShellOOD_cvpr2027.pdf` 的单页渲染（2508 × 1412）；2026-10-02，OOD-TV-IRM 图片更新为 `OODTVIRM_2026.pdf` 的单页渲染（1920 × 1080）。均保持原比例，图片地址带内容版本标识以避免旧缓存。

- **CROSS**：student rollouts、peer cross evidence、verified local correction、recovery 与 CrossSignal；图示将 correction 的位置、内容和置信度连接到 suffix-localized KL distillation。
- **OOD-TV-IRM**：突出已知环境下的 shared feature extractor、prediction risk、TV penalty 与 primal-dual updates。没有把 TV penalty 画成风险方差，也没有声称对任意未知分布均有保证。
- **ECTR**：PDF 图展示 per-sample loss、global weights、environment conditioning、shared tail risk、TV stationarity、TV multiplier 与 KL concentration control 如何汇入 joint minimax objective。
- **ShellOOD**：ID-only warm-up、cross-class feature mixup、inner shells、辅助 shell head；推理阶段保留 backbone 与 classifier，使用标准 post-hoc scores。图中的半径为训练几何示意，未把径向阈值当作论文唯一的推理规则。
- **Attention**：attention discretization、history features、Silas decision trees、high/low prediction 与 influence analysis。观察限定在论文研究的模型内。

研究叙述保留 OOD generalization 与 OOD detection 的区别。ECTR 的尾部样本与 ShellOOD 的 OOD 输入未被等同于噪声。

## 下轮可确认的具体字段

1. ECTR 与 ShellOOD 最新非匿名稿件的作者顺序；正式录用后再更新发表状态。
2. ShellOOD 的公开 arXiv 是否已经更新题目。
3. CROSS 的公开 PDF 链接及可以公开的方法细节。
4. 主页中是否继续保留创业经历。

首轮 Projects 包含本次四篇 PDF 对应的项目和 CROSS 占位。原仓库草稿中的 Modular Cross-lingual Speech-to-Text Framework 可在提供简述后另加。
