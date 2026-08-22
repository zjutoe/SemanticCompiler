# IR Design Memo v0

## 项目名称

**Semantic Compiler：面向可靠 AI 执行的可细化契约中间表示**

## 文档定位

本文档冻结第一版 **Contract IR / Semantic Compiler** 实验所需的核心设计决定。

目标不是一次性设计最终的通用语义 IR，而是提出一个：

- 保守；
- 可扩展；
- 可验证；
- 可证伪；
- 适合快速实验；

的 **v0 版本**。

第一阶段要回答的核心问题是：

\[
\boxed{
\text{显式、有限、支持未知语义的 Contract IR，是否能够成为自然语言与可靠执行之间的有效 semantic bottleneck？}
}
\]

---

# 1. v0 设计结论

第一版作出以下四项决定：

\[
\boxed{
\begin{aligned}
&\text{Primitive：通用规范模态 + 领域 typed predicate；}\\
&\text{结构：语义上采用 typed attributed graph；}\\
&\text{序列化：采用 canonical JSON / tree serialization；}\\
&\text{数据：先进行形式化语义变换，再由 teacher verbalize。}
\end{aligned}
}
\]

同时，将此前笼统的“多层 IR”重新定义为三个生命周期不同、更新权限不同的对象：

\[
\boxed{
S_t=(C,K_t,P_t)
}
\]

其中：

- \(C\)：稳定的 Normative Contract；
- \(K_t\)：可修订的 Grounded Knowledge State；
- \(P_t\)：可丢弃、可重新生成的 Execution / Verification Plan。

这三个对象共同构成 agent 当前的语义状态，但不能被混为一体。

---

# 2. 核心设计原则

## 2.1 Core IR 表达语义角色，而不是领域动作

Core IR 不应包含：

```text
FIX_BUG
REFACTOR
ADD_FEATURE
WRITE_FUNCTION
RUN_TEST
CLARIFY
ESCALATE
SUBMIT
```

这些词混合了：

- 用户目标；
- 领域任务类型；
- agent 控制动作；
- 具体执行步骤。

Core IR 只负责表达一条命题在契约中的逻辑地位。

形式上：

\[
\operatorname{Clause}
=
\operatorname{Modality}
\left(
\operatorname{DomainPredicate}
\right)
\]

例如：

\[
\operatorname{PRESERVE}
\left(
\operatorname{Behavior}
(\text{valid legacy config})
\right)
\]

其中：

- `PRESERVE` 是通用 Core primitive；
- `Behavior` 是 Coding Dialect 中的 typed predicate；
- `valid legacy config` 是领域 operand。

---

## 2.2 规范性语义与认识论状态必须分离

下面两句话不是同一种信息：

```text
用户要求不能修改公共 API。
```

```text
Teacher 认为 bug 很可能在 parser.py。
```

前者是规范性要求，后者是可被证伪的技术假设。

因此每个 IR clause 应同时表达：

1. 它在契约中的规范性角色；
2. 它的认识论状态；
3. 它的来源和证据。

---

## 2.3 未知语义必须是一等结构

IR 不能迫使模型在信息不足时“选一个最可能答案”。

必须支持：

```text
OPEN<T>
```

例如：

```yaml
open_slot:
  id: invalid_input_policy
  type: coding.ErrorPolicy
  owner: USER
  alternatives:
    - RETURN_NONE
    - RAISE_VALUE_ERROR
    - RAISE_PARSE_ERROR
```

未知信息不是一个笼统的低置信度，而是一个：

- 有类型；
- 有所有者；
- 可进一步 refinement；
- 可触发调查或澄清；

的 semantic hole。

---

## 2.4 Contract、Knowledge 和 Plan 具有不同更新权限

- 用户目标和 hard constraints 不能被 executor 自行修改；
- teacher 假设和 repository grounding 可以被新证据推翻；
- execution plan 可以完全失败并重新生成。

因此三者必须分层保存。

---

## 2.5 IR lowering 必须保留 traceability

低层 plan step 必须能够回答：

- 它服务哪条 requirement？
- 它由哪条 permission 授权？
- 它依赖哪些事实或假设？
- 它由什么 verifier 检查？

