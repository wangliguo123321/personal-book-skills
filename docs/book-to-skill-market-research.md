# Book-to-Skill 市场/开源做法调研

调研日期：2026-05-31。

## 已调研方向

### apple-ouyang/book-to-skill

定位：拆书元技能。核心优点：

- 先按页数/上下文窗口评估单 Agent 或多 Agent。
- 先读目录和前言，识别主框架和章节分工。
- 对长书使用多 Agent 分章节提取。
- 提取内容强调：核心概念、可执行步骤、案例、触发信号、注意事项。
- 最终组装 `SKILL.md`，并用真实场景自测。

可吸收点：

- 保留“先建框架骨架，再提取章节”的流程。
- 长书使用章节级 extraction，而不是一次性总结。
- 输出必须可执行，不只做读书笔记。

不足：

- 更像一次性拆书流程；对版本迭代、差异更新、可追溯引用支持不足。
- 容易把书压缩成 Skill，导致详细表格和证据丢失。

### virgiliojr94/book-to-skill

定位：把技术书 PDF/EPUB 转成 Claude Code skill，强调 on-demand chapter loading 和从原内容回答。

核心优点：

- 目标不是“搜索 PDF 页码”，而是把书组织成 Claude 可按需加载的 Skill。
- 面向技术书，强调安装后直接按书名/主题调用。
- 适合快速把单本书变成可用技能包初稿。

可吸收点：

- 保留原始章节内容，让回答能回到实际内容，而不是只剩摘要。
- reference 文件要按主题/章节渐进加载，避免一次塞满上下文。

不足：

- 更偏“一本书 -> 一个可用 Skill”；对 V3/V4 持续同步、source hash、canonical diff、回归测试支持不足。

### mystijk/pdf2skills / kitchen-engineer42/pdf2skills

定位：把专业书 PDF 转成 Claude-Code-ready skills。公开说明包含 Markdown AST 文档解析、自适应切分、语义密度算法、知识量化、知识融合、Skill 生成等模块。

核心优点：

- 有更明确的 pipeline 思路：parse/split -> density/quantization -> structure/fusion -> generate skill。
- 对超长 PDF 做切分，适合处理上下文放不下的大书。
- 有 `skills2app`、router generator 等扩展方向，说明不只生成一个静态 `SKILL.md`。

可吸收点：

- 引入 `canonical/concept-map.yaml`，把“语义密度高的核心模型”保存成可审查结构。
- 引入 `evidence-index.yaml`，把融合后的结论绑定到来源、置信度和支持对象。
- 后续可扩展自动章节切分、抽取状态、router。

不足：

- pipeline 强，但仍需要本仓库这种版本化 library 和发布流程来解决持续更新。

### bmad-labs Book to Claude Skill Converter

定位：把长 Markdown 书籍/技术指南转成结构化、上下文高效的 Claude skills。

核心优点：

- 多阶段框架，适合 extensive markdown books 和 technical guides。
- 将知识拆成 core concepts、rules、examples 等颗粒化 reference files。
- 使用 subagents 做并行抽取，并维护 progress tracking，适合跨会话长任务。

可吸收点：

- 不把所有内容放在 `SKILL.md`，而是拆成 `concept-map`、`safety-rules`、`decision-tree`、`consumer-traps` 等 references。
- 未来增加 `sources/<version>/extraction-status.yaml` 做长书断点续跑。

不足：

- 偏 markdown/技术文档转换；PDF/EPUB/DOCX 等格式和版本管理仍要补齐。

### ClawHub shenshuo-03/book-to-skill

定位：中文“书本即技能”元技能，支持 PDF/TXT/EPUB/MOBI/DOCX/Markdown，按模板提取技能、方法论或思维方式。

核心优点：

- 中文场景友好，强调从书中提取“核心技能、方法论或思维方式”。
- 有不同模板：技能型、思维模型型、综合型。
- 明确要求 skill 简洁、聚焦 1-2 个核心技能。

可吸收点：

- 对中文书籍保留“技能型 / 思维模型型 / 综合型”分类。
- 本仓库的 `concept-map.yaml` 对应思维模型型；`decision-tree.yaml` 对应技能型；`evidence-index.yaml` 对应综合型的保真层。

不足：

- 如果只按模板输出，很容易遗漏表格、对比和证据链；仍需 canonical + source + eval。

### Agent Skills 生态趋势

GitHub 已将 agent skills 描述为一组 portable instructions/scripts/resources，并在 GitHub CLI 中加入 skill 管理能力；技能正在从某个单一 Agent 的私有格式转向跨 Claude Code、Codex、Cursor、Gemini CLI 等宿主的开放形态。

可吸收点：

- 仓库保持通用 `SKILL.md` 结构，不绑定私有公司/工具命名。
- public repo 命名和说明保持个人中性：`personal-book-skills`。
- Skill 内只放必要 instructions/scripts/resources；完整资料走 `libraries/`。

## 本仓库吸收后的设计原则

1. **不把 Skill 当书**：Skill 是执行入口；完整资料进入 `libraries/`。
2. **版本化来源**：每个版本保存 source 文件、抽取文本、outline、extraction 和 hash。
3. **结构化 canonical**：品牌、型号、安全规则、决策树、消费陷阱、概念地图、证据索引用 YAML 管理。
4. **生成 references**：面向 Codex 上下文的 Markdown 由 canonical 自动生成。
5. **支持 diff 和审核**：新版本先 diff，再更新 canonical，避免旧结论残留或新资料漏同步。
6. **可追溯**：reference 和 canonical 中保留 version/chapter/page_range/confidence。
7. **渐进加载**：用户问安全只读 safety，问品牌只读 brand，跨章节问题读 concept-map，需要核对再读 evidence/source。
8. **回归测试**：每次资料更新后跑 eval，尤其防止安全建议被改弱。

## 后续可继续跟踪

- GitHub/Agent Skills CLI 对 package metadata、安装路径和跨宿主兼容的更新。
- Claude Skills 社区中对 PDF/EPUB ingest、RAG、chunking 的工具实现。
- 针对中文书籍的目录识别、表格抽取、版本 diff 的自动化方案。
