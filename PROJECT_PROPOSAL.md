# CS4031 Compiler Construction - Project Proposal

## Project Title
**AdventureScript**

## Theme
8-Bit Adventure / Retro Computing

---

## Team Members
| Student Name | Student ID |
|---|---|
| [To be added] | [To be added] |
| [To be added] | [To be added] |
| [To be added] | [To be added] |

---

## 1. Language Concept

**AdventureScript** is a high-level domain-specific language (DSL) designed to simplify the creation of text-based adventure games and interactive fiction in a retro 8-bit computing style. The language abstracts away low-level implementation details while providing game designers with intuitive constructs for defining game state (items, stats), interactions (combining items, equipping gear), narrative elements (narration, dialogue), and control flow (loops, conditionals). AdventureScript targets educators, hobbyist game developers, and retro computing enthusiasts who want to create engaging text adventures without wrestling with assembly language or verbose general-purpose languages.

---

## 2. Key Features

**Feature 1: Game State Management**
- Support for `item` declarations (game objects with quantities: `item health_potion = 5 qty`)
- Support for `stat` declarations (character attributes with ranges: `stat player_hp = 100 hp`, `stat mana_pool = 50 mp`)
- Variables maintain units throughout execution (e.g., "2 qty" + "3 qty" = "5 qty")

**Feature 2: Adventure Operations**
- `combine` operation: Merge items together (e.g., `combine herbs with potion`)
- `equip` operation: Apply stats and transformations (e.g., `equip player_hp to 100 hp`)
- `rest` operation: Time-based delays and cooldowns (e.g., `rest 5 turns`)
- `narrate` operation: Display story text and dialogue (e.g., `narrate "You enter the dark dungeon..."`)
- `acquire` / `discard` operations: Inventory management

**Feature 3: Control Flow Structures**
- `loop` statements with iteration counts (e.g., `loop 10 iterations { ... }`)
- `if`-`then`-`else` conditionals for branching gameplay
- Comparison operators: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Boolean expressions for complex decision logic

**Feature 4: Function/Quest Abstraction**
- `quest` declarations for reusable game mechanics
- Parameter passing and return types
- Enables modular adventure design and code reuse
- Example: `quest open_treasure_chest returns turns { ... }`

**Feature 5: Compile-Time Optimizations**
- Constant folding: Arithmetic expressions evaluated at compile time
- Constant propagation: Variable values inlined where possible
- Dead code elimination: Unused assignments removed before execution
- Ensures efficient execution even on resource-constrained retro platforms

---

## 3. Example Program

```adventurescript
# A simple dungeon adventure game
item health_potion = 3 qty;
item herbs = 5 qty;
stat player_hp = 100 hp;
stat dragon_hp = 50 hp;

narrate "You enter the dark dungeon...";
narrate "A dragon blocks your path!";

# Combat loop
loop 5 iterations {
    if player_hp > 0 then
        narrate "You drink a potion to restore health!";
        rest 2 turns;
        player_hp = player_hp + 20 hp;
    else
        narrate "You have been defeated!";
    end
}

# Healing phase
if health_potion > 0 then
    combine health_potion with herbs;
    narrate "You craft a powerful healing tonic...";
    player_hp = 150 hp;
else
    narrate "No potions left... you are doomed!";
end

narrate "Victory! You defeated the dragon and claimed treasure!";
```

### Output of Above Program
```
You enter the dark dungeon...
A dragon blocks your path!
You drink a potion to restore health!
(resting for 2 turns...)
You drink a potion to restore health!
(resting for 2 turns...)
You drink a potion to restore health!
(resting for 2 turns...)
You drink a potion to restore health!
(resting for 2 turns...)
You drink a potion to restore health!
(resting for 2 turns...)
You craft a powerful healing tonic...
Victory! You defeated the dragon and claimed treasure!
```

---

## 4. Target Output

**Direct Execution and Display of Results**

The AdventureScript compiler produces an **interpreted execution system** that:

1. **Lexical Analysis (Phase 1):** Tokenizes `.adv` source files using adventure-specific keywords
2. **Syntax Analysis (Phase 2):** Parses tokens into an Abstract Syntax Tree (AST)
3. **Semantic Analysis (Phase 3):** Validates type correctness, variable declarations, and scope
4. **Intermediate Code Generation (Phase 4):** Generates Three-Address Code (TAC) with labels and jumps
5. **Optimization (Phase 5):** Applies constant folding, dead code elimination, and constant propagation
6. **Execution (Phase 6):** Interprets TAC instructions and outputs narrative text and game state

**Output:** Console/terminal output showing narrative text, game state changes, and execution results

---

## 5. Expected Challenges

**Challenge 1: Unit Preservation Through Arithmetic Operations**
The language requires tracking units (hp, mp, qty, turns) through variable assignments and operations. For example, `stat player_hp = 100 hp` creates a value with units, and `player_hp = player_hp + 20 hp` must preserve the hp unit while updating the numeric value. This requires careful design of value representation in the TAC layer and code generator to avoid losing unit information during optimization and execution.

**Challenge 2: Scope and Symbol Table Management for Nested Structures**
AdventureScript supports nested control flow (loops within conditionals, quests with local variables) that require proper scope handling. The semantic analyzer must maintain a symbol table stack to track variable declarations at different scope levels, validate no redeclaration within a scope, and ensure referenced variables are accessible. Managing parameter scoping for quests (functions) adds additional complexity.

