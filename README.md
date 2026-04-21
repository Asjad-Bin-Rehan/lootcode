# LootCode Compiler

LootCode is a small domain-specific language (DSL) for text adventure style scripting.
This repository contains a full compiler pipeline implemented in Python:

1. Lexer
2. Parser
3. Semantic analyzer
4. TAC generator
5. Optimizer
6. TAC execution engine

## Requirements

- Python 3.8+

## Quick Start

Run a program:

```powershell
python adventurescript.py tests\01_simple_adventure.adv
```

Run with phase/debug output:

```powershell
python adventurescript.py tests\01_simple_adventure.adv --debug
```

Write TAC to file:

```powershell
python adventurescript.py tests\01_simple_adventure.adv -o output.tac
```

Interactive mode:

```powershell
python adventurescript.py --interactive
```

## Run Tests

Canonical suite:

```powershell
python tests\run_all_tests.py
```

CLI integration checks:

```powershell
python test_cli_phase5.py
```

Optimizer checks:

```powershell
python test_optimizer_phase4.py
```

## Input and Output

Input:
- A `.adv` text file containing LootCode statements.
- Or line-by-line statements in interactive mode.

Output:
- Narrative and operation messages printed to terminal.
- Optional TAC file when `-o` is used.
- Success or error status messages.

## Project Layout

```text
adventurescript.py          Entry point
src/                        Compiler and runtime phases
tests/                      Adventure test programs and test runner
```

## Notes

- Use `python` or `py` depending on your Windows setup.
- Test runner is path-safe and can be invoked from repository root.
