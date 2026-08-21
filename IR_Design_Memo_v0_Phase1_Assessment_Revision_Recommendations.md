# `IR_Design_Memo_v0_Phase1_Assessment.md` 修改建议

## 文档用途

本文件用于指导 Codex 修改：

```text
IR_Design_Memo_v0_Phase1_Assessment.md
```

修改应以以下两份上游文档为依据：

```text
IR_Design_Memo_v0.md
Semantic_Compiler_Contract_IR_Research_Plan.md
```

当前评估文件的总体方向是正确的：它成功将一个较大的长期研究计划，压缩成了一个有限、可证伪、可归因的实验流程。建议保留其主要实验框架，但在开始实现之前，必须补足若干关键形式语义，并修正可能导致循环论证、baseline 不公平或实验结论过度外推的问题。

建议将本次修改定位为：

> **在保留当前有限语义实验框架的基础上，对 Contract / Knowledge 边界、OPEN 的执行语义、冲突分类、micro-world 中立性、baseline、executor 和 Go / No-Go 逻辑进行重大补充。**

---

# 一、总体修改原则

## 1. 保留当前评估文件的核心方向

以下内容原则上保留，不应因本轮修改被重新扩张：

- 第一轮只采用一个有限 dialect；
- 不直接进入真实 repository、Lean、SWE-bench 或任意 patch generation；
- 先构建 schema、type checker、canonicalizer 和 reference interpreter；
- 先做程序化 semantic mutation，再由 teacher verbalize；
- 数据按完整 lineage 划分 train / validation / test；
- 设置人工撰写的 confirmatory test set；
- generic JSON 必须与 Contract IR 信息量匹配；
- 所有结构化输出采用同等级 constrained decoding；
- 同时比较 Oracle representation 与 Predicted representation；
- 统计独立单位是 base scenario，而不是 paraphrase；
- 同时报告 reliability、coverage、completion 和 cost；
- 任一前置阶段失败时，不通过扩大模型、增加 paraphrase 或增加领域掩盖问题。

## 2. 不把当前实验误称为完整 Coding Phase 1

当前文件提出的有限动作 micro-world，本质上更接近原 Research Plan 中的：

```text
Phase 0: Toy Semantic Compiler
```

而不是完整的：

```text
Phase 1: Coding Contract IR
```

因此应修改文档定位。可采用以下任一名称：

```text
Stage 0A–0F: Formal Contract IR Falsification Pilot
```

或：

```text
Phase 1A: Finite Semantic Kernel
```

文档应明确：

> micro-world 实验通过，只能证明有限 dialect 中的表示和执行收益；不能直接证明 Contract IR 已经适用于真实 coding agent。

---

# 二、必须解决的五项 blocking issues

以下五项应视为开始生成正式数据之前必须冻结的设计。

---

## 1. 不做完整动态 C/K/P，但必须保留静态 Contract / Knowledge 类型边界

当前评估文件建议第一阶段只保留静态 Contract 和 source-attributed claim，这一缩减总体正确；但不能将以下三个维度混成单一标签：

1. provenance：命题来自哪个 source event 或 source span；
2. epistemic status：命题是明确陈述、观察、推导还是假设；
3. normative authority：该来源是否有权修改 Contract。

例如：

```text
USER: I think the bug may be in parser.py.
```

正确表示应类似：

```yaml
kind: KNOWLEDGE_ASSERTION
predicate: coding.root_cause
args: [parser.py]
epistemic_status: ASSUMED
normative_authority: NONE
provenance:
  source_role: USER
  source_id: message_001
  span_id: span_003
```

不能因为 provenance 是 `USER`，就把它自动解释为用户 hard requirement。

又例如：

```text
ASSISTANT: As you requested, the public API must not change.
```

表面 provenance 是 `ASSISTANT`，但规范性 authority 应追溯到被引用的 USER span，而不是由 assistant 自己产生。

### 建议的第一阶段最小 schema

第一阶段可以删除动态 `Plan`，也可以暂不实现 Knowledge revision，但至少保留两类静态对象：

```yaml
contract_clauses:
  - id
  - modality
  - predicate
  - args
  - strength
  - epistemic_status
  - normative_authority
  - provenance

knowledge_assertions:
  - id
  - predicate
  - args
  - epistemic_status
  - normative_authority
  - provenance
```

建议增加明确规则：

