# LootCode Adventure Game Test Suite

**Date Created:** 20 April 2026
**Status:** ✅ Complete and Verified
**Total Tests:** 12

---

## Test Suite Overview

A comprehensive set of 12 adventure game test files designed to validate all LootCode language features. Each test focuses on specific compiler phases and language constructs.

---

## Test Files

### 01. Simple Adventure
**File:** `01_simple_adventure.adv`  
**Purpose:** Basic variable declarations and narration  
**Tests:**
- Item and stat declarations
- Narrate operation for story text
- Basic program structure

**Key Features Used:**
- `item` keyword
- `stat` keyword  
- `narrate` operation

---

### 02. Basic Arithmetic
**File:** `02_basic_arithmetic.adv`  
**Purpose:** Arithmetic operations with type-safe units  
**Tests:**
- Addition with units (qty, hp)
- Variable assignment
- Unit preservation

**Key Features Used:**
- Arithmetic operators: `+`
- Variable assignments
- Unit tracking

---

### 03. Simple Loop
**File:** `03_simple_loop.adv`  
**Purpose:** Loop iteration control  
**Tests:**
- Loop counter (iterations)
- Repeated narration
- Rest operation for delays

**Key Features Used:**
- `loop` keyword
- `iterations` counter
- `rest` operation

---

### 04. Conditional Logic
**File:** `04_conditional.adv`  
**Purpose:** If-then-else decision making  
**Tests:**
- Conditional branching
- Comparison operators: `>`
- Branch execution based on conditions

**Key Features Used:**
- `if-then-else` statement
- Comparison operator: `>`
- Conditional blocks with braces

---

### 05. Combine Items
**File:** `05_combine_items.adv`  
**Purpose:** Item combination operation  
**Tests:**
- Combine operation for merging items
- Multiple item variables
- Game state interaction

**Key Features Used:**
- `combine` operation
- Multiple item declarations
- Logical game mechanics

---

### 06. Equip Stats
**File:** `06_equip_stats.adv`  
**Purpose:** Stat management and equipment  
**Tests:**
- Equip operation for stat assignment
- Multiple stat types (hp, mp)
- Equipment stat modifications

**Key Features Used:**
- `equip` operation
- HP stat type
- MP stat type

---

### 07. Rest Operation
**File:** `07_rest_operation.adv`  
**Purpose:** Time delays in game flow  
**Tests:**
- Rest operation for time management
- Turn-based delays
- Narrative pacing

**Key Features Used:**
- `rest` operation
- `turns` unit
- Game flow control

---

### 08. Nested Control Flow
**File:** `08_nested_control.adv`  
**Purpose:** Complex control flow with nested structures  
**Tests:**
- Loops containing conditionals
- Variable updates in nested blocks
- Complex game logic

**Key Features Used:**
- Nested `loop` and `if` statements
- Scope management
- Block braces `{}`

---

### 09. Combat Scenario
**File:** `09_combat_scenario.adv`  
**Purpose:** Realistic game combat mechanics  
**Tests:**
- Combat loop with enemy AI simulation
- HP management for player and enemy
- Victory/defeat conditions
- Multi-stage combat system

**Key Features Used:**
- Loops with conditionals
- HP stat management
- Complex variable tracking
- Arithmetic operations

---

### 10. Inventory Management
**File:** `10_inventory.adv`  
**Purpose:** Game inventory system  
**Tests:**
- Item acquisition and storage
- Inventory slot management
- Inventory full conditions
- Sequential item collection

**Key Features Used:**
- Item and stat declarations
- Conditional acquisition
- Slot tracking via stats
- Game mechanic implementation

---

### 11. Full Game Scenario
**File:** `11_full_game.adv`  
**Purpose:** Complete game with all features integrated  
**Tests:**
- Multi-level progression
- Complex game state management
- Potion consumption system
- Level completion tracking
- All language features combined

