# Contract IR v0 Phase 0 有限语义实验协议

## 1. 文档定位与结论边界

本文将 `IR_Design_Memo_v0.md` 原称的“第一阶段”重新编号为 **Phase 0**，并压缩为一个有限、可穷举、可证伪的 semantic-kernel pilot。本文已经是可用于冻结实现与预注册的实验协议，不再只是评估意见。当前沿用历史文件名；待仓库建立初始 clean commit 后，再用 Git rename 改为 `IR_Design_Memo_v0_Phase0_Experimental_Protocol.md`，避免在尚无提交历史时制造两个权威副本。

Phase 0 分开回答五个问题：显式、直接监督的 typed semantic bottleneck/interface 是否比预算匹配的 untyped two-stage baseline 有价值、当前 Contract IR encoding 是否额外有价值、自然语言能否稳定编译到该语义、困难数据覆盖及其生成方法是否有价值、frozen LM 是否真正消费该接口。任何一项的成功或失败都不得替代另一项的结论。

Phase 0 保留两个静态对象：

- Normative Contract \(\mathcal C\)：描述被授权的目标、约束、保持项、禁止项和允许项；
- Knowledge State \(K\)：描述显式陈述、观察、推导和假设，但不修改 Contract。

Phase 0 不实现动态 Knowledge revision、Execution Plan、C/K/P lowering、repository grounding、verification lifecycle、真实代码执行、Lean、SWE-bench、任意 patch generation、model-size scaling、RL 或复杂多 agent。真实代码的受控候选补丁桥接只作为本阶段通过后的未来边界，不属于本文实验或 Go 条件。

因此，即使实验通过，也只能说明目标表示在预定义有限 dialect 中具有增量价值，不能外推为通用 semantic compiler 或真实 coding agent 已经更可靠。

---

## 2. Phase 0 研究问题

### RQ1a：直接监督的 typed semantic bottleneck 增量价值

在 source information、总监督量、模型容量、解码约束、分析 token 和计算预算匹配时，直接监督并显式编码 normative modality、typed unknown、authority/support 与 C/K 类型边界的 semantic bottleneck，是否比 `extractive untyped content → learned semantic bridge` 的 two-stage pipeline 降低由 Gold semantics 判定的不安全执行，且不降低 common-semantic recovery？

RQ1a 的主对比是 `SemanticIsomorphicJSON`（B）与 `ContentMatchedUntypedJSON`（C）。C 必须经预算匹配的 learned semantic bridge 才能进入共同 deterministic runtime；因此 RQ1a 只允许支持“直接监督的 typed bottleneck 相对 extractive-untyped two-stage pipeline 有增量价值”，不声称 common semantic model 的存在本身或任一 semantic primitive 已获得纯因果识别。Full Contract IR（A）相对 C 只作支持性对比。

### RQ1b：encoding / factorization 的增量价值

当 A 与 B 承载完全相同的 common semantics、使用同等级 constrained decoding，并由各自 adapter 无损投影到同一共同语义时，当前 Contract IR serialization/factorization 是否比 semantic-isomorphic JSON 更易学习、更稳定或成本更低？A 与 B 相近不否定 RQ1a。

### RQ1c：LM interface 的可消费性

在 common semantics 相同的前提下，同一个 frozen LM executor 是否能可靠消费 A 或 B，并对 modality、OPEN owner、authority、provenance 与 conflict 作出预期响应？主分析使用 Oracle A/B 隔离接口效应；Predicted A/B 只作包含 compiler error 的次级端到端分析。

### RQ2：语义编译的稳定性

自然语言 source envelope 能否稳定编译为 canonical Contract/Knowledge 表示，并在 paraphrase、minimal pair、未见模板、未见 verbalizer 和独立人写数据上保持正确的 OPEN、authority 与 provenance？

### RQ3a：困难语义覆盖的增量价值

在 base scenario、样本量、模型和预算匹配时，覆盖 omission、ambiguity、HARD_UNSAT、unsupported inference 和 provenance counterfactual 的 mutation-enriched training，是否优于只覆盖完整语义的 paraphrase-only training？RQ3a 只能证明困难语义覆盖的价值。

### RQ3b：certified mutation 方法的增量价值

在 semantic target family、family proportion、base scenario、teacher/verbalizer、语言风格、样本量、token、optimizer、seed 与调参预算匹配时，`programmatic mutation + certificate + faithful verbalization` 是否优于 teacher-direct difficult-example generation？RQ3b 为资源允许时的独立实验；未实施或未通过时，不得声称 programmatic mutation 本身优于其他困难数据生成方法。

模型规模是否降低不是 Phase 0 研究问题；prompted compiler 可用于 pilot，但支持 RQ2、RQ3a 或 RQ3b 的最终结论必须包含 learned compiler。RQ1b、RQ1c 或 RQ3 的失败不自动否定 RQ1a。

---

## 3. Representation-neutral micro-world

### 3.1 中性环境

先定义与任何输出 schema 无关的有限环境：

\[
W=(S,A,T,O,E)
\]

其中：

- \(S\)：有限状态集合；
- \(A\)：候选动作集合；
- \(T:S\times A\rightarrow S\times E^*\)：确定性状态转移；
- \(O:S\rightarrow \mathcal O\)：可观察量；
- \(E\)：轨迹中的 effect event 集合。

world、动作和 effect 使用内部枚举 ID，不复用某个表示的字段名。有限 dialect 另行定义 sorts、enum values、predicate signatures、scope 和解释函数。每个 predicate 只能作用于 `INITIAL | FINAL | TRACE | EVENT` 中已冻结的 scope；Phase 0 不支持自由文本 operand、开放量词或 repository-dependent predicate。

### 3.2 Common semantic projection

A/B 先由各自 deterministic adapter 映射到同一个、只含语言可恢复字段的 post-adapter 类型：

\[
\alpha_A:
ContractSurfaceState\rightarrow CanonicalSurfaceSemanticState
\]

\[
\alpha_B:
SemanticIsomorphicSurfaceState\rightarrow CanonicalSurfaceSemanticState
\]

A/B 的 lossless property 指 arm surface 与 `CanonicalSurfaceSemanticState` 之间的 semantic round trip，不包含任何由 dialect 或 world 推导的字段。随后统一调用：

\[
Elaborate:
CanonicalSurfaceSemanticState
\times DialectManifest
\times W_{visible}
\times ReferencedSupportView
\rightarrow \mathcal S_{common}
\]

所有 satisfaction、OPEN、authority、conflict 和 action-validity 判断只读取 \(\mathcal S_{common}\)，不读取原始字段名、字段顺序或字节表示。评价依次区分：

1. syntax/schema validity；
2. common semantic projection recovery；
3. induced valid-action set 与行为。

SemanticIsomorphicJSON 必须能够表达与 Contract IR 相同的 clause、knowledge、unknown、support claim 和 authority claim，并相对 canonical surface 具有无损 adapter。若 Oracle A/B 映射到同一 canonical surface，则同一 elaborator/runtime 必须产生相同结果；这一 Oracle structured parity 是实现与公平性的 sanity check，不是要求 Contract IR 胜出的 Go 条件。

`ContentMatchedUntypedJSON`（C）不具有固定、无损的 common projection。为使 deterministic-runtime 对比可执行，C 使用一个预算匹配、在相同 split 上训练的 learned semantic bridge：

```text
ContentMatchedUntypedState
→ learned β_C bridge
→ CanonicalSurfaceSemanticState
→ deterministic elaborator
→ common semantic state
```

\(\beta_C\) 只能读取 `ContentMatchedUntypedState`、其中 support refs 对应的 `ReferencedSupportView`，以及对所有条件相同的 dialect/visible context；不得绕过 C 扫描未引用的 SourceEnvelope 内容，也不得读取 candidate actions、action effects、gold outcome 或 Gold common semantics。C 的 schema 与 channel restrictions 在第 9.2 节冻结。

C compiler 只接受 extractive-content supervision；bridge 只接受 canonical-surface supervision。两者分开训练，禁止 joint fine-tuning、跨模块 gradient、hidden state/logit side channel；bridge 只能接收通过 schema/smuggling audit 的离散 C artifact。bridge training 必须使用 training split 的 Oracle C 与 out-of-fold Predicted C 混合输入，混合比例、两阶段监督 token/step 分配及总参数/训练/推理预算在 pilot 后、confirmatory data 前冻结。A/B 单阶段与 C 两阶段按完整流水线匹配总监督 token、推理 token、可训练参数预算、调参次数与 compute。另行报告 content extraction error、bridge error 与 elaboration failure，避免将 C 的接口缺失伪装成 runtime failure。

### 3.3 最小动作协议

runtime 只能返回以下封闭 discriminated union：