```text
normative_authority ∈ {USER, DELEGATED_TEACHER, EXECUTOR, NONE}
```

第一阶段通常只有：

- 用户明确提出的命题可直接进入 normative Contract；
- assistant / teacher 的技术判断默认进入 Knowledge；
- tool observation 进入 Knowledge；
- 只有显式授权或可追溯引用，teacher proposition 才能获得 Contract authority。

### 需要修改当前文件的地方

当前文件第 5 节中类似：

```text
USER_EXPLICIT
ASSISTANT_HYPOTHESIS
TOOL_OBSERVATION
```

的标签可以保留为便捷的派生类别，但不能作为底层数据模型。应改成由以下正交字段组合产生：

```text
source_role × epistemic_status × normative_authority
```

---

## 2. 为 typed `OPEN` 增加安全执行语义，而不只定义 denotation

当前文件已经规定：

- `OPEN` 有有限类型；
- `admissible_values` 是完整候选域；
- unresolved slot 表示所有合法补全；
- resolution 不得扩大合法执行集合。

这些规定仍不足以判断 executor 何时可以行动、何时必须 `ASK`。

设一个 open slot 为：

\[
u : T, \qquad V_u = \{v_1,\ldots,v_n\}
\]

所有可能的 Contract completion 为：

\[
\mathcal{C}(u)
=
\{C[u=v] \mid v\in V_u\}
\]

从表示的 denotation 角度，可以定义：

\[
\llbracket C[u]\rrbracket
=
\bigcup_{v\in V_u}
\llbracket C[u=v]\rrbracket
\]

但可靠执行不能使用这个并集直接选择 action。对于用户所有的未知项，一个无需澄清即可执行的 action，必须对所有 admissible completion 都安全：

\[
A_{\mathrm{safe}}(u)
=
\bigcap_{v\in V_u}
A_{\mathrm{valid}}(C[u=v])
\]

### 建议冻结的决策规则

#### `resolver_authority = USER`

\[
\mathrm{ExecutableWithoutAsk}(a,u)
\iff
\forall v\in V_u,
\ a\models C[u=v]
\]

若不存在满足该条件的有效 action，则应输出：

```text
ASK
```

#### `resolver_authority = EXECUTOR`

允许 executor 选择一个 admissible value，但必须：

- 选择值属于 `admissible_values`；
- 记录选择；
- 后续验证基于被选择的 completion；
- 不得将选择伪装成用户明确要求。

形式上：

\[
\exists v\in V_u:
 a\models C[u=v]
\]

并输出 resolution trace。

#### `resolver_authority = ENVIRONMENT`

第一阶段可以简化为：

- 若有限 observation action 能唯一解析 slot，则先 `INSPECT`；
- 若 micro-world 不实现 inspection，可暂时统一为 `ASK/REJECT`，但必须在 scope 中写清。

### 必须区分两类候选范围

应区分：

```text
schema-defined admissible domain
```

和：

```text
natural-language explicitly mentioned alternatives
```

例如 dialect 已冻结：

```text
coding.ErrorPolicy = {
  RETURN_NONE,
  RAISE_VALUE_ERROR,
  RAISE_PARSE_ERROR
}
```

即使文本没有逐项列出，IR 仍可引用该完整类型域；但不能声称这些 alternatives 是用户明确列出的。

### 增加相关评价指标

- necessary ASK recall；
- unnecessary ASK rate；
- unsafe execute under USER-owned OPEN；
- valid autonomous resolution under EXECUTOR-owned OPEN；
- resolution trace correctness。

---

## 3. 将 conflict 从单一类别拆成至少四类

当前文件把 contradiction 主要定义为 Contract 不可满足，并要求返回 conflict witness。这对部分冲突正确，但不适用于所有 modality 和 assertion 组合。

例如：

```text
REQUIRE api_changed(X)
FORBID  api_changed(X)
```

通常是 hard unsatisfiable。

但：

```text
ALLOW  api_changed(X)
FORBID api_changed(X)
```

未必不可满足。`ALLOW` 只表示授权，不表示必须发生；选择不改变 API 的轨迹仍可能满足 Contract。这可能是 policy tension 或冗余规则，而不是 SAT 意义上的矛盾。

同样：

```text
ASSUMED bug_in(parser)
OBSERVED bug_in(validator)
```

是 epistemic contradiction，不是 normative Contract unsat。

