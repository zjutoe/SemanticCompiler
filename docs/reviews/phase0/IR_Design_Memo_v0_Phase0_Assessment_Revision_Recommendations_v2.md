> [!CAUTION]
> **STATUS: HISTORICAL INPUT / SUPERSEDED / NON-AUTHORITATIVE**
>
> 本文件针对现已删除的历史 assessment，仅作为历史输入保留，绝不能驱动当前工作。当前唯一权威入口是
> [`IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md`](../../../Phase0/IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md)。本状态块之前的原始 bytes 仍完整保存在 Git 历史 commit `af1833e` 中。

# Contract IR v0 Phase 0 实验协议第二轮修订意见

## 文档用途

本文针对 `IR_Design_Memo_v0_Phase0_Assessment.md` 提出第二轮修订要求，供 Codex 直接据此修改当前 Phase 0 文档。

当前版本已经解决上一轮评估中的大部分核心问题，包括：Phase 0 范围收缩、representation-neutral micro-world、common semantic projection、Oracle parity、静态 Contract/Knowledge 分离、多 slot `OPEN`、`HARD_UNSAT` 与 `NO_AUTHORIZED_ACTION` 分离、source envelope、lineage split，以及 deterministic runtime 与 frozen LM executor 的分层。

因此，本轮不要求推翻或重写整体设计。修订重点是消除以下仍会影响实验结论有效性的歧义：

1. 当前 schema-matched generic JSON 与 Contract IR 几乎语义同构，导致 RQ1 实际检验的问题过窄；
2. learned compiler 的真实输入、模型输出与 deterministic elaborator 的职责尚未冻结；
3. 下游行为评价尚未明确区分 predicted semantics 与 gold semantics；
4. `ASK(slot_ids)` 在多 slot 情况下没有唯一、可机械评价的正确性定义；
5. `EXPLICITLY_DELEGATED` 只有授权链，没有授权范围；
6. RQ3 仍可能退化成“见过困难样本优于没见过困难样本”的平凡比较；
7. deterministic runtime 与 LM executor 的失败仍可能被错误归因到同一层次。

建议将当前文档从“Assessment”进一步改名为：

```text
IR_Design_Memo_v0_Phase0_Experimental_Protocol.md
```

若暂不改名，不影响内容实施，但正文应明确它已经是一份实验协议，而非仅仅是评估意见。

---

# 1. 应保留、不应回退的既有决定

Codex 修改时应保留以下设计，不要因本轮修订重新打开：

1. **Phase 0 只做有限 semantic-kernel pilot**，不纳入 repository grounding、真实 patch、Lean、SWE-bench、动态 C/K/P lowering、model-size scaling 或 RL。
2. 使用与输出格式无关的有限环境：

   \[
   W=(S,A,T,O,E)
   \]

3. 所有 structured representation 必须通过独立 adapter 投影到共同语义空间，runtime 不直接读取原始字段名。
4. 信息匹配、无损投影的 Oracle Contract IR 与 Oracle isomorphic JSON 应达到 runtime parity；Oracle 阶段不是 Contract IR superiority test。
5. Phase 0 保留静态 Normative Contract 与 Knowledge State，Plan 暂不进入学习目标。
6. active Contract 由 deterministic authority gate 派生，而不是由模型直接生成。
7. normative authority 与 `OPEN` resolution authority 分离。
8. 多个 `OPEN` 必须按 joint completion 解释，不能逐 slot 贪心解析。
9. `HARD_UNSAT` 与 `NO_AUTHORIZED_ACTION` 必须分开报告。
10. generation provenance 与 proposition provenance 必须分开。
11. data lineage 以 base scenario 为独立单位，mutation、verbalization 和 seed 不得跨 split。
12. deterministic semantic runtime 是主要归因实验；frozen LM executor 是接口与实际利用诊断。
13. micro-world 通过后，真实代码桥接属于后续 Phase 1，而不是 Phase 0 Go 条件。

---

# 2. Blocking Revision A：拆分“语义模型价值”与“序列化价值”

## 2.1 当前问题

当前 `SchemaMatchedGenericJSON` 使用：

```text
DESIRED_OUTCOME
MUST_HOLD
KEEP_SAME
MUST_NOT_HAPPEN
MAY_HAPPEN
FACTUAL_CLAIM
```

并同时携带：

- typed predicate；
- typed arguments；
- authority；
- provenance；
- epistemic basis；
- typed unknown；
- schema domain；
- context-admissible values；
- owner；
- delegation trace。

