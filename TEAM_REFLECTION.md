# Team Reflection: LootCode Compiler Project

**Course:** CS4031 Compiler Construction  
**Project:** LootCode - An 8-Bit Adventure Language Compiler  
**Date:** May 10, 2026  
**Team Members:** [member 1] [member 2] [member 3]

---

## Executive Summary

The LootCode compiler project successfully implements a complete six-phase compiler for a domain-specific language (DSL) targeting text-based adventure games. Over the course of development, our team tackled significant technical challenges involving type systems, intermediate code generation, and program optimization. This reflection documents the challenges we faced, the valuable lessons learned about compiler design, and opportunities for future enhancement.

---

## Part 1: Challenges Faced and Solutions

### Challenge 1: Unit Preservation Through the Compilation Pipeline

**The Problem:**

One of the most complex aspects of LootCode is that values carry units (e.g., `hp`, `mp`, `qty`, `turns`). A variable like `player_hp = 100 hp` must maintain the "hp" unit through:
- Arithmetic operations (`player_hp + 20 hp`)
- Variable assignments (`new_hp = player_hp`)
- TAC transformations
- Optimization passes
- Runtime execution

If units were lost at any stage, the program would produce incorrect results or crash with mysterious type errors.

**Our Approach:**

1. **Design Phase:** We created a `Value` class that pairs numeric values with unit metadata:
   ```python
   class Value:
       def __init__(self, numeric, unit):
           self.numeric = numeric
           self.unit = unit
   ```

2. **Validation at Semantic Analysis:** The semantic analyzer validates unit compatibility before any operation:
   - Addition of `hp + hp` → valid, produces `hp`
   - Addition of `hp + qty` → invalid, raises type error
   - Operations store unit information in the symbol table

3. **TAC Representation:** Three-Address Code instructions carry unit annotations:
   ```
   t1 = player_hp + 20 hp
   ```

4. **Optimizer Preservation:** The optimizer's constant folding and dead code elimination specifically preserve unit information:
   ```
   Before: t1 = 2 + 3; x = t1 qty
   After:  x = 5 qty        # Unit preserved!
   ```

5. **Runtime Engine:** The code generator's memory model represents variables as `Value` objects, maintaining units throughout execution.

**Result:** Units are now correctly preserved through all compilation phases, enabling type-safe adventure game scripts.

---

### Challenge 2: Scope and Symbol Table Management for Nested Structures

**The Problem:**

LootCode supports nested control structures (loops within conditionals, conditionals within quests, etc.). This requires:
- Tracking variables at different scope levels
- Preventing redeclaration at current scope
- Resolving variable references to correct scope
- Cleaning up scope when exiting blocks
- Handling quest parameters with their own scope

For example:
```adventurescript
stat global_hp = 100 hp;
if global_hp > 50 hp then {
    stat local_potion = 10 qty;  # Different scope!
    combine local_potion with global_hp;
}
# local_potion should be inaccessible here
```

Our initial implementation used a flat symbol table, causing scope pollution where local variables leaked into parent scopes.

**Our Approach:**

1. **Scope Stack Architecture:** Implemented a stack-based symbol table:
   ```python
   class SymbolTable:
       def __init__(self):
           self.scopes = [{}]  # Stack of dictionaries
       
       def enter_scope(self):
           self.scopes.append({})
       
       def exit_scope(self):
           self.scopes.pop()
       
       def lookup(name):
           # Search from top of stack down
           for scope in reversed(self.scopes):
               if name in scope:
                   return scope[name]
           raise UndefinedVariableError(f"{name} not defined")
   ```

2. **Scope Entry/Exit Points:** Identified all points where scope changes:
   - Entering a loop body → new scope
   - Entering a conditional block → new scope
   - Entering a quest definition → new scope with parameters
   - Exiting any block → pop scope

3. **Semantic Analysis Traversal:** Modified the semantic analyzer to explicitly call `enter_scope()` and `exit_scope()` during AST traversal:
   ```python
   def analyze_loop(self, loop_node):
       self.symbol_table.enter_scope()
       for statement in loop_node.body:
           self.analyze(statement)
       self.symbol_table.exit_scope()
   ```

4. **Redeclaration Checking:** At declaration time, verify the variable doesn't exist in the **current** scope:
   ```python
   def declare(self, name, var_type, unit):
       if name in self.scopes[-1]:  # Only check current scope
           raise RedeclarationError(f"{name} already declared")
       self.scopes[-1][name] = (var_type, unit)
   ```