### 建议的 conflict taxonomy

```text
HARD_UNSAT
NORMATIVE_TENSION
EPISTEMIC_CONTRADICTION
AUTHORITY_CONFLICT
```

#### `HARD_UNSAT`

不存在满足全部 hard Contract clauses 的执行轨迹。

第一阶段正式 conflict oracle 建议只覆盖这一类，例如：

- `REQUIRE p` 与 `FORBID p`；
- `REQUIRE p` 与 `REQUIRE not_p`；
- 两个互斥 enum resolution 同时被 REQUIRE；
- 一个 required effect 未得到 default-deny managed effect universe 中的必要授权，且无合法替代轨迹。

#### `NORMATIVE_TENSION`

规则之间存在覆盖、冗余或优先级问题，但 Contract 仍可满足。

第一阶段可以标注但不纳入主要 conflict F1，或暂时排除。

#### `EPISTEMIC_CONTRADICTION`

Knowledge assertions 在相同 scope、时间和实体上不兼容。

它不应自动使 Normative Contract 不可满足。

#### `AUTHORITY_CONFLICT`

不同来源对 Contract 的修改主张不一致，但来源权威不同。

例如 assistant 自行提出的 requirement 与 user explicit requirement 冲突。系统应优先按 authority 处理，而不是把两者等价地送入 SAT solver。

### 修改要求

- 为每类 conflict 定义 witness；
- 明确第一阶段主要指标究竟评价哪一类；
- 避免把 `ALLOW + FORBID` 自动标成 hard unsat；
- 避免把 Knowledge disagreement 直接当 Contract contradiction；
- 若第一阶段只实现 `HARD_UNSAT`，必须在文档中明确限制结论。

---

## 4. 将 micro-world 改成 representation-neutral 的环境语义

当前文件建议直接使用：

```text
api_changed
behavior_preserved
dependency_added
effect_occurred
```

等 predicate，同时 Contract IR 也使用这些 predicate。若直接以相同 ontology 设计 world、gold 和 oracle，容易形成循环论证：

1. 使用 Contract IR ontology 设计环境；
2. 使用同一 ontology 定义正确答案；
3. 再证明 Contract IR 比 generic JSON 更适合该 oracle。

这只能证明“与 oracle 共享 ontology 的表示更易连接到 oracle”，不能充分证明 Contract IR 的额外价值。

### 建议先定义中性的 world model

\[
W=(S,A,T,O,E)
\]

其中：

- \(S\)：环境状态；
- \(A\)：候选动作；
- \(T\)：状态转移函数；
- \(O\)：可观察量；
- \(E\)：轨迹中的 effect event。

环境自身不依赖某一种输出 schema。

不同 representation 分别通过独立 parser 映射到共同 semantic model：

\[
\pi_R:
\mathrm{Output}_R
\rightarrow
\mathcal{S}_{common}
\]

其中：

```text
R ∈ {
  RAW_NL,
  GENERIC_JSON,
  SCHEMA_MATCHED_JSON,
  CONTRACT_IR
}
```

所有 satisfaction、conflict、OPEN 和 action-validity 判断，都应在共同的 `semantic model` 上完成，而不是直接比较某个 schema 的字段或 byte equality。

### 建议增加三层评价

1. **Syntax / schema validity**：能否被各自 parser 接受；
2. **Semantic projection accuracy**：映射后的共同语义是否正确；
3. **Behavioral equivalence**：投影结果是否诱导相同合法 action set。

### 防止 ontology leakage 的具体措施

- world state 和 action 使用内部枚举 ID，不直接复用 IR 字段名；
- generic JSON 与 Contract IR 使用各自 serialization；
- oracle 只读取共同 semantic projection；
- field name、字段顺序和示例数量尽量控制；
- 下游 executor 不应通过识别 `FORBID` 字样而绕过语义解析；
- 增加 field-renaming 或 canonical label permutation robustness check。

---

## 5. 重新定义 downstream executor 实验

当前文件要求固定 executor checkpoint、prompt、预算和 action set，这是必要条件，但仍不足以区分：

- compiler 是否恢复了正确语义；
- representation 是否易于被 runtime 机械解释；
- LM executor 是否真的利用了表示。

建议将 downstream 分为两层。

### 第一层：确定性 semantic runtime

```text
Predicted representation
→ representation-specific parser
→ common semantic projection
→ deterministic action oracle
```

