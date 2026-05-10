# LootCode Language Specification

## 1. Overview

LootCode is an adventure-themed DSL for scripting text-based gameplay behavior.
Programs declare values, perform adventure operations, and use control flow.

## 2. Lexical Elements

### 2.1 Core Keywords

- Types: `item`, `stat`, `text`, `qty`
- Operations: `combine`, `equip`, `rest`, `narrate`, `show`, `power_up`, `acquire`, `discard`
- Control: `loop`, `iterations`, `if`, `then`, `else`, `end`
- Functions: `quest`, `return`, `returns`
- Input: `input`
- Prepositions: `to`, `with`, `by`

### 2.2 Units

- Quantity: `qty`, `count`
- Stats: `hp`, `mp`
- Time: `turns`, `seconds`, `hours`
- Currency/loot literals also exist as tokens (for example `gold`, `treasure`, `coin`, `loot`, `gems`).

### 2.3 Operators and Delimiters

- Assignment and arithmetic: `=`, `+`, `-`, `*`, `/`
- Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Delimiters: `;`, `,`, `(`, `)`, `{`, `}`

### 2.4 Literals

- Number: integer or decimal
- String: double quoted text
- Identifier: letters/digits/underscore, starting with letter or underscore
- Comments: `#` to end of line

## 3. Syntax (Implemented Form)

### Program

A program is zero or more quest declarations followed by statements.

### Declarations and Assignments

```adventurescript
item potion = 3 qty;
stat player_hp = 100 hp;
player_hp = player_hp + 10 hp;
```

### Operations

```adventurescript
combine herb with potion;
equip player_hp to 120 hp;
rest 2 turns;
narrate "A shadow moves...";
show player_hp;
power_up potion by 2;
acquire key to inventory;
discard broken_key;
```

### Control Flow

```adventurescript
loop 3 iterations {
    narrate "Exploring...";
}

if player_hp > 0 then {
    narrate "Still alive";
} else {
    narrate "Defeated";
}

if player_hp > 0 then
    narrate "Still alive";
else
    narrate "Defeated";
end
```

### Quests

```adventurescript
quest heal(stat hp_value) returns hp {
    return hp_value;
}

heal(player_hp);
```

### Input

```adventurescript
input difficulty;
```

## 4. Formal Syntax Specification (EBNF)

```
<Program>           → <Quest>* <Statement>*

<Quest>             → 'quest' IDENTIFIER '(' <ParamList>? ')' 'returns' UNIT '{' <Statement>* '}'

<ParamList>         → <Type> IDENTIFIER (',' <Type> IDENTIFIER)*

<Statement>         → <Declaration> 
                    | <Assignment> 
                    | <Operation> 
                    | <LoopStmt> 
                    | <ConditionalStmt> 
                    | <ReturnStmt>
                    | <InputStmt>

<Declaration>       → <Type> IDENTIFIER '=' <Expr> UNIT ';'

<Type>              → 'item' | 'stat' | 'text'

<Assignment>        → IDENTIFIER '=' <Expr> UNIT ';'

<Expr>              → <Term> (('+' | '-') <Term>)*

<Term>              → <Factor> (('*' | '/') <Factor>)*

<Factor>            → NUMBER 
                    | IDENTIFIER 
                    | '(' <Expr> ')'

<Condition>         → <Expr> <CompOp> <Expr>

<CompOp>            → '==' | '!=' | '>' | '<' | '>=' | '<='

<Operation>         → 'combine' IDENTIFIER 'with' IDENTIFIER ';'
                    | 'equip' IDENTIFIER 'to' <Expr> UNIT ';'
                    | 'rest' <Expr> UNIT ';'
                    | 'narrate' STRING ';'
                    | 'show' IDENTIFIER ';'
                    | 'power_up' IDENTIFIER 'by' <Expr> ';'
                    | 'acquire' IDENTIFIER 'to' 'inventory' ';'
                    | 'discard' IDENTIFIER ';'

<LoopStmt>          → 'loop' NUMBER 'iterations' '{' <Statement>* '}'

<ConditionalStmt>   → 'if' <Condition> 'then' '{' <Statement>* '}' ('else' '{' <Statement>* '}')?
                    | 'if' <Condition> 'then' <Statement> 'else' <Statement> 'end'

<ReturnStmt>        → 'return' IDENTIFIER ';'

<InputStmt>         → 'input' IDENTIFIER ';'

UNIT                → 'qty' | 'hp' | 'mp' | 'turns' | 'seconds' | 'hours'

NUMBER              → [0-9]+ ('.' [0-9]+)?

STRING              → '"' ([^"\\] | '\\' .)* '"'

IDENTIFIER          → [a-zA-Z_] [a-zA-Z0-9_]*

COMMENT             → '#' [^\n]* '\n'
```

