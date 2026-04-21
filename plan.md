# LootCode Completion Plan (Submission-Ready)

## Objective
Bring the project from current partial completion to a clean, fully working, submission-ready state:
- All compiler phases working end-to-end.
- No failing tests.
- No stale/dead code paths.
- Consistent documentation and naming.
- Deterministic validation workflow for final submission.

---

## Phase 1 - Stabilize Baseline and Define Targets

Status: Completed on 2026-04-21 (see PHASE_1_BASELINE_REPORT.md)

### Goals
- Lock current state and reproduce all known failures.
- Establish exact acceptance criteria for completion.

### Tasks
1. Create a baseline report from current branch:
   - Run full test suite and capture failing cases.
   - Run all standalone validation scripts.
2. Build a failure matrix:
   - Parser failures (unit-bearing expressions, reserved-word collisions).
   - Runtime failures (string-number arithmetic in code generator).
   - Optimization coverage mismatches (old op names vs current TAC ops).
3. Define completion criteria:
   - 100% pass on all automated tests.
   - No syntax/semantic/runtime regressions on sample programs.
   - No obsolete operation names in active code paths.

### Exit Criteria
- A single baseline status document exists with failing tests and root causes.
- Team agrees on what “done” means for submission.

---

## Phase 2 - Parser and Lexer Correctness Fixes

Status: Completed on 2026-04-21 (parser/lexer fixes validated; see PHASE_2_COMPLETION.md)

### Goals
Fix all front-end language issues preventing valid programs from compiling.

### Tasks
1. Resolve keyword/identifier collision strategy:
   - Allow practical identifiers like `gold` when used in declaration/assignment contexts, or adjust token model to distinguish unit keywords from identifiers contextually.
2. Fix unit-aware expression parsing:
   - Support expressions like `health = 50 hp + 50 hp;` and `x = x + 1 qty;`.
   - Ensure consistent AST shape for literals with units inside arithmetic.
3. Validate grammar consistency:
   - Ensure parser supports all intended language constructs from proposal/spec.
4. Update/align parser tests:
   - Add focused tests for unit + arithmetic combinations.
   - Add tests for reserved-word identifier edge cases.

### Exit Criteria
- All previously failing parse cases pass.
- No parser regressions in existing passing tests.

---

## Phase 3 - Semantic and Runtime Type/Unit Safety

Status: Completed on 2026-04-21 (semantic/runtime fixes validated; see PHASE_3_COMPLETION.md)

### Goals
Make semantic analysis and execution robust for typed/unit values.

### Tasks
1. Fix semantic analyzer inconsistencies:
   - Replace invalid token references (e.g., non-existent token variants).
   - Standardize declared type/unit handling for input and declarations.
2. Implement unit-safe arithmetic model in runtime:
   - Normalize internal value representation (e.g., structured numeric + unit, not fragile strings).
   - Enforce compatibility rules for add/sub/mul/div and comparisons.
   - Provide clear runtime errors for invalid unit operations.
3. Verify loop/conditional behavior with updated value model.
4. Add regression tests for runtime arithmetic failures seen in nested/combat/full-game scenarios.

### Exit Criteria
- Runtime errors from mixed string/int arithmetic are eliminated.
- Complex scenarios (nested control, combat, full game) execute successfully.

---

## Phase 4 - TAC and Optimizer Alignment

Status: Completed on 2026-04-21 (optimizer alignment validated; see PHASE_4_COMPLETION.md)

### Goals
Ensure intermediate representation and optimizer are fully aligned and effective.

### Tasks
1. Remove stale operation-name assumptions in optimizer:
   - Replace legacy names with current TAC vocabulary.
2. Improve optimization correctness with units:
   - Constant folding only when safe with unit semantics.
   - Constant propagation and dead-code elimination without altering behavior.
3. Add optimizer verification tests:
   - Confirm optimization does not change output semantics.
   - Confirm optimization actually triggers on valid opportunities.
4. Produce before/after TAC samples for key programs.

### Exit Criteria
- Optimizer uses only valid current TAC ops.
- Optimization tests pass and preserve behavior.

---

## Phase 5 - CLI, Integration, and End-to-End Validation

Status: Completed on 2026-04-21 (CLI/integration validated; see PHASE_5_COMPLETION.md)

### Goals
Make developer/user experience complete and reliable for grading/demo.

### Tasks
1. Verify all CLI modes work as specified:
   - Compile/run file.
   - Debug/TAC output.
   - TAC file output.
   - Interactive mode.
2. Add integration tests for CLI behavior and error handling.
3. Ensure deterministic outputs where feasible for grading.
4. Confirm all test assets (including dungeon and advanced cases) are wired into canonical test runner.

### Exit Criteria
- Full test suite is green.
- CLI features are verified with command examples and expected output.

---

## Phase 6 - Codebase Cleanup and Submission Hardening

Status: Completed on 2026-04-21 (cleanup and final gates complete; see PHASE_6_COMPLETION.md)

### Goals
Deliver a clean, professional, maintainable codebase ready for submission.

### Tasks
1. Dead code cleanup:
   - Remove unused methods/imports/branches.
   - Remove obsolete comments and legacy vocabulary remnants.
2. Documentation synchronization:
   - Align README, language spec, and reports with final LootCode behavior.
3. Quality gates:
   - Run syntax checks, linting (if configured), and full tests one final time.
4. Submission packaging:
   - Confirm required deliverables and file structure.

### Exit Criteria
- No dead/obsolete active code paths.
- No failing tests.
- Documentation reflects actual implementation.
- Project is ready for demo and submission.

---

## Suggested Execution Order and Timeboxing

1. Phase 1: 0.5 day
2. Phase 2: 1-2 days
3. Phase 3: 1-2 days
4. Phase 4: 1 day
5. Phase 5: 0.5-1 day
6. Phase 6: 0.5-1 day

Total estimated remaining effort: ~4.5 to 7.5 focused days.

---

## Definition of Done (Final)

The project is complete when all of the following are true:
1. All automated tests pass with no known intermittent failures.
2. All compiler phases function correctly on provided language features.
3. No known dead code or legacy/stale operation paths remain.
4. CLI and integration flows work end-to-end.
5. Documentation and examples are accurate and executable.
6. Repository is clean and submission artifacts are ready.