目的：

- 隔离 compiler error；
- 检查表示是否保留了足够的执行语义；
- 得到可完全复现的 violation、ASK 和 completion 指标。

这一层是第一阶段最干净的主要实验。

### 第二层：固定 LM executor

```text
Raw NL / Generic JSON / Contract IR
→ same frozen LM executor
→ action / ASK / REJECT
```

目的：

- 检查 Contract IR 是否作为 harness interface 改善实际 LM 行为；
- 检查不同表示是否降低 executor 的推理负担。

必须固定：

- executor checkpoint；
- system prompt；
- task information；
- candidate action set；
- maximum token budget；
- retry budget；
- decoding parameters；
- wall-clock / tool budget；
- action ordering和 display format。

### 必须增加的 executor-use 检查

加入 corrupted IR：

- modality permutation；
- OPEN owner permutation；
- provenance permutation；
- clause deletion；
- irrelevant field insertion。

若这些 corruption 不改变 executor 行为，则说明 executor 没有真正使用 IR，当前 downstream gain 不能归因于 Contract semantics。

---

# 三、Baseline 需要进一步增强

当前文件已经要求 content-matched generic JSON，但仍应将 baseline 分得更细，以避免 Contract IR 仅因字段更丰富或 schema 更接近 oracle 而获益。

## 建议的表示层 baseline

1. `Raw NL`；
2. `Raw NL + matched analysis budget`；
3. `Free-form generic JSON`；
4. `Schema-matched untyped JSON`；
5. `Typed IR without OPEN`；
6. `Typed IR without provenance`；
7. `Typed IR without authority separation`；
8. `Full Contract IR`；
9. `Oracle generic JSON`；
10. `Oracle Contract IR`。

### `Schema-matched untyped JSON` 的要求

它必须能够表达与 Contract IR 相同的信息，例如：

```yaml
goals:
  - text: preserve valid legacy behavior

constraints:
  - kind: do_not
    text: change public API

unknowns:
  - field: invalid input behavior
    possible_values:
      - return none
      - raise value error

source_notes:
  - text: parser.py may contain the bug
    source_role: assistant
    status: hypothesis
```

它与 Contract IR 的差异应主要是：

- 缺少正式 modality type；
- 缺少 typed predicate signature；
- 缺少正式 OPEN refinement semantics；
- 缺少机械 authority / satisfaction rules。

不能故意删除 unknown、source 或约束信息，否则 baseline 不公平。

## 解码与预算匹配

所有结构化表示必须：

- 获得同等级 constrained decoding；
- 使用近似相同的示例数量；
- 使用相同 checkpoint；
- 报告输入和输出 token 数；
- 报告 schema validation retry；
- 对字段长度差异进行 cost accounting。

`Raw NL + matched analysis budget` 用于控制：

> 收益是否仅仅来自让模型先进行一个额外的显式分析步骤。

---

# 四、数据生成与数据划分补充

## 1. 区分 generation provenance 与 proposition provenance

teacher verbalizer 生成了某句话，并不意味着该句话中的 proposition 来源是 teacher。

必须分别记录：

```yaml
generation_provenance:
  generator_model: ...
  prompt_version: ...
  decoding_seed: ...

proposition_provenance:
  source_role: USER
  source_id: message_001
  span_id: span_004
```

例如 teacher 可以 verbalize 一个 USER requirement；此时：

- generation provenance = teacher；
- proposition provenance = user。

## 2. Mutation 必须有形式语义合同

每种 mutation 应实现成：

```text
mutation(input_semantics)
→ output_semantics + machine-checkable certificate
```

建议冻结以下性质：

- surface variation：denotation 不变；
- information deletion：合法执行集合不得缩小；
- genuine ambiguity：产生 typed OPEN，且候选域可计算；
- hard contradiction：输出 semantic model 不可满足，并返回 witness；
- unsupported inference：只增加 Knowledge assertion，不改变 Normative Contract；
- irrelevant context：Contract denotation 不变；
- provenance counterfactual：文本命题相同，只改变 source envelope，gold authority / epistemic role 相应变化。

## 3. 增加 same-text / different-role counterfactual

构造完全相同的 proposition：

```text
The public API must not change.
```

分别放在：

- USER message；
- ASSISTANT hypothesis；
- TOOL observation；
- quoted user statement in assistant message。

测试模型是否真正读取 source envelope，而不是仅凭词面推断 provenance。