5. **Testing:** Created comprehensive test cases covering:
   - Global variable access from nested blocks
   - Local variable shadowing of globals
   - Proper cleanup after block exit

**Result:** Scope is now correctly managed, preventing variable leakage and enabling proper shadowing semantics.

---

### Challenge 3: Translating Control Flow to Three-Address Code

**The Problem:**

Translating high-level `loop` and `if` structures into TAC with labels and conditional jumps is error-prone:

```adventurescript
loop 3 iterations {
    player_hp = player_hp + 10 hp;
}
```

Must become:
```
L0: counter = 0
L1: if counter >= 3 goto L2
    player_hp = player_hp + 10 hp
    counter = counter + 1
    goto L1
L2: (next statement)
```

Problems we encountered:
- **Label generation conflicts:** Two loops generating the same label L1
- **Jump target errors:** Incorrect jumps causing infinite loops
- **Counter management:** Loop counter increments not placed correctly
- **Condition evaluation:** Comparing loop counters with the wrong operator
- **Dead code:** Unreachable instructions after unconditional jumps

**Our Approach:**

1. **Systematic Label Generation:** Implemented a global label counter:
   ```python
   class TACGenerator:
       def __init__(self):
           self.label_counter = 0
       
       def get_label(self):
           label = f"L{self.label_counter}"
           self.label_counter += 1
           return label
   ```

2. **TAC Template for Loops:**
   ```python
   def generate_loop(self, loop_node):
       start_label = self.get_label()
       end_label = self.get_label()
       counter = self.get_temp()
       
       # Counter initialization
       self.emit(TACInstr("ASSIGN", counter, 0, counter))
       
       # Loop condition
       self.emit(TACInstr("LABEL", start_label))
       cond_temp = self.get_temp()
       self.emit(TACInstr("BINARY_OP", counter, ">=", 
                         loop_node.iterations, cond_temp))
       self.emit(TACInstr("IF_GOTO", cond_temp, end_label))
       
       # Loop body
       for stmt in loop_node.body:
           self.generate(stmt)
       
       # Counter increment
       self.emit(TACInstr("BINARY_OP", counter, "+", 1, counter))
       self.emit(TACInstr("GOTO", start_label))
       
       # End label
       self.emit(TACInstr("LABEL", end_label))
   ```

3. **TAC Template for Conditionals:**
   ```python
   def generate_conditional(self, if_node):
       else_label = self.get_label()
       end_label = self.get_label()
       
       # Evaluate condition
       cond_result = self.generate(if_node.condition)
       
       # Jump to else if condition false
       self.emit(TACInstr("IF_GOTO", cond_result, else_label))
       
       # Then branch
       for stmt in if_node.then_branch:
           self.generate(stmt)
       self.emit(TACInstr("GOTO", end_label))
       
       # Else branch
       self.emit(TACInstr("LABEL", else_label))
       if if_node.else_branch:
           for stmt in if_node.else_branch:
               self.generate(stmt)
       
       # End
       self.emit(TACInstr("LABEL", end_label))
   ```

4. **Verification:** Added TAC validation phase to check:
   - All labels have corresponding jumps
   - All jumps target valid labels
   - No infinite loops in static analysis
   - Unreachable code detection

5. **Testing:** Created test programs with:
   - Nested loops
   - Nested conditionals
   - Complex boolean expressions
   - Loop early exit patterns

**Result:** Control flow is now correctly translated to TAC with proper label management and jump semantics.

---

## Part 2: What We Learned About Compiler Design

### Lesson 1: Separation of Concerns is Critical

The six-phase architecture proved invaluable. When we encountered bugs, separating compilation into distinct phases made debugging straightforward:

- **Bug in variable output?** Check the code generator (Phase 6), not the parser.
- **Type error?** Focus on semantic analyzer (Phase 3), not the lexer.
- **Performance issue?** Look at optimizer (Phase 5).

This separation allowed us to develop and test phases independently, catching errors early before they propagated downstream. We learned that:
- Each phase should have a single, well-defined responsibility
- Phases should be loosely coupled (one phase's output is the next phase's input)
- Testing at phase boundaries catches integration issues

### Lesson 2: Intermediate Representations Are Powerful

TAC proved to be a crucial bridge between high-level source code and execution:

