# AIPM+ Skills 工具箱

一套为 AI 产品经理打造的 Claude Skills，覆盖从灵感发现、商业判断、需求分析、项目规范到求职上岗的完整链路。

## 为什么做这套 Skills？

市面上大多数 AI 工具要么是通用模板，要么是信息聚合。它们的问题在于：**没有针对 AI 产品经理这个岗位的专业判断力。**

比如你让通用 AI 帮你改简历，它会帮你把句子写得更漂亮，但不会告诉你"这段经历应该突出数据闭环而不是功能迭代，因为目标 JD 要的是有 AI 评测体系经验的人"。

**这套 Skills 的不同之处：**

- **内置 AI PM 领域知识**：每个 Skill 都内嵌了 AI 产品经理岗位的能力模型、专业框架
- **流程驱动而非问答驱动**：触发后 Claude 会按照完整的专业流程主动推进
- **Skill 间数据打通**：BRD → MRD → PRD → 编码，每一步的结论自动传递给下一步，不重复提问
- **实战验证**：每个 Skill 都经历了多轮真实场景的测试和迭代

## 包含哪些 Skills？

### 产品决策链（BRD → MRD → PRD → Code）

这是最核心的一条链路，覆盖从"我有一个想法"到"AI Agent 可以开始写代码"的全过程：

```
/product-insight-miner → 采集用户原声（可选，没数据时推荐先跑）
  ↓
/brd → 评估方向值不值得做 → BRD.md（含数据索引 + 交接区）
  ↓ 自动继承
/mrd → 深入分析市场需求 → MRD.md（含 P0/P1/P2 优先级 + 数据索引）
  ↓ 自动继承
/vibe-prd-writer → 生成完整项目规范 → PRD/ 文件夹（10 模块 + README 导航）
  ↓ 投喂
Claude Code / Cursor 读 PRD/README.md 开始编码
```

| Skill | 解决什么问题 | 触发方式 |
|-------|------------|---------|
| **product-insight-miner** | 没数据，想知道用户在抱怨什么 | "帮我挖掘用户痛点"、"去三个平台看看" |
| **brd** 🆕 | 有想法但不确定值不值得做 | "帮我评估这个方向"、"这个能不能做" |
| **mrd** 🆕 | 方向确认了，需要梳理市场需求 | "帮我写 MRD"、"从用户反馈里提炼需求" |
| **vibe-prd-writer** 🔄 | 需求清楚了，要出一份 AI Agent 能执行的项目规范 | "帮我写个 PRD"、"我想做一个 XX" |
| **ai-agent-prd-writer** | 工作场景的正式 PRD（给开发团队看） | "帮我写正式的需求文档" |

#### BRD / MRD 的数据驱动特性

BRD 和 MRD 都**严格要求数据支撑**：

- **有数据就用数据**：用户粘贴原声 / 上传文件 / product-insight-miner 的产出
- **没数据就跑爬虫**：内置 DuckDuckGo 爬虫脚本（`brd/scripts/fetch_market_data.py`），自动采集并按来源打索引前缀（X=Twitter, R=Reddit, Z=知乎, H=小红书...）
- **所有结论挂索引**：`核心痛点是信息过载 [X3, R1, W5]`，每个索引可回溯到原始数据
- **禁止捏造**：没有数据支撑的数字/比例/增长率，一律不写

#### vibe-prd-writer v2.0 的变化

从"一页纸 PRD"升级为**完整项目规范**：

- 输出 `PRD/` 文件夹（10 模块独立文件 + README 导航），AI Agent 按需加载，不一次性塞爆上下文
- 自动继承 BRD.md / MRD.md / DESIGN.md 的数据
- Phase 3 会扫描你已安装的前端设计 skill（design-consultation / web-design-pro），避免重复造轮子
- 三层自检：文件结构完整性 / 各模块内容质量 / 跨文件一致性

### 求职核心链路

| Skill | 解决什么问题 | 典型使用场景 |
|-------|------------|------------|
| **ai-pm-resume-writer** | 简历不知道怎么写、投了没回音 | "帮我针对这个 JD 调简历" |
| **ai-pm-interview-diagnosis** | 面试完不知道问题在哪、不知道怎么准备下一场 | "帮我分析这个面试录音" |

### 能力建设 & 入职加速

