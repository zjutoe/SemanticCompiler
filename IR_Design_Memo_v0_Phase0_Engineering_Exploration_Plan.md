# Contract IR v0 Phase 0 工程探索计划

## 1. 定位与待做决策

Phase 0 是一次有限、可穷举、以实现反馈为目标的工程探索。它只回答：

> 当前 Contract IR 想法是否值得继续投入，以及下一阶段最先需要修正什么？

Phase 0 不判断该想法是否已经支持 publication-grade claims，也不试图证明某个表示具有普遍优势。成功表示最小语义内核、运行时和一条真实内容桥接路径已经足够清楚，可以进入后续研究；失败应尽早暴露表示能力、复杂度或可调试性问题。

本阶段分别记录两类工程判断：

- A 对 B：在语义完全相同且 adapter 都是确定性的前提下，Contract IR encoding 是否比薄的语义同构 control 更清晰、更容易保持不变量；
- B 对 C：直接产生 typed semantics 的路径，与先抽取内容再经过真实 bridge 的路径，在实现复杂度、失败位置和端到端可用性上有何差别。

这两个判断不能互相替代。它们是工程取舍记录，不是 primitive 级因果结论，也不需要独立的统计裁决体系。

## 2. 范围与非目标

### 2.1 Phase 0 范围

Phase 0 只实现：

- 一个有限 micro-world 和固定 dialect；
- 最小 Contract/Knowledge canonical semantics；
- typed OPEN、authority、deterministic elaboration 和 reference runtime；
- A、B、C 三条最小路径；
- 手写或 gold blocking fixtures；
- 有界、逐场景的结构化 trace；
- 对每个 fixture 可穷举的 decision oracle 和测试。

所有 enum、predicate signature、fixture、action、effect、tie-break 和 trace schema 都必须在运行前固定。Phase 0 可以使用小型脚本或 reference interpreter 穷举有限状态，不需要扩大数据规模。

### 2.2 非目标

Phase 0 不包含：

- repository grounding、真实 patch 或真实代码执行；
- Lean、SWE-bench 或跨领域迁移；
- 动态 Contract/Knowledge/Plan（C/K/P）lowering 或 revision；
- 动态 OPEN domain、环境 owner 或 inspection-based resolution；
- RL、model scaling 或复杂 multi-agent；
- mutation study、data-method study 或训练 campaign；
- human confirmatory set、分布漂移基础设施或正式统计研究；
- publication claim、通用 semantic compiler claim 或 deployment claim。

## 3. 最小三臂拓扑

三条路径共享同一 dialect、visible world、fixtures、canonical semantics、elaborator、runtime 和 result schema。Phase 0 只要求 C 具备从 `SourceEnvelope` 开始的 normal end-to-end path；A/B 使用 fixture 直接构造 surface，避免为验证语义内核而提前建设三个 NL compiler：

```text
A: fixture/direct typed construction -> ContractSurfaceState
                                    -> deterministic alpha_A ---------+
B: fixture/direct typed construction -> SemanticIsomorphicSurfaceState
                                    -> deterministic alpha_B ---------+
C: SourceEnvelope -> normal C extractor -> ExtractiveContentState
                    -> exactly one real beta_C bridge -------------+
                                                                    |
                                                                    v
                                                       CanonicalSemanticState
                                                                    |
                                                       deterministic Elaborate
                                                                    |
                                                       OPEN / ASK / executor
                                                                    |
                                                       EXECUTE | ASK | REJECT
                                                                    |
                                                                 Result
```

### 3.1 A：Contract IR path

A 由 fixture 直接构造 `ContractSurfaceState`。`alpha_A` 只做字段 canonicalization、ID/link 归一化和机械校验，不能读取 action、effect、gold semantic state 或 fixture expected result。Phase 0 不实现 `SourceEnvelope -> ContractSurfaceState` 的 learned 或 prompted compiler；它属于后续工作。

### 3.2 B：薄的语义同构 control

