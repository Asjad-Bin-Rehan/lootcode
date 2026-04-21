# CS4031 – Compiler Construction
## Course Project Proposal - Spring 2026

---

# **LootCode: An 8-Bit Adventure Language**

## Project Title
**LootCode**

## Theme
**8-Bit Adventure / Retro Computing**

---

## 1. Language Concept

**LootCode** is a high-level domain-specific language (DSL) designed to simplify the creation of text-based adventure games and interactive fiction in a retro 8-bit computing style. The language abstracts away low-level implementation details while providing game designers with intuitive constructs for defining game state (items, stats), interactions (combining items, equipping gear), narrative elements (narration, dialogue), and control flow (loops, conditionals).

LootCode targets educators, hobbyist game developers, and retro computing enthusiasts who want to create engaging text adventures without wrestling with assembly language or verbose general-purpose languages.

**Inspiration:** Classic text adventure games like Zork, Dungeon Master, and early graphical adventure games that emphasized exploration, inventory management, and narrative storytelling.

---

## 2. Key Features

**Feature 1: Game State Management**
- Support for `item` declarations (game objects with quantities: `item health_potion = 5 qty`)
- Support for `stat` declarations (character attributes with ranges: `stat player_hp = 100 hp`, `stat mana_pool = 50 mp`)
- Variables maintain units throughout execution (e.g., "2 qty" + "3 qty" = "5 qty")
- Type safety: operations must be appropriate for the variable type

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
- Scope isolation: quest parameters are local

**Feature 5: Compile-Time Optimizations**
- Constant folding: Arithmetic expressions evaluated at compile time
- Constant propagation: Variable values inlined where possible
- Dead code elimination: Unused assignments removed before execution
- Ensures efficient execution even on resource-constrained retro platforms

---

## 3. Example Programs

### Example 1: Simple Combat Scenario
```adventurescript
# Simple combat scenario
item health_potion = 3 qty;
item herbs = 5 qty;
stat player_hp = 100 hp;
stat dragon_hp = 50 hp;

narrate "You encounter a dragon!";

loop 5 iterations {
    if player_hp > 0 then
        narrate "You drink a potion!";
        rest 2 turns;
        player_hp = player_hp + 20 hp;
    else
        narrate "You have been defeated!";
    end
}

if health_potion > 0 then
    combine health_potion with herbs;
    narrate "You craft a powerful potion!";
    player_hp = 150 hp;
else
    narrate "No resources left!";
end

narrate "Victory!";
```

**Expected Output:**
```
You encounter a dragon!
You drink a potion!
(resting for 2 turns...)
You drink a potion!
(resting for 2 turns...)
You drink a potion!
(resting for 2 turns...)
You drink a potion!
(resting for 2 turns...)
You drink a potion!
(resting for 2 turns...)
You craft a powerful potion!
Victory!
```

---

### Example 2: Quest/Function Demonstration
```adventurescript
# Define a healing quest
quest heal_player(stat current_hp, item potion_count) returns hp {
    if current_hp < 50 then
        current_hp = current_hp + 30 hp;
        narrate "Healing applied!";
    else
        narrate "Health is sufficient!";
    end
    return current_hp;
}

# Main program
stat my_hp = 40 hp;
item potions = 10 qty;

narrate "Starting adventure...";
my_hp = heal_player(my_hp, potions);
narrate "Adventure complete!";
```

**Expected Output:**
```
Starting adventure...
Healing applied!
Adventure complete!
```

---

### Example 3: Inventory Management
```adventurescript
# Inventory management example
item sword = 1 qty;
item shield = 1 qty;
item gold = 100 qty;
stat inventory_slots = 3 qty;

narrate "You find a treasure chest!";

if inventory_slots > 0 then
    acquire sword to inventory_slots;
    narrate "Added sword to inventory!";
    inventory_slots = inventory_slots - 1 qty;
else
    narrate "Inventory full!";
    discard sword;
end

narrate "Current gold: 100 qty";
```

**Expected Output:**
```
You find a treasure chest!
Added sword to inventory!
Current gold: 100 qty
```

