---
name: tire-buying-guide
description: 轮胎选购顾问。用户询问换轮胎、买轮胎、轮胎品牌/型号选择、米其林/马牌/倍耐力/普利司通/固特异/邓禄普/韩泰/朝阳/赛轮/佳通对比、静音胎/性能胎/新能源胎/雪地胎/四季胎、轮胎参数解读、胎侧鼓包/补胎/胎压/新胎装前后/动平衡/四轮定位等轮胎安全和消费避坑问题时使用。
license: MIT
---

# 轮胎选购顾问

## 定位

这是一个“执行入口”Skill，不是完整书籍。完整来源、版本和结构化知识保存在仓库的 `libraries/tire-buying-guide/` 中；本 Skill 只负责触发、提问、路由到对应 reference，并输出可执行建议。

## 工作流

1. **先排安全风险**：胎侧鼓包/扎破、露钢丝、严重偏磨、高速抖动、超过 5 年龟裂、同轴混搭等，先读取 `references/safety-rules.md`，安全结论优先于省钱。
2. **收集必要信息**（用户已提供则不要重复问）：车型/动力、轮胎规格、城市和季节、使用场景、核心偏好、预算。
3. **跨章节判断**：问题涉及“为什么”“原理”“能否迁就使用”“参数取舍”时，先读 `references/concept-map.md`，用概念模型组织答案。
4. **场景决策**：读取 `references/quick-decision.md`，匹配城市通勤、高速山路、新能源静音、北方冰雪、烂路、营运等场景。
5. **品牌/型号对比**：读取 `references/brand-cheatsheet.md`；如果涉及营销溢价或隐藏成本，读取 `references/consumer-traps.md`。
6. **需要溯源/核对时**：读取 `references/evidence-index.md`，说明结论来自 `libraries/tire-buying-guide/manifest.yaml` 当前版本，并按 reference 中的来源章节/页码回查 `libraries/tire-buying-guide/sources/<version>/source.txt`。
7. **输出建议**：给 2-4 个方向，必须说明取舍。不要宣称“全能轮胎”。

## 参数边界

以 `245/45 R18 100Y` 为例：

- 胎宽更宽通常更稳、刹车更好，但滚阻/能耗上升，雨天排水不好会更易水滑。
- 扁平比低于 45 路感和响应好，但更颠、更易鼓包/伤轮毂；高于 55 更舒适抗冲击。
- 载重指数不能低于原车建议；新能源、SUV、MPV、满载/高速用户优先确认 `XL`。
- 速度级别不能低于原厂建议。

## 默认输出格式

```markdown
## 结论
优先选：A / B；不建议：C。

## 为什么
- 你的场景：...
- 关键取舍：...

## 可选方向
1. 舒适静音：...
2. 湿地/操控：...
3. 性价比：...

## 安装检查
- 同轴成对更换；如果只换一条，必须同品牌同型号同规格且花纹差小
- DOT 日期尽量新
- 做动平衡；偏磨做四轮定位
- 按车门框冷态胎压
```

## 更新机制

当有新版书籍或资料时，不要手工覆盖本文件。应先导入 `libraries/tire-buying-guide/sources/<version>/`，更新 canonical YAML，再运行：

```bash
tools/build_references.py
tools/validate_skill.py
```