- **For Optimization:** TAC's simplified structure made optimization algorithms straightforward to implement
- **For Debugging:** TAC is human-readable, making it easy to inspect intermediate results
- **For Flexibility:** We could easily add new optimizations or target multiple backends from TAC
- **For Correctness:** TAC validation helped catch subtle bugs in earlier phases

We realized that investing time in a good intermediate representation pays dividends throughout the compilation pipeline.

### Lesson 3: Type Systems Are More Complex Than Expected

LootCode's unit system taught us that types extend beyond simple categories (int, string, etc.):

- **Domain-Specific Types:** Adventure types (item, stat) have special semantics beyond general-purpose languages
- **Compound Types:** A value isn't just an "hp stat" — it's an "hp stat with numeric value 100"
- **Type Compatibility:** Unit compatibility rules can be as complex as arithmetic rules
- **Type Propagation:** Types must flow through all compilation phases correctly

This reinforced the importance of sound type checking and early error detection.

### Lesson 4: Semantic Analysis is the Real Gatekeeper

While lexical and syntax analysis are important for parsing, semantic analysis is where the "real" compilation happens:

- **Catching User Errors:** Most bugs appear at semantic time (undefined variables, type mismatches)
- **Optimization Opportunities:** Type information enables optimizations
- **Runtime Safety:** Catching errors at compile-time prevents runtime crashes

We learned that a robust semantic analyzer is worth its weight in gold.

### Lesson 5: Testing is Non-Negotiable

Our comprehensive test suite (12 programs) caught numerous bugs:

- **Parser Errors:** Tests revealed grammar misinterpretations
- **Semantic Bugs:** Tests exposed scope and type checking issues
- **Optimization Problems:** Tests verified optimizer correctness
- **Integration Issues:** End-to-end tests caught phase interactions

We learned to:
- Write tests that incrementally build complexity
- Test each language feature in isolation first, then in combination
- Create tests that expose edge cases (nested structures, complex expressions)
- Use tests as documentation of expected behavior

### Lesson 6: Compiler Development is Iterative

We didn't get it right the first time. Development involved:
- Building a minimal compiler (Phases 1-3)
- Testing with simple programs
- Adding features (Phases 4-6)
- Fixing bugs exposed by complex tests
- Refactoring for clarity

This taught us that compiler development is incremental, and accepting that mistakes will be found (and fixed) is part of the process.

### Lesson 7: Performance Optimization is a Trade-Off

The optimizer taught us about trade-offs:

- **Aggressive optimization:** Faster runtime code, but risks breaking semantics
- **Conservative optimization:** Guaranteed correctness, but misses opportunities
- **Profiling:** Some optimizations matter more than others

We chose a conservative approach, optimizing only when correctness was guaranteed (constant folding, dead code elimination).

---

## Part 3: Future Improvements

Given more time, we would prioritize the following enhancements:

### High-Priority Improvements

1. **Advanced Optimization Techniques**
   - **Common Subexpression Elimination (CSE):** Identify and eliminate redundant calculations
   - **Loop Optimization:** Hoist loop-invariant code outside loops
   - **Register Allocation:** Minimize temporary variable creation
   - **Peephole Optimization:** Local instruction sequence improvements
   - **Impact:** Significant performance improvements for complex adventures

2. **Enhanced Error Recovery**
   - **Multiple Error Reporting:** Collect and report all errors, not just the first
   - **Error Suggestions:** Propose fixes for common mistakes
   - **Error Locations:** Improved source mapping with line/column highlighting
   - **Impact:** Better developer experience during debugging

3. **Extended Language Features**
   - **String Manipulation:** Concatenation, substring operations, formatting
   - **Data Structures:** Arrays, dictionaries for managing inventories
   - **Functions with Parameters:** Beyond current quest definitions
   - **Exception Handling:** Try-catch blocks for adventure failures
   - **Impact:** More expressive adventure scripts

### Medium-Priority Improvements

4. **Debugging Support**
   - **Breakpoints:** Pause execution at specific locations
   - **Variable Inspection:** View values during execution
   - **Step-Through Debugging:** Execute one instruction at a time
   - **Impact:** Easier troubleshooting of complex programs

5. **Standard Library**
   - **Built-in Functions:** Common adventure operations (inventory management, combat calculations)
   - **Predefined Quests:** Reusable game mechanics
   - **Impact:** Faster adventure development