不能在从高层到低层的转换中丢失原始委托语义。

---

# 3. Core Contract IR v0

## 3.1 规范模态

v0 采用五种核心 modality。

| Modality | 含义 |
|---|---|
| `GOAL` | 希望达到的终态或结果 |
| `REQUIRE` | 最终必须成立的性质 |
| `PRESERVE` | 修改前后必须保持的可观察性质 |
| `FORBID` | 不允许出现的状态、行为或副作用 |
| `ALLOW` | 明确委托给 executor 的自由度或副作用 |

示例：

```text
GOAL    malformed_config_is_handled

REQUIRE invalid_yaml_has_explicit_failure

PRESERVE behavior(valid_legacy_config)

FORBID  change(public_api)

ALLOW   add(private_helper)
```

---

## 3.2 认识论状态

每条 assertion 使用以下 epistemic status：

| 状态 | 含义 |
|---|---|
| `EXPLICIT` | 输入明确表达 |
| `OBSERVED` | 由环境、测试或工具直接观察 |
| `DERIVED` | 由其他事实推导 |
| `ASSUMED` | 暂时假设，允许被证伪 |

示例：

```yaml
assertion:
  id: a1
  predicate: coding.root_cause
  args:
    - coding.symbol: ConfigParser.parse
  epistemic_status: ASSUMED
  provenance:
    source: TEACHER
    source_span: "The problem is probably in parse_config."
```

---

## 3.3 Provenance

每条 clause 或 assertion 应记录来源：

```text
USER
TEACHER
REPOSITORY
DOCUMENTATION
TEST_RESULT
COMPILER
LEAN_KERNEL
EXECUTOR_INFERENCE
```

建议最小字段：

```yaml
provenance:
  source: TEACHER
  source_id: handoff_001
  span: "The issue is probably in parse_config."
```

后续可加入：

- 时间；
- 工具调用 ID；
- 文件和行号；
- teacher model；
- 置信度；
- 是否被后续证据 supersede。

---

## 3.4 Typed Open Slots

最小结构：

```yaml
open_slot:
  id: u1
  type: coding.ErrorPolicy
  owner: USER
  alternatives:
    - RAISE_VALUE_ERROR
    - RETURN_NONE
  status: UNRESOLVED
```

`owner` 可以是：

```text
USER
TEACHER
EXECUTOR
ENVIRONMENT
```

其语义分别为：

- `USER`：需要用户决定；
- `TEACHER`：需要强模型进一步设计；
- `EXECUTOR`：已授权 local executor 自主选择；
- `ENVIRONMENT`：应通过代码、文档、测试或工具调查。

这使系统能够区分：

- 应该澄清；
- 应该升级；
- 应该自行选择；
- 应该继续调查。

---

## 3.5 关系

v0 保留五种通用关系：

| 关系 | 含义 |
|---|---|
| `DEPENDS_ON` | 一个节点依赖另一个节点 |
| `REFINES` | 一个节点进一步精化另一个节点 |
| `CONFLICTS_WITH` | 两个节点语义冲突 |
| `JUSTIFIED_BY` | assertion 由证据或其他 assertion 支持 |
| `VERIFIED_BY` | contract clause 由某 verifier 检查 |

示例：

```yaml
relations:
  - type: VERIFIED_BY
    from: requirement_r1
    to: verification_v1

  - type: JUSTIFIED_BY
    from: assumption_a1
    to: evidence_e3
```

---

## 3.6 Verification Obligations

Contract 不仅应表达“必须满足什么”，还应表达“如何证明已经满足”。

```yaml
verification:
  id: v1
  target: requirement_r1
  method:
    predicate: coding.run_test
    args:
      - test_malformed_yaml
  status: PENDING
```

Coding Dialect 可定义：

```text
RUN_TEST
TYPE_CHECK
STATIC_ANALYSIS
CHECK_API_DIFF
CHECK_DEPENDENCY_DIFF
PROPERTY_TEST
```

Lean Dialect 可定义：

```text
KERNEL_CHECK
CHECK_NO_SORRY
CHECK_NO_NEW_AXIOM
CHECK_IMPORT_POLICY
```

---

# 4. 不属于 Contract IR 的内容

