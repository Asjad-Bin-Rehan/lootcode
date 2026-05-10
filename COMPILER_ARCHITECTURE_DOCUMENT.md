# LootCode Compiler Architecture

**Date:** May 10, 2026  
**Project:** CS4031 Compiler Construction - LootCode

---

## Overview

LootCode is a domain-specific language (DSL) for scripting text-based adventure games. The compiler transforms `.adv` files into executable game logic using a **6-phase architecture**.

### Compilation Pipeline

```
Input (.adv) → Lexer → Parser → Semantic → TAC → Optimizer → Executor → Output
```

---

## The Six Phases

### Phase 1: Lexical Analysis (Tokenization)
- **File:** `src/lexer.py`
- **Input:** Raw source code
- **Output:** Stream of tokens
- **Purpose:** Break code into meaningful units (keywords, identifiers, operators, numbers)

**Example:**
```
Input:  "item potion = 5 qty;"
Output: [ITEM, IDENTIFIER(potion), ASSIGN, NUMBER(5), QTY, SEMICOLON]
```

---

### Phase 2: Syntax Analysis (Parsing)
- **File:** `src/parser.py`
- **Input:** Token stream
- **Output:** Abstract Syntax Tree (AST)
- **Purpose:** Build tree structure representing program logic

**Example:**
```
Tokens: [ITEM, potion, ASSIGN, 5, qty, ;]
AST:    Declaration(type=item, name=potion, value=5, unit=qty)
```

---

### Phase 3: Semantic Analysis
- **File:** `src/semantic_analyzer.py`
- **Input:** AST
- **Output:** Validated AST + Symbol Table
- **Purpose:** Type checking, variable validation, scope management

**Checks:**
- All variables are declared before use
- Operations match types (can't add item to stat)
- Units are compatible (hp + hp = valid, hp + qty = invalid)
- No variable redeclaration in same scope

---

### Phase 4: Intermediate Code Generation (TAC)
- **File:** `src/intermediate_code.py`
- **Input:** Validated AST
- **Output:** Three-Address Code (TAC) instructions
- **Purpose:** Convert to machine-independent intermediate form

**Example:**
```
Loop Code:
  loop 3 iterations { x = x + 1; }

TAC:
  L0: counter = 0
  L1: if counter >= 3 goto L2
      x = x + 1
      counter = counter + 1
      goto L1
  L2: (next)
```

---

### Phase 5: Optimization
- **File:** `src/optimizer.py`
- **Input:** TAC instructions
- **Output:** Optimized TAC
- **Techniques:**
  - **Constant Folding:** `2 + 3` → `5` at compile time
  - **Dead Code Elimination:** Remove unreachable instructions
  - **Copy Propagation:** Eliminate redundant assignments

---

### Phase 6: Code Generation & Execution
- **File:** `src/code_generator.py`
- **Input:** Optimized TAC
- **Output:** Adventure game output
- **Purpose:** Execute instructions and print results

**Runtime Operations:**
- `narrate` - Print story text
- `combine` - Merge items
- `equip` - Apply stat modifiers
- `rest` - Pause execution
- `acquire/discard` - Manage inventory

---

## Key Data Structures

### Value (with Unit)
```python
class Value:
    numeric = 100      # The number
    unit = "hp"        # The unit (hp, qty, mp, turns)
```
Units travel with values through all compilation phases.

### Symbol Table (with Scopes)
```python
class SymbolTable:
    scopes = [{}]      # Stack of scope dictionaries
    
    def enter_scope(): # Enter block (loop, if, quest)
        scopes.push({})
    
    def exit_scope():  # Exit block
        scopes.pop()
```
Scope stack handles nested blocks and proper variable visibility.

### TAC Instruction
```python
class TACInstr:
    op = "ASSIGN"      # Operation type
    arg1 = "x"         # First operand
    arg2 = "5"         # Second operand
    result = "t0"      # Destination
```

---

## File Organization

```
src/
├── compiler.py              Main orchestrator
├── lexer.py                 Phase 1: Tokenization
├── token_types.py           Token/keyword definitions
├── parser.py                Phase 2: Parsing
├── semantic_analyzer.py     Phase 3: Validation
├── intermediate_code.py     Phase 4: TAC generation
├── optimizer.py             Phase 5: Optimization
└── code_generator.py        Phase 6: Execution
```

---

## Example: Complete Compilation

**Input Program:**
```adventurescript
item potion = 5 qty;
stat hp = 100 hp;

loop 2 iterations {
    hp = hp + 10 hp;
    narrate "Healing!";
}
```

**Phase 1 (Tokens):**
```
[ITEM, IDENTIFIER, ASSIGN, NUMBER(5), QTY, SEMICOLON, ...]
```

**Phase 2 (AST):**
```
Program(
  statements=[
    Declaration(item, potion, 5, qty),
    Declaration(stat, hp, 100, hp),
    Loop(iterations=2, body=[...])
  ]
)
```

**Phase 3 (Symbol Table):**
```
{
  potion: (item, qty),
  hp: (stat, hp)
}
```

**Phase 4 (TAC):**
```
0: potion = 5 qty
1: hp = 100 hp
2: L0: counter = 0
3: L1: if counter >= 2 goto L2
4: hp = hp + 10 hp
5: narrate "Healing!"
6: counter = counter + 1
7: goto L1
8: L2: (end)
```

**Phase 5 (Optimized):**
Same (no optimizations applicable here)

**Phase 6 (Output):**
```
Healing!
Healing!
```

---

## Design Decisions

1. **Why 6 Phases?** Mirrors textbook compiler design with clear separation of concerns
2. **Why TAC?** Machine-independent intermediate form that's easy to optimize and execute
3. **Why Recursive Descent Parser?** Simple, readable, sufficient for LootCode's grammar
4. **Why Scope Stack?** Proper handling of nested blocks and variable visibility
5. **Why Value + Unit?** Enables type-safe adventure game scripts

---

## Conclusion

The LootCode compiler demonstrates core compiler concepts through a clean 6-phase pipeline. Each phase handles one responsibility: tokenization, parsing, validation, code generation, optimization, and execution.