```yaml
Decision:
  oneOf:
    - kind: EXECUTE
      action_id: action_01
      executor_resolutions: [ResolutionTrace, ...]
    - kind: ASK
      semantic_slot_links: [SlotSemanticLink, ...]  # nonempty
    - kind: REJECT
      reason: HARD_UNSAT | NO_AUTHORIZED_ACTION
      witness: HardUnsatWitness | NoAuthorizedActionWitness
```

`ClauseSemanticLink` 冻结为 elaborated canonical `(modality, predicate, typed_args, proposition_support)`；`SlotSemanticLink` 冻结为 `(type, owner=USER|EXECUTOR, referenced_clause_link, argument_position, proposition_support)`。`ASK.semantic_slot_links` 中每个 link 必须 `owner=USER`；`ResolutionTrace` 冻结为 `(slot_semantic_link(owner=EXECUTOR), selected_value, resolver=EXECUTOR)`。REJECT 的 reason 与 witness variant 必须匹配，EXECUTE 的每个 executor resolution 必须在 action 前记录且覆盖实际选择。所有 decision links 使用 canonical semantic links，不输出 arm-local clause/slot IDs。

`ASK([])` 非法；不需要询问时必须进入 EXECUTE 或 REJECT。syntax/schema/type/linking failure 在 runtime 前记为 `SYSTEM_FAILURE(ELABORATION_ERROR)`，不是第三种 REJECT reason。候选动作、动作 effect 和转移均由 \(W\) 冻结。`ASK` 只用于尚需用户决定且会影响安全动作，或会影响 ADT 强制要求的正确 REJECT reason/witness 的 slot；`REJECT` 不能用作提高条件可靠率的捷径。

---

## 4. 编译边界与 Phase 0 静态语义 schema

### 4.1 CompilerInput 与不可见信息

learned front-end 的输入冻结为：

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

support refs 由一个只读、确定性的 resolver 转为：

```yaml
ReferencedSupportView:
  referenced_spans:
    - ref: message_001:span_004
      event_role: USER | ASSISTANT | TOOL
      text: ...
      quoted_from?: message_000:span_002
```

`ReferencedSupportView` 只包含当前 predicted surface/content 实际引用且在 SourceEnvelope 中存在的 spans、role 与 quote metadata；不得提供未引用文本。不存在的 event/span ref 是 elaboration failure。引用了有效但非 USER 的 span 在 schema 上合法，authority gate 将其归一化为 `NONE`。

模型能看到 source envelope、frozen dialect、可观察 state 与 entity symbol table；不能看到 candidate action set、action effects、隐藏 world state、gold outcome、Gold common semantics 或 Gold witnesses。candidate actions 与 effects 只在 downstream runtime 提供，防止 compiler 根据“哪个动作容易执行”反推语义。

各表示先生成 arm-specific surface，而不是强迫 A/B/C 共用一个 `SurfaceSemanticState`：

```text
A: ContractSurfaceState ───────────────┐
B: SemanticIsomorphicSurfaceState ─────┼→ CanonicalSurfaceSemanticState
C: ContentMatchedUntypedState ─────────┘
```

A/B 的 surface 都表达完整语义，但字段组织不同；C 只保留 source 中可观察的内容整理。这样 A/B 的 encoding intervention 不会被一个预先统一的 Contract-shaped surface 抹除。

### 4.2 Learned surface output

A 的最小 learned output 为：

```yaml
ContractSurfaceState:
  normative_candidates:
    - id: c1
      modality: GOAL | REQUIRE | PRESERVE | FORBID | ALLOW
      predicate: world.predicate_name
      args: [surface_term, ...]
      proposition_support: [source_ref, ...]
      claimed_authority_support: [source_ref, ...]  # 可为空
  knowledge_assertions:
    - id: k1
      predicate: world.root_cause
      args: [surface_term, ...]
      epistemic_basis: EXPLICIT_STATEMENT | OBSERVATION | DERIVATION | ASSUMPTION
      commitment: ASSERTED | TENTATIVE | DENIED
      proposition_support: [source_ref, ...]
  open_slot_mentions:
    - id: u1
      type: ErrorPolicy
      owner: USER | EXECUTOR
      text_mentioned_alternatives: [surface_term, ...]
      proposition_links: [c1]
      proposition_support: [source_ref, ...]
```

模型不得重复输出可机械推导的 `schema_domain`、`context_admissible_values`、normalized authority、`active_contract`、joint completion、valid action set、conflict classification 或 witness。B 使用第 9.1 节的 `SemanticIsomorphicSurfaceState`；C 使用第 9.2 节的 `ContentMatchedUntypedState`。

`CanonicalSurfaceSemanticState` 冻结为与上面三个 arrays 相同的 language-recoverable semantic fields：canonical normative candidates、knowledge assertions 与 open-slot mentions。它仍保留 claimed support refs，不包含 authority result、world-derived domains、joint completion、action、conflict 或 witness。\(\alpha_A\) 与 \(\alpha_B\) 是 deterministic、lossless adapter；\(\beta_C\) 是 learned bridge。三者的 codomain 必须完全相同。

### 4.3 Deterministic elaborator 与 runtime 边界

系统明确分为：

```text
arm-specific learned front-end
→ deterministic α_A/α_B adapter or learned β_C bridge
→ CanonicalSurfaceSemanticState
→ deterministic elaborator
→ deterministic runtime
```

elaborator 的签名是第 3.2 节冻结的 `Elaborate(CanonicalSurfaceSemanticState, DialectManifest, W_visible, ReferencedSupportView)`，负责：

- symbol linking、type checking 与 canonicalization；
- 从 dialect 填充 `schema_domain`；
- 只从 frozen enum domain、visible observable state 与不依赖 transition/action/effect 的静态 active hard clauses 计算 `context_admissible_values`；
- 验证 proposition support 和 USER authority support；
- 派生 `authority = USER | NONE` 与 `active_contract`；
- 生成 canonical `ElaboratedCommonSemanticState`。

runtime 才能读取完整 \(W\)、candidate actions 与 effects，负责：

- joint completion \(\Omega\) 与 ASK query-set oracle；
- safe/valid/authorized action set；
- `EXECUTE | ASK | REJECT`；
- HARD_UNSAT 与 NO_AUTHORIZED_ACTION classification/witness；
- executor-owned resolution coverage 与 trace。

任何需要 transition、candidate action/effect 或 hidden world 的 feasibility filtering 留在 runtime，不能反向修改 `context_admissible_values`。HARD_UNSAT、NO_AUTHORIZED_ACTION、joint \(\Omega\) 或 action witness 不得由 elaborator 生成。分别报告 surface/content recovery error、bridge error（仅 C）、elaboration/type failure、common semantic projection error 与 downstream policy/action error。

### 4.4 Elaborated Normative Contract

Phase 0 的最小 clause 为：

```yaml
ContractClause:
  id: c1
  modality: GOAL | REQUIRE | PRESERVE | FORBID | ALLOW
  predicate: world.predicate_name
  args: [typed_term, ...]
  authority: USER | NONE
  proposition_support: [message_001:span_004]
  authority_support: [message_001:span_004]
```

elaborator 输出中的顶层容器为：

```yaml
ElaboratedCommonSemanticState:
  normative_candidates: [ContractClause, ...]
  knowledge_assertions: [KnowledgeAssertion, ...]
  open_slots: [OpenSlot, ...]
```

`active_contract` 不由模型生成，而由 authority gate 从
`normative_candidates` 确定性派生。这样，`authority = NONE` 的
normative-looking proposition 有唯一归属，可以参与 authority 诊断，但不会进入
Contract denotation。

字段职责如下：

- `modality/predicate/args` 给出规范命题；
- `authority` 判断该命题是否有权进入 active Contract；
- `proposition_support` 指向表达命题的可观察 source spans；
- `authority_support` 只指向赋予规范效力的原始 USER spans。

`ContractClause` 不含 `epistemic_status`。Phase 0 所有 active normative clauses 都按 hard constraint 解释，不额外引入 strength 层级。`authority = NONE` 的 normative-looking proposition 只保留为 authority diagnostic，不进入 active Contract；active Contract 只接受经 envelope 验证、由原始 USER span 直接支持的 clause。

五种 modality 的有限语义为：

- `GOAL φ`：最终状态满足 \(\phi\)；
- `REQUIRE φ`：冻结 scope 上 \(\phi\) 必须成立；
- `PRESERVE o`：指定 observation 的初值与终值相同；
- `FORBID e`：轨迹不得包含 effect \(e\)；
- `ALLOW e`：在 default-deny 的 managed-effect universe 中授权 \(e\)，但不要求 \(e\) 发生。

0A 结束前必须用 scope semantics、区分性 counterexample、property tests 与 canonical mapping 冻结 `GOAL`/`REQUIRE` 关系。若无法给出可计算区分，两者必须在任何训练数据生成前合并，或将 `GOAL` 降为非逻辑分组字段。

### 4.5 Knowledge Assertions

Phase 0 的最小 knowledge object 为：