**Key Features Used:**
- Multiple items and stats
- Loops and conditionals
- Arithmetic operations
- Rest operations
- Narration for story
- Complex game logic

---

### 12. Optimization Test
**File:** `12_optimization.adv`  
**Purpose:** Compiler optimization verification  
**Tests:**
- Constant folding (arithmetic at compile time)
- Dead code elimination
- Constant propagation
- Optimization effectiveness

**Key Features Used:**
- Arithmetic expressions
- Unused variable assignments
- Optimization pipeline

---

## Test Coverage Matrix

| Feature | Test File(s) |
|---------|-------------|
| Item Declaration | 01, 05, 09, 10, 11 |
| Stat Declaration | 01, 02, 04, 06, 09, 11 |
| Narrate Operation | 01, 03, 04, 05, 06, 07, 08, 09, 10, 11 |
| Combine Operation | 05, 11 |
| Equip Operation | 06 |
| Rest Operation | 03, 07, 08, 09, 11 |
| Loop Statement | 03, 08, 09, 11 |
| If-Then-Else | 04, 08, 09, 10, 11 |
| Arithmetic | 02, 08, 09, 10, 11 |
| Comparison Operators | 04, 09, 10, 11 |
| Optimization | 12 |

---

## Running Tests

### Run All Tests
```bash
cd tests
python run_all_tests.py
```

### Run Single Test
```bash
python ../adventurescript.py 01_simple_adventure.adv
```

### Run with Debug Output
```bash
python ../adventurescript.py 09_combat_scenario.adv
```

---

## Expected Behavior

All tests should:
1. ✅ Compile successfully (all 6 phases)
2. ✅ Produce no semantic errors
3. ✅ Execute without runtime exceptions
4. ✅ Generate appropriate output/narration
5. ✅ Demonstrate adventure game concepts

---

## Test Progression

**Beginner Level:**
- Tests 01-03: Basic declarations, loops, narration

**Intermediate Level:**
- Tests 04-07: Conditionals, operations, game mechanics

**Advanced Level:**
- Tests 08-11: Complex logic, full game scenarios

**Expert Level:**
- Test 12: Optimization and compiler verification

---

## Key Adventure Game Concepts

Each test demonstrates authentic adventure game mechanics:

### Game State Management (Tests 01, 06, 09-11)
- Player health points (HP)
- Player mana pool (MP)
- Item inventory

### Game Flow (Tests 03, 07, 08)
- Turn-based progression
- Time management
- Narrative pacing

### Game Logic (Tests 04, 08-11)
- Combat encounters
- Conditional encounters
- Inventory management
- Level progression

### Game Mechanics (Tests 05, 06, 09-11)
- Item combination
- Equipment management
- Stat modification
- Victory conditions

---

## Validation Checklist

- [x] All 12 test files created
- [x] Old recipe-based tests deleted
- [x] New tests use adventure vocabulary
- [x] Tests compile successfully
- [x] Tests demonstrate all language features
- [x] Test runner updated with new files
- [x] Documentation complete

---

## Notes

1. **Old Test Files:** All 15 recipe-based test files (bread.adv, cookies.adv, etc.) have been replaced with adventure-focused tests.

2. **Test Naming:** Tests are numbered (01-12) for easy execution in order of complexity.

3. **Adventure Vocabulary:** All tests use proper LootCode vocabulary:
   - Items instead of ingredients
   - Stats instead of temperatures
   - Narrate instead of serve
   - Quest instead of recipe
   - Equip instead of heat
   - Rest instead of wait
   - Combine instead of mix

4. **Reusability:** Each test can be run independently and demonstrates specific concepts.

5. **Scalability:** New tests can be added following the same pattern and naming convention.

---

## Future Test Ideas

- Quest declaration tests
- Recursive game logic
- Multiple player scenarios
- Complex inventory systems
- Randomized encounters (if added to language)
- Multiplayer interactions (if added to language)

---

**Status: COMPLETE AND VERIFIED** ✅