---

## 4. Formal Language Specification

### 4.1 EBNF Grammar

```ebnf
<program> ::= {<quest_declaration>} {<statement>}

<quest_declaration> ::= "quest" <identifier> "(" [<parameter_list>] ")" 
                        ["returns" <type>] "{" {<statement>} "}"

<parameter_list> ::= <type_specifier> <identifier> 
                    {"," <type_specifier> <identifier>}

<statement> ::= <declaration>
              | <assignment>
              | <operation>
              | <control_flow>
              | <return_statement>
              | <input_statement>

<declaration> ::= <type_specifier> <identifier> "=" <value> ";"

<type_specifier> ::= "item" | "stat" | "text" | "qty"

<assignment> ::= <identifier> "=" <expression> ";"

<operation> ::= <combine_op>
              | <equip_op>
              | <rest_op>
              | <narrate_op>
              | <acquire_op>
              | <discard_op>

<combine_op> ::= "combine" <identifier> "with" <identifier> ";"

<equip_op> ::= "equip" <identifier> "to" <value> ";"

<rest_op> ::= "rest" <value> ";"

<narrate_op> ::= "narrate" <string_literal> ";"

<acquire_op> ::= "acquire" <identifier> "to" <identifier> ";"

<discard_op> ::= "discard" <identifier> ";"

<control_flow> ::= <loop_statement> | <if_statement>

<loop_statement> ::= "loop" <number> "iterations" "{" {<statement>} "}"

<if_statement> ::= "if" <condition> "then" "{" {<statement>} "}" 
                   ["else" "{" {<statement>} "}"]

<condition> ::= <expression> [<comparison_op> <expression>]

<comparison_op> ::= "==" | "!=" | "<" | ">" | "<=" | ">="

<expression> ::= <term> {("+" | "-") <term>}

<term> ::= <factor> {("*" | "/") <factor>}

<factor> ::= <number> | <identifier> | <quest_call> | "(" <expression> ")"

<quest_call> ::= <identifier> "(" [<argument_list>] ")"

<argument_list> ::= <expression> {"," <expression>}

<value> ::= <number> [<unit>]

<unit> ::= "qty" | "hp" | "mp" | "turns" | "gold" | "treasure"

<return_statement> ::= "return" [<expression>] ";"

<input_statement> ::= "input" <identifier> ";"

<number> ::= <digit> {<digit>} ["." <digit> {<digit>}]

<identifier> ::= <letter> {<letter> | <digit> | "_"}

<string_literal> ::= '"' {<character>} '"'

<digit> ::= "0" | "1" | "2" | ... | "9"

<letter> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"

<character> ::= any printable character
```

---

## 5. Lexical Grammar

### 5.1 Token Categories

#### Keywords (27 total)
```
item, stat, text, qty, combine, equip, rest, narrate, acquire, discard,
show, loop, iterations, if, then, else, in, quest, return, returns, input,
to, with, for, at, from, by
```

#### Units (7 total)
```
qty, hp, mp, turns, gold, treasure, coin
```

#### Operators (11 total)
```
= (assignment)
+ - * / (arithmetic)
== != < > <= >= (comparison)
```

#### Delimiters (6 total)
```
; (semicolon)
, (comma)
( ) (parentheses)
{ } (braces)
```

#### Literals
- **Numbers:** Integers and floating-point (e.g., `42`, `3.14`)
- **Strings:** Double-quoted text (e.g., `"You enter a dark room"`)
- **Identifiers:** Start with letter or underscore, contain alphanumeric and underscore

#### Comments
- Single-line: `#` to end of line (e.g., `# This is a comment`)

### 5.2 Token Specification (Regular Expressions)

