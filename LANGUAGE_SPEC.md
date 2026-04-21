# RecipeScript Language Specification

## 1. Overview

RecipeScript is a domain-specific language for cooking recipe automation. It provides structured syntax for defining ingredients, cooking operations, timing, and serving instructions.

## 2. Lexical Specification

### 2.1 Keywords
```
Data Types: ingredient, time, temp, quantity, text
Operations: mix, heat, wait, serve, scale, add, remove
Control Flow: repeat, foreach, when, then, else, times, in
Functions: recipe, return, returns
Input/Output: input
Prepositions: to, with, for, at, from, by
Units (Volume): cups, tbsp, tsp, ml, oz
Units (Weight): grams, lbs
Units (Temperature): F, C
Units (Time): minutes, seconds, hours
```

### 2.2 Operators
```
=   Assignment
+   Addition
-   Subtraction
*   Multiplication
/   Division
==  Equal
!=  Not equal
>   Greater than
<   Less than
>=  Greater or equal
<=  Less or equal
```

### 2.3 Delimiters
```
;   Statement terminator
,   Separator
( ) Parentheses
{ } Braces
```

### 2.4 Literals

**Numeric Literals:**
```
Integer: [0-9]+
Float: [0-9]+\.[0-9]+
Examples: 2, 3.5, 100, 0.25
```

**Text Literals:**
```
"[characters]*"
Examples: "Mix well", "Preheat oven"
```

**Unit Literals:**
```
cups, tbsp, tsp, grams, ml, oz, lbs
F, C (temperature)
minutes, seconds, hours (time)
```

### 2.5 Identifiers
```
[a-zA-Z_][a-zA-Z0-9_]*
Examples: flour, sugar, oven_temp, mix1
```

### 2.6 Comments
```
# This is a single-line comment
```

## 3. Syntax Specification (BNF Grammar)

**Note:** This grammar is LL(1) compatible with left recursion eliminated.

```bnf
<program> ::= <recipe_list> <statement_list>
            | <recipe_list>
            | <statement_list>

<recipe_list> ::= <recipe_decl> <recipe_list>
                | <recipe_decl>

<recipe_decl> ::= "recipe" IDENTIFIER "(" <param_list> ")" "{" <statement_list> "}"
                | "recipe" IDENTIFIER "(" <param_list> ")" "returns" <type> "{" <statement_list> "}"

<param_list> ::= <parameter> <param_list'>
               | ε

<param_list'> ::= "," <parameter> <param_list'>
                | ε

<parameter> ::= <type> IDENTIFIER

<statement_list> ::= <statement> <statement_list>
                   | <statement>

<statement> ::= <input_stmt> ";"
              | <declaration> ";"
              | <operation> ";"
              | <control_flow>
              | <recipe_call> ";"
              | <return_stmt> ";"

<recipe_call> ::= IDENTIFIER "(" <arg_list> ")"

<arg_list> ::= <expression> <arg_list'>
             | ε

<arg_list'> ::= "," <expression> <arg_list'>
              | ε

<return_stmt> ::= "return" <expression>
                | "return"

<input_stmt> ::= "input" IDENTIFIER

<declaration> ::= <type> IDENTIFIER "=" <value>

<type> ::= "ingredient" | "time" | "temp" | "quantity" | "text"

<value> ::= <expression> <value_tail>
          | STRING

<value_tail> ::= <unit>
               | ε

<unit> ::= "cups" | "tbsp" | "tsp" | "grams" | "ml" | "oz" | "lbs"
         | "F" | "C"
         | "minutes" | "seconds" | "hours"

<operation> ::= "mix" <ingredient_list>
              | "heat" IDENTIFIER "to" <value>
              | "wait" <value>
              | "serve" STRING
              | "display" IDENTIFIER
              | "add" IDENTIFIER "to" IDENTIFIER
              | "scale" IDENTIFIER "by" NUMBER

<ingredient_list> ::= IDENTIFIER <ingredient_list'>

<ingredient_list'> ::= "with" IDENTIFIER <ingredient_list'>
                     | ε

<control_flow> ::= <repeat_stmt>
                 | <foreach_stmt>
                 | <when_stmt>

<repeat_stmt> ::= "repeat" NUMBER "times" "{" <statement_list> "}"

<foreach_stmt> ::= "foreach" IDENTIFIER "in" IDENTIFIER "{" <statement_list> "}"

<when_stmt> ::= "when" <condition> "then" "{" <statement_list> "}" <when_tail>

<when_tail> ::= "else" "{" <statement_list> "}"
              | ε

<condition> ::= <expression> <comparison_op> <expression>

<comparison_op> ::= "==" | "!=" | ">" | "<" | ">=" | "<="

<expression> ::= <term> <expression'>

<expression'> ::= "+" <term> <expression'>
                | "-" <term> <expression'>
                | ε

<term> ::= <factor> <term'>

<term'> ::= "*" <factor> <term'>
          | "/" <factor> <term'>
          | ε

<factor> ::= NUMBER
           | IDENTIFIER
           | "(" <expression> ")"
           | <recipe_call>
```