B 承载与 A 完全相同的 clause、knowledge、OPEN、support 和 authority 信息，但使用一个薄的不同字段组织。`alpha_B` 是确定性、无损的 adapter，codomain 与 `alpha_A` 完全相同。

B 保持便宜：

- 与 A 复用全部 fixtures、dialect、canonical types 和 runtime tests；
- 只增加 surface schema、确定性 adapter 和 A/B parity tests；
- 与 A 一样由 fixture 直接构造 surface，不单独实现 NL compiler；
- 不建立独立数据集、统计 gate、报告体系或实验基础设施。

若 gold A 与 gold B 表达相同语义，它们必须投影到相同 canonical value，并产生相同 decision 和 result。A/B 的差别只能来自 encoding 和 adapter ergonomics，不能来自额外信息。

### 3.3 C：extractive content path

C 是 Phase 0 唯一从 `SourceEnvelope` 开始的 normal end-to-end path。normal C extractor 使用共同 deterministic segmenter，并按 source order 选择当前 envelope 中全部可表示的 atomic spans；它不得读取 gold relevance、fixture expected mapping、scenario result 或 canonical semantics。Phase 0 fixtures 足够小，不增加截断、排序学习或 relevance classifier。

C 的 surface 只有 source 中已存在的内容引用：

```yaml
ExtractiveContentState:
  content_refs:
    - message_001:span_002
    - message_001:span_004
```

引用必须存在、去重并按 source order 排序；C 不得携带 modality、typed predicate、OPEN owner、authority label、gold outcome 或 fixture ID side channel。

`beta_C` 是 C 路径中恰好一个真实、非 gold bridge。它读取 `ExtractiveContentState`、被引用 spans、固定 dialect 和 visible context，输出 `CanonicalSemanticState`。它必须实际解释内容，不能调用 expected mapping、gold canonical state、candidate action、effect 或 expected decision。

Phase 0 将 `beta_C` 冻结为针对 controlled language 的确定性 parser；parser 不得按 scenario ID 分支。该实现必须版本化；本阶段不为 bridge 启动训练 campaign，也不增加第二个 bridge 或上界 condition。

### 3.4 共同边界

共同流水线冻结为：

```text
arm surface
-> alpha_A | alpha_B | beta_C
-> CanonicalSemanticState
-> Elaborate(canonical, dialect, visible context, referenced support)
-> ElaboratedSemanticState
-> Runtime(elaborated, full finite world, candidate actions/effects)
-> Decision and Result
```

adapter/bridge 之前的组件不能看到 gold semantic state；elaborator 不能看到 candidate actions 或 effects；只有 runtime 可以读取完整有限 world 和 action catalog。

## 4. 核心语义与运行时 contract

### 4.1 Canonical state

最小 canonical state 包含：

```yaml
CanonicalSemanticState:
  normative_candidates:
    - modality: GOAL | REQUIRE | PRESERVE | FORBID | ALLOW
      predicate: world.predicate
      args: [typed_term, ...]
      proposition_support: [source_ref, ...]
      claimed_authority_support: [source_ref, ...]
  knowledge_assertions:
    - predicate: world.predicate
      args: [typed_term, ...]
      basis: EXPLICIT_STATEMENT | OBSERVATION | DERIVATION | ASSUMPTION
      commitment: ASSERTED | TENTATIVE | DENIED
      proposition_support: [source_ref, ...]
  open_slot_mentions:
    - type: FrozenEnumType
      owner: USER | EXECUTOR
      proposition_link: canonical_clause_link
      argument_position: 0
      proposition_support: [source_ref, ...]
```

Canonical state 不包含 derived authority、admissible domain、joint completion、valid action、conflict class 或 witness。这些都由下游确定性组件产生。

### 4.2 Authority 与 OPEN ownership 必须分离

规范性 authority 只有：

```text
USER | NONE
```

只有可解析、直接支持该规范命题的原始 USER span 能使 normative candidate 进入 active Contract。assistant、tool、bridge 推断或 executor resolution 都不能创建规范性 authority。

OPEN ownership 只有：

```text
USER | EXECUTOR
```

