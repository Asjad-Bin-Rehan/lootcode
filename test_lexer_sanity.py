#!/usr/bin/env python3
"""
Sanity check: Lexer test with AdventureScript syntax
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from lexer import Lexer
from token_types import TokenType

# Test code in AdventureScript
code = '''
item health_potion = 2 qty;
stat player_hp = 100 hp;
equip player_hp to 100 hp;
rest 15 turns;
narrate "Entering the dungeon...";
combine health_potion with herbs;
'''

print("=" * 60)
print("LEXER SANITY CHECK - AdventureScript Tokenization")
print("=" * 60)
print("\nSource Code:")
print(code)
print("\n" + "-" * 60)
print("Tokens Generated:")
print("-" * 60)

try:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    for i, token in enumerate(tokens):
        print(f"{i:3d}. {token}")
    
    print("\n" + "-" * 60)
    print(f"[OK] SUCCESS: Generated {len(tokens)} tokens")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[FAIL] ERROR: {e}")
    print("=" * 60)
    sys.exit(1)