## 4. 同时保留 IR-first 与 NL-first 数据

### IR-first synthetic set

```text
Valid semantic object
→ mutation
→ verbalization
```

用于大规模训练和可控消融。

### NL-first human set

```text
Human writes instruction independently
→ annotators construct semantic gold
```

用于检验：

- 真实语言分布；
- generator artifacts；
- teacher style leakage；
- IR ontology 是否只适合 IR-first 数据。

人工 confirmatory set 不能只是让人类改写已有 IR verbalization，而应包含独立写作的任务。

## 5. Split 规则继续保留并加强

完整 lineage 必须进入同一 split：

```text
scenario family
→ base world
→ base contract
→ mutation
→ verbalization
→ decoding seed
```

另需尽量隔离：

- world template family；
- predicate composition；
- action effect pattern；
- verbalizer model；
- prompt template；
- human author；
- annotator overlap。

---

# 五、重新组织研究问题

建议在文档前部增加四个彼此独立的研究问题：

\[
RQ_1:
\text{Oracle Contract IR 是否比信息量匹配的 generic JSON 有表示和 runtime 上限收益？}
\]

\[
RQ_2:
\text{NL 是否可以稳定编译为 Contract IR？}
\]

\[
RQ_3:
\text{Structured semantic mutation 是否优于 paraphrase-only 数据？}
\]

\[
RQ_4:
\text{Contract IR 是否降低达到给定可靠性所需的模型规模？}
\]

第一轮 finite semantic kernel 应主要回答：

```text
RQ1 + RQ2 + RQ3
```

`RQ4` 明确后移到 model scaling 阶段。

### 对 QLoRA 的修正表述

可以保留：

> 在确认 Oracle representation 有下游价值之前，不必立即训练 7B–8B student。

但应补充：

- QLoRA 对 `RQ1` 不是必需；
- 对 `RQ2`、`RQ3`，最终必须有 learned compiler 实验；
- prompted compiler 可作为 pilot 或冻结 baseline，不能替代全部 student-learning 结论；
- “small model approaches large model”必须另设 model-size scaling 实验，不能由第一阶段外推。

---

# 六、修正 Go / No-Go 逻辑

当前文件的 Oracle / Predicted 三级裁决应扩展为四种主要结果。

## 情况 A：Oracle Contract IR 不优于 Oracle generic JSON

结论：

```text
specialized Contract representation / runtime No-Go
```

优先检查：

- modality 是否提供额外语义；
- OPEN 的 action semantics 是否有效；
- authority / provenance 是否被 runtime 使用；
- world 是否过于简单；
- Contract IR 是否只是复杂 JSON。

## 情况 B：Oracle Contract IR 有益，但 Predicted Contract IR 无益

结论：

```text
representation potentially useful;
compiler or data generation No-Go
```

检查：

- teacher fidelity；
- mutation correctness；
- schema complexity；
- source observability；
- constrained decoding；
- training objective；
- synthetic-to-human distribution shift。

## 情况 C：Predicted generic JSON 与 Predicted Contract IR 相近，且二者都优于 Raw NL

结论：

```text
只证明 structured decomposition 有价值；
尚未证明 typed Contract IR 有额外价值。
```

这种结果不能写成第一阶段核心假设通过。

## 情况 D：Predicted Contract IR 优于 Predicted schema-matched generic JSON

且满足：

- hard-contract violation 显著下降；
- valid completion 不劣；
- coverage 不劣；
- unnecessary ASK 不显著增加；
- 在 human-written set 上方向一致；
- corrupted IR 会按预期改变 executor 行为；

则可判定第一阶段核心假设通过。

## 冻结主要 contrast

建议 confirmatory experiment 的主要比较明确为：

\[
\boxed{
\text{Predicted Contract IR}
\quad\text{vs}\quad
\text{Predicted schema-matched generic JSON}
}
\]

Raw NL 是重要 baseline，但不是证明 Contract-specific semantics 的充分对照。

## 冻结主要 outcome

建议采用：

```text
base-scenario-level hard-contract violation rate
```

作为主要 outcome。

同时预注册：

- valid completion non-inferiority margin；
- coverage non-inferiority margin；
- unnecessary ASK ceiling；
- cluster bootstrap confidence interval；
- paired base-scenario analysis。

## 单独验证 mutation 方法

