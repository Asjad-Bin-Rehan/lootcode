# LootCode Compiler Architecture Document

**Date:** May 10, 2026  
**Status:** Final Submission  
**Project:** CS4031 Compiler Construction - LootCode Mini Language Compiler

---

## Table of Contents

1. [Overview](#overview)
2. [Compiler Pipeline](#compiler-pipeline)
3. [Phase-Wise Breakdown](#phase-wise-breakdown)
4. [Data Structures](#data-structures)
5. [Design Decisions](#design-decisions)
6. [Implementation Details](#implementation-details)

---

## Overview

LootCode is a domain-specific language (DSL) for scripting text-based adventure games. The compiler is implemented in **Python** and follows a traditional **6-phase compilation architecture**, transforming high-level adventure scripts (.adv files) into executable game logic.

### Compilation Flow

```
Input Program (.adv)
        ↓
   PHASE 1: Lexical Analysis (Tokenization)
        ↓
   PHASE 2: Syntax Analysis (Parsing)
        ↓
   PHASE 3: Semantic Analysis (Type Checking & Validation)
        ↓
   PHASE 4: Intermediate Code Generation (Three-Address Code)
        ↓
   PHASE 5: Optimization (Dead Code Elimination, Constant Folding)
        ↓
   PHASE 6: Code Generation & Execution (Runtime Interpretation)
        ↓
   Adventure Game Output
```

---

## Compiler Pipeline

### Entry Point: `compiler.py`

The main compiler orchestrator (`src/compiler.py`) coordinates all phases:

```python
def compile_and_run(source_code, show_phases=True):
    # Phase 1: Lexical Analysis
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    # Phase 2: Syntax Analysis
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Phase 3: Semantic Analysis
    semantic_analyzer = SemanticAnalyzer()
    symbol_table = semantic_analyzer.analyze(ast)
    
    # Phase 4: Intermediate Code Generation
    ic_generator = IntermediateCodeGenerator()
    tac_instructions = ic_generator.generate(ast)
    
    # Phase 5: Optimization
    optimizer = Optimizer()
    optimized_tac = optimizer.optimize(tac_instructions)
    
    # Phase 6: Code Generation & Execution
    code_generator = CodeGenerator()
    code_generator.execute(optimized_tac)
```

---

## Phase-Wise Breakdown

### Phase 1: Lexical Analysis (Tokenization)

**File:** `src/lexer.py`, `src/token_types.py`

**Purpose:** Break source code into meaningful tokens (keywords, identifiers, operators, literals)

**Input:** Raw LootCode source code string

**Output:** List of `Token` objects with type and value

#### Key Components:

- **Token Classes:** Defined in `token_types.py`
  - Keywords: `item`, `stat`, `loop`, `if`, `quest`, etc.
  - Operators: `+`, `-`, `*`, `/`, `==`, `!=`, `>`, `<`, etc.
  - Delimiters: `{`, `}`, `;`, `,`, `(`, `)`
  - Identifiers and Literals (numbers, strings)

- **Lexer Algorithm:**
  - Character-by-character scanning with lookahead
  - Pattern matching for keywords vs. identifiers
  - Unit tracking (qty, hp, mp, turns) as special tokens
  - Comment stripping (`#` to end-of-line)
  - Error detection: Invalid characters, malformed strings

#### Example:

```
Input: "item potion = 3 qty;"
Output: [
  Token(ITEM, "item"),
  Token(IDENTIFIER, "potion"),
  Token(ASSIGN, "="),
  Token(NUMBER, "3"),
  Token(QTY, "qty"),
  Token(SEMICOLON, ";")
]
```

---

### Phase 2: Syntax Analysis (Parsing)

**File:** `src/parser.py`

**Purpose:** Construct Abstract Syntax Tree (AST) by parsing token stream according to grammar rules

**Input:** List of tokens from lexer

**Output:** AST representing program structure

#### Grammar Overview:

```
Program     → (Quest)* Statement*
Quest       → "quest" IDENTIFIER "{" Statement* "return" IDENTIFIER ";" "}"
Statement   → Declaration | Assignment | Operation | Control | Narrate
Declaration → Type IDENTIFIER "=" Expr Unit ";"
Assignment  → IDENTIFIER "=" Expr Unit ";"
Expr        → Term (("+"|"-") Term)*
Term        → Factor (("*"|"/") Factor)*
Factor      → NUMBER | IDENTIFIER | "(" Expr ")"
Control     → Loop | Conditional
Loop        → "loop" NUMBER "iterations" "{" Statement* "}"
Conditional → "if" Condition "then" "{" Statement* "}" 
              ("else" "{" Statement* "}")?
```

#### Key Components:

- **AST Node Classes:**
  - `Program`: Contains quests and statements
  - `Quest`: Function definition with parameters and return type
  - `Declaration`: Variable declaration with type and initial value
  - `Assignment`: Variable assignment
  - `BinaryOp`: Arithmetic expressions (e.g., `a + b`)
  - `Loop`: Iteration control structure
  - `Conditional`: If-then-else branch
  - `Operation`: Adventure operations (combine, equip, rest, narrate)

- **Parsing Strategy:** Recursive descent parser
  - `parse_program()`: Top-level entry
  - `parse_statement()`: Parse individual statements
  - `parse_expr()`: Parse expressions with operator precedence
  - `parse_control()`: Parse loops and conditionals
  - Error recovery: Reports syntax errors with line information

#### Example:

```
Input Tokens: [ITEM, IDENTIFIER(potion), ASSIGN, NUMBER(3), QTY, SEMICOLON]
Output AST:   Declaration(
                type=ITEM,
                name=potion,
                value=BinaryOp(left=3, op=+, right=0),
                unit=qty
              )
```

---

### Phase 3: Semantic Analysis (Type Checking & Validation)

**File:** `src/semantic_analyzer.py`

**Purpose:** Validate program semantics, maintain symbol table, and check type safety

**Input:** AST from parser

**Output:** Annotated AST + Symbol Table

#### Key Responsibilities:

1. **Symbol Table Management:**
   - Track all declared variables and their types/units
   - Maintain scope stack for nested structures (loops, conditionals, quests)
   - Detect redeclarations and undefined variable references

2. **Type Checking:**
   - Validate operations are appropriate for types (e.g., can't combine a stat with an item)
   - Ensure units are compatible in arithmetic (hp + hp = hp, qty + qty = qty)
   - Check function/quest return types match declarations

3. **Validation Rules:**
   - All variables used must be declared
   - No variable redeclaration in same scope
   - Operations match type constraints
   - Loop iterations must be positive
   - Quest parameters and return values must match calls

#### Symbol Table Structure:

```python
class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Stack of scope dictionaries
    
    def declare(name, type, unit):
        """Add variable to current scope"""
    
    def lookup(name):
        """Search variable in scope stack"""
    
    def enter_scope():
        """Push new scope (enter block)"""
    
    def exit_scope():
        """Pop scope (exit block)"""
```

#### Example:

```
AST Node: Assignment(name=player_hp, value=BinaryOp(...))
Semantic Check:
  - Lookup player_hp: Found (type=stat, unit=hp)
  - Check RHS expression type/unit: hp
  - Validate types match: ✓ stat = (hp operation) → OK
Symbol Table: { player_hp: (stat, hp, value=120) }
```

---

### Phase 4: Intermediate Code Generation (Three-Address Code)

**File:** `src/intermediate_code.py`

**Purpose:** Translate high-level AST to intermediate representation (Three-Address Code / TAC)

**Input:** Validated AST + Symbol Table

**Output:** List of TAC instructions

#### TAC Format:

Each instruction has at most 3 addresses:
```
result = operand1 operator operand2
label:
goto label
if condition goto label
call procedure
```

#### TAC Instruction Types:

1. **Arithmetic:** `t1 = a + b`, `t2 = t1 * 3`
2. **Assignment:** `x = 5`
3. **Control Flow:** `goto L1`, `if a > b goto L2`
4. **Function Calls:** `call quest_name`
5. **Adventure Operations:** `combine(herb, potion)`, `equip(player_hp, 100)`

#### Key Components:

- **Label Generation:** Systematic labels (L0, L1, L2, ...) for control flow targets
- **Temporary Variables:** t0, t1, t2, ... for intermediate values
- **Loop Counter Management:** Generate counters for loop iteration tracking
- **Condition Evaluation:** Convert boolean expressions to conditional jumps

#### Example:

```
Input AST: Loop(iterations=3, body=[Assignment(x = x + 1)])

Output TAC:
  L0: counter_1 = 0
  L1: if counter_1 >= 3 goto L2
      t1 = x + 1
      x = t1
      counter_1 = counter_1 + 1
      goto L1
  L2: (continue to next statement)
```

---

### Phase 5: Optimization

**File:** `src/optimizer.py`

**Purpose:** Improve TAC code by reducing redundancy and eliminating unnecessary instructions

**Input:** TAC instructions

**Output:** Optimized TAC instructions

#### Optimization Techniques:

1. **Constant Folding:**
   - Pre-compute expressions with constant values
   - Replace `t = 2 + 3` with `t = 5` at compile-time

2. **Dead Code Elimination:**
   - Remove unreachable instructions after unconditional jumps
   - Remove assignments to variables never used afterward
   - Remove unreachable branches in conditionals

3. **Copy Propagation:**
   - Eliminate redundant copy assignments
   - Replace `t2 = t1; x = t2` with `x = t1`

#### Conservative Approach:

- Preserves loop semantics and control flow integrity
- Does NOT remove instructions that might have side effects (adventure operations)
- Validates jump targets remain valid after optimization

#### Example:

```
Before Optimization:
  L0: t1 = 2 + 3
      x = t1
      y = 5 * 2
      z = y
      goto L1

After Optimization:
  L0: x = 5
      z = 10
      goto L1
```

---

### Phase 6: Code Generation & Execution

**File:** `src/code_generator.py`

**Purpose:** Execute TAC instructions and produce adventure game output

**Input:** Optimized TAC instructions

**Output:** Adventure game narrative and state updates printed to console

#### Execution Model:

- **Register/Memory:** Maps variables to Python objects maintaining type and unit
- **Runtime Stack:** Manages function call frames for quest execution
- **Instruction Dispatch:** Switch on instruction type and execute corresponding action

#### Execution Flow:

```python
class CodeGenerator:
    def execute(self, tac_instructions):
        for instruction in tac_instructions:
            if instruction.type == "ASSIGN":
                self.execute_assignment(instruction)
            elif instruction.type == "BINARY_OP":
                self.execute_binary_op(instruction)
            elif instruction.type == "GOTO":
                self.pc = self.find_label(instruction.target)
            elif instruction.type == "IF_GOTO":
                if self.evaluate_condition(instruction):
                    self.pc = self.find_label(instruction.target)
            # ... etc
```

#### Adventure Operations:

- **narrate(text):** Print story text to console
- **combine(item1, item2):** Merge inventory items
- **equip(stat, value):** Apply stat modifiers
- **rest(turns):** Pause execution
- **acquire(item, qty):** Add items to inventory
- **discard(item, qty):** Remove items from inventory

#### Example Output:

```
You enter the dark dungeon...
[Acquired: health potion x3]
[Equipped: player_hp = 100]
```

---

## Data Structures

### Value Type

Represents a value with both numeric and unit components:

```python
class Value:
    def __init__(self, numeric, unit):
        self.numeric = numeric
        self.unit = unit  # "qty", "hp", "mp", "turns", etc.
    
    def __add__(self, other):
        if self.unit != other.unit:
            raise TypeError(f"Cannot add {self.unit} to {other.unit}")
        return Value(self.numeric + other.numeric, self.unit)
```

### AST Nodes

All AST nodes inherit from base class with location tracking:

```python
class ASTNode:
    def __init__(self, line, column):
        self.line = line
        self.column = column

class Program(ASTNode):
    def __init__(self, quests, statements):
        self.quests = quests
        self.statements = statements
```

### TAC Instruction

```python
class TACInstruction:
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op              # "ASSIGN", "ADD", "GOTO", etc.
        self.arg1 = arg1          # First operand
        self.arg2 = arg2          # Second operand
        self.result = result      # Destination
```

---

## Design Decisions

### 1. Why Six Phases?

The six-phase architecture mirrors textbook compiler design:
- **Phases 1-2:** Frontend (lexical + syntax analysis)
- **Phase 3:** Semantic validation
- **Phases 4-5:** Code generation and optimization
- **Phase 6:** Execution engine

This separation of concerns ensures each phase has a single responsibility, making the code maintainable and testable.

### 2. Why Three-Address Code (TAC)?

TAC provides:
- **Machine-independent representation:** Easy to optimize
- **Simplified execution:** Each instruction is simple and uniform
- **Control flow clarity:** Labels and jumps are explicit
- **Standard intermediate form:** Used in professional compilers (GCC, LLVM)

### 3. Why Recursive Descent Parser?

Chosen for simplicity and debuggability:
- Natural fit with LootCode's straightforward grammar
- Easy to implement and understand
- Good error recovery with clear error messages
- Sufficient performance for small to medium programs

### 4. Symbol Table as Scope Stack

Nested structure support requires:
- Stack of scopes for entering/exiting blocks
- Linear search up the stack for variable lookup
- Prevents redeclaration at current scope level
- Clean handling of shadowing rules

### 5. Unit Preservation Strategy

Units are first-class citizens:
- Every value carries its unit alongside numeric value
- Operations validate unit compatibility before execution
- Type system is unit-aware (not just type-aware)
- Enables catching user errors at compile-time

---

## Implementation Details

### File Organization

```
src/
├── compiler.py               Main orchestrator (6 phases)
├── lexer.py                  Phase 1 tokenization
├── token_types.py            Token definitions & keywords
├── parser.py                 Phase 2 parsing & AST
├── semantic_analyzer.py      Phase 3 validation & symbol table
├── intermediate_code.py      Phase 4 TAC generation
├── optimizer.py              Phase 5 optimization
└── code_generator.py         Phase 6 execution engine
```

### Testing Strategy

- **Unit Tests:** Each phase validated independently
- **Integration Tests:** End-to-end compilation flow
- **Test Suite:** 12 adventure game programs covering all features
- **Regression Tests:** Verify previous fixes don't break

### Error Handling

Errors are caught at each phase:

1. **Lexical Errors:** Invalid characters, malformed literals
2. **Syntax Errors:** Grammar violations with line/column info
3. **Semantic Errors:** Undefined variables, type mismatches, unit conflicts
4. **Runtime Errors:** Division by zero, invalid operations

Example error output:
```
SyntaxError at line 5, column 12:
  Unexpected token: IDENTIFIER where SEMICOLON expected
  5 | item potion qty
            ^
```

---

## Compilation Example

### Input Program (`example.adv`)

```adventurescript
item potion = 5 qty;
stat player_hp = 100 hp;

loop 3 iterations {
    player_hp = player_hp + 10 hp;
    narrate "Healing...";
}

if player_hp > 120 hp then {
    narrate "Fully healed!";
}
```

### Phase 1: Tokens

```
[ITEM, IDENTIFIER(potion), ASSIGN, NUMBER(5), QTY, SEMICOLON,
 STAT, IDENTIFIER(player_hp), ASSIGN, NUMBER(100), HP, SEMICOLON,
 LOOP, NUMBER(3), ITERATIONS, LBRACE, ...]
```

### Phase 2: AST

```
Program(
  quests=[],
  statements=[
    Declaration(type=ITEM, name=potion, value=5, unit=qty),
    Declaration(type=STAT, name=player_hp, value=100, unit=hp),
    Loop(iterations=3, body=[
      Assignment(name=player_hp, value=BinaryOp(player_hp + 10, unit=hp)),
      Operation(narrate, "Healing...")
    ]),
    Conditional(...)
  ]
)
```

### Phase 3: Symbol Table

```
{
  potion: (item, qty, value=5),
  player_hp: (stat, hp, value=100)
}
```

### Phase 4: TAC

```
0: potion = 5 qty
1: player_hp = 100 hp
2: L0: counter_1 = 0
3: L1: if counter_1 >= 3 goto L2
4: t1 = player_hp + 10 hp
5: player_hp = t1
6: narrate "Healing..."
7: counter_1 = counter_1 + 1
8: goto L1
9: L2: if player_hp > 120 hp goto L3
10: narrate "Fully healed!"
11: L3: end
```

### Phase 5: Optimized TAC

```
0: potion = 5 qty
1: player_hp = 100 hp
2: L0: counter_1 = 0
3: L1: if counter_1 >= 3 goto L2
4: player_hp = player_hp + 10 hp     # Constant folding merged
5: narrate "Healing..."
6: counter_1 = counter_1 + 1
7: goto L1
8: L2: if player_hp > 120 hp goto L3
9: narrate "Fully healed!"
10: L3: end
```

### Phase 6: Execution Output

```
Healing...
Healing...
Healing...
Fully healed!
```

---

## Conclusion

The LootCode compiler demonstrates all fundamental compiler design concepts: lexical analysis, parsing, semantic validation, intermediate code generation, optimization, and execution. The six-phase architecture provides clear separation of concerns, making the system maintainable, testable, and extensible for future language enhancements.