这与 Contract IR 中的 `GOAL / REQUIRE / PRESERVE / FORBID / ALLOW / KnowledgeAssertion` 基本一一对应。因此，它不是“普通 generic JSON”，而是：

> 同一个 Contract common semantic model 的另一种 surface encoding。

这个 baseline 很有价值，但它只能回答：

> 在共同语义完全相同的前提下，Contract IR 的字段组织、标签和 canonical serialization 是否更容易被模型恢复？

它不能单独回答：

> 显式 modality、typed `OPEN`、authority、provenance 和 Contract/Knowledge 分离是否比普通结构化分析有价值？

当前 Level 3 将“Contract IR 与 isomorphic JSON 相近”直接判为不进入 Phase 0 Go，过于严格，也会把“语义模型有效但序列化不唯一”误判为核心假设失败。

## 2.2 必须拆分的研究问题

建议将 RQ1 拆成两个正式子问题。

### RQ1a：Semantic-model hypothesis

显式的 Contract common semantic model 是否比只进行内容整理、但不显式编码规范模态、typed unknown、authority 和 C/K 类型边界的结构化表示更可靠？

### RQ1b：Encoding / factorization hypothesis

在承载完全相同 common semantics 时，当前 Contract IR serialization 是否比一个 semantic-isomorphic JSON serialization 更容易学习、更稳定或更节省成本？

可另设一个次级问题：

### RQ1c：LM-interface hypothesis

在 common semantics 相同的情况下，frozen LM executor 是否更容易正确消费 Contract IR，而不是其他同构编码？

RQ1c 是 harness/interface 研究问题，不应与 RQ1a 的 semantic-model validity 混为一体。

## 2.3 建议的表示条件

Phase 0 至少保留以下四种条件：

### A. Full Contract IR

当前正式 Contract IR。

### B. Semantic-isomorphic JSON control

与 Contract IR 无损映射到同一个 common semantic state，但使用不同字段组织和标签。当前 `SchemaMatchedGenericJSON` 应重命名为类似：

```text
SemanticIsomorphicJSON
```

避免继续把它描述为普通 generic JSON。

### C. Content-matched untyped JSON

它应包含相同 source text 中可观察的任务内容，例如：

```yaml
goals:
  - "handle malformed input"
constraints:
  - "do not change the public API"
unknowns:
  - "invalid-input behavior is unspecified"
source_notes:
  - text: "The bug may be in parser_03"
    source_event_id: message_002
```

但不提供：

- 冻结的 normative modality algebra；
- typed predicate signature；
- mechanically interpreted authority gate；
- typed `OPEN` completion domain；
- Contract 与 Knowledge 的强制 sum-type distinction。

该 baseline 的目的不是与 Contract IR 语义同构，而是回答“明确 Contract semantics 是否比普通结构化 decomposition 有增量价值”。

### D. Raw NL + matched analysis budget

作为次级诊断，判断收益是否仅来自更多显式思考、更多 token 或分步分析。

## 2.4 推荐的裁决逻辑

建议使用以下结论表：

| 结果 | 允许结论 | 项目处理 |
|---|---|---|
| A、B 均不优于 C | 未证明显式 Contract semantic model 有价值 | RQ1a No-Go 或 Inconclusive |
| A、B 均优于 C，且 A≈B | 显式 Contract common semantics 有价值，但当前 serialization 不具有唯一优势 | RQ1a Go；RQ1b No-Go/Inconclusive；项目可继续 |
| A、B 均优于 C，且 A>B | common semantics 有价值，当前 Contract IR encoding 还有额外优势 | RQ1a Go；RQ1b Go |
| A>B，但 A、B 对 C 都无稳定优势 | 可能只是格式或 lexical prior 效应，不支持 semantic bottleneck | 不构成核心 Go |

项目 continuation 不应要求 RQ1b 必须通过。更合理的核心 gate 是：

\[
\boxed{RQ1a\ Go\quad \land\quad RQ2\ Go}
\]

## 2.5 统计与 robustness 控制

正式实验前应冻结：

1. A vs C 与 B vs C 的 semantic-model contrasts；
2. A vs B 的 encoding contrast；
3. 多重比较或层级检验规则；
4. field-renaming / label-permutation robustness test。

field-renaming 不应继续仅列为 Remaining Open Decision，而应成为正式控制。至少包括：

- 将 `GOAL/REQUIRE/...` 替换为无语义标签；
- 将 isomorphic JSON role 同样替换为无语义标签；
- 保持结构不变，仅随机化字段名；
- 测量优势是否来自结构本身，还是模型预训练中对英语标签的 lexical prior。

---