要支持 structured semantic corruption 的独立贡献，必须比较：

```text
mutation-trained compiler
vs
paraphrase-only-trained compiler
```

主要关注：

- OPEN recall；
- false OPEN；
- hard conflict detection；
- unsupported inference；
- provenance counterfactual；
- minimal-pair sensitivity；
- human-written set generalization。

否则实验最多证明 IR 有用，不能证明当前 synthetic data 方法有用。

---

# 七、增加 Controlled Real-Code Bridge

micro-world 通过后，不建议直接进入 hierarchy、任意 patch generation 或 SWE-bench。应先增加一个真实代码桥接阶段。

## 建议名称

```text
Phase 1G: Controlled Real-Code Bridge
```

## 任务形式

使用小型 Python repository 或人工控制的真实代码库：

- 每个任务提供 3–8 个候选 patch；
- 候选 patch 的 API diff、dependency diff、test effect 和 side effect 可机械计算；
- executor 只选择 patch、`ASK` 或 `REJECT`；
- 不要求模型生成任意 patch；
- 每个任务包含 machine-checkable Contract；
- 同时包含 synthetic instruction 和 independent human instruction。

## 该阶段的价值

它保留：

- 真实代码；
- 真实测试；
- 真实 API / dependency effects；
- 可机械 oracle；
- 有限 action space；
- 较低实现成本。

它可以检验 micro-world 结果是否迁移到真实 coding semantics，同时避免任意 patch generation 带来的巨大噪声。

只有通过该桥接阶段，才建议进入：

- repository grounding；
- plan generation；
- arbitrary patch generation；
- SWE-bench subset；
- hierarchy / lowering；
- Coding + Lean 多领域比较。

---

# 八、建议重写后的文档结构

请将目标文件重组为以下结构，避免新增内容散落在原章节中。

```text
1. 文档定位与结论边界
2. 第一阶段研究问题 RQ1–RQ3
3. 实验范围与明确排除项
4. Representation-neutral micro-world
5. 第一阶段静态语义 schema
   5.1 Normative Contract
   5.2 Knowledge Assertions
   5.3 Provenance
   5.4 Epistemic Status
   5.5 Normative Authority
6. Typed OPEN 的 denotation 与 action semantics
7. Conflict taxonomy 与 mechanical oracle
8. Source Envelope 与数据可观察性
9. Semantic Mutation 与数据生成
10. Split、人工 Gold 与 fidelity audit
11. Representation baselines 与 ablations
12. Deterministic runtime 实验
13. Frozen LM executor 实验
14. Metrics、统计单位与功效设计
15. 四级 Go / No-Go
16. Controlled Real-Code Bridge
17. 第一阶段允许和不允许支持的结论
18. 实施顺序与 deliverables
```

---

# 九、建议的实施顺序

可在现有 1A–1F 基础上改写为：

| 阶段 | 工作 | 主要目的 | 阻断条件 |
|---|---|---|---|
| 0A 语义冻结 | 中性 world model、common semantic projection、Contract/Knowledge schema、authority/provenance/status 正交化 | 消除 ontology 和标签歧义 | 无法机械定义 denotation / authority |
| 0B OPEN / Conflict Kernel | OPEN safe-action semantics、ASK oracle、HARD_UNSAT oracle、witness | 使核心语义可执行 | OPEN 或 conflict 无法穷举判定 |
| 0C 手写 Gold | 独立人写场景、source-role counterfactual、标注指南 | 验证任务可判定 | adjudication 低或多 gold 不等价 |
| 0D Mutation Pilot | semantic mutation、certificate、teacher fidelity audit、lineage split | 验证数据管线 | mutation 改变错误语义或 teacher 泄漏 target |
| 0E 无训练 Baseline | raw NL、matched analysis、schema-matched JSON、prompted Contract IR | 判断表示上限和任务可学性 | Oracle IR 无上限收益 |
| 0F Learned Compiler | paraphrase-only vs mutation-trained；小规模到 QLoRA | 验证 RQ2 / RQ3 | synthetic gain 不迁移到 human set |
| 0G Deterministic Runtime | predicted representation → common semantics → oracle action | 干净测量 compiler + representation | 收益仅来自拒绝或 OPEN 泛滥 |
| 0H Frozen LM Runtime | 同一 executor 使用不同输入表示 | 验证 harness interface | corrupted IR 不影响行为 |
| 1G Real-Code Bridge | 小 repo + 候选 patch + 机械 verifier | 检验真实 coding 迁移 | micro-world 收益无法迁移 |

