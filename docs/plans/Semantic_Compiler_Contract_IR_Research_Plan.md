# Research Plan: Semantic Compiler for Reliable AI Agents

> Historical roadmap: its Phase 1-3 sequence is not current execution authority. The controlled-code Phase 1 branch is paused before C1, and current work is governed only after acceptance of the [Contract IR Kernel and Coding Plugin Research Plan](Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md).

## Proposed Title

**Semantic Compiler: Learning a Contract-Based Intermediate
Representation for Reliable AI Execution**

Alternative titles:

1.  **From Natural Language Intent to Executable Semantics: A Contract
    IR Framework for Reliable AI Agents**
2.  **Semantic Bottlenecks for AI Agents: Learning Domain-Agnostic
    Contract Representations from Language**
3.  **Contract IR: A Universal Semantic Interface Between Human Intent
    and AI Execution**
4.  **Semantic Compilation for AI Agents: From Free-Form Instructions to
    Verified Execution**

------------------------------------------------------------------------

# 1. Research Motivation

Current Large Language Model agents are powerful but unreliable. A major
reason is that natural language is a high-entropy communication medium:

-   the same intent can have many expressions;
-   important constraints are often implicit;
-   ambiguity is easily hidden;
-   models may confidently execute unintended interpretations.

For reliable AI systems, the goal should not simply be improving model
capability, but transforming probabilistic language models into systems
whose behavior approaches a reliable software component.

The central hypothesis of this research is:

> Human intent expressed in natural language can be compiled into a
> compact, structured, and refinable semantic representation. This
> intermediate representation can serve as a reliable interface between
> language models and execution systems.

The proposed approach introduces a Contract Intermediate Representation
(Contract IR) as a semantic bottleneck between human instructions and AI
execution.

------------------------------------------------------------------------

# 2. Core Research Question

Can a domain-independent semantic compiler transform free-form natural
language instructions into structured intermediate representations that
improve:

-   behavioral consistency;
-   ambiguity detection;
-   clarification decisions;
-   execution reliability;
-   small-model performance?

Formally:

Given:

-   natural language intent H;
-   IR definition D;
-   domain environment E;

learn:

F(H, D, E) → IR

such that the generated IR:

1.  preserves user intent;
2.  explicitly represents uncertainty;
3.  enables reliable downstream execution.

------------------------------------------------------------------------

# 3. Key Hypotheses

## H1: Semantic Bottleneck Hypothesis

Natural language contains many irrelevant degrees of freedom.

A structured IR can remove linguistic variation while preserving
execution-relevant semantics.

Expected result:

NL → IR → Execution

should outperform:

NL → Execution

in:

-   consistency;
-   robustness;
-   token efficiency.

------------------------------------------------------------------------

## H2: Semantic Denoising Hypothesis

A valid IR can be used to generate diverse natural language descriptions
through teacher models:

IR → Natural Language

The reverse task:

Natural Language → IR

is analogous to denoising latent semantic structures from noisy
observations.

This enables scalable synthetic training data generation.

------------------------------------------------------------------------

## H3: Hierarchical Representation Hypothesis

A multi-level IR is superior to a single-level representation.

Proposed hierarchy:

Natural Language

↓

Intent IR

↓

Domain IR

↓

Execution IR

↓

Actions

Different abstraction levels support different reasoning and
verification mechanisms.

------------------------------------------------------------------------

## H4: Representation Reduces Model Size Requirement

Explicit semantic structure can compensate for model capacity.

A smaller model receiving Contract IR should approach the performance of
a larger model directly interpreting natural language.

------------------------------------------------------------------------

# 4. Conceptual Framework

## 4.1 Contract IR

Core primitives:

-   GOAL
-   REQUIRE
-   PRESERVE
-   FORBID
-   ALLOW
-   ASSUME
-   OPEN
-   VERIFY
-   ESCALATE

The IR should not only represent known information but also preserve
unknowns.

Example:

Bad:

    Invalid input must raise ValueError

when the user never specified this.

Better:

    OPEN:
      invalid_input_behavior
      alternatives:
        - return_none
        - raise_error
      owner:
        USER

------------------------------------------------------------------------

## 4.2 Hierarchical IR

### Level 1: Intent IR

Represents user goals and constraints.

Example:

    GOAL:
      Fix configuration handling

    PRESERVE:
      Existing valid behavior

    FORBID:
      Public API changes

------------------------------------------------------------------------

### Level 2: Domain IR

Adds domain concepts.

Coding:

    TARGET:
      ConfigParser

    PROPERTY:
      malformed_config_behavior

Lean:

    GOAL:
      theorem_proof

    REQUIRE:
      kernel_verified

------------------------------------------------------------------------

### Level 3: Execution IR

Represents concrete operations.

Coding:

    INSPECT:
      parser.py

    MODIFY:
      parse_config()

    VERIFY:
      regression_test

------------------------------------------------------------------------

# 5. Training Strategy

## Stage 1: Synthetic Semantic Diffusion

Generate training data:

Valid IR

↓

Teacher LM

↓

Multiple natural language descriptions

↓

Student LM training

The generated language should include:

-   paraphrases;
-   concise descriptions;
-   verbose descriptions;
-   ambiguous descriptions;
-   incomplete descriptions;
-   contradictory descriptions.

The goal is to train:

NL → IR

rather than memorizing specific phrasing.

------------------------------------------------------------------------

## Stage 2: IR Recovery Evaluation