```yaml
KnowledgeAssertion:
  id: k1
  predicate: world.root_cause
  args: [component_03]
  epistemic_basis: EXPLICIT_STATEMENT | OBSERVATION | DERIVATION | ASSUMPTION
  commitment: ASSERTED | TENTATIVE | DENIED
  proposition_support: [message_002:span_001]
```

`epistemic_basis` 表示命题依据，`commitment` 表示 source 对命题的承诺强度或否定立场。Knowledge 不含恒定的 `normative_authority` 字段，也不会因 source role 是 USER 就自动变成 Contract。若一个 knowledge proposition 后来要修改 Contract，必须由新的、可观察的 USER source event 产生相应 ContractClause。

字段适用范围冻结如下：

| Object | Normative authority | Epistemic basis / commitment | Proposition support |
|---|---|---|---|
| Normative candidate | claimed-support 字段必须存在但可为空；gate 派生 USER/NONE | 不适用 | 必须有 |
| Active ContractClause | 从 candidate 派生 | 不适用 | 必须有 |
| KnowledgeAssertion | 不适用 | 必须有 | 必须有 |

`N/A` 表示该字段在对象类型上不存在，而不是使用一个恒定枚举值占位。

### 4.6 Authority 与 OPEN resolution 的边界

Phase 0 normalized normative authority 只有：

```text
USER | NONE
```

Phase 0 不允许 assistant 或 executor 创建 delegated ContractClause，也不以一条无 scope 的 trace 代表授权。assistant 的 quote 可以构成 proposition support，但 authority support 必须落在原始 USER span；assistant 自述、teacher generation、tool output 或 executor inference 均不能产生 normative authority。

authority gate 的机械规则为：

1. `claimed_authority_support` 字段必须存在但可为空；
2. 所有 refs 必须能在 `ReferencedSupportView` 解析，否则是 elaboration failure；
3. 只有同时属于该 candidate 的 `proposition_support`、role 为原始 USER、且不是 assistant/tool quote surrogate 的 ref 才是 valid authority support；
4. 至少有一个 valid authority support 时归一化为 `USER`，否则归一化为 `NONE`；引用有效但 role 错误不是 schema failure；
5. Gold evaluator 另行判断 predicted proposition/authority support 是否语义充分，deterministic gate 不用词面相似度猜测 support correctness。

用户授予 executor 的有限选择权只通过 `OpenSlot.owner = EXECUTOR` 表达。该权限只允许从 slot 的 `context_admissible_values` 中选值，不允许新增、删除或改写 ContractClause，也不构成第三种 normative authority。scoped `DelegationGrant` 与 `EXPLICITLY_DELEGATED` 延后到 Phase 1。

---

## 5. Typed OPEN 的 denotation 与行动语义

### 5.1 Slot schema 与三种候选范围

Phase 0 仅支持有限枚举 slot：

```yaml
OpenSlot:
  id: u1
  type: ErrorPolicy
  schema_domain: [RETURN_NONE, RAISE_VALUE_ERROR, RAISE_PARSE_ERROR]
  context_admissible_values: [RETURN_NONE, RAISE_VALUE_ERROR]
  text_mentioned_alternatives: [RAISE_VALUE_ERROR]
  owner: USER | EXECUTOR
  status: UNRESOLVED | RESOLVED
  resolved_value?: RAISE_VALUE_ERROR
```

三种集合不得混用：

- `schema_domain` 是 dialect 定义的完整类型域；
- `context_admissible_values` 是结合当前 world 与明确约束后仍合法的值；
- `text_mentioned_alternatives` 只记录文本实际列出的候选，可以为空，也不默认穷尽合法值。

必须满足：

\[
V_{ctx}(u)\subseteq D_{schema}(u),
\qquad
V_{text}(u)\subseteq D_{schema}(u)
\]

不要求 \(V_{text}(u)\subseteq V_{ctx}(u)\)：文本明确提到的候选可能被其他 hard constraint 或 world context 排除。需要“被提及且当前合法”的值时，显式使用 \(V_{text}(u)\cap V_{ctx}(u)\)。若文本候选不能 link 到 schema domain，则在 runtime 前计为 elaboration failure。

`context_admissible_values` 只能由冻结的 schema、可观察静态 world context 和不依赖 transition/action/effect 的输入 hard constraints 计算；不得依据隐藏 state、候选动作、动作 effects、期望 outcome 或 executor 偏好事后裁剪。full-world feasibility 只在 runtime 的 \(\Omega\) 与 action oracle 中计算。

### 5.2 多 slot completion

将未解析 slot 分为 USER-owned 集合 \(U_U\) 与 EXECUTOR-owned 集合 \(U_E\)。所有与类型、world 和跨 slot 约束一致的 joint completion 为：

\[
\Omega(\mathcal C,W)=
\left\{
\left(\omega_U,\omega_E\right)
\in
\prod_{u\in U_U}V_{ctx}(u)
\times
\prod_{u\in U_E}V_{ctx}(u)
\mid (\omega_U,\omega_E)\text{ 满足跨 slot 约束}
\right\}
\]

定义 USER assignment 的原始可行投影：

\[
P_U(\mathcal C,W)=\operatorname{proj}_{U_U}\Omega(\mathcal C,W)
\]

以及给定 executor assignment 的 USER fiber：

\[
F_U(\omega_E)=
\left\{
\omega_U:(\omega_U,\omega_E)\in\Omega(\mathcal C,W)
\right\}
\]

因此多个 slot 的安全判断必须覆盖 joint completion，不能逐 slot 贪心解析。表示 denotation 是所有 admissible joint completion denotation 的并集；可靠行动使用下面的量词条件。

### 5.3 USER-owned OPEN

对所有 USER-owned unresolved slots，一个 action 无需澄清即可执行，当且仅当它对所有 admissible completion 都有效且已授权：

\[
a\in A_{safe}(\mathcal C,W,\omega_E)
\iff
P_U(\mathcal C,W)\neq\varnothing
\quad\land\quad
\forall\omega_U\in P_U(\mathcal C,W),
\ a\in A_{valid}(\mathcal C[\omega_U,\omega_E],W)
\]

当不存在 EXECUTOR-owned slot 时，\(\omega_E\) 是唯一空 assignment。schema/type/linking 错误已在 runtime 前计为 elaboration failure；进入 runtime 后若 \(P_U(\mathcal C,W)=\varnothing\)，必须路由到 Gold/runtime 定义的 HARD_UNSAT，不得进入 action tie-break。若 \(P_U(\mathcal C,W)\neq\varnothing\) 且 \(A_{safe}\neq\varnothing\)，runtime 可以执行其中的确定性 tie-break 选择；若每个相关 USER completion 各自可能有动作、但安全交集为空，则必须 `ASK`。由此分别计算 necessary ASK recall、unnecessary ASK rate 和 unsafe execute rate。

### 5.4 EXECUTOR-owned OPEN

executor 可以联合选择所有自己拥有的 slot 值，但该选择不得缩小用户原本拥有的合法选择集合。一个 executor assignment 只有在以下 coverage 条件成立时才允许使用：

\[
F_U(\omega_E)=P_U(\mathcal C,W)\neq\varnothing
\]

在此基础上，无需 ASK 的执行条件是：

\[
\exists\omega_E\ \exists a\quad
F_U(\omega_E)=P_U(\mathcal C,W)\neq\varnothing
\quad\land\quad
\forall\omega_U\in P_U(\mathcal C,W),
a\in A_{valid}(\mathcal C[\omega_U,\omega_E],W)
\]

这避免 executor 通过先选自己的 slot，把部分 USER completion 排除掉，或利用空 fiber 获得 vacuous success。多个 EXECUTOR-owned slot 必须作为一个 joint assignment 选择，不能逐 slot 贪心解析。选定后必须在行动前输出 resolution trace：

```yaml
resolution:
  slot_semantic_link:
    type: ErrorPolicy
    owner: EXECUTOR
    referenced_clause_link:
      modality: REQUIRE
      predicate: world.error_policy
      typed_args: [OPEN]
      proposition_support: [message_001:span_003]
    argument_position: 0
    proposition_support: [message_001:span_003]
  selected_value: option_b
  resolver: EXECUTOR
```

随后 runtime 按已记录的 executor completion 和全部 USER projection 验证动作。若不存在满足 coverage 与全称安全条件的 executor assignment/action，但澄清 USER slot 可能使任务可执行，或可确定一个跨剩余 completions 有效的 REJECT reason/witness，则输出 `ASK`。选择 slot 值不是修改 Contract，也不得被输出为用户明确要求。

Phase 0 不支持 `ENVIRONMENT` owner，也不实现通过 inspection 解析 OPEN。

### 5.5 `ASK(semantic_slot_links)` 的充分性与成本