# 3. Blocking Revision B：冻结 compiler 输入、模型输出与 deterministic elaborator

## 3.1 当前问题

当前文档把 learned task 写成：

```text
Source Envelope + Natural Language
→ Canonical Contract/Knowledge
```

但 target 中包含：

- `schema_domain`；
- `context_admissible_values`；
- active Contract membership；
- world-valid typed terms；
- delegation validity；
- HARD_UNSAT 与 NO_AUTHORIZED_ACTION 的后续判断基础。

其中部分信息不是单凭自然语言可以恢复的，而是由 frozen dialect、visible world context 和 deterministic rules 推导的。

如果 compiler 只看 SourceEnvelope，就无法可靠知道：

- 当前 dialect 中有哪些 enum value；
- 哪些 entity ID 存在；
- 哪些 value 因 world state 或其他 hard constraints 被排除；
- 某个 proposition 是否 type-valid；
- 某个 delegation 是否覆盖当前 clause。

反过来，如果 compiler 能看完整 candidate actions 或 gold outcome，它又可能通过下游答案反推语义，污染 NL→semantics 的独立性。

## 3.2 推荐的三段式架构

应把系统明确拆成：

```text
Learned semantic front-end
→ Deterministic elaborator
→ Common semantic state / runtime
```

### 3.2.1 CompilerInput

建议冻结为：

```yaml
CompilerInput:
  source_envelope:
    events: [...]
  dialect_manifest:
    sorts: [...]
    predicate_signatures: [...]
    enum_domains: [...]
  visible_world_context:
    observable_state: [...]
    entity_symbol_table: [...]
```

必须明确：

- 哪些 world facts 对模型可见；
- 哪些只对 runtime 可见；
- candidate action set 和 action effects 是否可见。

推荐 Phase 0 中 **candidate action set 不作为 compiler 输入**。它只在 downstream runtime 阶段提供，以避免 compiler 根据“哪个动作方便执行”反向选择语义。

### 3.2.2 Learned compiler output

模型只输出真正需要从语言中恢复的 surface semantic content，例如：

```yaml
SurfaceSemanticState:
  normative_candidates:
    - modality
      predicate
      args
      claimed_authority_source
      proposition_support
  knowledge_assertions:
    - predicate
      args
      epistemic_basis
      commitment
      proposition_support
  open_slot_mentions:
    - id
      type
      owner
      text_mentioned_alternatives
```

不建议让模型重复输出可由系统机械确定的完整字段，例如：

- `schema_domain`；
- `context_admissible_values`；
- active Contract；
- normalized authority result；
- conflict witness；
- valid action set。

### 3.2.3 Deterministic elaborator

由 elaborator 计算：

```text
schema_domain
context_admissible_values
joint completion Ω
active_contract
authority/delegation validity
HARD_UNSAT witness
NO_AUTHORIZED_ACTION witness
canonical common semantic projection
```

形式上：

\[
\widehat S_{surface}=Compiler(X)
\]

\[
\widehat S_{common}=Elaborate(\widehat S_{surface},D,W_{visible})
\]

该分层可以：

- 避免模型输出冗余、可机械推导字段；
- 减少 schema 学习难度；
- 明确区分语言理解错误与类型/推理错误；
- 防止不可观察 gold 被强迫作为 supervised target。

## 3.3 必须新增的评价分解

至少分别报告：

1. surface semantic recovery error；
2. elaboration/type failure；
3. common semantic projection error；
4. downstream policy/action error。

否则 compiler 错误和 elaborator/runtime 错误仍会被混在一起。

---

# 4. Blocking Revision C：所有行为结果必须由 Gold semantics 判定

## 4.1 当前问题

当前文档定义：执行动作违反 active hard clause 时，hard violation 记为 1。但必须明确这里用于评价的 active Contract 不能是 predicted active Contract。

若 evaluator 使用 predicted semantics，则模型漏掉一条 constraint 后，runtime 选择的动作在它自己的错误 Contract 下仍可能“合法”，从而被错误记为无违规。

## 4.2 必须冻结的评价链路

行为生成使用 predicted semantics：

\[
\hat a_R=Runtime(\widehat{\mathcal S}_R,W,A)
\]

行为评价必须使用 gold semantics：

\[
Violation(\hat a_R,\mathcal S_{gold},W)
\]

同理，以下判断都必须由 gold oracle 决定：

- 是否必须 ASK；
- ASK 的 slot 集是否充分；
- 是否应 REJECT；
- HARD_UNSAT 是否真实成立；
- NO_AUTHORIZED_ACTION 是否真实成立；
- action 是否满足 goal 和 hard clauses；
- action effects 是否获得授权；
- executor slot resolution 是否保留全部用户选择权。