```
ITEM        : "item"
STAT        : "stat"
TEXT        : "text"
COMBINE     : "combine"
EQUIP       : "equip"
REST        : "rest"
NARRATE     : "narrate"
ACQUIRE     : "acquire"
DISCARD     : "discard"
LOOP        : "loop"
ITERATIONS  : "iterations"
IF          : "if"
THEN        : "then"
ELSE        : "else"
QUEST       : "quest"
RETURN      : "return"
RETURNS     : "returns"
INPUT       : "input"

NUMBER      : [0-9]+ ('.' [0-9]+)?
STRING      : '"' (~["\n])* '"'
IDENTIFIER  : [a-zA-Z_] [a-zA-Z0-9_]*
COMMENT     : '#' (~[\n])*
WHITESPACE  : [ \t\n\r]+ (skip)

ASSIGN      : '='
PLUS        : '+'
MINUS       : '-'
MULTIPLY    : '*'
DIVIDE      : '/'
EQ          : '=='
NEQ         : '!='
GT          : '>'
LT          : '<'
GTE         : '>='
LTE         : '<='
SEMICOLON   : ';'
COMMA       : ','
LPAREN      : '('
RPAREN      : ')'
LBRACE      : '{'
RBRACE      : '}'
TO          : "to"
WITH        : "with"
```

---

## 6. Type System & Semantic Rules

### 6.1 Type System

LootCode uses a **static type system** with four primitive types:

| Type | Description | Example | Default Value |
|------|-------------|---------|---|
| `item` | Game objects with quantity | `item sword = 1 qty` | 0 qty |
| `stat` | Character attributes (hit points, mana) | `stat player_hp = 100 hp` | 0 hp |
| `text` | String literals for narrative | `text message = "Hello"` | "" |
| `qty` | Numeric quantity with unit | `qty gold = 100 gold` | 0 qty |

### 6.2 Type Coercion Rules

- **Arithmetic operations:** Numeric types (`qty`, `stat`) can be combined
- **Unit preservation:** Operations preserve units (2 qty + 3 qty = 5 qty)
- **Stat ranges:** Stats must stay within valid ranges (0-999 for hp/mp)
- **Type mismatches:** Error if combining incompatible types (e.g., text + stat)

### 6.3 Semantic Rules

1. **Variable Declaration Rule:** Every variable must be declared before use
2. **No Redeclaration:** Variables cannot be redeclared in the same scope
3. **Type Safety:** Operations must match variable types
   - `combine` only works on `item` types
   - `equip` only works on `stat` types
   - `narrate` only works with strings
4. **Scope Visibility:** Quest parameters and local variables are visible only within quest body
5. **Return Type Matching:** If quest declares return type, must return value of that type
6. **Unit Consistency:** Units must match during assignment (cannot assign `hp` value to `qty` variable)

### 6.4 Operator Semantics

| Operation | Operands | Result | Example |
|-----------|----------|--------|---------|
| Addition | qty + qty | qty | `2 qty + 3 qty = 5 qty` |
| Subtraction | qty - qty | qty | `10 qty - 3 qty = 7 qty` |
| Multiplication | qty * qty | qty | `2 qty * 3 = 6 qty` |
| Division | qty / qty | qty | `10 qty / 2 = 5 qty` |
| Equality | any == any | boolean | `100 hp == 100 hp = true` |
| Comparison | qty < qty | boolean | `50 hp < 100 hp = true` |

---

## 7. Memory Model & Scope Management

### 7.1 Variable Storage

- **Global Scope:** Variables declared at program level
- **Function/Quest Scope:** Parameters and local variables within quest
- **Lifetime:** Variables exist for entire program duration (global) or quest execution (local)

### 7.2 Scope Hierarchy

```
Global Scope
├── Global Variables (items, stats, text, qty)
├── Quest: heal_player
│   ├── Parameter: current_hp (stat)
│   ├── Parameter: potion_count (item)
│   └── Local Variables: (any declared within quest)
└── Quest: another_quest
    ├── Parameter: ...
    └── Local Variables: ...
```

### 7.3 Symbol Table Structure

```
{
  "global": {
    "player_hp": {"type": "stat", "value": "100 hp", "scope": "global"},
    "health_potion": {"type": "item", "value": "5 qty", "scope": "global"}
  },
  "quests": {
    "heal_player": {
      "parameters": [
        {"name": "current_hp", "type": "stat"},
        {"name": "potion_count", "type": "item"}
      ],
      "return_type": "hp",
      "local_scope": {
        "current_hp": {"type": "stat", "scope": "function"}
      }
    }
  }
}
```