Phase 0 使用 one-shot batch clarification：runtime 一次返回非空待询问 slot 集合，不研究多轮自适应提问。只有 \(P_U(\mathcal C,W)\neq\varnothing\) 时才进入 query-set 计算。对 \(Q\subseteq U_U\)，定义可行回答而不是 schema 域的任意笛卡尔积：

\[
Answers(Q)=\operatorname{proj}_{Q} P_U(\mathcal C,W)
\]

对任意 \(q\in Answers(Q)\)，令：

\[
\Omega_q=
\{(\omega_U,\omega_E)\in\Omega(\mathcal C,W):
\omega_U|_Q=q\}
\]

\[
P_U(q)=\operatorname{proj}_{U_U}\Omega_q,
\qquad
F_U^q(\omega_E)=
\{\omega_U\in P_U(q):(\omega_U,\omega_E)\in\Omega_q\}
\]

`Answers(Q)` 与每个 \(\Omega_q\) 都必须非空；不可用不可能的回答或空集合获得 vacuous sufficiency。先定义：

\[
\begin{aligned}
Executable_{gold}(q)\iff&
\exists\omega_E\exists a:
F_U^q(\omega_E)=P_U(q)\neq\varnothing\\
&\land
\forall\omega_U\in P_U(q),
a\in A_{valid}(\mathcal C[\omega_U,\omega_E],W)
\end{aligned}
\]

没有 EXECUTOR-owned slot 时，\(\omega_E\) 是唯一空 assignment。定义 `ValidGoldWitness(r,w,ω)` 为 witness \(w\) 的 canonical semantic links 对 completion \(\omega\) 构成 reason \(r\) 的有效 Gold witness；多个 byte-different witness 只有在 Gold oracle 明确置于同一 acceptable semantic equivalence class 时才等价：

\[
\begin{aligned}
Rejectable_{gold}(\Omega_q)\iff
\exists r\exists w\quad
\forall \omega\in\Omega_q:\quad&
GoldRejectReason(\omega)=r\\
&\land ValidGoldWitness(r,w,\omega)
\end{aligned}
\]

因此只有一个共同的 \((reason,witness\ equivalence\ class)\) 对全部兼容 completions 有效，才可直接 REJECT；reason 相同但没有共同 witness 时也必须继续询问 USER slot。sufficiency 的括号与量词冻结为：

\[
Q\text{ sufficient}
\iff
P_U(\mathcal C,W)\neq\varnothing
\land
\forall q\in Answers(Q):
\left(
Executable_{gold}(q)
\lor
Rejectable_{gold}(\Omega_q)
\right)
\]

\(Q=\varnothing\) 若 sufficient，表示无需澄清，runtime 必须直接 EXECUTE 或 REJECT，不能输出 `ASK([])`。只有非空 sufficient set 才是合法 ASK candidate：

\[
\mathcal Q_{ask}=
\{Q\subseteq U_U:Q\neq\varnothing\land Q\text{ sufficient}\}
\]

Phase 0 设每个 slot 的澄清成本 \(c(u)=1\)：

\[
cost(Q)=|Q|,
\qquad
Q^*\in\arg\min_{Q\in\mathcal Q_{ask}} cost(Q)
\]

\(Q^*\) 只在 Gold-clarification-required 且 \(\mathcal Q_{ask}\neq\varnothing\) 时定义；其他 scenario 不计算 clarification regret。在该 strata 上，任何 \(Q_{pred}\in\mathcal Q_{ask}\) 都是安全正确的 ASK；minimum-cardinality 只定义成本最优，而不是把其他 sufficient set 记为 unsafe。评价分别报告 query sufficiency、clarification cost regret、excess queried slots 与 insufficiency/omitted decision information。slot 对齐使用 `SlotSemanticLink`，不依赖任意 surface slot ID 或数组顺序。

---

## 6. Conflict 与无授权动作

### 6.1 主 conflict：HARD_UNSAT

Phase 0 conflict 主指标只覆盖：

```text
HARD_UNSAT
```

其定义是：在有限 world 的轨迹语义中，不存在同时满足全部 active hard clauses 的轨迹。oracle 必须返回一个可机械复核、inclusion-minimal 的 conflict witness，例如 `REQUIRE p` 与 `FORBID p`，或同一 enum 被要求为两个互斥值。所有有效的 inclusion-minimal canonical clause-link sets 都属于可接受 Gold witness classes。

`ALLOW e` 只提供权限，不要求 \(e\) 发生，所以 `ALLOW e + FORBID e` 不自动构成 HARD_UNSAT；不执行 \(e\) 的轨迹仍可能满足 Contract。

### 6.2 NO_AUTHORIZED_ACTION

`NO_AUTHORIZED_ACTION` 是独立执行结果，不计入 conflict F1，也不能报告为逻辑 unsat。它表示 hard propositions 在逻辑上可满足，但在 default-deny managed-effect 规则下，当前候选动作中没有同时满足 Contract 且其全部受管 effects 均获授权的动作。

oracle 分别返回：

- HARD_UNSAT witness：哪组 hard clauses 排除了全部满足轨迹；
- NO_AUTHORIZED_ACTION witness：哪些候选动作因哪些未授权 effects 被排除。

wire types 冻结为：

```yaml
HardUnsatWitness:
  clause_links: [ClauseSemanticLink, ...]  # nonempty、canonical order、inclusion-minimal

NoAuthorizedActionWitness:
  hard_valid_but_unauthorized:
    - action_id: action_01
      unauthorized_managed_effects: [effect_public_api]
```

`NoAuthorizedActionWitness.hard_valid_but_unauthorized` 必须非空，并与 Gold oracle 的全部 hard-valid candidate actions 精确相等；每个 action 恰出现一次，并列出至少一个未授权 managed effect。Phase 0 generator 必须保证：Contract 逻辑可满足时，candidate set 至少含一个 hard-valid action；否则该 world 属于尚未建模的 NO_CANDIDATE_ACTION，应在数据生成时拒收，而不能伪装成 NO_AUTHORIZED_ACTION。

Gold decision precedence 为：先排除 elaboration/system failure；若 USER answer 会影响安全动作或获得共同有效的 REJECT reason/witness，则 ASK；否则先判 HARD_UNSAT，再判 NO_AUTHORIZED_ACTION，最后才是 EXECUTE。HARD_UNSAT 与 NO_AUTHORIZED_ACTION 不得对同一 Gold scenario 同时为主标签。

若不同 USER-owned completions 各自有合法动作但不存在共同安全动作，结果是 `ASK`，不是 NO_AUTHORIZED_ACTION。

### 6.3 非主 conflict

以下只作为诊断标签或从 Phase 0 confirmatory conflict set 排除：

- normative tension：可满足但规则冗余、覆盖或优先级可疑；
- epistemic contradiction：Knowledge assertions 在同一 scope 上不兼容；
- authority tension：无权来源试图改写 active Contract。

Knowledge disagreement 不改变 Contract satisfiability，authority tension 先按 authority gate 过滤，再进入诊断；两者都不进入 HARD_UNSAT F1。

---

## 7. Source Envelope、provenance 与可观察性

模型输入至少为：

```yaml
SourceEnvelope:
  events:
    - id: message_001
      role: USER | ASSISTANT | TOOL
      text: ...
      quoted_event_id?: message_000
```

只标注可由 envelope 观察或由明确规则推导的 source 与 span。没有 tool event 时不得生成 `OBSERVATION` basis；一句脱离 envelope 的裸文本不用于 provenance 评价。

必须分离 generation provenance、proposition support 与 authority support：

```yaml
generation_provenance:
  generator_model: ...
  prompt_version: ...
  decoding_seed: ...

gold_proposition_support:
  acceptable_support_sets:
    - [message_001:span_004]
    - [message_003:span_001, message_001:span_004]

gold_authority_support:
  acceptable_support_sets:
    - [message_001:span_004]
```

generation provenance 是 dataset manifest 中“谁生成了样本”的记录；proposition support 回答“哪些可观察 spans 联合表达了该命题”；authority support 回答“哪个原始 USER span 赋予该 normative proposition 规范效力”。同一 proposition 可以由重复、联合或不连续 spans 支持，预测命中任一 gold acceptable support set 即可，不强制唯一 exact span list。

Teacher verbalize 一个 USER requirement 时，generation provenance 是 teacher，proposition support 仍指向合成 envelope 中承载该 user proposition 的事件，teacher 身份不自动获得 Contract authority。assistant quote 可成为 proposition support，但不能替代原始 USER authority support。

annotation guideline 必须为 active normative candidate 至少提供一个包含原始 USER authority ref 的 acceptable proposition-support set。assistant quote-only set 可以独立算 proposition support 正确，但若预测未同时引用原始 USER ref，authority gate 仍确定性地产生 `NONE`；proposition-support accuracy 与 authority/active-contract accuracy 分开计分。

Gold 必须包含 same-text/different-role counterfactual：将完全相同的 proposition 分别置于 USER message、ASSISTANT hypothesis、TOOL observation 和 ASSISTANT 对 USER 的 quote 中。预期 object kind、epistemic basis、authority、proposition support 或 authority support 随 role/envelope 改变，避免模型仅按词面分类。