---

## 5. Memory Model

### Variables and Storage

- **Variable Declaration:** Variables are declared with a type and unit: `item potion = 5 qty;`
- **Storage:** Variables are stored in a runtime memory map as `Value` objects containing:
  - **Numeric value:** The actual number (e.g., 5, 100)
  - **Unit:** The measurement unit (e.g., qty, hp, mp, turns)
- **Type Information:** Each variable maintains type information (item, stat, text) alongside its numeric value and unit

### Scope Management

- **Global Scope:** Top-level variables accessible throughout the program
- **Local Scope:** Variables declared within blocks (loops, conditionals, quests) are local to that block
- **Scope Stack:** The semantic analyzer uses a scope stack to manage variable visibility:
  - When entering a block (loop, if, quest), a new scope is pushed
  - When exiting a block, the scope is popped
  - Variable lookup searches the scope stack from current scope upward

**Scope Rules:**
- Variables in inner scopes can shadow outer scope variables
- Variables declared in a block are inaccessible after the block exits
- Quest parameters create their own scope within the quest body
- All variables must be declared before use

### Allocation Strategy

- **Compile-Time:** Type checking and semantic validation occur at compile time
- **Runtime:** Variables are allocated in memory when initialized with a value
- **Stack-Based:** Local variables are managed through scope stack; cleaned up when scope exits
- **No Manual Deallocation:** Memory is automatically managed through scope exit

### Example Scope Behavior

```adventurescript
stat global_hp = 100 hp;           # Global scope

if global_hp > 50 hp then {        # Enter if scope
    stat local_potion = 10 qty;    # Local to if scope
    global_hp = global_hp + 10 hp; # Accessible (outer scope)
}                                   # Exit if scope

# local_potion is NOT accessible here (out of scope)
# global_hp is still accessible
```

---

## 6. Complete Example Programs

### Example 1: Simple Healing Quest

**File:** `example1_healing.adv`

```adventurescript
# A simple healing quest
stat player_hp = 50 hp;
item health_potion = 3 qty;

narrate "You drink a health potion";
player_hp = player_hp + 25 hp;
health_potion = health_potion - 1 qty;

show player_hp;
narrate "Potions remaining:";
show health_potion;
```

**Expected Output:**
```
You drink a health potion
Current player_hp: 75 hp
Potions remaining:
Current health_potion: 2 qty
```

**Demonstrates:** Basic declarations, arithmetic with units, narration, variable display

---

### Example 2: Combat Loop with Conditional

**File:** `example2_combat.adv`

```adventurescript
# Combat scenario with loop and conditionals
stat enemy_hp = 30 hp;
stat player_hp = 100 hp;
item weapon = 1 qty;

loop 3 iterations {
    narrate "Player attacks!";
    enemy_hp = enemy_hp - 10 hp;
}

if enemy_hp > 0 hp then {
    narrate "Enemy survived! Battle continues...";
    narrate "Current enemy HP:";
    show enemy_hp;
} else {
    narrate "Victory! Enemy defeated!";
}
```

**Expected Output:**
```
Player attacks!
Player attacks!
Player attacks!
Enemy survived! Battle continues...
Current enemy HP:
Current enemy_hp: 0 hp
```

**Demonstrates:** Loops, conditionals, comparisons, narration

---

### Example 3: Inventory Management with Combine

**File:** `example3_inventory.adv`

