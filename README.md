# RecipeScript Compiler

A domain-specific language (DSL) compiler for cooking recipe automation and meal planning.
---

## 🎯 Project Overview

RecipeScript is a complete compiler implementation for CS4031 Compiler Construction course. It demonstrates all six phases of compilation for a practical, domain-specific language designed for cooking recipes.

### Why RecipeScript?

- **Unique Domain**: Cooking recipe automation (completely different from typical languages)
- **Natural Syntax**: Easy-to-read commands like "mix flour with sugar"
- **Type Safety**: Domain-specific validation (temperature ranges, ingredient types)
- **Practical Application**: Real-world use in smart kitchens and meal planning

---

## 🚀 Quick Start

### Run a Test Recipe
```bash
python recipescript.py tests/test1.recipe
```

### Run All Tests
```bash
cd tests
python run_all_tests.py
```

### Interactive Mode
```bash
python recipescript.py
>>> ingredient flour = 2 cups;
>>> serve "Hello RecipeScript!";
>>> exit
```

---

## 📝 Language Features

### Data Types
```recipe
ingredient flour = 2 cups;      # Food ingredients with quantities
temp oven = 350 F;              # Temperature (F or C)
time duration = 30 minutes;     # Time duration
quantity servings = 4;          # Numeric quantities
text message = "Ready!";        # Text strings
```

### Input Parameters
```recipe
input servings;                     # Get user input
ingredient flour = 0.5 * servings cups;  # Dynamic calculation
serve "Recipe for servings people!";     # Scalable recipes
```

### Recipe Functions
```recipe
recipe make_dough(ingredient flour, ingredient water) returns ingredient {
    mix flour with water;
    wait 30 minutes;
    return flour;
}

ingredient flour = 2 cups;
ingredient water = 1 cups;
ingredient dough = make_dough(flour, water);  # Call recipe function
serve "Dough ready!";
```

### Operations
```recipe
mix flour with sugar with butter;   # Combine ingredients
heat oven to 350 F;                 # Set temperature
wait 15 minutes;                    # Timing control
serve "Cookies ready!";             # Output message
scale flour by 2;                   # Adjust quantities
add sugar to flour;                 # Add ingredient
display servings;                   # Show variable value
```

### Control Flow
```recipe
# Repeat loops
repeat 3 times {
    mix dough;
    wait 5 minutes;
}

# Conditionals
when temp < 350 then {
    heat oven to 350 F;
} else {
    serve "Already hot!";
}
```

### Units Supported
- **Volume**: cups, tbsp, tsp, ml, oz
- **Weight**: grams, lbs
- **Temperature**: F (Fahrenheit), C (Celsius)
- **Time**: minutes, seconds, hours

---

## 🏗️ Compiler Architecture

### All 6 Phases Implemented:

1. **Lexical Analysis** (`lexer.py`)
   - Tokenization with unit recognition
   - Multi-character operators
   - Comment handling
   - Line/column tracking

2. **Syntax Analysis** (`parser.py`)
   - Recursive descent parser
   - AST construction
   - Natural language syntax support
   - Error recovery

3. **Semantic Analysis** (`semantic_analyzer.py`)
   - Symbol table with scoping
   - Type checking
   - Domain validation (temp ranges, etc.)
   - Semantic error detection

4. **Intermediate Code** (`intermediate_code.py`)
   - Three-address code generation
   - Temporary variables
   - Label management
   - Control flow translation

5. **Optimization** (`optimizer.py`)
   - Constant folding
   - Dead code elimination
   - Extensible framework

6. **Code Generation** (`code_generator.py`)
   - TAC interpreter
   - Variable storage
   - Control flow execution
   - Recipe operation execution

---

## 🔧 Project Structure

```
recipescript-compiler/
├── recipescript.py              # Main entry point - Run this!
├── README.md                    # This file
│
├── src/                         # Source code
│   ├── compiler.py              # Main compiler
│   ├── lexer.py                 # Phase 1: Lexical analysis
│   ├── parser.py                # Phase 2: Syntax analysis
│   ├── semantic_analyzer.py     # Phase 3: Semantic analysis
│   ├── intermediate_code.py     # Phase 4: TAC generation
│   ├── optimizer.py             # Phase 5: Optimization
│   ├── code_generator.py        # Phase 6: Code generation
│   └── token_types.py           # Token definitions
│
├── tests/                       # Test files
    ├── name.recipe
    └── run_all_tests.py         # All test runner
```

---

## 🌟 What Makes RecipeScript Unique

### Compared to Similar Projects:

| Feature | RecipeScript | Typical Languages |
|---------|--------------|-------------------|
| **Domain** | Cooking recipes | General purpose |
| **Keywords** | mix, heat, serve, wait | print, if, while |
| **Types** | ingredient, temp, time | int, float, string |
| **Syntax** | Natural language | C-like |
| **Units** | Built-in (cups, F, minutes) | None |
| **Validation** | Domain-specific (temp ranges) | Generic |

### Key Innovations:
1. **Natural language syntax** - "mix flour with sugar"
2. **Domain-specific types** - ingredient, temp, time
3. **Built-in unit system** - cups, F, minutes, etc.
4. **Recipe operations** - mix, heat, wait, serve, scale
5. **Safety validation** - Temperature ranges, positive values
6. **Practical application** - Real-world cooking automation

---

## 💡 Usage Examples

### Command Line
```bash
# Compile and run a recipe
python recipescript.py my_recipe.recipe

# See all 6 phases
python recipescript.py tests/test1.recipe

# Run test suite
cd tests
python run_all_tests.py
```

### Interactive REPL
```bash
python recipescript.py
>>> ingredient pasta = 500 grams;
>>> temp water = 212 F;
>>> heat water to 212 F;
>>> wait 10 minutes;
>>> serve "Pasta ready!";
>>> exit
```
---

**RecipeScript - Making Cooking Computable** 🍳👨‍💻

*A complete compiler implementation demonstrating all phases of compilation for a practical domain-specific language.*