`USER/EXECUTOR` 回答“未决 enum 值由谁选择”，不回答“谁有权创建或修改 Contract”。尤其：

- `authority=USER` 与 `owner=USER` 是不同字段；
- `authority=USER` 与 `owner=EXECUTOR` 可以同时出现；
- `authority=NONE` 的 normative-looking item 不进入 active Contract；
- executor 只能选择已授权 clause 内、admissible domain 中的值。

### 4.3 Deterministic elaboration

`Elaborate` 负责：

- symbol linking、type checking 和 canonical ordering；
- support ref existence/role 检查；
- 派生 `authority=USER|NONE` 和 active Contract；
- 从固定 enum domain 与 visible static constraints 计算 slot domain；
- 产出 canonical clause/slot links。

任何 schema、link、type 或 support failure 都必须立即成为结构化 stage failure。不得补默认值，也不得把失败 surface 当作空 Contract 继续执行。

### 4.4 Closed decision

runtime 的成功输出只有：

```yaml
Decision:
  oneOf:
    - kind: EXECUTE
      action_id: action_01
      executor_resolutions: [ResolutionTrace, ...]
    - kind: ASK
      semantic_slot_links: [SlotSemanticLink, ...]
    - kind: REJECT
      reason: HARD_UNSAT | NO_AUTHORIZED_ACTION
      witness: structured_witness
      executor_resolutions: [ResolutionTrace, ...]
```

`ASK` links 必须非空且全部指向 USER-owned unresolved slots。executor resolution 必须在 action 或 reject 前记录，并覆盖实际使用的完整 executor assignment。

`HARD_UNSAT` 仅表示 active hard clauses 没有任何 joint semantic completion/trace 可满足。`NO_AUTHORIZED_ACTION` 仅表示 Contract 可满足，但当前 candidate actions 中没有同时 hard-valid 且其 managed effects 均获授权的动作。该区分只保留到足以产生确定行为和可理解 witness 的程度，不扩展错误分类体系。

reference harness 对 `Decision` 的处理构成最小闭环：`EXECUTE` 按冻结的 action transition 产生 post-state 与 ordered effects；`ASK` 不改变 world，只返回待补充的 slot links；`REJECT` 不改变 world，只返回 reason 与 witness。`Result` 只是这一处理的结构化记录，不引入第四种 decision，也不得反向修改 Contract 或 OPEN completion。

## 5. 冻结的 OPEN 边界

Phase 0 明确冻结：

```text
finite enum domains only
max_unresolved_open_slots_per_scenario <= 2
one-shot batch ASK only
```

每个 slot 都有 `schema_domain`、由静态可见约束筛出的 `context_admissible_values`、`owner` 和 canonical semantic link。空 domain 是显式失败或 `HARD_UNSAT` 的输入，不得被默认值修复。

### 5.1 Joint completion

即使最多只有两个 unresolved slots，runtime 也必须枚举满足类型和跨 slot constraints 的 joint completions `Omega`。核心语义不得退化为两个独立 per-slot choices。

对于 USER projection `P_U` 和给定 executor assignment 的 USER fiber `F_U(e)`：

- 无需 ASK 的 action 必须对 `P_U` 中所有 user completions 安全；
- executor assignment 只有在 `F_U(e) = P_U` 且两者非空时才保持用户 coverage；
- 空 fiber 不能产生 vacuous EXECUTE 或 REJECT；
- 多个 executor slots 必须联合解析并完整记录。

### 5.2 One-shot ASK 与 minimum sufficient information

当没有跨全部 legal user completions 的共同安全 decision 时，runtime 穷举 USER-owned slot subsets。合法 query set 必须使每个可行回答都能在剩余 uncertainty 下导向一个安全 `EXECUTE` 或确定的 `REJECT`。

对于冻结 fixtures，选择 cardinality 最小的 sufficient set；并列时按 canonical slot-link order 决定。`ASK([])` 非法。Phase 0 不实现自适应多轮问答或通用 query planner。

## 6. Blocking fixture catalog

