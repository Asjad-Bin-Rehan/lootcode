# Team Reflection: LootCode Compiler Project

**Course:** CS4031 Compiler Construction  
**Project:** LootCode - An 8-Bit Adventure Language Compiler  
**Date:** May 10, 2026  
**Team Members:** [member 1] [member 2] [member 3]

---

## Challenges Faced and Solutions

### Challenge 1: Unit Preservation

**Problem:** Values in LootCode carry units (`hp`, `qty`, `turns`). Example: `stat hp = 100 hp`. Units must survive through arithmetic, assignments, TAC, optimization, and execution without being lost.

**Solution:** Created a `Value` class pairing numbers with units:
```python
class Value:
    numeric = 100
    unit = "hp"
```
Units are checked during semantic analysis (hp + hp = valid, hp + qty = invalid) and preserved through all phases.

**Result:** Type-safe adventure scripts with proper unit tracking ✓

---

### Challenge 2: Scope and Variable Management

**Problem:** LootCode supports nested blocks (loops in conditionals, etc.). Need to track variables at different scope levels, prevent redeclaration, and resolve references correctly.

**Solution:** Implemented a scope stack in the symbol table:
```python
class SymbolTable:
    scopes = [{}]  # Stack of dictionaries
    
    enter_scope()  # When entering block
    exit_scope()   # When exiting block
    lookup(name)   # Search stack from top down
```
Each block (loop, if, quest) enters a new scope on entry and exits on exit. Variables are only visible in their scope and below.

**Result:** Proper variable scoping with no leakage ✓

---

### Challenge 3: Control Flow to Three-Address Code

**Problem:** Translating loops and conditionals to TAC with labels and jumps is error-prone. Label conflicts, incorrect jumps, and counter mismanagement can cause infinite loops or wrong execution.

**Solution:** Used templates for systematic TAC generation:
- **Loop template:** Initialize counter → Check condition → Jump to end → Execute body → Increment counter → Jump back → End label
- **Conditional template:** Evaluate condition → Jump to else if false → Execute then → Jump to end → Else label → Else branch → End label

Label generation is systematic (L0, L1, L2...) to avoid conflicts.

**Result:** Correct control flow translation with proper jumps ✓

---

## What We Learned

### 1. Separation of Concerns is Critical
The 6-phase architecture was invaluable. Bugs were easy to locate because each phase had one job. Testing phases independently caught errors early.

### 2. Intermediate Representations Matter
TAC was a crucial bridge between high-level code and execution. It made optimization straightforward and debugging easy.

### 3. Type Systems Are Complex
LootCode's unit system taught us that types aren't just categories. Unit preservation and type checking required careful design.

### 4. Semantic Analysis is the Gatekeeper
Most user errors (undefined variables, type mismatches) appear at semantic time, not during parsing.

### 5. Testing is Essential
Our 12-test suite caught numerous bugs in parser, semantic, optimization, and integration phases. Testing incrementally exposed edge cases.

### 6. Compiler Development is Iterative
We built incrementally: minimal compiler first, tested, added features, fixed bugs, refactored. Mistakes were expected and learned from.

### 7. Optimization is a Trade-Off
Aggressive optimization risks breaking semantics. We chose conservative optimization (constant folding, dead code elimination) where correctness was guaranteed.

---

## Future Improvements

1. **Advanced Optimization:** Loop-invariant code hoisting, common subexpression elimination, better constant propagation
2. **Extended Language Features:** String manipulation, arrays/dictionaries, function parameters, exception handling
3. **Debugging Support:** Breakpoints, variable inspection, step-through execution
4. **Standard Library:** Built-in functions for common operations and reusable game mechanics
5. **Performance:** Bytecode compilation, JIT compilation for faster execution
6. **Module System:** Import/export for code reuse across files
7. **IDE Support:** Syntax highlighting, language server protocol integration

---

## Individual Contributions

### [member 1] - Frontend (Phases 1-2)
**Lexer and Parser Implementation**
- Designed recursive descent parser
- Implemented tokenization and AST construction
- Created error recovery with line/column reporting
- Authored all 12 test programs

### [member 2] - Semantic Analysis (Phase 3)
**Type Checking and Symbol Table**
- Implemented scope stack for variable management
- Designed unit preservation mechanism
- Created type checking and validation rules
- Extensively tested semantic edge cases

### [member 3] - Backend (Phases 4-6)
**Intermediate Code, Optimization, Execution**
- Designed TAC instruction format
- Implemented optimizer (constant folding, dead code elimination)
- Built execution engine with proper state management
- Integrated all phases into cohesive pipeline

### Team Achievements
- Complete 6-phase compiler with clear separation of concerns
- Comprehensive test suite (12 programs covering all features)
- Language specification and architecture documentation
- Clean, readable, well-commented codebase
- Regular code reviews, knowledge sharing, collaborative debugging

---

## Conclusion

The LootCode compiler project demonstrated core compiler design concepts through a complete 6-phase pipeline. By tackling real challenges—unit preservation, scope management, control flow translation—we learned that building a compiler is achievable and deeply educational. The six-phase architecture proved invaluable for managing complexity, and our comprehensive test suite ensured correctness. Team collaboration, iterative development, and continuous testing were essential to success.