Measure:

### Exact semantic recovery

Does predicted IR match the original?

### Behavioral equivalence

Do two different NL descriptions produce equivalent execution
constraints?

### Ambiguity detection

Does the model preserve unresolved decisions?

### Robustness

Does paraphrasing change the generated IR?

------------------------------------------------------------------------

## Stage 3: Domain Adaptation

Implement multiple IR dialects.

Initial domains:

1.  Software engineering
2.  Lean theorem proving

Future domains:

-   SQL/data analysis;
-   scientific workflows;
-   robotics;
-   quantitative research.

------------------------------------------------------------------------

# 6. Experimental Roadmap

## Phase 0: Toy Semantic Compiler

Goal:

Decide whether the Contract IR idea is worth further engineering work. Phase 0 is
a finite engineering exploration, not a publication-grade evaluation.

Tasks:

-   implement a minimal A/B/C topology that converges on shared canonical
    semantics, deterministic elaboration, typed OPEN handling, and a closed
    `EXECUTE | ASK | REJECT` runtime;
-   freeze executable finite-world predicate interpretations/scopes, candidate
    trajectories, managed-effect authorization, and unique invalid/empty-domain
    routes before implementation;
-   keep OPEN to finite enum domains with at most two unresolved slots per
    scenario while testing joint USER/USER and USER/EXECUTOR behavior;
-   exercise the hand-authored F1-F9 blocking fixtures, executor coverage,
    authority, and bounded per-scenario traces;
-   require the real non-gold C bridge to satisfy the exact named
    `C_NORMAL_END_TO_END_EXACT` fixture, including its fixed-reference
    distractor-invariance test, plus separate Gold C and Gold canonical debug
    paths;
-   use an optional frozen-LM interface smoke test only after the deterministic
    path closes.

Engineering exit:

All F1-F9 blocking fixtures and gold typed paths close; ASK/executor behavior is
correct; invalid and empty domains follow their unique frozen routes; failures
are inspectable; the real C bridge exactly matches
`C_NORMAL_END_TO_END_EXACT`; and no invalid state can execute silently. Stop
and revise if the IR is unexpressive, the two-slot semantics are already
excessively complex, or the exact C fixture/trace contract cannot be met.

The authoritative scope, topology, fixtures, debug paths, exit checklist, and
provenance rules are defined in
[`IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md`](../../Phase0/IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md). Repository
grounding, real patches, Lean/SWE-bench, dynamic C/K/P, RL, model scaling,
complex multi-agent work, mutation/data studies, training campaigns, and
publication claims are deferred.

------------------------------------------------------------------------

## Phase 1: Coding Contract IR

Build:

-   Coding dialect;
-   repository grounding;
-   execution verifier.

Evaluation:

-   SWE-bench subsets;
-   controlled coding tasks;
-   contract violation tests.

Metrics:

-   task success;
-   silent deviation rate;
-   clarification accuracy;
-   execution consistency.

------------------------------------------------------------------------

## Phase 2: Lean Contract IR

Build:

-   theorem/proof IR;
-   proof obligation representation;
-   kernel verification.

Evaluation:

-   theorem proving benchmarks;
-   proof correctness;
-   ambiguity handling.

------------------------------------------------------------------------

## Phase 3: Reliable Local Agent

Integrate:

-   open-weight model;
-   24GB inference;
-   Contract IR;
-   execution runtime;
-   verifier.

Goal:

A local model that:

-   executes clear tasks;
-   asks meaningful questions;
-   escalates when needed;
-   produces evidence-backed completion reports.

------------------------------------------------------------------------

# 7. Evaluation Metrics

Traditional benchmark scores are insufficient.

Important metrics:

## Reliability

P(valid completion \| accepted task)

## Coverage

P(task accepted)

## Silent Divergence Rate

Cases where the model claims completion but violates intent.

## Clarification Quality

-   necessary questions asked;
-   unnecessary questions avoided.

## Semantic Stability

Equivalent instructions should produce equivalent behavior.

## Efficiency

-   tokens;
-   latency;
-   GPU cost.

------------------------------------------------------------------------

# 8. Theoretical Connections

This research connects several fields:

## Compiler Design

Natural language → IR → execution

Inspired by:

-   LLVM IR;
-   MLIR;
-   progressive lowering.

## Formal Methods

Inspired by:

-   refinement types;
-   abstract interpretation;
-   specification languages.

## Machine Learning

Inspired by:

-   denoising autoencoders;
-   diffusion models;
-   self-supervised learning;
-   representation learning.

## AI Agents

Provides a semantic interface between:

-   human intent;
-   language models;
-   deterministic verification systems.

------------------------------------------------------------------------

# 9. Expected Contributions

A successful project could contribute:

1.  A general Contract IR framework.
2.  A semantic compiler architecture independent of domains.
3.  A synthetic training methodology based on IR-to-language generation.
4.  A benchmark for intent preservation and reliable execution.
5.  Open-source local AI agents with improved behavioral reliability.

------------------------------------------------------------------------

# 10. Long-Term Vision

The long-term goal is not to build a larger language model.

It is to build a semantic compilation layer:

Human Intent

↓

Semantic IR

↓

AI Backend

↓

Verified Execution

Similar to how modern software systems separate:

Programming Language

↓

Compiler Intermediate Representation

↓

Machine Execution

Future AI systems may require an equivalent semantic infrastructure
layer between humans and intelligent machines.