```adventurescript
# Inventory management and item combination
item herb = 5 qty;
item poison = 2 qty;

narrate "Starting inventory:";
show herb;
show poison;

narrate "Combining herb with poison...";
combine herb with poison;

narrate "Final inventory:";
show herb;
```

**Expected Output:**
```
Starting inventory:
Current herb: 5 qty
Current poison: 2 qty
Combining herb with poison...
Final inventory:
Current herb: 5 qty
```

**Demonstrates:** Multiple variables, combine operation, item management

---

## 7. Type System and Semantic Rules

### Type System

- **item:** Represents inventory objects (potions, weapons, keys) - measured in `qty`
- **stat:** Represents character attributes (health, mana) - measured in `hp`, `mp`, `turns`
- **text:** Represents string literals - used in narration and output

### Type Checking Rules

1. **Operation Type Compatibility:**
   - `combine` requires two `item` operands
   - `equip` requires a `stat` and compatible unit
   - `rest` requires a time unit (turns, seconds, hours)
   - Arithmetic operations require compatible units (hp + hp, qty + qty)

2. **Unit Compatibility:**
   - Same units can be added/subtracted (hp + hp = hp, qty + qty = qty)
   - Different units cannot be mixed (hp + qty = error)
   - All operations preserve unit type

3. **Variable Declaration:**
   - Type must be specified: `item name` or `stat name`
   - Initial value and unit required: `= value unit`
   - Type is fixed after declaration

---

## 8. Error Handling Strategy

### Syntax Error Reporting

Syntax errors occur during lexical analysis and parsing. Reported with:
- **Format:** `SyntaxError at line X, column Y: error message`
- **Location:** Exact line and column where error was detected
- **Cause:** Grammar violation

**Examples:**
```
SyntaxError at line 5, column 10:
  Unexpected token: IDENTIFIER where SEMICOLON expected
```

```
SyntaxError at line 8, column 1:
  Unexpected end of file in loop block
```

### Semantic Error Reporting

Semantic errors occur during semantic analysis. Reported with:
- **Format:** `SemanticError at line X: error message`
- **Type:** Type checking, scope, or validation violation
- **Cause:** Program violates semantic rules

**Common Semantic Errors:**

1. **Undefined Variable:**
   ```
   SemanticError at line 3: Variable 'player_hp' used before declaration
   ```

2. **Redeclaration:**
   ```
   SemanticError at line 5: Variable 'potion' already declared in this scope
   ```

3. **Type Mismatch:**
   ```
   SemanticError at line 7: Cannot combine stat type with item type
   ```

4. **Unit Incompatibility:**
   ```
   SemanticError at line 4: Cannot add hp to qty (incompatible units)
   ```

5. **Invalid Operation:**
   ```
   SemanticError at line 6: 'rest' operation requires time unit (turns, seconds, hours)
   ```

### Runtime Error Reporting

Runtime errors occur during execution. Reported with:
- **Format:** `RuntimeError: error message`
- **Cause:** Logic or execution error

**Examples:**
```
RuntimeError: Division by zero in expression
```

### Error Recovery Strategy

- **Single-Error Reporting:** Parser reports first syntax error and stops
- **Multiple Semantic Errors:** Semantic analyzer collects all errors and reports together
- **Error Context:** All errors include line numbers for source mapping
- **User-Friendly Messages:** Error messages explain the problem and suggest fixes

---

## 9. Execution Model

LootCode source is compiled through six phases:

1. **Lexical Analysis:** Source code → Tokens
2. **Syntax Analysis:** Tokens → Abstract Syntax Tree (AST)
3. **Semantic Analysis:** AST → Validated AST + Symbol Table
4. **Intermediate Code Generation:** AST → Three-Address Code (TAC)
5. **Optimization:** TAC → Optimized TAC
6. **Execution:** Optimized TAC → Program Output

---

## 10. CLI Usage

- Compile/run: `python adventurescript.py file.adv`
- Debug phases: `python adventurescript.py file.adv --debug`
- Export TAC: `python adventurescript.py file.adv -o output.tac`
- Interactive: `python adventurescript.py --interactive`
