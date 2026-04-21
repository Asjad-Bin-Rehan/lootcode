# LootCode Language Specification

## 1. Overview

LootCode is an adventure-themed DSL for scripting text-based gameplay behavior.
Programs declare values, perform adventure operations, and use control flow.

## 2. Lexical Elements

### 2.1 Core Keywords

- Types: `item`, `stat`, `text`
- Operations: `combine`, `equip`, `rest`, `narrate`, `show`, `power_up`, `acquire`
- Control: `loop`, `iterations`, `if`, `then`, `else`
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
```

### Quests

```adventurescript
quest heal(stat hp_value) returns stat {
    return hp_value;
}

heal(player_hp);
```

### Input

```adventurescript
input difficulty;
```

## 4. Semantic Notes

- Variables must be declared before use.
- `combine` expects declared `item` operands.
- `loop` count must be positive.
- `rest` duration must be non-negative.
- Runtime arithmetic/comparisons are unit-aware and reject incompatible unit operations.

## 5. Execution Model

LootCode source is compiled through lexer, parser, semantic analysis, TAC generation, optimization, then TAC execution.

## 6. CLI Usage

- Compile/run: `python adventurescript.py file.adv`
- Debug phases: `python adventurescript.py file.adv --debug`
- Export TAC: `python adventurescript.py file.adv -o output.tac`
- Interactive: `python adventurescript.py --interactive`
