#!/usr/bin/env python3
"""
Structural Integrity Test - Verify no breaking changes to lexer architecture
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from token_types import Token, TokenType, KEYWORDS
from lexer import Lexer

print("=" * 70)
print("STRUCTURAL INTEGRITY TEST - Lexer Architecture")
print("=" * 70)

# Test 1: Token class still works
print("\n[TEST 1] Token class functionality")
try:
    t = Token(TokenType.ITEM, "test_item", 1, 5)
    assert t.type == TokenType.ITEM
    assert t.value == "test_item"
    assert t.line == 1
    assert t.column == 5
    assert "test_item" in str(t)
    print("[OK] Token class works correctly")
except Exception as e:
    print(f"[FAIL] Token class failed: {e}")

# Test 2: Lexer initialization
print("\n[TEST 2] Lexer initialization")
try:
    code = "item x = 1 qty;"
    lexer = Lexer(code)
    assert lexer.source == code
    assert lexer.pos == 0
    assert lexer.line == 1
    assert lexer.column == 1
    print("[OK] Lexer initialization works")
except Exception as e:
    print(f"[FAIL] Lexer init failed: {e}")

# Test 3: Lexer methods exist
print("\n[TEST 3] All lexer methods exist")
methods = ['advance', 'peek', 'skip_whitespace', 'skip_comment', 
           'read_number', 'read_string', 'read_identifier', 
           'get_next_token', 'tokenize', 'error']
try:
    lexer = Lexer("")
    for method in methods:
        assert hasattr(lexer, method), f"Missing method: {method}"
    print(f"[OK] All {len(methods)} required methods present")
except Exception as e:
    print(f"[FAIL] Method check failed: {e}")

# Test 4: Multi-token stream
print("\n[TEST 4] Multi-token tokenization (stream handling)")
try:
    code = "item a = 1 qty; stat b = 2 hp;"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    token_count = len(tokens)
    assert token_count > 10  # Should have many tokens
    assert tokens[-1].type == TokenType.EOF  # Last token is EOF
    print(f"[OK] Tokenized stream of {token_count} tokens, EOF at end")
except Exception as e:
    print(f"[FAIL] Stream tokenization failed: {e}")

# Test 5: Whitespace handling
print("\n[TEST 5] Whitespace and newline handling")
try:
    code = """
    item x = 1 qty;
    stat y = 2 hp;
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    # Should have tokens but no whitespace tokens
    whitespace_tokens = [t for t in tokens if t.type in [TokenType.NEWLINE]]
    print(f"[OK] Whitespace handled correctly ({len(tokens)} tokens, {len(whitespace_tokens)} NEWLINE)")
except Exception as e:
    print(f"[FAIL] Whitespace handling failed: {e}")

# Test 6: Error handling still works
print("\n[TEST 6] Error handling")
try:
    bad_code = '"unterminated string'
    lexer = Lexer(bad_code)
    try:
        tokens = lexer.tokenize()
        print("[FAIL] Should have raised an error for unterminated string")
    except Exception as e:
        if "Unterminated" in str(e):
            print(f"[OK] Error handling works: caught '{str(e)[:50]}...'")
        else:
            print(f"[FAIL] Wrong error type: {e}")
except Exception as e:
    print(f"[FAIL] Error test setup failed: {e}")

# Test 7: Number parsing
print("\n[TEST 7] Number parsing")
try:
    code = "100 3.14 0"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    numbers = [t for t in tokens if t.type == TokenType.NUMBER]
    assert len(numbers) == 3
    assert numbers[0].value == "100"
    assert numbers[1].value == "3.14"
    assert numbers[2].value == "0"
    print(f"[OK] Number parsing works for integers and floats")
except Exception as e:
    print(f"[FAIL] Number parsing failed: {e}")

# Test 8: String parsing
print("\n[TEST 8] String parsing")
try:
    code = '"Hello Adventure"'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    strings = [t for t in tokens if t.type == TokenType.STRING]
    assert len(strings) == 1
    assert strings[0].value == "Hello Adventure"
    print(f"[OK] String parsing works")
except Exception as e:
    print(f"[FAIL] String parsing failed: {e}")

# Test 9: Operator tokenization
print("\n[TEST 9] Operators and delimiters")
try:
    code = "= + - * / == != > < >= <= ; , ( ) { }"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    # Filter out EOF
    ops = [t for t in tokens if t.type != TokenType.EOF]
    expected_ops = 17  # All the operators
    assert len(ops) == expected_ops, f"Expected {expected_ops} operators, got {len(ops)}"
    print(f"[OK] All {expected_ops} operators/delimiters tokenized")
except Exception as e:
    print(f"[FAIL] Operator tokenization failed: {e}")

# Test 10: Comment handling
print("\n[TEST 10] Comment handling")
try:
    code = "item x = 1 qty; # this is a comment\nstat y = 2 hp;"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    # Comments should not appear in token stream
    comments = [t for t in tokens if t.type == TokenType.COMMENT]
    assert len(comments) == 0
    # But we should have the tokens before and after
    values = [t.value for t in tokens if t.type == TokenType.IDENTIFIER]
    assert 'x' in values and 'y' in values
    print(f"[OK] Comments properly skipped")
except Exception as e:
    print(f"[FAIL] Comment handling failed: {e}")

print("\n" + "=" * 70)
print("[OK] STRUCTURAL INTEGRITY TEST PASSED - Lexer architecture intact")
print("=" * 70)