### 7.4 Allocation Strategy

- **Static Allocation:** All variables allocated at program start
- **Stack-based Parameters:** Quest parameters pushed to stack on call, popped on return
- **No Dynamic Memory:** Fixed-size memory allocation for all variables

---

## 8. Error Handling Strategy

### 8.1 Lexical Errors

| Error | Message Format | Example |
|-------|---|---|
| Unterminated String | `Lexical Error at line X: Unterminated string literal` | `narrate "hello` |
| Invalid Number Format | `Lexical Error at line X: Invalid number format` | `3.14.159` |
| Unexpected Character | `Lexical Error at line X: Unexpected character 'X'` | `@` in code |

### 8.2 Syntax Errors

| Error | Message Format | Example |
|-------|---|---|
| Expected Token | `Syntax Error at line X: Expected TOKEN, got TOKEN2` | `if x > 5 narrate "hi"` (missing then) |
| Unexpected Token | `Syntax Error at line X: Unexpected token TOKEN` | Extra semicolon |
| Missing Semicolon | `Syntax Error at line X: Expected ';'` | `item x = 5 qty` (no semicolon) |

### 8.3 Semantic Errors

| Error | Message Format | Example |
|-------|---|---|
| Undefined Variable | `Semantic Error at line X: Variable 'name' is not defined` | Using undeclared variable |
| Redeclaration | `Semantic Error at line X: Variable 'name' already declared` | Declaring same variable twice |
| Type Mismatch | `Semantic Error at line X: Type mismatch in operation` | `combine stat_var with item_var` |
| Invalid Operation | `Semantic Error at line X: Operation not supported for type` | `combine stat_var` |
| Invalid Range | `Semantic Error at line X: Value out of range for stat type` | `stat hp = 1000 hp` (exceeds 999) |
| Missing Return | `Semantic Error at line X: Quest expects return value` | Quest with return type but no return |

### 8.4 Error Recovery Strategy

1. **Lexer:** Skip invalid characters and continue tokenization
2. **Parser:** Synchronize at statement boundaries (`;`, `}`) and continue parsing
3. **Semantic Analyzer:** Report all errors in single pass, don't stop at first error
4. **TAC Generator:** Assume reasonable defaults for type errors and continue

---

## 9. Target Output

**Direct Execution and Display of Results**

The LootCode compiler produces an **interpreted execution system** that:

1. **Lexical Analysis (Phase 1):** Tokenizes `.adv` source files using adventure-specific keywords
2. **Syntax Analysis (Phase 2):** Parses tokens into an Abstract Syntax Tree (AST)
3. **Semantic Analysis (Phase 3):** Validates type correctness, variable declarations, and scope
4. **Intermediate Code Generation (Phase 4):** Generates Three-Address Code (TAC) with labels and jumps
5. **Optimization (Phase 5):** Applies constant folding, dead code elimination, and constant propagation
6. **Execution (Phase 6):** Interprets TAC instructions and outputs narrative text and game state

**Output Format:** Console/terminal output showing narrative text, game state changes, and execution results

---

## 10. Technology Stack

| Component | Technology |
|-----------|---|
| **Programming Language** | Python 3.8+ |
| **Testing Framework** | Python unittest |
| **Version Control** | Git |
| **Documentation** | Markdown |
| **Target Platform** | Cross-platform (Windows, Linux, macOS) |
| **Python Dependencies** | None (standard library only) |

### Implementation Architecture