文档应加入一句明确规则：

> Predicted representation 只用于产生系统决策；所有安全性、完成度、澄清必要性、拒绝正确性和 witness 指标均以 Gold common semantic state 为评价 oracle。

## 4.3 按 scenario type 分层报告

不应把所有 scenario 混在同一个 completion denominator 中。建议至少分为：

### Gold-directly-executable scenarios

报告：

- safe valid completion；
- unsafe execute rate；
- execution coverage；
- unnecessary ASK；
- unnecessary REJECT。

### Gold-clarification-required scenarios

报告：

- correct ASK rate；
- query sufficiency；
- queried-slot precision/recall；
- unsafe execute instead of ASK；
- premature REJECT。

### Gold-HARD_UNSAT scenarios

报告：

- correct REJECT；
- HARD_UNSAT classification；
- witness validity/minimality。

### Gold-NO_AUTHORIZED_ACTION scenarios

报告：

- correct REJECT；
- authorization diagnosis；
- witness coverage；
- 与 HARD_UNSAT 的混淆率。

### 全部 scenarios

报告：

- overall policy decision accuracy；
- hard-clause violation；
- authorization violation；
- goal non-achievement；
- system failure；
- cost。

建议把当前 composite `hard-contract violation` 拆分为至少三个可解释指标：

```text
normative-clause violation
authorization-policy violation
goal non-achievement
```

可以继续保留一个预注册 composite primary outcome，但必须同步报告上述分量，避免 default-deny meta-policy 被隐藏在一个数字中。

---

# 5. Blocking Revision D：定义 `ASK(slot_ids)` 的正确集合

## 5.1 当前问题

当前文档已经定义什么时候必须 ASK，但没有定义多个 USER-owned slot 存在时，runtime 应询问：

- 所有 unresolved slots；
- 所有 decision-relevant slots；
- 任意一个足够消除风险的 slot；
- 最小问题集合；
- 最小成本问题集合。

如果询问 `u1` 或 `u2` 都能独立使后续动作安全，则不能强迫模型匹配唯一 exact slot list。

## 5.2 推荐的正式定义

设 USER-owned unresolved slots 为 \(U_U\)。对任意候选询问集合 \(Q\subseteq U_U\)，若对 \(Q\) 的每一个 admissible answer，剩余未询问 completion 上都存在一个共同安全动作，或可机械确定应 REJECT，则称 \(Q\) 为 sufficient query set。

可写为：

\[
Q\text{ sufficient}
\iff
\forall q\in Answers(Q),
\left[
\exists a\ \forall \omega\in \Omega(q),\ a\in A_{valid}(C[\omega],W)
\right]
\lor
Rejectable(\Omega(q))
\]

定义 clarification cost：

\[
cost(Q)=\sum_{u\in Q}c(u)
\]

Phase 0 可先设 \(c(u)=1\)，于是 gold 接受所有 minimum-cardinality sufficient query sets。

评价时不要求单一 exact list，而是接受：

```text
Q_pred ∈ GoldMinimumSufficientQuerySets
```

并分别报告：

- query sufficiency；
- excess queried slots；
- omitted necessary slots；
- clarification cost regret。

## 5.3 简化备选

若不希望 Phase 0 引入最小询问集优化，可以使用更简单但必须机械定义的规则：

> 询问全部 decision-relevant USER slots。

此时必须给出 `decision_relevant(u)` 的形式定义，并允许多个等价顺序，不以 JSON 数组字节完全一致作为语义正确性。

Codex 必须在上述两种方案中选择一种并冻结；不能继续只定义“是否 ASK”而不定义“ASK 什么”。

---

# 6. Blocking Revision E：为 delegation 增加 scope，或在 Phase 0 删除 delegated clause

## 6.1 当前问题

当前 authority：

```text
USER | EXPLICITLY_DELEGATED | NONE
```

只要求 `EXPLICITLY_DELEGATED` 能追溯到一个用户授权 span。但存在授权 span不等于任意 assistant clause 都在授权范围内。

例如：

```text
USER: You may choose the error handling policy.
```

这只授权 resolver 选择 `ErrorPolicy`，不能授权 assistant 新增：

```text
ALLOW change(public_api)
```

因此，当前 `authority_trace` 只能证明存在一条授权链，不能证明 candidate clause 位于 delegation scope 中。

## 6.2 推荐方案 A：Phase 0 简化 authority

这是本轮最推荐的方案。

Phase 0 active normative clause 只接受：

