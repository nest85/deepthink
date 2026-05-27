# DeepThink

通用问题分析元工具,通过多种方法论独立分析同一问题再综合输出。根据问题类型自动选择最合适的分析方法论组合(第一性原理、对立面、系统思维、Pre-mortem、JTBD、利益结构、二阶思维、可逆性判断、5 Whys、机会成本等10种),逐个执行后综合输出。当用户提出需要深度分析、思考、判断、决策、机会发现、原因诊断、未来预测、方案设计、对比选择等问题时,触发此 skill。

---

## 包内容

```
deepthink/
├── README.md                   ← 本文件
├── deepthink.skill             ← 可直接安装到 Claude 的 skill 包
├── deepthink/                  ← skill 源文件(可查看/修改)
│   ├── SKILL.md                ← 主路由
│   ├── synthesis.md            ← 综合逻辑
│   ├── methodologies/          ← 10 个方法论文件
│   │   ├── first-principles.md
│   │   ├── inversion.md
│   │   ├── second-order.md
│   │   ├── systems-thinking.md
│   │   ├── pre-mortem.md
│   │   ├── reversibility.md
│   │   ├── stakeholder-analysis.md
│   │   ├── jobs-to-be-done.md
│   │   ├── 5-whys.md
│   │   └── opportunity-cost.md
│   └── output-templates/
│       ├── analysis.md         ← 报告 MD 模板
│       ├── analysis.html       ← 报告 HTML 模板
│       ├── index.html          ← 索引页模板
│       └── build-index.py      ← 索引重建脚本
└── sample-outputs/             ← 样例输出
    ├── index.html              ← 索引页样例
    └── 中国占星师职业增长分析.html ← 完整分析样例
```

---

## 怎么用

### 安装

1. 打开 Claude 设置 → Capabilities → Skills
2. 上传 `deepthink.skill`
3. 安装完成

### 触发

提任何需要结构化思考的问题,Claude 会自动调用 deepthink:
- "为什么..."、"怎么看..."、"...的本质是什么"
- "我应该不应该..."、"要不要..."
- "...会怎么发展"、"未来..."
- "这里有什么机会"
- "为什么坏了"、"哪里出问题"
- "怎么做出..."、"X 还是 Y"

### 流程

1. **分类问题** → 主要类型 + 次要类型
2. **选方法论**(3-7 个,基于问题特性)→ **停顿等你确认**
3. **逐个执行**每个方法论
4. **检查信息缺口**(全部跑完后)→ 如缺信息,问你补充,可重跑选定方法论
5. **综合**:收敛结论 / 分歧结论 / 主导约束 / 行动建议(直接在对话输出)
6. **询问是否生成文件**:md / html / 两者 / 不需要

文件输出到 `/mnt/user-data/outputs/deepthink/`,同时自动重建索引页。

---

## 方法论清单

| 方法论 | 主要用途 |
|---|---|
| 第一性原理 | 理解·设计·横切 |
| 对立面分析 | 机会·横切 |
| 二阶思维 | 决策·预测 |
| 系统思维 | 理解·预测·诊断 |
| Pre-mortem(事前验尸) | 决策·设计 |
| 可逆性判断 | 决策 |
| 利益结构分析 | 机会·诊断·横切 |
| JTBD(用户雇佣理论) | 机会·设计 |
| 5 Whys | 诊断 |
| 机会成本 | 决策·比较 |

每个方法论文件含:适用/不适用场景、互补/冗余关系、执行步骤、输出模板、质量自检、worked example。

---

## 测试建议

推荐用这个问题做首测:

> 30+ 岁的产品经理/工程师,要不要现在全力转向 AI 方向?

理由:
- 决策类问题,会触发 Pre-mortem / 可逆性 / 机会成本(占星样例没用到的)
- 个人决策,信息天然不足,能测出"问用户补充信息"逻辑
- 话题热度高,Claude 会有丰富的背景知识

---