**Challenge 3: Correct Translation of Loop and Conditional Statements to TAC**
Translating high-level `loop` and `if` constructs into Three-Address Code with labels and conditional jumps requires careful management of jump targets, loop counters, and condition evaluation. Incorrect label placement or jump logic can cause infinite loops, skipped code, or runtime errors. Additionally, optimization passes must not break loop semantics when removing dead code or folding constants.

---

## 6. Compiler Architecture

### Six-Phase Pipeline (4031 Requirement)

```
SOURCE CODE (.adv)
      ↓
[Phase 1: LEXER] ─→ Token Stream
      ↓
[Phase 2: PARSER] ─→ Abstract Syntax Tree (AST)
      ↓
[Phase 3: SEMANTIC ANALYZER] ─→ Validated AST + Symbol Table
      ↓
[Phase 4: TAC GENERATOR] ─→ Three-Address Code
      ↓
[Phase 5: OPTIMIZER] ─→ Optimized TAC
      ↓
[Phase 6: CODE GENERATOR] ─→ Execution Output
      ↓
CONSOLE OUTPUT (Narrative + Game State)
```

---

## 7. Language Grammar Overview

### Core Syntax

```
program → {recipe_decl | statement}

statement → declaration | operation | control_flow | narration

declaration → item_decl | stat_decl | assignment

item_decl → ITEM identifier ASSIGN number unit SEMICOLON
stat_decl → STAT identifier ASSIGN number unit SEMICOLON

operation → COMBINE identifier WITH identifier SEMICOLON
          | EQUIP identifier TO number unit SEMICOLON
          | REST number unit SEMICOLON
          | NARRATE string SEMICOLON

control_flow → loop_stmt | if_stmt

loop_stmt → LOOP number ITERATIONS LBRACE {statement} RBRACE

if_stmt → IF expression THEN {statement} [ELSE {statement}] END

quest_decl → QUEST identifier [parameters] [RETURNS type] LBRACE {statement} RBRACE
```

---

## 8. Success Metrics

The project will be considered successful when:

1. ✅ **All 6 compiler phases are implemented and functional**
2. ✅ **Example programs compile without errors**
3. ✅ **Semantic validation catches type errors and duplicate declarations**
4. ✅ **Optimization passes reduce TAC size (constant folding, dead code elimination)**
5. ✅ **Narrative output is correct and in expected order**
6. ✅ **Unit preservation works correctly through operations**
7. ✅ **Loop and conditional logic executes correctly**
8. ✅ **Test suite passes all dungeon adventure program tests**

---

## 9. Deliverables

| Deliverable | Description |
|---|---|
| `README.md` | Language documentation and usage guide |
| `LANGUAGE_SPEC.md` | Formal language specification |
| `src/` | Complete compiler source code (6 phases) |
| `tests/` | Test suite with `.adv` adventure programs |
| `PROJECT_PROPOSAL.md` | This document |
| `dungeon.adv` | Example adventure game program |
| Documentation | Inline code comments and phase explanations |

---

## 10. Technology Stack

- **Language:** Python 3.x
- **Architecture:** Multi-phase compiler (Lexer → Parser → Semantic → TAC → Optimizer → Interpreter)
- **Data Structures:** Token streams, Abstract Syntax Trees, Symbol Tables, Three-Address Code
- **Testing:** Python unittest framework
- **Version Control:** Git

---

## 11. Retro Theme Justification

AdventureScript embraces the 8-bit adventure game aesthetic through:

- **Vocabulary:** Using game-domain keywords (items, stats, quests, inventory) rather than generic programming language terms
- **Simplicity:** Intentionally limited feature set mirrors the constraints of retro platforms
- **Narrative Focus:** Core `narrate` operation reflects the text-adventure games of the 1980s-90s (Zork, Dungeon, etc.)
- **Unit System:** The "qty", "hp", "mp", "turns" unit system mirrors RPG mechanics from retro gaming
- **Direct Interpretation:** No compilation to separate output format; results appear directly on console like retro BASIC programs

---

## 12. Timeline & Milestones

| Phase | Task | Status |
|---|---|---|
| Phase 1 | Lexer & Token Definitions | ✅ COMPLETE |
| Phase 2 | Parser & AST Construction | 🚀 IN PROGRESS |
| Phase 3 | Semantic Analysis & Validation | ⏳ PENDING |
| Phase 4 | TAC Generation | ⏳ PENDING |
| Phase 5 | Optimization | ⏳ PENDING |
| Phase 6 | Code Generator & Execution | ⏳ PENDING |
| Testing | Full test suite & documentation | ⏳ PENDING |

---

## Appendix: Language Keywords Reference

| Category | Keywords |
|---|---|
| **Types** | item, stat, text |
| **Operations** | combine, equip, rest, narrate, acquire, discard, show |
| **Control** | loop, iterations, if, then, else, when |
| **Functions** | quest, return, returns |
| **I/O** | input, narrate |
| **Units** | qty, hp, mp, turns, gold, treasure, coin, loot, gems |

---

**Document Version:** 1.0  
**Date:** [Current Date]  
**Course:** CS4031 Compiler Construction  
**Assignment:** Retro Computing Theme Language Compiler
