# 研究依据与设计取舍

研究日期：2026-11-19。这里是设计依据及阅读范围，不是运行时必须读取的材料，也不宣称该实现已经过学术验证。

## 现有项目

1. [Personal Context Portfolio](https://github.com/nlwhittemore/personal-context-portfolio)：查阅 README、GETTING-STARTED、identity、preferences-and-constraints、decision-log 模板。借鉴模块化上下文、最低可用摘要、决策语境、独立主题、可中断访谈。扩展至私人生活；索引默认按需加载，不将所有事实放在全局指令。仓库子目录及 API 列表访问受限，未逐文件审计。
2. [setup-my-iq / SKILL.md](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/setup-my-iq/SKILL.md)：查看原始 Skill 的状态分流、初始访谈、预填、局部修改、配置接入、确认和示例等关键章节。借鉴先查已有信息、足够即起草、直接处理明确更新、避免重复询问。放宽固定采访顺序、逐条批准及强制再次追问；不自动访问企业系统、邮箱、日历或其他数据源，也不自动更改全局 Agent 配置。未实机运行项目。
3. [me.md](https://github.com/memd-app/me.md)：阅读 README 中的访谈、验证队列、个人画像、导入导出、MCP、数据存储和安全说明，并查看 DESIGN.md 的部分内容。借鉴事实与推断分层、用户可修改/拒绝、来源追溯、便携摘要。以纯 Markdown 代替其浏览器数据库与独立应用；不内置心理测评、人格分数或模仿本人发言；未审计其完整代码或安全实现。

上述三者是项目设计灵感而非实证科学依据。本 Skill 采用原创中文工作流程，未复制其代码或整段模板。

## 研究文献与规范

| 研究/规范 | 阅读范围 | 转化为本 Skill 的规则 |
|---|---|---|
| William Jones (2007), [Personal Information Management](https://doi.org/10.1002/aris.2007.1440410117), ARIST | 综述页面、书籍公开介绍和检索内容 | 将获取、保存、组织、查找、使用、维护视为整体；主题导航、稳定路径、可迁移 |
| Li, Dey & Forlizzi (2010), [A Stage-Based Model of Personal Informatics Systems](https://www.ianli.com/publications/2010-ianli-chi-stage-based-model.pdf), CHI | 正文关键章节，模型、阶段迭代与用户控制 | 初稿可用、自由迭代、跨主题整合；自动化与用户掌控平衡 |
| Epstein et al. (2015), [A Lived Informatics Model of Personal Informatics](https://doi.org/10.1145/2750858.2804250), UbiComp | PubMed 摘要与公开正文检索内容 | 无强制记录周期；暂停和恢复、不按完成度评分 |
| Wang & Strong (1996), [Beyond Accuracy: What Data Quality Means to Data Consumers](https://courses.washington.edu/geog482/resource/14_Beyond_Accuracy.pdf), JMIS 12(4) | 正文数据质量分类及研究结论 | 准确、相关、及时、一致、清晰、可检索、访问安全；质量体检 |
| Wu et al. (2025), [LongMemEval](https://arxiv.org/abs/2410.10813), ICLR 2025 | 论文正文：任务类别、索引与检索、时间筛选、知识更新、实验 | 单一当前事实、显式历史、跨文档推理、相关检索、缺失信息拒绝猜测；验收场景覆盖这五类能力 |
| W3C (2013), [PROV Primer](https://www.w3.org/TR/prov-primer/), [PROV-O](https://www.w3.org/TR/prov-o/) | Primer 的实体、活动、责任、时间、修订说明及 PROV 概览 | 简化来源/时间/核实状态/修订；不要求实现 RDF 或完整 PROV 标准 |
| Helen Nissenbaum (2004), [Privacy as Contextual Integrity](https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/), Washington Law Review | 摘要与论文页面 | 根据用途、接收者和资料范围控制信息流，最小授权导出 |

## 设计假设和限制

这些研究分别聚焦生活记录、个人信息管理、数据质量、AI 记忆和隐私，没有提供适用于所有人的完整个人画像分类标准。当前分类、轻量 YAML、默认时效参考窗口、独立权威文件和三档访问分类是工程选择，非论文规定，也不是强制填写标准。LongMemEval 的实验结果不能直接转化为本 Skill 的准确率；本实现在日常场景的效果需通过实际 Agent 试用与回归评估。只查阅了部分论文全文或关键章节、部分论文摘要；不是系统性文献综述，不宣称穷尽所有研究。

## 平台资料

- [Agent Skills Specification](https://agentskills.io/specification)：标准 SKILL.md、YAML 元信息、按需加载参考资料。
- [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)：原生 Skill 的资格、安装与工作区设置。
- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)：用文件和项目说明搭建聊天模式替代工作流。

产品能力随时可能变化，使用时查阅当前官方说明。

## 1.2.0 的设计依据

在定向个人资料维护中，人的任务入口和稳定的实体名可以同时指向同一条目。需要另一聊天工具的历史线索时，以一次有范围、有文件名的交接减少反复解释。把接收位置、证据等级、阅读者和用途写进操作流程；对可判断的事实直接归档，只有会改变结论的疑点才集中请本人填写。以上为使用观察与设计选择，适用性由真实任务验证。

- [Teevan 等，CHI 2004](https://people.csail.mit.edu/teevan/work/publications/papers/chi04.pdf) 支持用熟悉情境找回资料。索引是否改善具体问题的检索，需要改前、改后同题测量。
- [W3C PROV Primer](https://www.w3.org/TR/prov-primer/) 的原始来源、转引和修订区别适合用自然语言标记。多次转载同一聊天不构成多条独立证据。
- [CIMemories，ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/9a2bcfaf383638e166162a25b6dff125-Abstract-Conference.html) 用不同任务检验记忆的合理流转；[Windows AccessCheck](https://learn.microsoft.com/en-us/windows/win32/secauthz/how-dacls-control-access-to-an-object) 解释了为何用同一身份运行的工具不能仅靠文件夹命名或 ACL 实现 Agent 之间的隔离。
- [LongMemEval，ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf) 将提取、跨会话、时间、更新和未知弃答分别评估。本 Skill 借鉴其测试维度；本地夹具、单次试用和宿主强制隔离分别记录结果。