### Terminal Symbols (Tokens from Lexer)
```
NUMBER      - Integer or floating-point literal: [0-9]+ | [0-9]+\.[0-9]+
IDENTIFIER  - Variable/function name: [a-zA-Z_][a-zA-Z0-9_]*
STRING      - Text literal: "[^"]*"
```

### Lexical Notes
- **Comments:** `#` followed by any characters until newline. Handled by lexer; ignored by parser.
- **Whitespace:** Spaces, tabs, newlines are ignored by lexer.
- **Keywords:** Reserved words like `recipe`, `return`, `ingredient`, etc. are recognized by lexer.
```

## 4. Semantic Rules

### 4.1 Type System

**Primitive Types:**
- `ingredient` - Food ingredients with quantities
- `time` - Duration values (minutes, seconds, hours)
- `temp` - Temperature values (F, C)
- `quantity` - Numeric amounts with units
- `text` - String values

### 4.2 Type Compatibility

**Allowed Operations:**
- `ingredient` can be mixed, added, scaled
- `time` can be added, subtracted
- `temp` can be compared
- `quantity` supports arithmetic operations

### 4.3 Scope Rules

- Global scope for all declarations
- Block scope for control structures
- Variables must be declared before use

### 4.4 Semantic Checks

1. Ingredient must be declared before mixing
2. Temperature must be valid (0-500 F or 0-260 C)
3. Time must be positive
4. Quantity must be positive
5. Type compatibility in operations

## 5. Example Programs

### Example 1: Scalable Recipe with Input
```recipe
# Dynamic recipe that scales based on servings
input servings;

ingredient flour = 0.5 * servings cups;
ingredient sugar = 0.25 * servings cups;
temp oven = 350 F;

heat oven to 350 F;
mix flour with sugar;
wait 15 minutes;
serve "Cookies ready!";
```

### Example 2: Simple Cookie Recipe
```recipe
ingredient flour = 2 cups;
ingredient sugar = 1 cup;
ingredient butter = 0.5 cups;
temp oven = 350 F;

heat oven to 350 F;
mix flour with sugar with butter;
wait 15 minutes;
serve "Cookies ready!";
```

### Example 2: Scaled Recipe
```recipe
ingredient rice = 1 cups;
quantity servings = 4;

scale rice by 2;
wait 20 minutes;
serve "Rice for 8 people";
```

### Example 3: Conditional Cooking
```recipe
temp current = 300 F;
temp target = 350 F;

when current < target then {
    heat oven to 350 F;
    wait 10 minutes;
}
serve "Oven ready";
```

### Example 4: Repeated Steps
```recipe
ingredient dough = 1 lbs;

repeat 3 times {
    mix dough;
    wait 5 minutes;
}
serve "Dough kneaded";
```

### Example 5: Recipe Functions
```recipe
recipe make_dough(ingredient flour, ingredient water) returns ingredient {
    mix flour with water;
    wait 30 minutes;
    return flour;
}

ingredient flour = 2 cups;
ingredient water = 1 cups;
ingredient dough = make_dough(flour, water);
serve "Dough ready!";
```

## 6. Compiler Phases

### Phase 1: Lexical Analysis
- Tokenize recipe instructions
- Recognize keywords, units, identifiers
- Handle comments

### Phase 2: Syntax Analysis
- Build parse tree
- Validate grammar rules
- Create AST

### Phase 3: Semantic Analysis
- Type checking
- Symbol table construction
- Validate ingredient usage

### Phase 4: Intermediate Code Generation
- Generate three-address code
- Translate operations to TAC

### Phase 5: Optimization
- Constant folding
- Dead code elimination
- Instruction reordering

### Phase 6: Code Generation
- Generate executable instructions
- Produce recipe execution plan

## 7. Error Handling

### Lexical Errors
- Invalid character
- Unterminated string
- Invalid number format

### Syntax Errors
- Missing semicolon
- Unexpected token
- Unmatched braces

### Semantic Errors
- Undeclared ingredient
- Type mismatch
- Invalid temperature range
- Negative time/quantity

### Runtime Errors
- Division by zero
- Invalid operation
- Missing ingredient

## 8. File Extension
- `.recipe` - RecipeScript source files

## 9. Recipe Functions

RecipeScript supports reusable recipe functions using the `recipe` keyword:

### Function Declaration
```recipe
recipe make_dough(ingredient flour, ingredient water) returns ingredient {
    mix flour with water;
    return flour;
}
```

### Function Call
```recipe
ingredient my_dough = make_dough(flour, water);
```

### Features:
- Parameters with type declarations
- Optional return type with `returns` keyword
- Return statement to return values
- Functions without return type act as procedures

### Example:
```recipe
recipe double_quantity(quantity x) returns quantity {
    quantity result = x * 2;
    return result;
}

quantity servings = 4;
quantity doubled = double_quantity(servings);
display doubled;  # Shows: 8
```

## 10. Future Enhancements
1. Ingredient substitution rules
2. Nutritional calculation
3. Multi-recipe meal planning
4. Shopping list generation
5. Timing optimization
6. Recipe import/export
7. Unit conversion automation
8. Nested recipe calls
9. Recipe overloading
