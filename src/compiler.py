"""
LootCode Compiler - Main Entry Point
Demonstrates all 6 phases of compilation for adventure game language
"""

import sys
import os
import argparse

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from intermediate_code import IntermediateCodeGenerator
from optimizer import Optimizer
from code_generator import CodeGenerator


def print_quick_start(parser):
    """Show concise usage guidance for first-time users."""
    print("\nQuick start:")
    print("  1) Run an existing sample program")
    print("     python adventurescript.py tests\\01_simple_adventure.adv")
    print("  2) Start interactive mode")
    print("     python adventurescript.py --interactive")
    print("  3) Run with debug phases")
    print("     python adventurescript.py tests\\01_simple_adventure.adv --debug")
    print("  4) Export TAC to a file")
    print("     python adventurescript.py tests\\01_simple_adventure.adv -o output.tac")
    print("\nTip: 'game.adv' in examples means any .adv file path you actually have.")
    print("Use --help for the full option list.")

def print_separator(title):
    """Print section separator"""
    print("\n" + "=" * 60)
    print(f"PHASE {title}")
    print("=" * 60)

def compile_and_run(source_code, show_phases=True):
    """Compile and execute LootCode (adventure game) source code"""
    try:
        # Phase 1: Lexical Analysis
        if show_phases:
            print_separator("1: LEXICAL ANALYSIS")
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        if show_phases:
            print(f"Generated {len(tokens)} tokens:")
            for token in tokens[:20]:  # Show first 20 tokens
                print(f"  {token}")
            if len(tokens) > 20:
                print(f"  ... and {len(tokens) - 20} more tokens")
        
        # Phase 2: Syntax Analysis
        if show_phases:
            print_separator("2: SYNTAX ANALYSIS")
        parser = Parser(tokens)
        ast = parser.parse()
        if show_phases:
            print(f"Successfully parsed {len(ast.recipes)} quests and {len(ast.statements)} statements")
            print("Abstract Syntax Tree (AST) built successfully")
            print(ast)
        
        # # Phase 3: Semantic Analysis
        # if show_phases:
        #     print_separator("3: SEMANTIC ANALYSIS")
        # semantic_analyzer = SemanticAnalyzer()
        # symbol_table = semantic_analyzer.analyze(ast)
        # if show_phases:
        #     symbol_table.display()
        #     print("\nSemantic analysis completed successfully")
        # Phase 3: Semantic Analysis
        if show_phases:
            print_separator("3: SEMANTIC ANALYSIS")

        semantic_analyzer = SemanticAnalyzer()
        symbol_table = semantic_analyzer.analyze(ast)

        # Print symbol table
        symbol_table.display()

        # Print semantic errors (IMPORTANT)
        print("\n=== Semantic Analysis Summary ===")

        if semantic_analyzer.errors:
            print(f"Total Errors: {len(semantic_analyzer.errors)}")
            print("\nErrors:")
            for err in semantic_analyzer.errors:
                print(" -", err)
        else:
            print("No semantic errors detected.")

        print("\nSemantic analysis completed successfully")
        # Phase 4: Intermediate Code Generation
        if show_phases:
            print_separator("4: INTERMEDIATE CODE GENERATION")
        ic_generator = IntermediateCodeGenerator()
        tac_instructions = ic_generator.generate(ast)
        if show_phases:
            ic_generator.display()
        
        # Phase 5: Code Optimization
        if show_phases:
            print_separator("5: CODE OPTIMIZATION")
        optimizer = Optimizer()
        optimized_instructions = optimizer.optimize(tac_instructions)
        if show_phases:
            print("\n=== Optimized Code ===")
            for i, instr in enumerate(optimized_instructions, 1):
                print(f"{i:3}: {instr}")
            optimizer.display_optimizations()
        
        # Phase 6: Code Generation / Execution
        if show_phases:
            print_separator("6: CODE EXECUTION")
        code_generator = CodeGenerator()
        output = code_generator.execute(optimized_instructions)
        
        if show_phases:
            print("\nExecution completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

def run_file(filename):
    """Compile and run a LootCode adventure game file"""
    try:
        with open(filename, 'r') as f:
            source_code = f.read()
        
        print(f"\n{'=' * 60}")
        print(f"Compiling: {filename}")
        print(f"{'=' * 60}")
        
        success = compile_and_run(source_code, show_phases=True)
        
        if success:
            print(f"\n[SUCCESS] Successfully compiled and executed {filename}")
        else:
            print(f"\n[FAILED] Failed to compile {filename}")
        
        return success
        
    except FileNotFoundError:
        print(f"[ERROR] File '{filename}' not found")
        return False
    except Exception as e:
        print(f"[ERROR] Error reading file: {e}")
        return False

def interactive_mode():
    """Interactive REPL mode"""
    print("=" * 60)
    print("LootCode Interactive Mode")
    print("=" * 60)
    print("Enter LootCode adventure game code (type 'exit' to quit)")
    print("Type 'help' for examples")
    print("=" * 60)
    
    while True:
        try:
            line = input("\n>>> ")
            
            if line.strip().lower() == 'exit':
                print("Goodbye!")
                break
            
            if line.strip().lower() == 'help':
                print("\nExample commands:")
                print("  item sword = 1 qty;")
                print("  stat hp = 100 hp;")
                print("  narrate \"Adventure begins!\";")
                print("  combine sword with herbs;")
                print("  equip hp to 150 hp;")
                print("  rest 2 turns;")
                continue
            
            if not line.strip():
                continue
            
            # Compile and run the line
            compile_and_run(line, show_phases=False)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        prog='adventurescript',
        description='LootCode Compiler - A Domain-Specific Language for 8-Bit Adventure Games',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    %(prog)s tests/01_simple_adventure.adv                    # Compile and run
    %(prog)s tests/01_simple_adventure.adv -o output.tac      # Compile to file
    %(prog)s tests/01_simple_adventure.adv --debug            # Show TAC (intermediate code)
  %(prog)s --interactive               # Interactive mode (REPL)
        '''
    )
    
    # Positional argument: input file
    parser.add_argument('input', nargs='?', help='Input .adv file to compile')
    
    # Output file
    parser.add_argument('-o', '--output', help='Output file for compiled TAC code')
    
    # Debug mode (show TAC)
    parser.add_argument('--debug', action='store_true', help='Print intermediate code (TAC) to console')
    
    # Interactive mode
    parser.add_argument('--interactive', '-i', action='store_true', help='Launch interactive REPL mode')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("LootCode Compiler")
    print("A Domain-Specific Language for 8-Bit Adventure Games")
    print("=" * 60)
    
    if args.interactive:
        # Interactive mode
        interactive_mode()
    elif args.input:
        # File mode
        filename = args.input
        try:
            with open(filename, 'r') as f:
                source_code = f.read()
            
            print(f"\nCompiling: {filename}")
            
            # Compile with full details if debug mode
            show_phases = args.debug
            success = compile_and_run(source_code, show_phases=show_phases)
            
            # If output file specified, write TAC to file
            if args.output and success:
                try:
                    # Re-compile to get instructions for writing
                    lexer = Lexer(source_code)
                    tokens = lexer.tokenize()
                    parser_obj = Parser(tokens)
                    ast = parser_obj.parse()
                    semantic_analyzer = SemanticAnalyzer()
                    semantic_analyzer.visit(ast)
                    tac_gen = IntermediateCodeGenerator()
                    instructions = tac_gen.generate(ast)
                    
                    with open(args.output, 'w') as out_f:
                        out_f.write("=== Three-Address Code (TAC) ===\n\n")
                        for i, instr in enumerate(instructions, 1):
                            out_f.write(f"{i:3}: {instr}\n")
                    
                    print(f"TAC written to: {args.output}")
                except Exception as e:
                    print(f"Error writing output file: {e}")
            
            if success:
                print(f"\n[SUCCESS] Successfully compiled {filename}")
            else:
                print(f"\n[FAILED] Failed to compile {filename}")
                sys.exit(1)
                
        except FileNotFoundError:
            print(f"[ERROR] File '{filename}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            sys.exit(1)
    else:
        # No input and no --interactive flag: show concise quick-start help.
        print_quick_start(parser)
        sys.exit(0)

if __name__ == "__main__":
    main()