```
adventurescript-compiler/
├── src/
│   ├── lexer.py              (Phase 1: Tokenization)
│   ├── token_types.py         (Token definitions)
│   ├── parser.py              (Phase 2: Parsing)
│   ├── semantic_analyzer.py   (Phase 3: Semantic Analysis)
│   ├── intermediate_code.py   (Phase 4: TAC Generation)
│   ├── optimizer.py           (Phase 5: Optimization)
│   ├── code_generator.py      (Phase 6: Execution)
│   └── compiler.py            (Main orchestrator)
├── tests/
│   ├── run_all_tests.py       (Test runner)
│   ├── dungeon.adv            (Example adventure game)
│   ├── quest_test.adv         (Quest/function test)
│   └── inventory_test.adv     (Inventory management test)
├── README.md                   (Setup and usage instructions)
├── PROJECT_PROPOSAL.md         (This document)
└── LANGUAGE_SPEC.md           (Formal specification)
```

---

## 11. Expected Challenges

**Challenge 1: Unit Preservation Through Arithmetic Operations**

The language requires tracking units (hp, mp, qty, turns) through variable assignments and operations. For example, `stat player_hp = 100 hp` creates a value with units, and `player_hp = player_hp + 20 hp` must preserve the hp unit while updating the numeric value. This requires careful design of value representation in the TAC layer and code generator to avoid losing unit information during optimization and execution.

**Solution Approach:**
- Implement `Value` class with separate `numeric` and `unit` fields
- Preserve units through all TAC operations
- Validate unit compatibility before arithmetic operations

---

**Challenge 2: Scope and Symbol Table Management for Nested Structures**

AdventureScript supports nested control flow (loops within conditionals, quests with local variables) that require proper scope handling. The semantic analyzer must maintain a symbol table stack to track variable declarations at different scope levels, validate no redeclaration within a scope, and ensure referenced variables are accessible. Managing parameter scoping for quests (functions) adds additional complexity.

**Solution Approach:**
- Implement symbol table with scope stack
- Track variable visibility and lifetime
- Validate variable access against current scope
- Implement scope entry/exit for quest calls

---

**Challenge 3: Correct Translation of Loop and Conditional Statements to TAC**

Translating high-level `loop` and `if` constructs into Three-Address Code with labels and conditional jumps requires careful management of jump targets, loop counters, and condition evaluation. Incorrect label placement or jump logic can cause infinite loops, skipped code, or runtime errors. Additionally, optimization passes must not break loop semantics when removing dead code or folding constants.

**Solution Approach:**
- Use systematic label generation (L0, L1, L2, ...)
- Implement proper loop counter management
- Generate correct conditional jump patterns
- Preserve loop invariants during optimization
- Validate jump targets are reachable

---

## 12. Compiler Design Decisions

1. **Single-Pass Semantic Analysis:** Analyze after parsing to catch errors early
2. **TAC-based Interpretation:** Use Three-Address Code for portability
3. **Direct Execution:** No separate code generation step; interpret TAC directly
4. **No Heap Allocation:** All variables statically allocated for simplicity
5. **Unit as First-Class Value:** Units tracked alongside values, not separate metadata
6. **Scope Stack:** Dynamic scope management for quest calls

---

## 13. Success Criteria

The project will be considered successful when:

1. ✅ All 6 compiler phases are implemented and functional
2. ✅ Example programs compile without errors
3. ✅ Semantic validation catches type errors and duplicate declarations
4. ✅ Optimization passes reduce TAC size (constant folding, dead code elimination)
5. ✅ Narrative output is correct and in expected order
6. ✅ Unit preservation works correctly through operations
7. ✅ Loop and conditional logic executes correctly
8. ✅ Quest/function declarations and calls work properly
9. ✅ Test suite passes all adventure program tests
10. ✅ Error messages are meaningful with line/column information

---

## 14. References & Inspiration

- **Classic Adventure Games:** Zork, Dungeon Master, Ultima series
- **Compiler Design:** Aho & Ullman "Compilers: Principles, Techniques, and Tools"
- **Domain-Specific Languages:** Fowler "Domain Specific Languages"
- **EBNF Notation:** ISO/IEC 14977 standard

---

**Document Version:** 2.0 (Enhanced)  
**Date:** April 2026  
**Course:** CS4031 Compiler Construction  
**Assignment:** Retro Computing Mini Compiler - Creative Design Challenge