以下内容属于 agent policy 或 Action IR，而不是 Normative Contract：

```text
INSPECT
EXECUTE
EDIT
TEST
CLARIFY
REQUEST_APPROVAL
ESCALATE
SUBMIT
```

Contract IR 描述：

> 什么必须成立，什么不允许发生。

Agent policy 描述：

> 处理当前状态时下一步做什么。

典型推导关系：

### 用户所有的 semantic hole

\[
OPEN<T>,\quad owner=USER
\]

推出：

\[
CLARIFY
\]

### 拟议副作用超出授权

\[
Effects(a)\nsubseteq AllowedEffects(C)
\]

推出：

\[
REQUEST\_APPROVAL
\]

### 任务明确但能力或预算不足

推出：

\[
ESCALATE
\]

### 缺失信息可由环境获得

推出：

\[
INSPECT
\]

因此，`CLARIFY`、`ESCALATE` 等不写入 Core Contract IR，而由 policy 根据 IR 状态生成。

---

# 5. IR 数据结构

## 5.1 内部语义：Typed Attributed Graph

Contract 中天然存在多对多关系：

- 一个 requirement 由多个测试验证；
- 一个测试服务多个 requirement；
- 一个 assumption 依赖多个事实；
- 一个 low-level plan step 服务多个 goal；
- 一段自然语言支持多个 clause。

因此内部语义采用：

\[
\boxed{
G=(V,E,\tau,\alpha)
}
\]

其中：

- \(V\)：节点；
- \(E\)：关系；
- \(\tau\)：节点和边的类型；
- \(\alpha\)：属性、provenance、confidence 等。

---

## 5.2 表面表示：Canonical JSON

模型不直接输出任意 graph，而输出规范化 JSON：

```yaml
entities:
  - id: e1
    type: coding.Component
    value: ConfigParser

clauses:
  - id: c1
    modality: PRESERVE
    predicate: coding.behavior
    args:
      - valid_legacy_config
    strength: HARD
    epistemic_status: EXPLICIT
    provenance:
      source: USER
      span_id: s3

open_slots:
  - id: u1
    type: coding.ErrorPolicy
    owner: USER
    status: UNRESOLVED

verifications:
  - id: v1
    target: c1
    method:
      predicate: coding.regression_test
      args:
        - legacy_config_suite
    status: PENDING

relations:
  - type: VERIFIED_BY
    from: c1
    to: v1
```

解析后再转换为内部 graph。

这样兼顾：

- constrained decoding；
- schema validation；
- deterministic serialization；
- graph semantics；
- canonical comparison；
- 日后扩展。

---

# 6. 三层语义状态

## 6.1 Normative Contract \(C\)

描述：

- goals；
- hard requirements；
- preserve；
- forbid；
- allow；
- user-owned open decisions；
- acceptance and verification obligations。

特性：

- 稳定；
- 默认不可由 executor 修改；
- 只有用户澄清、teacher 修订或明确授权才能改变。

---

## 6.2 Grounded Knowledge State \(K_t\)

描述：

- repository symbol grounding；
- 已观察事实；
- teacher assumptions；
- test results；
- root-cause hypothesis；
- unresolved references；
- conflicts；
- superseded assertions。

例如：

```yaml
assertion:
  predicate: coding.root_cause
  args: [ConfigParser.parse]
  epistemic_status: ASSUMED
  status: SUPERSEDED
```

新证据：

```yaml
assertion:
  predicate: coding.behavior_owner
  args: [Validator.validate]
  epistemic_status: OBSERVED
  provenance:
    source: REPOSITORY
    location: src/validator.py:120-160
```

Knowledge State 允许非单调更新。

---

## 6.3 Execution / Verification Plan \(P_t\)

描述：

- 下一步读取哪些文件；
- 运行哪些命令；
- 修改哪些 symbol；
- 如何验证每条 requirement；
- 当前 milestone；
- 剩余预算。

Plan 可以：

- 回滚；
- 丢弃；
- 重写；
- 在不改变 Contract 的情况下换方案。

示例：

```yaml
plan_step:
  id: p3
  action: coding.modify_function
  target: ConfigParser.parse
  serves:
    - requirement_r1
  permitted_by:
    - allowance_a1
  verified_by:
    - verification_v2
```

