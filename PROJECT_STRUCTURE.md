# RecipeScript Compiler - Project Structure

## 📁 Directory Organization

```
recipescript/
├── ll1/                          # LL(1) Parser Files
│   ├── ll1_parser_generator.py   # Full LL(1) implementation
│   ├── ll1_mini_grammar.py       # Mini grammar generator
│   ├── ll1_parsing_table.xlsx    # Full grammar (38 NT, 59 T)
│   ├── ll1_mini_parsing_table.xlsx # Mini grammar (12 NT, 13 T)
│   ├── LL1_PARSER_README.md      # Documentation
│   └── verify_parsing_table.py   # Verification script
│
├── clr/                          # CLR(1) Parser Files
│   ├── clr_parser_generator.py   # Full CLR(1) implementation
│   ├── clr_mini_recipescript.py  # Mini grammar generator
│   ├── clr_mini_recipescript.xlsx # Mini grammar (18 states)
│   ├── test_full_grammar.py      # Full grammar test (163 states)
│   ├── CLR_FINAL_SUMMARY.md      # Documentation
│   └── CLR_PARSER_README.md      # Documentation
│
├── src/                          # Compiler Source Code
│   ├── lexer.py                  # Lexical analyzer
│   ├── parser.py                 # Syntax analyzer (AST)
│   ├── semantic_analyzer.py      # Semantic analyzer
│   ├── intermediate_code.py      # TAC generator
│   ├── optimizer.py              # Code optimizer
│   ├── code_generator.py         # Code generator
│   ├── compiler.py               # Main compiler
│   └── token_types.py            # Token definitions
│
├── docs/                         # Documentation
│   ├── CHART_1_GRAMMAR.md        # Grammar chart
│   ├── CHART_2_LEXER_DFA.md      # Lexer DFA chart
│   ├── CHART_3_SYMBOL_TABLE.md   # Symbol table chart
│   ├── CHART_4_TOP_DOWN_PARSING.md # Top-down parsing chart
│   ├── CHART_5_BOTTOM_UP_PARSING.md # Bottom-up parsing chart
│   ├── CHART_6_INTERMEDIATE_CODE.md # Intermediate code chart
│   ├── CHART_7_COMPLETE_COMPILATION.md # Complete compilation chart
│   ├── CHART_8_AST.md            # AST chart
│   ├── CHART_9_TAC.md            # TAC chart
│   ├── CHART_PAPERS_GUIDE.md     # Chart paper guide
│   ├── LANGUAGE_SPEC.md          # Language specification
│   ├── PROJECT_OVERVIEW.md       # Project overview
│   └── ...
│
├── examples/                     # Example programs
│   ├── bread.recipe
│   ├── chocolate_cookies.recipe
│   ├── pasta.recipe
│   └── pizza.recipe
│
├── tests/                        # Test files
│   ├── test1.recipe
│   ├── test2.recipe
│   └── ...
│
├── recipescript.py               # Main compiler entry point
├── FINAL_ANSWER.md               # ✅ CLR(1) Test Results
├── PROJECT_STRUCTURE.md          # This file
└── README.md                     # Project README
```

---

## 📊 Key Results

### LL(1) Parser:
- ✅ Full grammar: 38 non-terminals, 59 terminals
- ✅ Mini grammar: 12 non-terminals, 13 terminals
- ✅ No conflicts
- ✅ Excel files with FIRST, FOLLOW, NULLABLE, Parsing Table

### CLR(1) Parser:
- ✅ Full grammar: 163 states, 464 transitions
- ✅ Mini grammar: 18 states, 19 transitions
- ✅ No conflicts
- ✅ Excel files with Grammar, States, Transitions, ACTION, GOTO

---

## 🎯 For Chart Paper Presentation

### Use These Files:

**LL(1) Predictive Parser:**
- `ll1/ll1_mini_parsing_table.xlsx`
- Shows: NULLABLE, FIRST, FOLLOW, Parsing Table
- Size: 12×13 (manageable for chart)

**CLR(1) Bottom-Up Parser:**
- `clr/clr_mini_recipescript.xlsx`
- Shows: Grammar, States, Transitions, ACTION, GOTO
- Size: 18 states (perfect for chart)

---

## ✅ Final Answer

**Is the whole grammar CLR parsable?**

### YES! ✅

- Full grammar: 163 states, 0 conflicts
- Mini grammar: 18 states, 0 conflicts
- Both LL(1) and CLR(1) parsable
- Ready for presentation

---