```text
authority = USER
```

用户授予 executor 的选择权统一通过：

```text
OpenSlot.owner = EXECUTOR
```

表达。

Phase 0 暂不允许 assistant 或 executor 创建新的 delegated ContractClause。这样可以显著减少 authority 实验中的歧义，同时仍保留：

- USER requirement；
- assistant hypothesis；
- executor-owned resolution；
- unauthorized normative-looking proposition。

`EXPLICITLY_DELEGATED` 可在后续 Phase 1 引入。

## 6.3 备选方案 B：显式 DelegationGrant

若 Codex坚持在 Phase 0 保留 delegated normative clause，必须增加：

```yaml
DelegationGrant:
  id: d1
  delegator: USER
  delegatee: ASSISTANT | EXECUTOR
  scope:
    slot_ids: [u1]
    modalities: [ALLOW]
    predicate_signatures: [world.error_policy]
    managed_effects: [effect_private_helper]
  provenance:
    source_event_id: message_001
    span_id: span_003
```

Authority gate 至少验证：

1. grant 可追溯到 USER span；
2. delegatee 匹配；
3. candidate clause modality 在 scope 中；
4. predicate/effect/slot 在 scope 中；
5. grant 未被撤销或超出当前 scenario scope。

仅有 `authority_trace` 而无 scope 不能进入正式 confirmatory experiment。

---

# 7. Strong Revision F：将 RQ3 拆成“覆盖贡献”与“方法贡献”

## 7.1 当前问题

当前比较：

```text
mutation-trained
vs
paraphrase-only-trained
```

若 paraphrase-only 数据只包含完整、无冲突 Contract，而 mutation-trained 数据包含 `OPEN`、HARD_UNSAT、unsupported inference 和 provenance counterfactual，则后者获胜主要说明：

> 训练中见过这些 target classes，比完全没见过更好。

这并不能证明：

> programmatic semantic mutation + certificate 比其他构造困难样本的方法更好。

## 7.2 建议拆成两个问题

### RQ3a：Semantic coverage contribution

比较：

```text
complete-contract paraphrase-only
vs
mutation-enriched training
```

它回答加入 omission、ambiguity、conflict、authority 和 provenance-sensitive 样本是否必要。

### RQ3b：Formal mutation method contribution

比较 target distribution 匹配的困难样本生成方法：

```text
A. teacher directly prompted to generate incomplete/ambiguous/conflicting examples
B. programmatic semantic mutation + certificate + faithful verbalization
```

可选增加：

```text
C. human/template-authored matched semantic strata
```

至少必须匹配：

- base scenario；
- semantic target family；
- family proportion；
- training examples；
- token budget；
- teacher/verbalizer；
- language style；
- optimizer 与 seed policy。

只有 RQ3b 通过，才可声称 certified programmatic mutation 本身有独立增量价值。

如果资源有限，可以只完成 RQ3a，但结论必须写成：

> mutation-enriched semantic coverage 有益。

不得写成：

> programmatic semantic mutation 优于其他困难数据生成方法。

RQ3a 或 RQ3b No-Go 都不应自动否定 Contract IR 的 representation value。

---

# 8. Strong Revision G：分离 representation/runtime Go 与 LM-interface Go

## 8.1 当前问题

当前 Level 4 要求 task-directed corrupted IR 按预注册方向改变 executor 行为。若这里主要指 frozen LM executor，则可能发生：

- common semantics 与 deterministic runtime 正确；
- predicted Contract IR 确实降低 deterministic policy error；
- 但某个 frozen LM executor 没有可靠读取 modality、authority 或 OPEN 字段。

这说明的是 LM harness/interface 失败，不一定说明 Contract representation 失败。

## 8.2 必须拆分的裁决

建议单独报告：

### RQ1a / Core semantic runtime

```text
Predicted representation
→ common semantic projection
→ deterministic runtime
```

它检验 semantic representation 和 compiler 是否足以驱动可靠决策。

### RQ1c / LM executor interface

```text
Predicted representation
→ frozen LM executor
```

它检验当前格式与 harness 是否被实际 LM 正确消费。

Phase 0 核心 continuation gate 建议为：

\[
RQ1a\ Go\ \land\ RQ2\ Go
\]

LM executor interface 失败时，应报告：

```text
Representation/runtime: Go
LM interface: No-Go
```

随后修改 adapter、prompt 或 harness，而不是直接否定 semantic model。

若项目的工程目标要求当前 frozen LM 必须直接消费 IR，则可以把 LM-interface 作为单独工程 gate，但科学结论必须准确归因。