---

# 7. Refinement 与 Lowering

## 7.1 Contract Denotation

定义：

\[
\llbracket C\rrbracket
=
\{
\tau:
\tau
\text{ 是满足 }C\text{ 的执行轨迹和终态}
\}
\]

若：

\[
\llbracket C_2\rrbracket
\subseteq
\llbracket C_1\rrbracket
\]

则称：

\[
C_2\sqsubseteq C_1
\]

即 \(C_2\) 比 \(C_1\) 更精确。

示例：

```text
OPEN invalid_input_behavior
```

经用户澄清后变成：

```text
REQUIRE invalid_input_behavior = RAISE_VALUE_ERROR
```

语义可行集合因此收缩。

---

## 7.2 三种不同的更新逻辑

### Contract refinement

尽量单调：

\[
C_{t+1}\sqsubseteq C_t
\]

由澄清、授权和正式修订触发。

### Knowledge revision

允许非单调：

- assumption 可被推翻；
- grounding 可被修正；
- test hypothesis 可被否定。

### Plan revision

可以完全推翻重来。

这三个层次必须在实现和数据中明确区分。

---

## 7.3 Traceability

每个 low-level object 应链接回 high-level semantics：

- plan step → requirement；
- side effect → allowance；
- completion claim → evidence；
- verification → clause；
- assumption → provenance。

这允许系统机械检查：

```text
每一条 REQUIRE 是否被覆盖？
每一个副作用是否被授权？
每一条完成声明是否有 evidence？
是否存在未验证的 hard constraint？
```

---

# 8. Semantic Data Generation v0

## 8.1 不采用简单的 IR → NL paraphrase

简单流程：

\[
C
\xrightarrow{Teacher}
h_1,h_2,\ldots,h_n
\]

只能训练：

- 同义改写不变性；
- 顺序不变性；
- 风格不变性。

它不能训练：

- ambiguity detection；
- omission handling；
- contradiction detection；
- provenance distinction；
- clarification decisions。

---

## 8.2 正确流程

采用：

\[
\boxed{
C
\xrightarrow{\mu}
\widetilde C
\xrightarrow{\text{Teacher verbalizer}}
h
}
\]

其中：

- \(C\)：完整 valid IR；
- \(\mu\)：程序化 semantic mutation；
- \(\widetilde C\)：变换后的 partial/noisy IR；
- \(h\)：teacher 对 \(\widetilde C\) 的忠实自然语言表达；
- student target：\(\widetilde C\)，而不总是原始 \(C\)。

核心原则：

\[
\boxed{
\text{先改变语义，再生成语言。}
}
\]

---

## 8.3 六类 corruption family

### 1. Surface Variation

只改变：

- 措辞；
- 顺序；
- 冗长度；
- 文风；
- 句法形式。

目标 IR 不变。

---

### 2. Information Deletion

删除一个决定性字段。

例如：

```text
REQUIRE invalid_input_policy = RAISE_VALUE_ERROR
```

变成：

```text
OPEN invalid_input_policy : coding.ErrorPolicy
```

再 verbalize：

> Handle invalid input appropriately.

---

### 3. Genuine Ambiguity

保留多个语义候选：

```yaml
open_slot:
  type: coding.ErrorPolicy
  alternatives:
    - RETURN_NONE
    - RAISE_VALUE_ERROR
```

---

### 4. Contradiction Injection

例如同时加入：

```text
FORBID change(public_api)
REQUIRE change(public_api)
```

目标 IR 中必须出现：

```text
CONFLICTS_WITH
```

而不是由 student 随意选择一边。

---

### 5. Unsupported Inference

把技术推测作为自然语言内容：

> The bug is probably caused by parser.py.

目标：

```text
ASSUMED
provenance = TEACHER
```

不能转成 user hard requirement 或 repository fact。

---

### 6. Irrelevant Context

加入：

- 无关日志；
- 历史背景；
- teacher 的泛泛建议；
- 与 contract 无关的解释。

目标 IR 保持不变。

---

## 8.4 Domain-Specific Grounding Corruption

Coding：

```text
"the parser"
```