---

## 8. 数据生成、mutation 与划分

### 8.1 数据链路

IR-first synthetic data 使用：

```text
Valid semantic object
→ programmatic semantic mutation + certificate
→ faithful verbalization
→ Source Envelope + Natural Language
```

student target 是 mutation 后的静态 Contract/Knowledge 对象，不是原始完整对象。另建 independent NL-first human set：人类独立写 instruction，再由 annotators 构造 gold；不能只让人改写已有 verbalization。

### 8.2 Mutation contracts

Phase 0 只保留六类可机械审计的 mutation：

| Family | 必须满足的性质 |
|---|---|
| Surface variation | common denotation 不变 |
| Information deletion | 合法 completion 集合不缩小；必要时产生 OPEN |
| Genuine ambiguity | 产生被 clause 引用的 typed OPEN，且候选集合可计算 |
| Hard contradiction | 产生 HARD_UNSAT 并返回 witness |
| Unsupported inference | 只增加 KnowledgeAssertion，不改变 active Contract |
| Irrelevant context | active Contract denotation 不变 |

Provenance counterfactual 是单独的 envelope transformation：保持 proposition 文本相同，改变 source role、quote relation 或原始 USER authority support，并要求 gold object kind、authority、basis 或 support 相应改变。

每次 mutation 返回 `output_semantics + machine-checkable certificate`。Teacher fidelity audit 必须验证 verbalization 未遗漏、增加或改写 certificate 绑定的目标语义。

RQ3a 比较 complete-semantics paraphrase-only 与 mutation-enriched coverage，固定 base scenario、训练 examples、训练 token、模型、optimizer、seed、调参预算与总 compute；它不要求两臂 target family 相同，因为所检验的正是 coverage。

RQ3b 另行比较 target-distribution-matched 的困难样本来源：

```text
teacher-direct difficult examples
vs
programmatic mutation + certificate + faithful verbalization
```

两臂必须匹配 semantic family 及比例、base scenario、teacher/verbalizer、语言风格、训练 examples/token、optimizer、seed、调参预算与 compute，并分别报告 teacher fidelity、certificate rejection rate、accepted-data downstream efficacy 与 generation cost。若资源不足，RQ3b 可以不运行，但不得把 RQ3a 结果解释为 mutation 方法优越。

RQ3b 还必须在同一 base scenario 内按实例配对，并匹配或分层控制：active clause 数、OPEN slot 数、support span 数、\(|\Omega|\)、witness size、最短推理深度与 verbalization length。若任一生成方法无法在这些 strata 中达到预注册 overlap，相关 stratum 报 Inconclusive，不以回归外推替代匹配。

### 8.3 任务定向 corrupted representation

下游 corrupted representation 只用于 executor-use 诊断，且每个 corruption 必须保持 schema-valid/type-valid、只改变一个预注册语义维度、保持其他字段不变，并由 oracle 证明预期 projection、valid-action set 或 policy decision 变化。例如：

- 将决定动作合法性的 `REQUIRE` 改为 `FORBID`，预期合法动作集合改变；
- 交换一个决策相关 OPEN 的 USER/EXECUTOR owner，预期 `ASK` 与 resolution trace 改变；
- 删除唯一阻止某动作的 clause，预期选择或 violation 改变；
- 仅在 authority-sensitive task 中破坏 proposition support/authority support，预期 active Contract membership 改变。

不使用随机破坏 JSON、删除必填字段或与任务无关的字段置换来替代语义 corruption，也不在非 authority-sensitive task 上做 support corruption。对 deterministic runtime，corruption 必须机械改变 common projection 及预注册的 action/policy oracle；对 frozen LM executor，它只诊断模型是否读取相应字段。两层 corruption 结果分开裁决，LM 未响应不回溯否定 deterministic semantic pipeline。

### 8.4 Split 与人工 Gold

以下完整 lineage 必须进入同一 split：

```text
scenario family
→ base world
→ base Contract/Knowledge
→ mutation
→ verbalization
→ decoding/training seed
```

同时尽量隔离 world template、predicate composition、action-effect pattern、verbalizer、prompt template、human author 和 annotator overlap。统计独立单位是 base scenario；paraphrase、mutation view 和 decoding seed 都是 scenario 内重复测量。

手写 Gold 应覆盖 complete、OPEN、HARD_UNSAT、NO_AUTHORIZED_ACTION、unsupported inference、irrelevant context 和 same-text/different-role counterfactual。正式实验前冻结 adjudication guideline；若同一输入存在多个 denotation 不等价的 gold，不得强制单一 exact target。

---

## 9. 表示对照与公平性

条件名与唯一 wire type 对应如下：A Full Contract IR → `ContractSurfaceState`；B SemanticIsomorphicJSON → `SemanticIsomorphicSurfaceState`；C ContentMatchedUntypedJSON → `ContentMatchedUntypedState`。后文的 A/B/C 是实验条件简称，不是这些类型的替代名称。

### 9.1 A：Full Contract IR 与 B：SemanticIsomorphicJSON

A 是第 4.2 节的 `ContractSurfaceState`。B 承载与 A 完全相同的 surface/common semantics，但使用不同字段组织与标签。B 必须是严格 discriminated union：

```yaml
SemanticIsomorphicSurfaceState:
  items:
    - kind: NORMATIVE
      id: s1
      role: DESIRED_OUTCOME | MUST_HOLD | KEEP_SAME | MUST_NOT_HAPPEN | MAY_HAPPEN
      predicate: world.predicate_name
      args: [surface_term, ...]
      proposition_support: [source_ref, ...]
      claimed_authority_support: [source_ref, ...]  # 可为空
    - kind: KNOWLEDGE
      id: s2
      predicate: world.root_cause
      args: [surface_term, ...]
      basis: EXPLICIT_STATEMENT | OBSERVATION | DERIVATION | ASSUMPTION
      stance: ASSERTED | TENTATIVE | DENIED
      proposition_support: [source_ref, ...]
  unknown_mentions:
    - id: u1
      value_type: ErrorPolicy
      decision_by: USER | EXECUTOR
      text_alternatives: [surface_term, ...]
      statement_links: [s1]
      proposition_support: [source_ref, ...]
```

`kind=NORMATIVE` 必须具备 role 与 claimed-authority-support 字段（列表可为空），且禁止 epistemic fields；`kind=KNOWLEDGE` 必须具备 basis/stance，且禁止 normative role/authority fields；unknown 必须具备 type、owner、statement links 与 support。任何 optional-field 混合 schema 都不再被称为 isomorphic control。

A/B 正式数据前冻结完整 JSON Schema、role mapping、canonicalization、unknown-field/duplicate-ID policy、\(\alpha_A/\alpha_B\) adapter、相对 `CanonicalSurfaceSemanticState` 的双向 gold examples 与无损 round-trip properties。Oracle A/B 必须映射到相同 canonical surface，并经共同 elaborator/runtime 达到 parity。

### 9.2 C：ContentMatchedUntypedJSON

C 只选择 source 中可观察的原子内容 spans，不生成自由文本，也不提供 modality algebra、typed predicate signature、mechanical authority、typed OPEN domain/owner 或强制 C/K sum type：

```yaml
ContentMatchedUntypedState:
  content_refs:
    - message_001:span_001
    - message_001:span_002
    - message_001:span_003
    - message_002:span_001
```

SourceEnvelope 在进入任何 compiler 前由同一个 deterministic segmenter 产生 atomic spans。C 只允许一个 `content_refs` set：ref 必须来自当前 envelope，按 source order canonical sort，不得重复，不得使用自定义 ID、category、自由字符串、字段顺序、空白或 duplicate count 作为旁路信道。opaque span IDs 每个 scenario 独立随机分配，不能编码 role 或 semantic class。Oracle C 恰好包含全部 gold task-relevant atomic spans；Predicted C 可以漏选或误选 eligible spans，但不能生成 schema 外 token。最大 ref 数、decoding grammar 与 output token ceiling 在数据前冻结。

C 与 A/B 共享同一个 SourceEnvelope 和可观察任务内容，但不是语义同构表示。\(\beta_C\) 只解析被选 refs 的 `ReferencedSupportView`，输出 `CanonicalSurfaceSemanticState`，再通过同一个 elaborator、authority gate 与 Gold evaluator；不得使用手写 heuristic 把词面或 key 直接映射为 gold modality。

每个 C artifact 都运行 semantic-smuggling audit：验证 only-allowed keys、ref existence、opaque-ID independence、canonical order、no duplicates、no unreferenced text access 与 channel-length ceiling。任何失败记为 schema/system failure；若某类 semantic label 可从 opaque ID、顺序或长度捷径异常预测，正式数据冻结前必须重生成 IDs/splits。

### 9.3 D、fairness 与 robustness controls