## 8.3 Corrupted representation 诊断

对 deterministic runtime，task-directed corruption 应当机械改变：

- common projection；
- valid action set；
- ASK/EXECUTE/REJECT oracle。

对 frozen LM executor，corruption 的作用是检查模型是否真正读取该字段。

两类 corruption test 不应混用同一个 Go/No-Go 解释。

---

# 9. 其他应在正式数据前冻结的细节

## 9.1 Isomorphic JSON 必须是严格 discriminated union

当前 generic schema 中：

```text
authority?
epistemic_basis?
commitment?
```

都是 optional。若它被定义为 semantic-isomorphic control，则必须为不同 role 冻结 conditional required/prohibited fields，避免一臂 schema 更宽松、另一臂更严格。

例如：

- normative role：必须有 authority，不允许 epistemic fields；
- factual role：必须有 epistemic fields，不允许 authority；
- unknown：必须有 type、owner 与 mention support。

如果保留 optional 模糊字段，则该 arm 应被定义为 deliberately weaker ablation，而不能声称与 Contract IR 语义同构。

## 9.2 Provenance Gold 应允许多证据支持

同一 proposition 可能：

- 由多个 span 联合表达；
- 在两个 message 中重复；
- 通过 quote 与原 user span 同时获得支持；
- 需要不连续 span。

Gold 建议使用：

```yaml
proposition_support:
  acceptable_support_sets:
    - [message_001:span_002]
    - [message_003:span_001, message_001:span_002]
```

评价应接受任一语义充分的 support set，而不是只接受一个 exact span ID。

Authority trace 与 proposition support 应分开评价：

- proposition support：哪段文本表达了命题；
- authority support：哪段用户文本赋予它规范效力或委托范围。

## 9.3 Task-directed corruption 必须保持 schema-valid

每次 corruption 必须：

1. 只改变一个预注册语义维度；
2. 保持格式合法、类型合法；
3. 保持非目标字段不变；
4. 由 deterministic oracle 证明预期 valid-action set 或 policy decision 改变；
5. 不使用随机破坏 JSON、删除必填字段等低层异常替代语义 corruption。

## 9.4 GOAL 与 REQUIRE 的关系必须在 0A 结束前冻结

当前文档已经提出：若两者不可区分，应合并或降级。需要将这一点升级为 0A blocking decision，并给出：

- scope semantics；
- counterexample；
- property tests；
- canonical mapping。

不得在训练数据生成后再决定二者是否等价。

## 9.5 `context_admissible_values` 不应成为不可观察监督标签

若采用第 3 节的 elaborator 分层，compiler target 只标注：

- type；
- owner；
- text-mentioned alternatives；
- proposition links。

`context_admissible_values` 由 elaborator 机械计算，并单独测试 elaborator 正确性。这样可避免 synthetic generator 内部状态被当作自然语言可恢复的 gold。

---

# 10. 建议重写的 Go / No-Go 结构

建议将当前四级结构改成下列层次。

## Gate 0：Formal validity

必须全部通过：

- schema/type/canonicalization properties；
- common projection losslessness；
- Oracle A/B runtime parity；
- OPEN joint completion oracle；
- ASK query-set oracle；
- HARD_UNSAT 与 NO_AUTHORIZED_ACTION witness；
- authority/delegation gate；
- gold behavior evaluator 使用 Gold common semantics。

失败则停止 learned experiment。

## Gate 1：Semantic-model value，RQ1a

Full Contract IR 与 SemanticIsomorphicJSON 均相对 ContentMatchedUntypedJSON 在 human confirmatory set 上：

- 降低 gold-evaluated unsafe/hard violation；
- common projection error 更低；
- completion、coverage 与 unnecessary ASK 满足 guardrail；
- 方向不依赖单一 teacher/template；
- field-renaming 后仍保持核心方向。

若两种 full-semantic encoding 都无优势，则 RQ1a No-Go/Inconclusive。

## Gate 2：Encoding value，RQ1b

比较：

```text
Full Contract IR
vs
SemanticIsomorphicJSON
```

若 Contract IR 优于同构编码，则支持当前 serialization/factorization 的独立价值。

若二者相近，但 Gate 1 通过，则：

```text
RQ1a Go
RQ1b No-Go/Inconclusive
```

项目仍可继续。

## Gate 3：Compilation stability，RQ2

learned compiler 在 independent human set、unseen template 和 unseen verbalizer 上满足预注册的：

- surface semantic recovery；
- common projection error；
- OPEN owner/type；
- authority/provenance；
- minimal-pair sensitivity；
- same-text/different-role counterfactual；
- system failure ceiling。

