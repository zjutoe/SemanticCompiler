# Contract IR v0 Phase 0 Final Revision Recommendations for Codex

## 总体判断

当前 Phase 0
协议已经达到可以冻结实验设计的水平。本轮只提出最后冻结前的修改建议，不建议继续扩展研究范围。

主要建议：

1.  删除 Phase 0 中 EXPLICITLY_DELEGATED authority。
2.  降低 OPEN 实现范围，但保留理论形式。
3.  增加 ContentMatchedJSON Oracle + Perfect Bridge 上界。
4.  将 RQ3b（mutation method superiority）移出 Phase 0。
5.  将 frozen LM executor 从科学 continuation gate 调整为 optional
    engineering validation。

------------------------------------------------------------------------

# 1. Authority 简化

当前：

    USER | EXPLICITLY_DELEGATED | NONE

建议：

    USER | NONE

原因：

Delegation 属于 permission/governance 层，需要研究 delegation
scope、revocation、inheritance 等问题。

Phase 0 的问题只是：

> 模型是否能区分用户规范性要求和非规范性信息？

因此不需要引入 delegated authority。

------------------------------------------------------------------------

# 2. OPEN 实现范围限制

当前 OPEN 理论设计非常完整：

-   joint completion；
-   USER/EXECUTOR ownership；
-   fiber；
-   sufficient query set。

建议理论保留，但实现限制：

    max_open_slots <= 2
    finite enum domain only
    no cross-slot constraints

原因：

Phase 0 目标是验证 typed OPEN 的价值，而不是解决完整 partial-information
planning。

------------------------------------------------------------------------

# 3. 增加 Oracle ContentMatchedJSON

当前 C：

    ContentMatchedUntypedJSON
            |
            v
    learned bridge
            |
            v
    CanonicalSemanticState

C 失败可能来自：

1.  untyped representation 不足；
2.  bridge 学习失败。

因此增加：

    Oracle ContentMatchedJSON
    +
    Perfect Bridge

作为理论上界。

结果解释：

  结果                           解释
  ------------------------------ ---------------------------------
  Oracle C 失败                  untyped representation 本身不足
  Oracle C 成功，Learned C失败   bridge/compiler问题
  两者都失败                     typed semantics可能必要

------------------------------------------------------------------------

# 4. RQ3b 移出 Phase 0

RQ3a：

> mutation-enriched data 是否优于 paraphrase-only data？

应保留。

RQ3b：

> programmatic mutation 是否优于 teacher-direct difficult-example
> generation？

建议作为后续研究。

原因：

RQ3b 本身涉及：

-   generation cost；
-   diversity；
-   fidelity；
-   coverage；
-   teacher bias。

足以形成独立研究。

------------------------------------------------------------------------

# 5. Gate 5 调整

Frozen LM executor 失败不应自动否定 IR。

建议：

Gate 5 改为：

    Optional Deployment Validation

而不是科学 continuation gate。

原因：

LM failure 可能来自：

-   prompt；
-   harness；
-   instruction following；
-   model alignment。

Gate 1-4 判断科学有效性。

Gate 5 判断工程可用性。

------------------------------------------------------------------------

# 6. Baseline 命名

SemanticIsomorphicJSON 不应继续称为 generic JSON。

建议名称：

    Semantic-Isomorphic Control Representation

因为它已经包含：

-   proposition；
-   OPEN；
-   authority；
-   provenance；
-   typed predicate。

它测试的是 encoding/factorization，而不是普通 JSON。

------------------------------------------------------------------------

# 7. C 实验增加错误归因

必须分别报告：

    Content extraction error
    Bridge error
    Elaboration error
    Runtime error

否则无法判断 C 的失败来源。

------------------------------------------------------------------------

# 8. 不再扩展 Phase 0

当前 Phase 0 已足够复杂。

暂不加入：

-   C/K/P lowering；
-   repository grounding；
-   Lean；
-   SWE-bench；
-   multi-agent；
-   RL；
-   model scaling。

推荐路线：

    Semantic kernel
          |
          v
    Exhaustive oracle
          |
          v
    Human gold
          |
          v
    Compiler/data
          |
          v
    Deterministic runtime

------------------------------------------------------------------------

# 最终冻结建议

完成以下五项后冻结：

1.  authority 改为 USER/NONE；
2.  OPEN 实现限制；
3.  增加 Oracle C + Perfect Bridge；
4.  RQ3b 移至 future work；
5.  Gate 5 改为 optional engineering validation。

之后进入实现：

-   semantic kernel；
-   reference interpreter；
-   property tests；
-   exhaustive toy-world validation。
