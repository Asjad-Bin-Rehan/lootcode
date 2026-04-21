# Phase 1 Baseline Report

Date: 2026-04-21
Repository: lootcode
Baseline branch: initial-code

## 1) Scope of Phase 1
This report implements Phase 1 from [plan.md](plan.md):
1. Reproduce current failures.
2. Build a failure matrix with root causes.
3. Define completion/acceptance criteria for project completion.

## 2) Commands Executed

### Branch and environment
1. git branch --show-current

Result:
- Active branch: initial-code

### Full compiler test suite
1. From project root: python tests/run_all_tests.py
- This invocation reported missing test files due working-directory assumptions in the runner.
2. From tests directory: python run_all_tests.py
- This is the valid baseline invocation for the current runner behavior.

Result (valid invocation):
- Total tests: 12
- Passed: 6
- Failed: 6

Passing tests:
1. 01_simple_adventure.adv
2. 03_simple_loop.adv
3. 04_conditional.adv
4. 05_combine_items.adv
5. 06_equip_stats.adv
6. 07_rest_operation.adv

Failing tests:
1. 02_basic_arithmetic.adv
2. 08_nested_control.adv
3. 09_combat_scenario.adv
4. 10_inventory.adv
5. 11_full_game.adv
6. 12_optimization.adv

### Standalone validation scripts
1. python structural_integrity_test.py
2. python test_lexer_sanity.py
3. python test_parser_phase2.py
4. python test_semantic_phase3.py
5. python comprehensive_lexer_test.py
6. python validate_syntax.py

Results:
- PASS: structural_integrity_test.py
- PASS: test_lexer_sanity.py
- FAIL (partial): test_parser_phase2.py
- PASS: test_semantic_phase3.py
- PASS: comprehensive_lexer_test.py
- PASS: validate_syntax.py

## 3) Failure Matrix

### A) Parser/Lexer-level failures
1. 02_basic_arithmetic.adv
- Error: Syntax Error at line 4: Expected TokenType.IDENTIFIER, got TokenType.GOLD
- Likely cause: reserved keyword/unit token collision for identifier names such as gold.

2. 10_inventory.adv
- Error: Syntax Error at line 6: Expected TokenType.IDENTIFIER, got TokenType.GOLD
- Likely cause: same collision as above.

3. 12_optimization.adv
- Error: Syntax Error at line 9: Expected TokenType.SEMICOLON, got TokenType.PLUS
- Likely cause: parser does not accept arithmetic forms where unit-annotated values appear around operators (for example 50 hp + 50 hp).

### B) Runtime/value-model failures
1. 08_nested_control.adv
- Error: can only concatenate str (not "int") to str
- Likely cause: arithmetic performed on mixed string and numeric representations of unit values.

2. 09_combat_scenario.adv
- Error: unsupported operand type(s) for -: 'str' and 'int'
- Likely cause: subtraction on unit-carrying values stored as strings.

3. 11_full_game.adv
- Error: can only concatenate str (not "int") to str
- Likely cause: same mixed representation issue in runtime arithmetic.

### C) Additional script-level inconsistency
1. test_parser_phase2.py
- Error: Program object has no attribute quests
- Likely cause: test expects ast.quests while parser model currently uses ast.recipes.

## 4) Baseline Assessment

Current project status on initial-code:
1. Compiler pipeline exists end-to-end and executes simple programs.
2. Core sanity/structure checks pass.
3. Functional completeness is partial:
- 6/12 canonical adventure tests passing.
- Major remaining gaps in unit-aware parsing and runtime arithmetic semantics.

## 5) Completion Criteria (Project-Level)
The project is considered complete only when all checks below pass on the target submission branch.

### Mandatory quality gates
1. Full test suite in [tests/run_all_tests.py](tests/run_all_tests.py): 12/12 pass.
2. Standalone validation scripts: all pass.
3. No known parser collisions between practical identifiers and reserved unit keywords.
4. Unit-aware arithmetic works in declarations, assignments, conditionals, loops, and optimizer paths.
5. No runtime type errors in nested/combat/full-game scenarios.
6. No stale operation-name paths in active optimizer/execution behavior.
7. Docs and examples match actual implemented syntax/behavior.

### Cleanliness gates
1. No obsolete dead code paths used by current language model.
2. No outdated vocabulary remnants in active logic (except archived reports kept intentionally).
3. Repeatable one-command validation procedure documented for graders.

## 6) Phase 1 Exit Status
Phase 1 is complete.

Completed deliverables:
1. Baseline reproduced.
2. Failure matrix documented with concrete failing cases and causes.
3. Completion criteria defined for the remaining phases.

## 7) Next Immediate Step (Phase 2 Start)
Prioritize parser/lexer fixes for:
1. Identifier-keyword collision handling for names like gold.
2. Unit-bearing arithmetic expression grammar support.
3. Parser regression updates to align test expectations with current AST naming.
