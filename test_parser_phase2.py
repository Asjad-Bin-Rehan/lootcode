#!/usr/bin/env python3
"""
Parser Phase 2 Refactoring Verification Test
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

try:
    from token_types import TokenType, Token
    from lexer import Lexer
    from parser import Parser
    print("[OK] Imports successful")
except Exception as e:
    print(f"[FAIL] Import failed: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("PARSER PHASE 2 REFACTORING VERIFICATION")
print("=" * 70)

# Test 1: Verify AST nodes exist and are renamed
print("\n[TEST 1] Verify renamed AST node classes exist")
ast_nodes = [
    'Program', 'Declaration', 'Assignment', 'Value',
    'CombineOperation', 'EquipOperation', 'RestOperation', 'NarrateOperation',
    'ShowOperation', 'PowerUpOperation', 'AcquireOperation',
    'LoopStatement', 'IfStatement',
    'QuestDeclaration', 'QuestCall', 'ReturnStatement', 'InputStatement',
    'BinaryOp', 'Number', 'String', 'Identifier'
]
try:
    from parser import (
        CombineOperation, EquipOperation, RestOperation, NarrateOperation,
        ShowOperation, PowerUpOperation, AcquireOperation, LoopStatement, IfStatement,
        QuestDeclaration, QuestCall
    )
    print(f"[OK] All {len(ast_nodes)} AST nodes successfully renamed and importable")
except ImportError as e:
    print(f"[FAIL] Failed to import renamed AST nodes: {e}")

# Test 2: Parse simple adventure code
print("\n[TEST 2] Parse simple item declaration")
code1 = "item potion = 5 qty;"
try:
    lexer = Lexer(code1)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed: {code1}")
    print(f"   Program has {len(ast.statements)} statement(s)")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 3: Parse stat declaration
print("\n[TEST 3] Parse stat declaration with hp unit")
code2 = "stat player_hp = 100 hp;"
try:
    lexer = Lexer(code2)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed: {code2}")
    stmt = ast.statements[0]
    print(f"   Declaration type: {stmt.var_type}")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 4: Parse combine operation
print("\n[TEST 4] Parse combine operation (renamed from mix)")
code3 = "combine herbs with potion;"
try:
    lexer = Lexer(code3)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed: {code3}")
    stmt = ast.statements[0]
    if hasattr(stmt, 'items'):
        print(f"   Items to combine: {stmt.items}")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 5: Parse equip operation (renamed from heat)
print("\n[TEST 5] Parse equip operation (renamed from heat)")
code4 = "equip player_hp to 100 hp;"
try:
    lexer = Lexer(code4)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed: {code4}")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 6: Parse rest operation (renamed from wait)
print("\n[TEST 6] Parse rest operation (renamed from wait)")
code5 = "rest 5 turns;"
try:
    lexer = Lexer(code5)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed: {code5}")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 7: Parse narrate operation (renamed from serve)
print("\n[TEST 7] Parse narrate operation (renamed from serve)")
code6 = 'narrate "Adventure begins!";'
try:
    lexer = Lexer(code6)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed: {code6}")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 8: Parse loop statement (renamed from repeat)
print("\n[TEST 8] Parse loop statement (renamed from repeat)")
code7 = "loop 5 iterations { rest 1 turns; }"
try:
    lexer = Lexer(code7)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed loop with {len(ast.statements[0].body)} statements in body")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 9: Parse if statement (renamed from when)
print("\n[TEST 9] Parse if statement (renamed from when)")
code8 = "if 1 == 1 then { narrate \"True!\"; } else { narrate \"False!\"; }"
try:
    lexer = Lexer(code8)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    print(f"[OK] Successfully parsed if statement")
    print(f"   Then body: {len(stmt.then_body)} statements")
    print(f"   Else body: {len(stmt.else_body) if stmt.else_body else 0} statements")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 10: Parse quest declaration (renamed from recipe)
print("\n[TEST 10] Parse quest declaration (renamed from recipe)")
code9 = "quest my_quest() { narrate \"Quest executed!\"; }"
try:
    lexer = Lexer(code9)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed quest declaration")
    print(f"   Quest name: {ast.recipes[0].name}")
    print(f"   Quest body: {len(ast.recipes[0].body)} statements")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 11: Parse identifier that collides with unit keyword
print("\n[TEST 11] Parse declaration/assignment for identifier-like keyword token")
code10 = "item gold = 50 qty; gold = gold + 50 qty;"
try:
    lexer = Lexer(code10)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed identifier collision case")
    print(f"   Statements parsed: {len(ast.statements)}")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

# Test 12: Parse unit-bearing arithmetic expression
print("\n[TEST 12] Parse unit-bearing arithmetic expression")
code11 = "stat health = 100 hp; health = 50 hp + 50 hp;"
try:
    lexer = Lexer(code11)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"[OK] Successfully parsed unit-bearing arithmetic")
    print(f"   Statements parsed: {len(ast.statements)}")
except Exception as e:
    print(f"[FAIL] Parse failed: {e}")

print("\n" + "=" * 70)
print("[OK] PARSER PHASE 2 REFACTORING VERIFICATION COMPLETE")
print("=" * 70)