所有 fixtures 都是手写/gold、有限且可穷举。expected mappings 仅供 adapter、elaborator、runtime 和 trace tests 使用，不得暴露为 normal A/B/C path 的可调用 lookup。

### F1：`OPEN_UU_COUPLED_MIN_ASK`

- 两个 USER slots：`output_format in {JSON,YAML}`、`strictness in {STRICT,LENIENT}`；
- cross-slot constraint 只允许 `(JSON,STRICT)` 和 `(YAML,LENIENT)`；
- 两个 legal pairs 对应不同安全 actions；初始状态没有共同安全 action；
- 询问任一 slot 都能唯一确定另一 slot，canonical tie-break 要求只 ASK `output_format`；
- 预期：one-shot `ASK` 只含一个 link，不得逐 slot 独立求解或询问两个 slots。

### F2：`OPEN_UE_OWNER_BOUNDARY`

- USER slot：`error_policy in {RETURN_NONE,RAISE}`；
- EXECUTOR slot：`log_mode in {QUIET,VERBOSE}`；
- cross-slot constraint 只允许 `(RETURN_NONE,QUIET)` 和 `(RAISE,VERBOSE)`；
- 任一提前固定的 executor value 都会排除一个 legal USER completion；
- 预期：初始状态 ASK `error_policy`，不能由 executor 替用户选择；注入用户回答后的 resolved companion fixture 才能记录匹配的 executor resolution 并 EXECUTE。

### F3：`EXECUTOR_COVERAGE_NONVACUOUS`

- USER slot：`service_mode in {SAFE,FAST}`；
- EXECUTOR slot：`backend in {LOCAL,REMOTE}`；
- legal pairs 为 `(SAFE,LOCAL)`、`(FAST,LOCAL)`、`(FAST,REMOTE)`；
- `REMOTE` 的 USER fiber 只含 `FAST`，因而不能用它缩小用户选择；`LOCAL` 覆盖全部 USER projection；
- 一个 local action 对两个 USER completions 都安全；
- 预期：无需 ASK，选择 `LOCAL`，先输出 executor resolution trace，再 EXECUTE；任何基于空/narrow fiber 的成功均失败测试。

### F4：`EXECUTOR_JOINT_TRACE`

- 两个 EXECUTOR slots 具有 coupled legal pairs；
- 只有一个 joint pair 支持安全 action；
- 预期：在 action 前以 canonical order 记录两个 resolutions，不能逐 slot 贪心或漏记一个值。

### F5：`AUTHORITY_ROLE_COUNTERFACTUAL`

- 相同 normative text 分别来自 USER、ASSISTANT 和 TOOL；
- 只有原始 USER support 产生 `authority=USER` 和 active clause；
- USER clause 内的 EXECUTOR-owned OPEN 不提升 executor 的 normative authority。

### F6：`HARD_UNSAT_WITNESS`

- 两个 active clauses 对同一 finite enum 要求互斥值；
- 预期：`REJECT(HARD_UNSAT)` 和最小 canonical clause-link witness；不得继续 action tie-break。

### F7：`NO_AUTHORIZED_ACTION_WITNESS`

- 至少一个 candidate action 满足 hard clauses，但每个 hard-valid action 都包含未被 `ALLOW` 授权的 managed effect；
- 预期：`REJECT(NO_AUTHORIZED_ACTION)`，并列出被排除 action/effect；不得标成逻辑冲突。

### F8：`NO_SILENT_INVALID_EXECUTION`

- 输入包含 dangling support ref、wrong enum type 或缺失 adapter link；
- 预期：在对应 stage 显式失败，runtime 不执行任何 action，不使用空 Contract 或默认 slot value。

除上述 blocking fixtures 外，可增加少量 modality coverage cases，确保 `GOAL`、`REQUIRE`、`PRESERVE`、`FORBID` 和 `ALLOW` 至少各有一个区分性结果，但不扩展为数据研究。

## 7. 两条不同的 gold debug path

### 7.1 Gold C content 进入同一个真实 bridge