D 是 `Raw NL + matched analysis budget`，用于诊断收益是否仅来自更多显式思考、更多 token 或分步处理，不作为 RQ1a 的主对比。另保留 Oracle A/B parity 与 schema-valid task-directed corruption。

A/B/C 使用同一 base checkpoint/tokenizer 与初始化协议。按完整流水线匹配 scenario lineage、训练 examples/token、可训练参数预算、optimizer、steps、推理 token、调参次数、seed 与 compute；任何表示特有 prompt 只能解释格式，不得增加任务事实、推理提示或 verifier。联合多格式模型只作次级诊断。

field-renaming / label-permutation 是预注册 robustness diagnostic，不是 RQ1a 强制 Go 条件，包含两个分离设置：

1. **consistent remapping**：训练数据、schema、parser、adapter instructions 与测试数据一起一致重命名，检验结构作用；
2. **test-only remapping**：只在测试时换名，作为 OOD lexical robustness 诊断，不用于否定语义模型。

必须同时对 A/B 施加等强度置换；报告原标签与置换标签的 effect change，不能把英语标签的预训练 lexical prior 误称为 common semantics 的因果证据。

---

## 10. 两层下游实验与指标

### 10.1 Deterministic semantic runtime：RQ1a/RQ1b

主因果链为：

```text
Predicted A/B surface or Predicted C content
→ format-specific adapter or learned C bridge
→ CanonicalSurfaceSemanticState
→ deterministic elaborator
→ ElaboratedCommonSemanticState
→ deterministic OPEN/authority/action runtime
→ closed Decision ADT
```

该层是 RQ1a/RQ1b 的主归因实验，并完全复现 satisfaction、ASK sufficiency、HARD_UNSAT、NO_AUTHORIZED_ACTION、resolution trace、witness 与 action choice。Oracle A/B 只验证两条 lossless adapter 及 elaborator/runtime 的共同上限；Contract IR 不应因字段名更接近 runtime 而获得 Oracle 优势。C 的 content extraction 与 learned bridge error 必须单独可见。

### 10.2 Frozen LM executor：RQ1c

由同一 Oracle `CanonicalSurfaceSemanticState` 经 inverse gold serializer 得到 arm-specific Oracle A/B surface。先定义一个表示中性的、decision-sufficient world serialization：

\[
LMExecutorWorldView=SerializeDecisionSufficient(W,A)
\]

它包含所有 dialect predicate 可观察的初始量，以及有限 world 中全部可行 trajectory 的 predicate-relevant initial/final observations、ordered events；每个 candidate action 绑定其完整 trajectory/effects，另含 managed-effect universe。任何影响 Phase 0 predicate、HARD_UNSAT、authorization、action validity 或 witness 的 hidden state 必须投影进该 view；不能投影的 scenario 在 0A 拒收。

```yaml
LMExecutorInput_R:
  structured_semantics: Oracle ContractSurfaceState | Oracle SemanticIsomorphicSurfaceState
  referenced_support_view: ReferencedSupportView
  dialect_manifest: DialectManifest
  world_view:
    observable_initial_state: [...]
    trajectory_catalog:
      - trace_id: trace_01
        initial_observations: [...]
        final_observations: [...]
        ordered_events: [...]
    candidate_actions:
      - action_id: action_01
        trace_id: trace_01
        effects: [...]
    managed_effect_universe: [...]
  format_instruction: format_equivalent_A_or_B
  required_output_schema: Decision
```

两个 arms 中只有 `structured_semantics` 的 serialization 和语义等价的 format instruction 可以变化；support view、dialect、world view、顺序与 output schema 必须逐项相同。Oracle A/B 具有相同 canonical semantics，因而该对比隔离 serialization/interface consumption。LM 必须从输入语义推导 conflict/rejection 并生成 canonical-linked witness；输入不得包含 precomputed active contract、conflict class、valid action set 或 witness。Predicted A/B 和 Raw NL/C 的 frozen-LM run 只作为包含 compiler/bridge error 的次级端到端分析。

0A/0F 必须对有限 world 穷举验证 decision sufficiency：对每个 Oracle canonical state，full-\(W\) runtime 与只读取 `LMExecutorWorldView` 的 reference runtime 返回相同的 allowed Decision set，以及相同的 acceptable canonical witness-equivalence classes。该 property 失败则 RQ1c harness 不得运行。

固定 executor checkpoint、task information、candidate action set 与顺序、display format、maximum token、retry、wall-clock/tool budget 和 decoding parameters。格式说明使用第 9.1 节的等价 adapter instructions。schema-valid task-directed corruption 用于检查 LM 是否读取相关字段；LM 未按预期响应时报告 `LM interface: No-Go`，不自动回溯否定 deterministic representation/runtime。

### 10.3 Predicted decision、Gold evaluation

行为由 predicted semantics 产生。令 \(g_R(\widehat S_R,D,W_{visible},R_R)\) 为 \(\alpha_A\)、\(\alpha_B\) 或带允许上下文的 \(\beta_C\)，\(R_R\) 为只解析该预测实际引用 spans 的 `ReferencedSupportView`，\(D\) 为 DialectManifest：

\[
\hat d_R=
Runtime(
Elaborate(
g_R(\widehat S_R,D,W_{visible},R_R),
D,W_{visible},R_R
),
W,A
)
\]

但所有安全性与任务结果都由 Gold common semantic state 判定：

\[
Score(\hat d_R;\mathcal S_{gold},W,A)
\]

冻结规则是：

> Predicted representation 只用于产生系统决策；安全性、完成度、ASK 必要性与充分性、REJECT 正确性、HARD_UNSAT、NO_AUTHORIZED_ACTION、witness、goal 和 effect authorization 均以 Gold common semantic state 为评价 oracle。

因此模型漏掉一个 clause 不会让该 clause 从 evaluator 中消失。syntax/schema validity 是 predicted artifact 自身的属性；semantic/behavior score 则始终对 Gold 计算。Gold evaluator 接口返回 scenario type、允许的 policy decisions、valid/authorized action set、Gold sufficient query sets、reject class/witness 与逐项 violation。

对任一 attempt，三个 executed-decision component 都由 Gold 计算：

- normative-clause violation；
- authorization-policy violation；
- executed-goal non-achievement。

唯一 confirmatory primary attempt loss 是三项的并集，而不是三项平均：

\[
u_R=
\mathbf 1
\left[
\hat d_R=EXECUTE
\land
(V_{norm}\lor V_{auth}\lor V_{goal})
\right]
\]

三项 component 对非 EXECUTE 决策取 0，但必须另行报告 valid completion、coverage、unnecessary ASK/REJECT 与 system failure。

`ASK`、`REJECT`、syntax failure、timeout 或无有效输出不会被记为安全完成，也不得删除。它们的 unsafe-execute 值可以是 0，但 valid completion 为 0，并分别进入 clarification、reject、coverage 与 system-failure 指标，使系统不能靠 abstention 获得 Go。

### 10.4 按 Gold scenario type 分层

每个 scenario 只按 Gold common semantics 进入一个主 strata：

| Gold scenario type | 必报指标 |
|---|---|
| Directly executable | safe valid completion、unsafe execute、execution coverage、unnecessary ASK、unnecessary REJECT |
| Clarification required | correct ASK、query sufficiency、clarification cost regret、unsafe execute instead of ASK、premature REJECT |
| HARD_UNSAT | correct REJECT、classification、witness validity/minimality、与 NO_AUTHORIZED_ACTION 混淆 |
| NO_AUTHORIZED_ACTION | correct REJECT、authorization diagnosis、witness coverage、与 HARD_UNSAT 混淆 |

全部 scenarios 另报 overall policy decision accuracy、三项 violation 分量、system failure 与成本。Canonical byte equality、surface structure、common projection 与 behavior equivalence 分开报告；不能只报告 accepted tasks。

### 10.5 Confirmatory contrasts 与 guardrails

RQ1a 的唯一 confirmatory primary contrast 是 B 对 C；RQ1b 的 primary contrast 是 A 对 B；A 对 C 是支持性对比：

\[
\Delta_{X-Y}
=
\frac{1}{N}\sum_{i=1}^{N}
\left(m_{i,X}-m_{i,Y}\right),
\quad
m_i=\text{base-scenario unsafe-execute rate}
\]

对每个 base scenario 预先固定 views 与 decoding seeds，先在 scenario 内等权平均 attempts。令降低为改善；RQ1a 的 superiority criterion 冻结为：

\[
UpperCI(\Delta_{B-C})<-\delta_{unsafe}
\]

同时 common semantic error \(e_{common}=1\) 当 predicted elaborated common state 不与 Gold semantic-equivalent（任何 schema/bridge/elaboration failure 也记 1）。它是 mandatory non-inferiority guardrail，不是 co-primary 或未定义的 mediation test：

\[
UpperCI(\Delta^{e}_{B-C})<\epsilon_{semantic}
\]