阶段名称可以继续使用原文件的 1A–1F，但内容必须包含以上依赖关系。

---

# 十、Codex 修改后的交付要求

请 Codex 输出：

## 1. 主文档

```text
IR_Design_Memo_v0_Phase1_Assessment_v2.md
```

要求是完整可独立阅读的修订版，而不是仅输出 patch 或零散意见。

## 2. Change Log

在文档末尾增加：

```text
Appendix A: Revision Log
```

逐项说明：

- 哪些原章节被保留；
- 哪些被删除；
- 哪些被改写；
- 新增了哪些 formal definitions；
- 实验阶段名称是否调整；
- Go / No-Go 如何变化。

## 3. Open Questions

增加：

```text
Appendix B: Remaining Open Decisions
```

只列出真正不能在当前阶段凭原则冻结的参数，例如：

- default-deny managed effect universe 的具体元素；
- formal pilot 后的最小效应量；
- LM executor checkpoint；
- QLoRA 模型和训练预算；
- real-code bridge 的 repository selection。

不要把本文已经给出明确建议的核心语义重新列为开放问题。

---

# 十一、修订版验收标准

修改完成后，文档必须满足以下全部条件。

## 语义层

- [ ] Contract 与 Knowledge 在第一阶段仍是不同的对象类型；
- [ ] provenance、epistemic status、normative authority 是三个正交字段；
- [ ] generation provenance 与 proposition provenance 被区分；
- [ ] typed OPEN 具有 denotation、safe-action 和 ASK 语义；
- [ ] USER-owned 与 EXECUTOR-owned OPEN 的量词语义不同；
- [ ] schema domain 与文本显式 alternatives 被区分；
- [ ] conflict 至少区分 HARD_UNSAT 与 epistemic / normative 非 SAT 冲突；
- [ ] `ALLOW + FORBID` 不被无条件判定为 hard unsat。

## 实验层

- [ ] micro-world 先定义中性的 \(W=(S,A,T,O,E)\)；
- [ ] 所有表示映射到共同 semantic projection；
- [ ] generic JSON 能表达同样的 unknown、source 和 constraint 信息；
- [ ] 所有结构化条件获得同等级 constrained decoding；
- [ ] deterministic runtime 与 frozen LM executor 被分开；
- [ ] corrupted IR 用于检查 executor 是否真正读取语义字段；
- [ ] split 以完整 scenario lineage 为单位；
- [ ] 有 independent NL-first human confirmatory set；
- [ ] 主要统计单位是 base scenario；
- [ ] completion、coverage 和 unnecessary ASK 被同时控制。

## 结论层

- [ ] 主要 contrast 是 Predicted Contract IR vs Predicted schema-matched generic JSON；
- [ ] generic JSON 与 Contract IR 同样优于 raw NL 时，不宣称 Contract-specific hypothesis 通过；
- [ ] mutation-trained vs paraphrase-only 被单独比较；
- [ ] QLoRA 的“可选”只适用于 Oracle / prompted representation pilot；
- [ ] micro-world 结果不被外推为真实 coding agent 结论；
- [ ] 在 micro-world 与 SWE-bench 之间增加 controlled real-code bridge；
- [ ] 第一阶段允许和禁止支持的结论被明确列出。

---

# 十二、最终修改目标

修订后的评估文件应形成一条严格的证伪链：

```text
中性有限环境语义
→ 静态 Contract / Knowledge schema
→ OPEN 与 hard conflict 的机械语义
→ 人工 Gold
→ 可审计 semantic mutation
→ 信息量匹配的 representation baseline
→ Oracle upper bound
→ Learned compiler
→ Deterministic runtime
→ Frozen LM runtime
→ Controlled real-code bridge
```

最终应使第一阶段能够清楚地区分以下四种结论：

1. Contract IR 本身没有超过普通结构化表示；
2. Contract IR 有上限价值，但 compiler 或数据生成失败；
3. 结构化 decomposition 有价值，但 Contract-specific typing 没有额外价值；
4. Predicted Contract IR 确实在信息量、预算和 coverage 匹配时降低契约违规。

只有第 4 种结果，才支持继续投入 hierarchy、grounding、Coding / Lean executor 和 model–harness co-design。