6. **Code Generation Improvements**
   - **Bytecode Compilation:** Compile to bytecode for faster execution
   - **JIT Compilation:** Just-in-time compilation of hot paths
   - **Native Code Generation:** Compile to Python bytecode or native code
   - **Impact:** Significant speed improvements

### Lower-Priority Improvements

7. **Language Features for Advanced Use Cases**
   - **Module System:** Import/export mechanisms for code reuse across files
   - **Macros:** Meta-programming capabilities for code generation
   - **Pattern Matching:** Advanced control flow constructs
   - **Impact:** Support for larger projects and library ecosystems

8. **Tooling and IDE Support**
   - **Syntax Highlighting:** VS Code/IDE plugins
   - **Language Server Protocol (LSP):** Real-time error checking in editors
   - **Debugger Integration:** Standalone debugger with IDE hooks
   - **Package Manager:** Centralized repository for adventure libraries

9. **Documentation and Tooling**
   - **Interactive Tutorial:** Guided introduction to LootCode
   - **Adventure Templates:** Starter projects for common game types
   - **Community Forum:** Support and knowledge sharing

---

## Part 4: Individual Contributions

Our team of three members collaborated on the LootCode compiler project with the following role distribution:

### [member 1]
- **Primary Responsibilities:**
  - Lexer and parser implementation (Phases 1-2)
  - Token definition and grammar design
  - AST node design and parsing algorithm
  - Parser testing and error recovery mechanisms
- **Key Contributions:**
  - Designed the recursive descent parser architecture
  - Implemented comprehensive error recovery with line/column reporting
  - Created all 12 test programs for the test suite
  - Documented grammar and parsing strategy
- **Lessons Learned:**
  - Importance of clear grammar specification before implementation
  - Parser robustness requires careful lookahead and error handling
  - Testing early and often prevents downstream issues

### [member 2]
- **Primary Responsibilities:**
  - Semantic analyzer and symbol table (Phase 3)
  - Type checking and validation logic
  - Scope management and variable tracking
  - Integration with parser output
- **Key Contributions:**
  - Implemented scope stack for proper variable scoping
  - Designed unit preservation mechanism through semantic analysis
  - Created validation rules for type safety
  - Extensively tested semantic analysis with edge cases
- **Lessons Learned:**
  - Semantic analysis is where most user errors are caught
  - Symbol table design significantly impacts code clarity
  - Type systems require careful thought and testing

### [member 3]
- **Primary Responsibilities:**
  - Intermediate code generation, optimization, and code generation (Phases 4-6)
  - TAC instruction design and generation
  - Optimizer implementation
  - Execution engine and runtime
- **Key Contributions:**
  - Designed Three-Address Code format and generation templates
  - Implemented conservative optimization strategies
  - Built execution engine with proper variable management
  - Created debugging output for TAC inspection
  - Integrated all phases into cohesive compiler pipeline
- **Lessons Learned:**
  - Intermediate representations greatly simplify downstream phases
  - Optimization correctness is more important than aggressiveness
  - Execution engines must carefully manage state and control flow

### Collective Achievements
- **Architecture:** Designed and implemented complete 6-phase compiler
- **Testing:** Created comprehensive test suite with 12 diverse programs
- **Documentation:** Produced language specification and architecture documents
- **Integration:** Successfully integrated all phases into working system
- **Code Quality:** Maintained clean, readable, well-commented code throughout

### Teamwork and Collaboration
- **Code Reviews:** Regular peer review of implementations
- **Weekly Meetings:** Synchronized on progress and resolved blockers
- **Knowledge Sharing:** Documented decisions and shared understanding of system
- **Debugging Collaboration:** Worked together on complex issues
- **Iterative Refinement:** Incorporated feedback and improved implementations

---

## Conclusion

The LootCode compiler project was a comprehensive exercise in compiler design and implementation. Through tackling challenges in unit preservation, scope management, and control flow translation, we developed a deeper understanding of how modern compilers work. The six-phase architecture proved invaluable in managing complexity, and the comprehensive test suite ensured correctness.

Our team worked collaboratively to overcome technical challenges, learning valuable lessons about separation of concerns, intermediate representations, type systems, and iterative development. While the current implementation is complete and functional, numerous opportunities exist for enhancement in optimization, language features, and developer tooling.

This project demonstrates that building a compiler is achievable, rewarding, and—most importantly—deeply educational.