如果不能唯一绑定，目标应为：

```text
UNRESOLVED_REFERENCE<coding.Component>
```

Lean：

```text
"use the standard induction lemma"
```

若有多个候选，则保留 typed unresolved binding。

---

# 9. “Semantic Diffusion”的使用边界

第一阶段将 “semantic diffusion” 作为启发性类比，而不声称已经实现严格 diffusion model。

当前 v0 更准确的名称是：

```text
Structured Semantic Corruption
+
Teacher Verbalization
+
Semantic Denoising
```

若后续定义：

\[
C_0
\xrightarrow{\mu_1}
C_1
\xrightarrow{\mu_2}
\cdots
\xrightarrow{\mu_T}
C_T
\]

并训练：

\[
p_\theta(C_{t-1}\mid C_t,h,t)
\]

才能更严格地称为 semantic diffusion。

第一阶段使用多维 corruption vector：

\[
\eta=
(
\eta_{\text{surface}},
\eta_{\text{omission}},
\eta_{\text{ambiguity}},
\eta_{\text{conflict}},
\eta_{\text{grounding}},
\eta_{\text{irrelevance}}
)
\]

而不强行压缩成单一 noise level。

---

# 10. 第一版训练任务

建议联合训练四类任务。

## 10.1 Semantic Compilation

\[
h\rightarrow \widetilde C
\]

输出 canonical IR。

---

## 10.2 Semantic Equivalence

\[
(h_1,h_2)
\rightarrow
\{
EQUIVALENT,
DIFFERENT,
UNDECIDABLE
\}
\]

用于学习对表面变化的不变性。

---

## 10.3 Hole / Conflict Detection

\[
h
\rightarrow
\{
COMPLETE,
OPEN,
CONFLICT,
UNRESOLVED
\}
\]

专门训练“不擅自补全”。

---

## 10.4 Provenance Classification

判断一条 proposition 是：

```text
USER_REQUIREMENT
TEACHER_ASSUMPTION
ENVIRONMENT_OBSERVATION
DERIVED_CONCLUSION
```

---

# 11. 数据划分

不能将同一 IR 的不同 paraphrase 随机拆入训练和测试。

至少采用以下 split。

## 11.1 Composition Split

测试训练时未见过的 primitive 组合。

---

## 11.2 Graph-Topology Split

保留新的 dependency / verification graph 结构。

---

## 11.3 Lexical Split

使用新的表达方式和术语。

---

## 11.4 Teacher Split

测试数据由未参与训练数据生成的 teacher model 产生。

---

## 11.5 Domain / Dialect Split

测试未见过的 dialect，评估 universal semantic compiler 的可能性。

---

# 12. v0 实验规模

| 项目 | v0 决定 |
|---|---|
| Core modality | GOAL / REQUIRE / PRESERVE / FORBID / ALLOW |
| Epistemic status | EXPLICIT / OBSERVED / DERIVED / ASSUMED |
| 不确定性 | typed `OPEN<T>` |
| 关系 | DEPENDS / REFINES / CONFLICTS / JUSTIFIED / VERIFIED |
| 内部结构 | typed attributed graph |
| 表面格式 | canonical JSON |
| 语义层次 | Contract / Knowledge / Plan |
| Dialect | Coding + Lean |
| 数据生成 | semantic mutation → teacher verbalization |
| Corruption family | 六类 |
| Student | 7B–8B QLoRA pilot |
| 初始基础 IR | 每领域约 1,000 个 |
| 每个 IR 的 NL views | 10–20 个 |
| 第一阶段总样本 | 每领域约 10,000–20,000 |
| 第一阶段训练 | SFT + constrained decoding |
| 第一阶段不做 | SWE-bench 全量、RL、复杂 agent harness |

---

# 13. Baseline

## A. Raw Natural Language

\[
NL\rightarrow downstream\ answer
\]

---

## B. Generic Structured JSON

例如：

```yaml
goal: ...
constraints: ...
notes: ...
```

用于判断提升是否只是结构化 prompt 效应。

---

## C. Flat Contract IR

包含：

- typed modality；
- OPEN；
- provenance；
- verification；

但不分 Contract / Knowledge / Plan。