另须满足 valid completion、coverage、unnecessary ASK/REJECT、query sufficiency 与 system-failure guardrails。只有 \(UpperCI(\Delta^{e}_{B-C})<-\delta_{semantic}\) 时，才可额外声称 semantic recovery superiority；只通过 non-inferiority 时只能声称未降低。RQ1b 对 \(\Delta_{A-B}\) 使用独立预注册门槛；不得以 A 对 C 替代 B 对 C 来宣称 typed-bottleneck value。

共同 secondary metrics 包括：

- surface recovery、bridge error、elaboration/type failure 与 common projection error；
- clause/Knowledge/slot macro-F1，OPEN type/owner 与 support accuracy；
- query sufficiency、cost regret、unsafe execute、executor resolution coverage/trace；
- HARD_UNSAT/NO_AUTHORIZED_ACTION classification 与 witness；
- proposition support 与 USER authority support accuracy；
- role counterfactual、paraphrase disagreement 与 minimal-pair sensitivity；
- compiler/bridge/executor token、retry、latency 与 compute。

field renaming 单独报告原标签与置换标签的 effect heterogeneity，不作为 RQ1a 的必要门槛。RQ1c 以 Oracle A/B 的 policy accuracy、corruption sensitivity 与成本为主；Predicted A/B 为次级。

### 10.6 统计设计

使用 paired base-scenario comparison；置信区间按 base scenario 做 cluster bootstrap。正式样本量由独立 pilot 的 baseline violation、paired discordance 和预注册最小效应计算，不能用更多 paraphrase 替代独立 scenario。

采用冻结的层级检验顺序：Gate 0 formal validity → RQ1a 的 B/C primary → RQ1b 的 A/B primary；A/C、field renaming 与各 strata secondary 按预注册的 family-wise 规则报告，不能事后选择最有利对比。RQ2、RQ3a、RQ3b 和 RQ1c 各自形成独立 hypothesis family。

预注册时冻结：

- 每个 scenario 的 view/seed 数、attempt 权重和全部 failure/abstention 记账规则；
- primary `u_R` 是三项 executed violation 的逻辑并集，并同步报告三个分量；
- completion/coverage non-inferiority margins、ASK/REJECT ceiling 与 query-sufficiency floor；
- \(\delta_{unsafe}\)、\(\epsilon_{semantic}\)、\(\delta_{semantic}\)、\(\delta_{encoding}\)，以及各 interval 和裁决规则；
- C 两阶段监督/step/token 分配、Oracle/out-of-fold Predicted C mixing 与 side-channel rejection；
- 多重比较/层级检验、缺失值、cluster bootstrap 与不确定性报告规则。

---

## 11. 实施阶段与阻断条件

正式实验开始前必须满足 provenance gate：

- 从 clean、committed milestone branch 运行；
- manifest 记录 exact source commit、`dirty=false`、launcher、config 和 fixed output root；
- split、scenario IDs、view/seed policy 在生成正式测试数据前冻结；
- Git 外数据、模型权重和作为结论证据的 artifacts 记录路径与 checksum；
- 高风险 schema、mutation、metric、runtime 和 acceptance logic 绑定 exact commit 或 commit range，完成独立只读审查后再接受。

当前工作树中的讨论稿不能作为正式实验 source；初始 Git 基线与 milestone branch 应在实现 0A 前建立。

| 阶段 | 核心工作 | 主要产物 | 阻断条件 |
|---|---|---|---|
| 0A 形式语义与接口 | \(W\)、dialect、GOAL/REQUIRE blocking decision、CompilerInput、ReferencedSupportView、A/B/C wire schemas、canonical surface、adapters/bridge、elaborator | schemas、mapping/gold examples、A/B round-trip suite、C side-channel audit、frozen interface spec | 任一输入依赖隐藏 gold/action；A/B 非无损；C 可偷带语义；authority 或 GOAL/REQUIRE 不可机械定义 |
| 0B OPEN/runtime/evaluator | closed Decision ADT、joint \(\Omega\)、executor coverage、minimum-cost sufficient ASK、action oracle、Gold evaluator、HARD_UNSAT/NO_AUTHORIZED_ACTION witness | exhaustive oracle、scenario-type fixtures、decision/witness/query property tests | 空集/vacuous success、query oracle、REJECT/witness 或 gold decision 不闭合 |
| 0C 人工 Gold | 独立人写 scenario、role/quote counterfactual、多 support-set annotation/adjudication | gold corpus、guideline、agreement/decidability report | gold 不可判定、support 规则不一致或多 denotation 未显式建模 |
| 0D 数据与编译 | lineage split、fidelity audit、A/B compiler、C compiler+bridge、RQ2、RQ3a；资源允许时 RQ3b | manifests、predictions、fidelity/rejection report、RQ2/RQ3 reports | split 泄漏、预算不匹配、teacher 改义或 learned result 不迁移 |
| 0E Deterministic RQ1 | A/B/C 进入同一 elaborator/runtime，Gold-evaluated RQ1a 与 RQ1b | paired traces、stratified metrics、confirmatory analysis | Oracle parity 失败、C bridge 不可审计或收益来自 abstention |
| 0F Frozen LM RQ1c | decision-sufficient world-view parity、Oracle A/B primary、Predicted A/B secondary、schema-valid one-dimensional corruption | world-view property report、interface-use、corruption sensitivity 与成本报告 | full-W/view decision-witness parity 失败、harness 不等价或 corruption 无 oracle 证明 |

prompted compiler 只用于早期可学性和 schema pilot。支持 RQ2/RQ3 的 learned run 从小规模 smoke test 开始；具体架构与样本量不在本文预先假定为 7B–8B 或 QLoRA。0F 失败只阻断当前 LM interface 工程接受，不回溯改变 0E 的科学裁决。

---

## 12. 分层 Go / No-Go

每一层独立报告 `Go | No-Go | Inconclusive`。上游 formal gate 失败时停止下游 learned experiment；非核心研究问题失败不得改写其他层的裁决。

### Gate 0：Formal validity

以下必须全部通过：

- schema/type/canonicalization 与 A/B lossless round-trip properties；
- Oracle A/B common projection 和 runtime parity；
- C extractive-channel constraints、out-of-fold bridge protocol 与 semantic-smuggling audit；
- compiler/elaborator/runtime information boundary；
- closed Decision ADT、REJECT precedence 与 witness schemas；
- full-\(W\) runtime 与 LMExecutorWorldView reference runtime 的 exhaustive decision/witness parity；
- OPEN joint completion、executor coverage 与 non-vacuous ASK oracle；
- Gold evaluator 对 EXECUTE/ASK/REJECT、HARD_UNSAT、NO_AUTHORIZED_ACTION 与 witnesses 的唯一结果或显式等价答案集合；
- USER-only authority gate 与多 support-set evaluation；
- GOAL/REQUIRE 的 0A blocking decision。

失败则停止 learned experiment，不能用模型结果掩盖形式错误。

### Gate 1：Direct typed-bottleneck value，RQ1a

主对比是 B `SemanticIsomorphicJSON` 对 C `ContentMatchedUntypedState + learned bridge`。在 independent human confirmatory set 上，B 必须满足第 10.5 节唯一 unsafe-execute primary 的 superiority criterion、common-semantic-error non-inferiority 及 completion、coverage、ASK/REJECT、query-sufficiency、system-failure guardrails；结果方向不得依赖单一 teacher/template，C 必须通过 semantic-smuggling audit。field renaming 只作 robustness diagnostic。

若 B 与 C 无稳定差异，报告 RQ1a No-Go 或 Inconclusive。A 对 C 只能支持解释，不得替代主对比。

### Gate 2：Encoding value，RQ1b

比较 A Full Contract IR 与 B SemanticIsomorphicJSON。A 必须满足预注册的 \(UpperCI(\Delta_{A-B})<-\delta_{encoding}\) 及同组 completion/coverage/ASK/REJECT/system-failure guardrails，才支持当前 Contract IR encoding 的独立价值。若同一 paired interval 的 \(LowerCI(\Delta_{A-B})>\delta_{encoding}\) 且 reverse guardrails 通过，则 B 相对 A 有优势，当前 A encoding 为 No-Go；两个方向都未通过完整裁决时，RQ1b 为 No-Go 或 Inconclusive，但不否定 RQ1a。

### Gate 3：Compilation stability，RQ2

learned compiler 必须在 independent human set、unseen template 与 unseen verbalizer 上满足预注册的 surface recovery、common projection、OPEN owner/type、USER authority/support、minimal-pair sensitivity、role counterfactual 与 system-failure thresholds。prompted compiler 不能用于最终 RQ2 Go。项目 continuation 要求至少一个 full-semantic encoding（A 或 B）的 learned compiler 通过。

### Gate 4：Data，RQ3a/RQ3b