第一条 debug path 将 fixture 标注的 gold `ExtractiveContentState` 送入 normal C 所用的同一个 `beta_C`：

```text
Gold ExtractiveContentState
-> same real beta_C
-> CanonicalSemanticState
-> Elaborate
-> Runtime
```

它只用于区分 content selection failure 与 bridge/content interpretation failure。它不替换 bridge，不提供 gold canonical output，也不是独立 experimental condition。

### 7.2 Gold canonical semantics 绕过 bridge

第二条 debug path 从 gold `CanonicalSemanticState` 直接进入共同后端：

```text
Gold CanonicalSemanticState
-> Elaborate
-> Runtime
```

它用于 integration-test elaborator、OPEN oracle、authority、executor resolution、decision 和 result。它不经过 C bridge，因此不能诊断 C 的 content interpretation。

两条 debug paths 用途不同，结果必须分别标记。fixture expected mappings 只能由测试 harness 读取；normal A/B/C entry point 的依赖图中不得出现 gold fixture module。

## 8. 有界结构化 trace

每个 scenario 只写一条 bounded trace record。最小 schema 为：

```yaml
ScenarioTrace:
  scenario_id: fixture_or_run_id
  input_ref: source_or_artifact_ref
  arm: A | B | C | GOLD_C_DEBUG | GOLD_CANONICAL_DEBUG
  stages:
    - stage: surface | adapter_or_bridge | elaboration | runtime | execution
      input_ref: bounded_artifact_ref
      output_ref: bounded_artifact_ref | null
      failure_reason: stable_reason_code | null
  final_outcome: DECISION | SYSTEM_FAILURE
  final_decision: EXECUTE | ASK | REJECT | NOT_PRODUCED
  result_ref: bounded_artifact_ref | null
  ask_links: [SlotSemanticLink, ...]
  executor_resolutions: [ResolutionTrace, ...]
  reject_reason: HARD_UNSAT | NO_AUTHORIZED_ACTION | null
  reject_witness_ref: bounded_artifact_ref | null
```

大对象写为固定 artifact reference，trace 本身不复制任意 source/model output。每个 stage 必须明确输入、输出或失败原因。失败后立即停止；不得 silent fallback、default insertion、隐藏 retry 或将一种 arm 的失败转送另一 arm。若未来 smoke test 允许 retry，必须在独立 smoke 配置中显式计数，不能改变确定性主路径。

## 9. 实现顺序

### Stage E0：冻结 dialect 与 fixtures

- 定义 finite sorts、enum domains、predicate signatures、actions、effects 和 managed-effect policy；
- 将 F1-F8 编码为 hand-authored fixtures；
- 为每个 fixture 穷举 joint completions、expected decision 和 witness；
- 验证 unresolved OPEN 数量上限和 cross-slot coverage。

### Stage E1：共同语义、elaborator 与 runtime

- 实现 canonical types、authority gate 和 deterministic elaborator；
- 实现 joint completion、executor coverage、minimum sufficient ASK 和 closed decision；
- 先跑 gold canonical debug path，直到所有 backend blocking fixtures 闭合。

### Stage E2：A 与 B typed paths

- 实现两个最小 surface schemas 和 `alpha_A`/`alpha_B`；
- 添加 gold round-trip、canonical parity、decision parity 和 malformed-input tests；
- 记录 A/B encoding 的清晰度、重复逻辑和维护成本，不另建实验系统。

### Stage E3：C real bridge path

- 实现共同 segmenter、固定 normal C extractor、extractive content schema、ref validation 和唯一 `beta_C`；
- 先以 Gold C content debug path 验证同一 bridge，再运行 normal non-gold C extraction；
- 保持 bridge failure 与 elaboration/runtime failure 可区分。

### Stage E4：端到端 trace 与负例

- 对三臂和两条 debug paths 生成相同 schema 的 trace；
- 验证失败立即停止、artifact refs 可检查、decision 与 result 一致；
- 专门运行 F8，确认任何 invalid state 都不会静默执行。

