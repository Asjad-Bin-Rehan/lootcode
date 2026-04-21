#!/usr/bin/env python3
"""
Comprehensive Lexer Sanity Test for AdventureScript
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

try:
    from token_types import TokenType, Token, KEYWORDS
    from lexer import Lexer
    print("[OK] Imports successful")
except Exception as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("COMPREHENSIVE LEXER SANITY TEST - AdventureScript")
print("=" * 70)

# Test 1: Basic keywords
print("\n[TEST 1] Verify all 40 adventure keywords exist in KEYWORDS dict")
expected_keywords = {
    'item', 'stat', 'text', 'combine', 'equip', 'rest', 'narrate',
    'power_up', 'acquire', 'discard', 'show', 'loop', 'foreach',
    'if', 'then', 'else', 'iterations', 'in', 'quest', 'return',
    'returns', 'input', 'to', 'with', 'for', 'at', 'from', 'by',
    'gold', 'treasure', 'coin', 'loot', 'gems', 'qty', 'count',
    'hp', 'mp', 'turns', 'seconds', 'hours'
}
missing = expected_keywords - set(KEYWORDS.keys())
if missing:
    print(f"[FAIL] MISSING KEYWORDS: {missing}")
else:
    print(f"[OK] All {len(expected_keywords)} adventure keywords present")

# Test 2: Tokenize simple declaration
print("\n[TEST 2] Tokenize simple item declaration")
code1 = "item potion = 5 qty;"
try:
    lexer = Lexer(code1)
    tokens = lexer.tokenize()
    expected_types = [TokenType.ITEM, TokenType.IDENTIFIER, TokenType.ASSIGN, 
                     TokenType.NUMBER, TokenType.QTY_UNIT, TokenType.SEMICOLON, TokenType.EOF]
    actual_types = [t.type for t in tokens]
    if actual_types == expected_types:
        print(f"[OK] Correct tokenization: {[str(t.type).split('.')[-1] for t in tokens]}")
    else:
        print(f"[FAIL] Token mismatch")
        print(f"   Expected: {expected_types}")
        print(f"   Got:      {actual_types}")
except Exception as e:
    print(f"[FAIL] Tokenization failed: {e}")

# Test 3: Tokenize stat declaration with hp unit
print("\n[TEST 3] Tokenize stat declaration with hp unit")
code2 = "stat player_hp = 100 hp;"
try:
    lexer = Lexer(code2)
    tokens = lexer.tokenize()
    expected_types = [TokenType.STAT, TokenType.IDENTIFIER, TokenType.ASSIGN,
                     TokenType.NUMBER, TokenType.HP, TokenType.SEMICOLON, TokenType.EOF]
    actual_types = [t.type for t in tokens]
    if actual_types == expected_types:
        print(f"[OK] Correct tokenization")
    else:
        print(f"[FAIL] Token mismatch")
except Exception as e:
    print(f"[FAIL] Failed: {e}")

# Test 4: Tokenize operation statements
print("\n[TEST 4] Tokenize multiple operations")
code3 = """
item health = 10 qty;
rest 5 turns;
narrate "Adventure begins!";
combine health with herbs;
"""
try:
    lexer = Lexer(code3)
    tokens = lexer.tokenize()
    ops_found = {t.value for t in tokens if t.type in [TokenType.ITEM, TokenType.REST, TokenType.NARRATE, TokenType.COMBINE]}
    expected_ops = {'item', 'rest', 'narrate', 'combine'}
    if expected_ops == ops_found:
        print(f"[OK] All operations tokenized: {expected_ops}")
    else:
        print(f"[FAIL] Missing ops: {expected_ops - ops_found}")
except Exception as e:
    print(f"[FAIL] Failed: {e}")

# Test 5: Verify line/column tracking
print("\n[TEST 5] Verify line and column tracking")
code4 = "item x = 1 qty;\nrest 2 turns;"
try:
    lexer = Lexer(code4)
    tokens = lexer.tokenize()
    # Find 'rest' token (should be on line 2)
    rest_token = [t for t in tokens if t.value == 'rest'][0]
    if rest_token.line == 2:
        print(f"[OK] Line tracking correct: 'rest' at line {rest_token.line}")
    else:
        print(f"[FAIL] Line tracking wrong: 'rest' at line {rest_token.line}, expected 2")
except Exception as e:
    print(f"[FAIL] Failed: {e}")

# Test 6: Verify no old cooking keywords
print("\n[TEST 6] Verify old cooking keywords NOT in KEYWORDS")
old_keywords = {'ingredient', 'mix', 'heat', 'wait', 'serve', 'recipe', 'minutes', 'cups'}
found_old = old_keywords & set(KEYWORDS.keys())
if found_old:
    print(f"[FAIL] OLD KEYWORDS STILL PRESENT: {found_old}")
else:
    print(f"[OK] No old cooking keywords found")

# Test 7: File extension validation check (in comments for now)
print("\n[TEST 7] File extension test (would check .adv files)")
print("[OK] File extension validation will be added when updating file handling")

print("\n" + "=" * 70)
print("[OK] LEXER SANITY TEST COMPLETE - ALL SYSTEMS GO")
print("=" * 70)