---

## D. Hierarchical Contract System

\[
Contract + Knowledge + Plan
\]

用于验证分层本身的增益。

---

# 14. 核心评价指标

## 14.1 Paraphrase Consistency

同一 IR 的不同表达是否恢复为等价 IR。

---

## 14.2 Semantic Sensitivity

真正改变需求或权限时，输出 IR 是否相应变化。

不能通过“一律输出相似 IR”获得高稳定性。

---

## 14.3 OPEN Precision / Recall

- 信息缺失时是否保留 hole；
- 信息明确时是否避免不必要 OPEN。

---

## 14.4 Conflict Detection

是否识别：

- contradictory requirements；
- permission conflicts；
- incompatible assumptions。

---

## 14.5 Provenance Accuracy

是否区分：

- user requirement；
- teacher inference；
- repository observation；
- derived conclusion。

---

## 14.6 Canonicality

语义等价输入是否产生规范化、可比较的 IR。

---

## 14.7 Downstream Behavioral Gain

同一 executor 分别接收 raw NL 和 IR 后，比较：

- contract violation；
- silent assumption；
- clarification quality；
- task completion；
- token and compute cost。

---

# 15. Go / No-Go 标准

以下数值不是领域标准，而是第一阶段继续投入的内部门槛。

建议 Go 条件：

\[
\text{语义等价表达下的输出方差下降至少 }30\%
\]

\[
\text{OPEN recall}\geq85\%
\]

\[
\text{false OPEN rate}\leq10\%
\]

\[
\text{provenance accuracy}\geq90\%
\]

\[
\text{downstream contract violation 至少下降一半}
\]

同时：

- task completion 不出现明显下降；
- 模型不能通过“全部标记 OPEN”获得高可靠性；
- IR 相比 generic JSON 有额外、可统计验证的收益。

---

# 16. 第一阶段明确不做

v0 暂不包括：

- 自动发现 primitive；
- 完整自定义 RIDL；
- latent / continuous IR；
- graph neural network；
- 严格多步 diffusion；
- reinforcement learning；
- SWE-bench 全量；
- 复杂多 agent；
- NL→IR→patch 端到端联合训练；
- 大规模线上 human-in-the-loop。

这些内容均可作为后续阶段，但不应干扰第一轮核心假设验证。

---

# 17. 第一阶段的决定性问题

第一轮实验只回答：

\[
\boxed{
\text{显式、有限、可保留未知、带 provenance 的 Contract IR，是否比 raw NL 和 generic JSON 更能稳定地保留意图并驱动可靠执行？}
}
\]

若答案为否，应优先重新审视：

- primitive；
- unknown representation；
- data corruption process；
- graph/schema complexity；
- teacher bias；

而不是立即扩大模型、数据或 benchmark。

若答案为是，再进入：

1. hierarchical lowering；
2. Coding / Lean executor integration；
3. 24GB local model；
4. SWE-bench / theorem proving；
5. model–harness co-design；
6. constrained RL 或 preference learning。

---

# 18. 最终冻结版本

v0 的最终定义为：

\[
\boxed{
\textbf{一个以五种规范模态为核心、以领域 typed predicate 为操作数、}
}
\]

\[
\boxed{
\textbf{支持 typed holes、provenance、epistemic status 和 verification links 的图语义 IR；}
}
\]

\[
\boxed{
\textbf{其表面采用 canonical JSON，并分为稳定 Contract、可修订 Knowledge、}
}
\]

\[
\boxed{
\textbf{可丢弃 Plan 三个相互引用但更新权限不同的层次。}
}
\]

训练数据生成采用：

\[
\boxed{
\textbf{Valid IR}
\xrightarrow{\text{formal semantic mutation}}
\textbf{Partial / Noisy IR}
\xrightarrow{\text{Teacher verbalization}}
\textbf{Natural Language}
}
\]

student 学习：

\[
\boxed{
\textbf{Natural Language}
\rightarrow
\textbf{Partial / Noisy IR}
}
\]

而不是在信息不足时强行恢复一个原始完整 IR。

这一设计是目前最保守、最可验证、最容易归因，同时也最有可能形成独立研究贡献的第一版方案。