## 10. 工程 exit 与 stop/revise checklist

Phase 0 可以退出并建议继续工作，仅当以下项目全部为真：

- [ ] gold typed path 从 canonical semantics 到 elaboration、runtime、decision 和 result 完整闭合；
- [ ] A/B gold inputs 经各自确定性 adapter 得到相同 canonical semantics 和后端结果；
- [ ] F1-F8 所有 blocking fixtures 通过；
- [ ] USER ASK、minimum sufficient information、executor coverage 和 resolution trace 行为正确；
- [ ] 每个失败都能从 bounded trace 定位到 stage 和 stable reason；
- [ ] 同一个真实、非 gold `beta_C` 至少在一条 normal C path 上产生一个合理成功结果；
- [ ] gold C debug 与 gold canonical debug 能分别定位 extraction/bridge 和 backend integration 问题；
- [ ] 不存在 silent invalid execution、默认值掩盖、隐藏 retry 或 gold lookup 泄漏；
- [ ] 实现与记录满足 Git/provenance 规则。

以下任一情况应停止扩展并 revise 设计：

- Contract IR 无法表达任一 blocking fixture，而不是仅有实现 bug；
- 在最多两个有限 enum OPEN slots 时，joint completion、ASK 或 trace 已复杂到无法可靠解释和测试；
- 唯一真实 C bridge 无法产生任何合理路径，且 trace 不能区分 content、bridge 与 backend failure；
- trace 对关键错误不可读，或需要 silent fallback 才能让主路径继续；
- A/B 为维持 parity 需要隐藏 arm-specific semantics。

该 checklist 是工程退出条件，不是统计 truth table，也不授权将通过结果写成一般科学结论。

## 11. Optional LM smoke test

只有 deterministic E0-E4 完成后，才可运行一个可选的 frozen LM interface smoke test。输入使用同一 gold canonical semantics 的 A/B serialization、相同 world view 和相同 closed Decision output schema。

smoke test 只检查 harness 是否大致能消费 modality、OPEN owner、authority 和 decision fields。它不能阻断 Phase 0 工程退出，失败只记录为当前 LM/harness 的问题；成功也不支持 deployment claim。Predicted compiler、bridge training 或大规模模型对比不属于该 smoke test。

## 12. 延后工作

以下工作明确延后到 Phase 0 工程退出之后，且不得为了“完善”本计划而提前加入：

- RQ3a 式 coverage/data-method studies 和所有 mutation-method comparisons；
- learned compiler/bridge training campaigns 与 teacher-generated corpus；
- independent human confirmatory sets；
- 正式统计检验体系、不确定性区间或边际阈值规则；
- claim matrices、root-cause attribution protocol 或 distribution-shift infrastructure；
- field-renaming studies、模型规模研究和多领域 benchmark；
- repository grounding、real patches、Lean、SWE-bench、动态 C/K/P、RL 和复杂 multi-agent。

后续研究可以复用 Phase 0 的 canonical contracts、fixtures 和 traces，但必须另写范围、数据、比较和接受协议。

## 13. Git 与 provenance 规则

- 所有可复现实现在 milestone branch 上完成；
- 记录性运行只从 committed source 和 clean worktree 启动；
- run manifest 记录 exact source commit、fixture/config paths、launcher 和 fixed output root；
- fixtures、schemas、adapters、bridge config、runtime 和 tests 由 Git commit 绑定，不维护平行 source hash；
- 只有 Git 外 evidence（例如外部 dataset、未提交固定 split、model weights 或 run artifacts）才记录 path 和 checksum；
- 任何能影响记录性运行的 untracked/ignored input 必须先提交，或在 manifest 中以 path 和 checksum 明确绑定；
- debug path、normal path 和 optional smoke test 的 artifact roots 必须分开，避免把调试输出误当 normal C 结果。

本计划是 Phase 0 的唯一权威工程入口。实现发现语义 contract 需要修改时，应先修改本计划和对应 fixtures，再修改代码；不得用运行时 fallback 隐式改变 contract。