| Skill | 解决什么问题 | 典型使用场景 |
|-------|------------|------------|
| **ai-product-teardown** | 面试前拆解目标公司产品、入职后理解竞品 | "帮我拆解一下 Cursor" |
| **48h-accelerated-learning** | 短时间搞懂一个陌生领域 | "帮我 48 小时搞懂多模态" |
| **interactive-learning** | 系统深入学某个知识点 | "我想搞懂 RAG 的原理" |
| **simin-article-cowriter** | 写干货长文、内容共创 | "帮我写一篇关于 AI Agent 的文章" |

### 知识沉淀

| Skill | 解决什么问题 | 典型使用场景 |
|-------|------------|------------|
| **obsidian-knowledge-saver** | 和 Claude 聊完就忘了、知识散落各处 | "帮我沉淀到知识库"、"lint 一下知识库" |

v2.0 重构：存的是知识点不是对话记录，同一知识点只有一条笔记（更新而非新增），整理的活 LLM 干。支持沉淀 / 消化 / 健康检查 / 初始化四种模式。理念来自 Zettelkasten + [Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

## 快速开始

### 第一步：安装 Claude Desktop 或 Claude Code

- **Claude Desktop**：前往 [claude.ai/download](https://claude.ai/download) 下载，开启 Cowork 模式
- **Claude Code（CLI）**：`npm install -g @anthropic-ai/claude-code`

### 第二步：安装 Skills

**方式 A：手动安装（推荐）**

1. 点击本仓库页面的绿色 **Code** 按钮 → **Download ZIP**，解压
2. 把你要的 Skill 文件夹复制到 `~/.claude/skills/` 下
3. 重启 Claude Code 或开启新对话即可生效

**方式 B：Cowork 模式安装（Claude Desktop）**

1. 在 Cowork 模式下，点击 **Skills** → **Add Skill**
2. 选择你要安装的 Skill 文件夹

### 第三步：直接用自然语言触发

不需要记任何命令。直接跟 Claude 说你想做的事：

```
"这个方向值不值得做"          → BRD
"帮我梳理市场需求"            → MRD
"帮我写个 PRD"               → vibe-prd-writer
"帮我挖掘用户痛点"            → product-insight-miner
"帮我拆解一下 Kimi"           → ai-product-teardown
"帮我针对这个 JD 改简历"      → ai-pm-resume-writer
"帮我分析这个面试录音"        → ai-pm-interview-diagnosis
"帮我 48 小时搞懂多模态"      → 48h-accelerated-learning
"我想搞懂 RAG"               → interactive-learning
"沉淀到知识库"                → obsidian-knowledge-saver
```

## 推荐使用路径

### 路径 A：从想法到产品（Vibe Coding）

```
1. 挖需求 → product-insight-miner（从小红书/X/Reddit 挖掘用户痛点）
2. 判方向 → brd（评估值不值得做，跑爬虫补数据）
3. 理需求 → mrd（梳理 P0/P1/P2 需求优先级）
4. 出规范 → vibe-prd-writer（生成 PRD/ 文件夹，直接喂给 AI Agent）
5. 写代码 → 把 PRD/ 丢进 Claude Code / Cursor 开干
```

### 路径 B：AI PM 求职

```
1. 速成领域 → 48h-accelerated-learning（48 小时建立认知全景图）
2. 补知识 → interactive-learning（深入搞懂 RAG、Agent、评测体系）
3. 看产品 → ai-product-teardown（拆解目标公司的 AI 产品）
4. 攒作品 → ai-agent-prd-writer（写出能拿得出手的 AI PRD）
5. 写简历 → ai-pm-resume-writer（针对目标 JD 打磨简历）
6. 打面试 → ai-pm-interview-diagnosis（面试后复盘、面试前备战）
7. 全程沉淀 → obsidian-knowledge-saver（知识卡片持续积累）
```

入职之后，路径 A 的产品决策链继续帮你做市场调研、需求分析和项目规划。

## 前置依赖

- **BRD / MRD 爬虫功能**：需要 `pip install requests beautifulsoup4`（首次使用时 Skill 会提醒）
- **obsidian-knowledge-saver**：依赖 Desktop Commander MCP 工具进行本地文件读写
- 其他 Skill 无额外依赖

## 关于

这些 Skills 是在真实 AI PM 求职、教学和产品实践中，把反复遇到的痛点提炼成的可复用工具。它们不是完美的，但每一个都解决了真实遇到的问题。

欢迎 Fork 和改造成适合你自己的版本。
