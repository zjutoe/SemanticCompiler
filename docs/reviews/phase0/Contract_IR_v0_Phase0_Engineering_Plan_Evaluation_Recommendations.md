> [!CAUTION]
> **STATUS: REVIEW INPUT / NON-AUTHORITATIVE**
>
> 本文件是后续评审意见，不是当前实现授权，其中建议只有在 `main` 明确裁决并写入权威计划或当前阶段 handoff 后才生效。当前 Phase 0 唯一权威入口是
> [`IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md`](../../../Phase0/IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md)。加入本状态块之前，收到的原始正文 SHA-256 为
> `7f5f2fec79da69acb6a63549687f78f65b2958972bdbc69a5eea3173d65c764b`。

# Contract IR v0 Phase 0 工程探索计划评估与修订意见

## 总体评价

当前 Phase 0
工程探索计划是目前版本中最成熟的一版，已经从研究构想进入可执行工程规范。

评分：9.6 / 10。

主要优点：

-   明确 Phase 0 是有限、可穷举、以实现反馈为目标的工程探索；
-   通过 A/B/C 三路径分离 representation、bridge 和 runtime 问题；
-   将 semantic kernel 与 learned semantic compiler 分离；
-   对 OPEN、authority、provenance、runtime decision 建立了可测试
    contract；
-   通过 F1-F9 blocking fixtures 建立 exhaustive validation 基础。

------------------------------------------------------------------------

## 1. Phase 0 定位

当前定位正确。

Phase 0 不应证明：

-   universal semantic compiler；
-   通用 AI agent reliability；
-   SWE-bench 能力；
-   小模型替代大模型。

Phase 0 应验证：

-   semantic kernel 是否合理；
-   runtime contract 是否闭合；
-   representation 是否值得继续研究。

建议保持。

------------------------------------------------------------------------

## 2. A/B/C 三路径设计

当前：

    A: Contract IR
    B: Semantic-isomorphic control
    C: Extractive content path

设计非常好。

A/B 测试：

-   representation；
-   canonicalization；
-   runtime。

C 测试：

-   SourceEnvelope；
-   content extraction；
-   semantic bridge。

避免端到端失败无法归因。

------------------------------------------------------------------------

## 3. A/B 目标表述调整

建议不要描述为：

    encoding superiority

更准确：

    engineering invariant preservation advantage

原因：

Phase 0 测试的是：

-   schema complexity；
-   canonicalization；
-   invariant maintenance；
-   adapter burden。

不是完整的用户体验或长期维护优势。

------------------------------------------------------------------------

## 4. C bridge 定位调整

当前 beta_C 不应被描述为简单 parser。

建议改为：

    controlled-language semantic bridge

职责包括：

-   span interpretation；
-   predicate linking；
-   modality recognition；
-   OPEN extraction。

不需要训练，但不应弱化为字符串解析。

------------------------------------------------------------------------

## 5. 明确 Phase 0 不验证 learned semantic compilation

建议加入：

> Phase 0 validates the semantic substrate required before training
> semantic compilation models. It does not evaluate learned semantic
> compilation.

当前阶段验证的是：

    semantic representation
    +
    deterministic runtime
    +
    minimal bridge

不是：

    LLM learns NL → IR

------------------------------------------------------------------------

## 6. OPEN 实现范围

理论设计保留。

工程实现限制：

    max_open_slots <= 2
    finite enum domains only
    one-shot ASK only
    no complex cross-slot constraints

原因：

Phase 0 目标是验证 typed OPEN，而不是实现完整 uncertainty planner。

------------------------------------------------------------------------

## 7. Fixture 评价

F1-F9 已足够作为 blocking catalog。

尤其：

-   F1：joint OPEN + minimal ASK；
-   F2：USER/EXECUTOR boundary；
-   F3：executor coverage；
-   F6：HARD_UNSAT；
-   F7：NO_AUTHORIZED_ACTION；
-   F9：C normal end-to-end exact path。

建议不要继续增加大量 fixture。

------------------------------------------------------------------------

## 8. 可选增加 F10

Semantic false friend / effect composition。

例如：

    ALLOW change_internal_helper

    FORBID change_public_api

action 同时产生两个 effect。

测试 executor 是否理解 effect composition。

非 blocking。

------------------------------------------------------------------------

## 9. Elaborator

当前设计正确区分：

类型错误：

    elaboration failure

和：

语义不可满足：

    runtime HARD_UNSAT

建议保持。

------------------------------------------------------------------------

## 10. Decision 与 Result

当前：

    Decision:
     EXECUTE
     ASK
     REJECT

与：

    Result

分离。

这是正确设计。

------------------------------------------------------------------------

## 11. 工程规模

当前规模合理：

-   E0：1-2 周；
-   E1：2-4 周；
-   E2：约1周；
-   E3：2-3 周；
-   E4：1-2 周。

总计约 8-12 周。

不要继续增加：

-   modality；
-   domain；
-   benchmark；
-   fixture。

------------------------------------------------------------------------

## 12. 最终修改建议

### 必改 1

明确：

Phase 0 不验证 learned semantic compilation。

### 必改 2

beta_C：

    parser

改为：

    semantic bridge

### 必改 3

A/B：

    encoding superiority

改为：

    engineering invariant preservation advantage

### 建议 4

增加最小成功标准：

    F1-F9 passed

    +

    A/B parity

    +

    F9 C normal path

    +

    trace completeness

    +

    no silent invalid execution

------------------------------------------------------------------------

## 最终判断

当前版本已经达到：

> 停止设计，开始编码。

推荐执行：

    E0
    DialectManifest
    +
    F1-F9 fixtures

    ↓

    E1
    Canonical semantics
    +
    Reference runtime

    ↓

    E2
    A/B parity

    ↓

    E3
    C semantic bridge

    ↓

    E4
    Trace and failure analysis

如果 E0/E1 无法稳定实现，说明 semantic kernel 尚未冻结；如果 E0/E1
成功，则该研究具备进入后续 Semantic Compiler 学习实验的基础。
