# Personal Book Skills 架构

本仓库采用：

```text
书籍源文件 -> libraries 版本化知识库 -> canonical YAML -> skill references -> SKILL.md 执行入口
```

## 目录职责

- `skills/`：Codex 可安装 Skill。保持轻量，只包含入口、references 和少量脚本。
- `libraries/`：完整书籍/资料库，包含原始文件、抽取文本、版本 manifest、canonical 结构化知识。
- `tools/`：导入、差异比较、生成 references、验证 Skill 的工具。
- `schemas/`：结构化知识的字段契约。
- `docs/`：设计文档和调研记录。

## 更新一本书的流程

1. 导入新版本：

```bash
tools/ingest_book.py tire-buying-guide v3 /path/to/轮胎选购指南-V3.pdf --title '轮胎选购指南-V3'
```

2. 与上一版本比较：

```bash
tools/diff_versions.py tire-buying-guide v2 v3 > libraries/tire-buying-guide/sources/v3/diff-from-v2.patch
```

3. 人工/模型审查差异，更新：

```text
libraries/tire-buying-guide/canonical/*.yaml
libraries/tire-buying-guide/changelog.md
libraries/tire-buying-guide/manifest.yaml
```

4. 重新生成 Skill references：

```bash
tools/build_references.py
tools/validate_skill.py
```

5. 提交并发布。

## 为什么不直接把整本书塞进 Skill

- `SKILL.md` 应保持短小，避免每次触发消耗大量上下文。
- 完整书籍需要可追溯、可 diff、可多版本共存。
- 用户问题通常只需要知识子集，应按需读取 reference 或 source。

## 推荐知识分层

```text
SKILL.md                触发、提问、路由、输出格式
references/*.md         面向上下文的轻量知识卡片，由 canonical 生成
canonical/*.yaml        可审查、可 diff、可回归测试的结构化知识
sources/<version>/      原始书籍、抽取文本、章节提取、版本差异
evals/*.yaml           真实问题回归测试，防止更新后安全边界退化
```

关键原则：

- **Skill 不等于书**：Skill 负责“怎么用知识”，书和证据留在 `libraries/`。
- **Concept map 常驻，章节按需**：常用模型进入 `concept-map`，细节进入 reference/source。
- **Evidence index 保真**：安全结论、消费建议、参数边界都要能追到 version/chapter/page。
- **Canonical 是同步点**：V3/V4 来了以后，先 diff source，再更新 canonical，再生成 references。
- **Evals 防回退**：典型问题必须检查 must_include / must_not_include。

## 未来自动化路线

1. `ingest`：支持 PDF/EPUB/DOCX/Markdown/HTML/TXT，保存 source hash。
2. `extract`：章节级提取 claims、concepts、rules、examples、gotchas。
3. `diff`：source text diff + canonical entity diff。
4. `review`：人工/模型审查新增、删除、冲突和过期结论。
5. `build`：canonical -> references，保持 Skill 精简。
6. `eval`：运行真实问题回归测试。
7. `publish`：同步 GitHub，安装/更新本地 Skill。