RQ2 必须基于 learned compiler，prompted compiler 只能用于 pilot。

## Gate 4：Data method，RQ3a/RQ3b

分别裁决：

- mutation-enriched semantic coverage 是否有益；
- certified programmatic mutation 是否优于 target-matched teacher-direct generation。

不得将两个结论合并。

## Gate 5：LM interface，RQ1c

frozen LM executor 是否真正利用：

- modality；
- OPEN owner；
- authority；
- provenance；
- conflict/witness。

失败时报告 interface/harness No-Go，不自动回溯否定 RQ1a。

## 项目 continuation

推荐：

\[
\boxed{
Phase\ 1\ continuation
\iff
RQ1a\ Go\ \land\ RQ2\ Go
}
\]

RQ1b、RQ3 或 RQ1c 的失败分别表示：

- 当前 serialization 无独立优势；
- 当前数据方法无独立优势；
- 当前 LM harness 未能消费表示；

它们不应在没有进一步归因的情况下被写成“Contract semantic model 失败”。

---

# 11. 允许支持的分层结论

修订后的文档应根据实际结果使用不同强度的结论。

## 11.1 仅 RQ1a 通过

允许支持：

> 在有限 dialect 中，显式的 Contract common semantic model——包括规范模态、typed unknown、authority、provenance 和 Contract/Knowledge 类型边界——相对普通结构化 decomposition 改善了语义恢复和安全执行；但当前 Contract IR serialization 尚未证明优于其他语义同构编码。

## 11.2 RQ1a 与 RQ1b 均通过

允许进一步支持：

> 除共同语义模型本身外，当前 Contract IR 的 canonical factorization/serialization 相对一个信息完全匹配的同构编码也具有增量价值。

## 11.3 RQ3a 通过但 RQ3b 未通过或未实施

只能支持：

> 覆盖 omission、ambiguity、conflict 和 provenance counterfactual 的训练数据优于只做完整语义 paraphrase 的数据。

不能支持：

> certified programmatic mutation 优于其他困难样本生成方法。

## 11.4 Deterministic runtime 通过但 LM executor 失败

应表述为：

> semantic representation 与 deterministic decision layer 有效，但当前 frozen LM executor/harness 尚不能可靠消费该表示。

不得表述为 Contract representation 总体 No-Go。

---

# 12. 建议 Codex 修改的具体章节

| 当前章节 | 必须修改内容 |
|---|---|
| 第 1 节 文档定位 | 明确当前文件是 Experimental Protocol；保留 Phase 0 范围 |
| 第 2 节 RQ | 将 RQ1 拆为 RQ1a/RQ1b，可增加 RQ1c；将 RQ3 拆为 RQ3a/RQ3b |
| 第 3 节 Common projection | 将当前 generic JSON 重命名为 SemanticIsomorphicJSON；新增 ContentMatchedUntypedJSON |
| 第 4 节 Schema | 冻结 learned surface output 与 deterministic elaborator 的职责；处理 delegation scope |
| 第 5 节 OPEN | 新增 `ASK(slot_ids)` sufficient/minimum query-set semantics |
| 第 7 节 Source Envelope | 区分 proposition support 与 authority support；允许多 valid support sets |
| 第 8 节 Data | 增加 target-distribution-matched RQ3b control |
| 第 9 节 Baseline | 主条件扩展为 A/B/C；Raw NL 为诊断；加入 field renaming |
| 第 10 节 Metrics | 明确所有行为结果由 Gold common semantics 判定；按 scenario type 分层 |
| 第 11 节 Stages | 在 0A/0B 中加入 compiler/elaborator boundary、ASK oracle、delegation scope |
| 第 12 节 Go/No-Go | 改为 semantic-model、encoding、compilation、data method、LM interface 分层 gate |
| 第 13 节 Conclusions | 增加不同实验组合对应的分层结论，不再只有“Contract IR 胜过 generic JSON”一种结论 |

---

# 13. Codex 应提交的修订产物

Codex 不应只返回一份改写后的主文档。建议同时提交：

## 13.1 修订后的主协议

建议文件名：

```text
IR_Design_Memo_v0_Phase0_Experimental_Protocol.md
```

## 13.2 Change Log

逐项说明：

```yaml
- recommendation_id: A1
  disposition: ACCEPTED | PARTIALLY_ACCEPTED | REJECTED
  rationale: ...
  changed_sections: [2, 9, 12]
  residual_risk: ...
```

Codex 可以不接受某条建议，但必须：

