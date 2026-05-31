# Personal Book Skills

个人 book-to-skill 与 Codex skills 共享仓库。

## 核心思想

Book 不被 Skill 替代。书籍和资料作为版本化知识库保存在 `libraries/`；`skills/` 只提供 Codex 可触发的执行入口和轻量 references。

```text
source books -> versioned libraries -> canonical YAML -> generated references -> Codex Skill
```

## Skills

- `tire-buying-guide`：轮胎选购顾问。用于换轮胎、买轮胎、轮胎品牌/型号选择、胎压、胎侧鼓包、补胎、动平衡、四轮定位等轮胎安全和消费避坑问题。

## 安装

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo wangliguo123321/personal-book-skills \
  --path skills/tire-buying-guide
```

安装后重启 Codex。

## 仓库结构

```text
skills/       Codex 可安装 Skill
libraries/    版本化书籍源材料与 canonical 知识库
tools/        ingest / diff / build / validate 工具
schemas/      结构化知识字段契约
docs/         架构和调研文档
```

## 更新资料

详见 `docs/architecture.md`。

常用命令：

```bash
tools/ingest_book.py tire-buying-guide v3 /path/to/source.pdf --title '轮胎选购指南-V3'
tools/diff_versions.py tire-buying-guide v2 v3
tools/build_references.py
tools/validate_skill.py
```

## 调研

现有 book-to-skill 方案和吸收点见 `docs/book-to-skill-market-research.md`。

## 质量保障

- `canonical/concept-map.yaml`：保留书里的核心认知模型，避免 Skill 只剩零散摘要。
- `canonical/evidence-index.yaml`：把关键结论绑定到版本、章节、页码和置信度。
- `evals/`：用真实问题做回归测试，尤其防止安全建议被改弱。
- `tools/sync_github_contents.py`：当本地 `git push` 网络异常时，可用 GitHub Contents API 发布。