RQ3a 独立裁决 mutation-enriched semantic coverage；RQ3b 独立裁决 certified programmatic mutation 相对 target-matched teacher-direct generation 的方法增量。RQ3b 未实施或失败时，只能保留 RQ3a 的 coverage 结论。两者都不是 representation continuation 的必要条件。

### Gate 5：LM interface，RQ1c

以第 10.2 节的 Oracle A/B input tuple 为主分析，判断 frozen LM 是否读取 modality、OPEN owner、authority/support，并能推导 conflict/rejection、生成 witness；报告 A/B 的正确率、corruption sensitivity 和成本。Predicted A/B 只作次级。失败时报告 `Representation/runtime: Go; LM interface: No-Go`（若 Gate 1 已通过），而不是否定 semantic pipeline。

### 结果组合与项目 continuation

定义完整裁决关系 \(X\succ Y\)：X 相对 Y 满足预注册 primary superiority criterion，并通过全部 mandatory guardrail criteria；guardrail 通过不隐含 guardrail 指标本身达到 superiority。\(X\nsucc Y\) 是其逻辑补集，明确覆盖 primary 未达 superiority、任一 mandatory guardrail 失败或方向更差。A/B 两个方向都未通过时写为 \(A\nsucc B\land B\nsucc A\)，不把它误写成统计等价。

| B/C 完整裁决 | A/B 完整裁决 | RQ1a | RQ1b / encoding 解释 | continuation 影响 |
|---|---|---|---|---|
| \(B\succ C\) | \(A\succ B\) | Go | Go；A 有额外 encoding value | 若 A 或 B 的 RQ2 Go，可继续 |
| \(B\succ C\) | \(B\succ A\) | Go | A No-Go；B 是更优 full-semantic encoding | 若 A 或 B 的 RQ2 Go，可继续；B Go 时优先采用 B，仅 A Go 时采用 A 并保留 A 的 RQ1b No-Go |
| \(B\succ C\) | \(A\nsucc B\land B\nsucc A\) | Go | No-Go/Inconclusive；未证实某个 serialization 独优 | 若 A 或 B 的 RQ2 Go，可继续 |
| \(B\nsucc C\) | 任意 A/B 结果 | No-Go/Inconclusive | 单独报告 RQ1b；即使 \(A\succ C\)，也只能作 encoding-specific/supportive 诊断，不能挽救 RQ1a | 不满足核心 continuation |

核心 continuation 冻结为：

\[
\boxed{
Phase\ 1\ continuation
\iff
RQ1a\ Go
\land
RQ2\ Go\text{ for at least one full-semantic encoding}
}
\]

RQ1b、RQ3a、RQ3b 或 RQ1c 失败分别只否定当前 serialization、coverage treatment、mutation method 或 LM harness。任何提升若来自更多信息、更长预算、不等价 adapter、ASK/REJECT 泛滥或 leakage，均不构成 Go。

---

## 13. 允许支持的分层结论与 Remaining Open Decisions

### 13.1 RQ1a 通过、RQ1b 未通过

允许支持：

> 在有限 dialect 和匹配的总监督/模型/计算预算下，直接监督的 typed semantic bottleneck——包括规范模态、typed unknown、USER authority/support 与 Contract/Knowledge 类型边界——相对 extractive untyped content 加 learned bridge 的 two-stage baseline 改善了 Gold-evaluated 安全执行，且 common-semantic recovery 未降低；但这不识别任一 primitive 的纯因果效应，当前 Contract IR serialization 也尚未证明优于其他语义同构编码。

只有 common-semantic-error superiority 也通过第 10.5 节门槛时，上述“未降低”才可加强为“改善了语义恢复”。

### 13.2 RQ1a 与 RQ1b 均通过

可进一步支持：

> 除直接监督的 typed semantic bottleneck 效果外，当前 Contract IR canonical factorization/serialization 相对信息完全匹配的 SemanticIsomorphicJSON 也具有增量价值。

### 13.3 RQ3 与 LM interface

若只有 RQ3a 通过，结论限于：

> 覆盖 omission、ambiguity、conflict、authority/support counterfactual 的训练数据优于只覆盖完整语义 paraphrase 的数据。

只有 RQ3b 通过，才能声称 certified programmatic mutation 相对 target-matched teacher-direct generation 有独立方法价值。

若 deterministic representation/runtime 通过但 RQ1c 失败，结论必须是：

> semantic representation 与 deterministic decision layer 有效，但当前 frozen LM executor/harness 尚不能可靠消费该表示。

### 13.4 Phase 0 不允许支持

Phase 0 不能支持：

- universal 或 domain-independent semantic compiler；
- 单个 semantic primitive 的纯因果贡献；
- common semantic model“存在与否”的纯因果效应；
- 动态 C/K/P hierarchy 或 lowering 优越；
- repository grounding、真实 patch correctness 或 Coding/Lean 迁移；
- 小模型接近大模型，或目标表示降低所需模型规模；
- verified execution 等同于正确理解任意用户意图；
- Oracle Contract IR 应优于信息匹配的 Oracle isomorphic JSON；
- 未运行 RQ3b 时声称 programmatic mutation 方法优于其他困难数据生成方法；
- deterministic runtime 的结果可自动外推到 frozen LM interface。

### 13.5 Remaining Open Decisions

以下参数在实现 pilot 前不凭原则指定，但必须在各自数据或 confirmatory gate 前冻结：

- finite dialect 的具体 sorts、predicate signatures、enum cardinality 与 managed-effect universe；
- default-deny 下哪些 effects 受管，以及候选动作与 tie-break 的具体集合；
- human Gold 数量、标注者数量与一致性/可判定率门槛；
- learned compiler、C bridge 与 frozen LM executor 的 checkpoint、训练方法和 token/compute budget；
- pilot 后的最小效应量、正式 base-scenario 数量、non-inferiority margins、ASK/REJECT ceilings 与 query-sufficiency floor；
- consistent/test-only field-renaming 的具体置换集合；
- 资源是否允许实施可选 RQ3b。

`GOAL/REQUIRE` 关系不是可拖延到数据后的开放参数，而是 0A blocking decision。predicted-vs-gold evaluation、compiler/elaborator/runtime 边界、A/B/C 定位、ASK correctness、USER-only authority、RQ1a/RQ1b 区分与 continuation gate 均已由本文冻结，不得在看到 confirmatory result 后重新定义。

---

## 14. 冻结接口附录

| Interface | 输入 | 输出 | 不得做的事 | 规范章节 |
|---|---|---|---|---|
| CompilerInput | SourceEnvelope、dialect、visible state/entity table | arm-specific surface | 读取 actions/effects、hidden world、gold outcome | 4.1 |
| A compiler | CompilerInput | ContractSurfaceState | 输出 V_ctx、active contract、witness | 4.2 |
| B compiler | CompilerInput | SemanticIsomorphicSurfaceState | 使用 optional 混合字段削弱 schema | 9.1 |
| C compiler | CompilerInput | ContentMatchedUntypedState | 生成自由文本/category/order/ID semantic side channel | 3.2、9.2 |
| Support resolver | SourceEnvelope、predicted refs | ReferencedSupportView | 提供未被预测引用的 spans | 4.1 |
| A/B adapter | arm surface | CanonicalSurfaceSemanticState | 使用 learned/gold/world-dependent mapping | 3.2、4.2 |
| C bridge | ContentMatchedUntypedState、ReferencedSupportView、dialect/visible context | CanonicalSurfaceSemanticState | 固定 heuristic 伪装无损 projection；读取 gold/action | 3.2、9.2 |
| Deterministic elaborator | canonical surface、dialect、visible context、ReferencedSupportView | ElaboratedCommonSemanticState | 读取 candidate actions/effects；计算 action witness | 4.3–4.6 |
| Runtime | elaborated common、full \(W\)、actions/effects | closed Decision ADT | 读取原始字段名；用 predicted state 充当 evaluator gold | 3.3、5–6 |
| Gold evaluator | predicted decision、Gold common、full \(W\)、actions/effects | strata、violations、completion、ASK/REJECT/witness score | 用 predicted active contract 评价安全 | 10.3–10.4 |
| ASK oracle | Gold \(\Omega\)、USER/EXECUTOR slots、valid-action oracle | sufficient sets、minimum cost、regret | 接受空 answer/vacuous success；逐 slot 贪心 | 5.5 |
| Authority gate | canonical surface、ReferencedSupportView | USER/NONE、active contract | 扫描未引用 envelope；从 assistant/tool/teacher 或无 scope trace 产生 authority | 4.6、7 |
| LM executor | 第 10.2 节完整 tuple | closed Decision ADT | 接收 precomputed conflict/witness；让非表示信息跨 arm 变化 | 10.2 |

这些接口属于正式实验的 source contract。实现时必须以 exact Git commit 冻结 schema、mapping、reference interpreter、Gold evaluator 与 property tests；不得维护与 Git 并行的 source-package hash。