1. 说明不接受的形式理由；
2. 给出替代定义；
3. 证明替代定义仍能机械评价；
4. 说明对结论边界的影响。

## 13.3 冻结接口附录

至少包含：

- `CompilerInput`；
- `SurfaceSemanticState`；
- `ElaboratedCommonSemanticState`；
- Contract IR schema；
- SemanticIsomorphicJSON schema；
- ContentMatchedUntypedJSON schema；
- projection mapping；
- Gold evaluator interface；
- ASK query-set oracle；
- authority/delegation gate。

## 13.4 Open Decisions

只保留真正尚需 pilot 决定的参数，例如：

- finite dialect cardinality；
- base scenario 数量；
- checkpoint；
- effect size 与 margins；
- human annotator 数量。

以下内容不应继续列为开放决定：

- predicted vs gold behavior evaluation；
- compiler 与 elaborator 边界；
- isomorphic baseline 的定位；
- ASK 正确性定义；
- delegation scope；
- RQ1a 与 RQ1b 的区分。

---

# 14. 修订完成验收清单

在 Codex 返回新版本后，应逐项检查：

## 研究问题与 baseline

- [ ] RQ1a 与 RQ1b 已分开；
- [ ] 当前 schema-matched generic JSON 已明确标为 semantic-isomorphic control；
- [ ] 已增加 content-matched untyped JSON；
- [ ] 项目 continuation 不再强制要求 Contract IR 击败同构编码；
- [ ] field-renaming / label-permutation 已成为正式控制。

## Compiler boundary

- [ ] `CompilerInput` 已完整冻结；
- [ ] visible world information 已明确；
- [ ] candidate actions 是否可见已明确；
- [ ] model output 与 deterministic elaborator 输出已分离；
- [ ] `context_admissible_values` 不再作为不可观察的纯 NL target。

## Gold evaluation

- [ ] runtime 使用 predicted semantics；
- [ ] evaluator 使用 Gold common semantics；
- [ ] ASK、REJECT、violation、authorization、completion 均以 gold 判定；
- [ ] metrics 已按 executable / ASK / HARD_UNSAT / NO_AUTHORIZED_ACTION 分层；
- [ ] composite violation 的分量已单独报告。

## OPEN / ASK

- [ ] 多 slot `ASK(slot_ids)` 有机械定义；
- [ ] 接受多个等价 sufficient query sets，或已冻结 decision-relevant-all 规则；
- [ ] clarification cost 或 excess-slot 指标已定义。

## Authority

- [ ] Phase 0 已删除 delegated normative clause，或增加显式 scoped DelegationGrant；
- [ ] proposition support 与 authority support 已分离；
- [ ] 仅凭 authority trace 不能越权创建 clause。

## RQ3

- [ ] RQ3a 与 RQ3b 已分开；
- [ ] RQ3b 有 target-distribution-matched control；
- [ ] 未实施 RQ3b 时，结论边界已收窄。

## Runtime 与 LM interface

- [ ] deterministic runtime Go 与 frozen LM executor Go 分开；
- [ ] corrupted IR 对两层实验的解释已分开；
- [ ] LM executor 失败不会自动判定 semantic model No-Go。

---

# 15. 最终修改建议

当前 Phase 0 文档已经具备高质量形式实验协议的主体，不需要全盘重写。本轮修改的核心不是增加更多功能，而是将实验所检验的命题进一步拆开：

\[
\boxed{
\text{Contract common semantics 是否有价值？}
}
\]

\[
\boxed{
\text{当前 Contract IR encoding 是否具有额外价值？}
}
\]

\[
\boxed{
\text{NL 是否能稳定编译到该语义？}
}
\]

\[
\boxed{
\text{programmatic mutation 是否具有独立数据方法价值？}
}
\]

\[
\boxed{
\text{frozen LM executor 是否真正消费了该语义接口？}
}
\]

只有将这些问题分开，实验失败时才能准确定位到：

- semantic model；
- serialization；
- compiler；
- data generation；
- deterministic runtime；
- LM harness/interface。

建议允许 Codex 在形式细节上提出替代方案，但任何替代方案必须满足三个最低条件：

1. 输入与 gold 均可观察或可机械推导；
2. evaluation oracle 唯一或显式允许等价答案集合；
3. 失败能够归因到明确层次，而不是由多个组件共同决定。

完成本轮修订后，可以开始冻结 0A–0B 的实现接口，并在 property tests、exhaustive oracle 和 human Gold guideline 通过后进入 0C–0D。正式 confirmatory baseline、learned compiler target 和 continuation gate 应以修订后的协议为准。
