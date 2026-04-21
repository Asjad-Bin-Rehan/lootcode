#!/usr/bin/env python3
"""
Validate token_types.py and lexer.py syntax
"""
import sys
import os
import py_compile

base_dir = os.path.dirname(os.path.abspath(__file__))

files = [
    os.path.join(base_dir, 'src', 'token_types.py'),
    os.path.join(base_dir, 'src', 'lexer.py'),
]

print("=" * 60)
print("VALIDATING PYTHON SYNTAX")
print("=" * 60)

errors = []
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print(f"[OK] {f}")
    except py_compile.PyCompileError as e:
        print(f"[FAIL] {f}")
        errors.append(str(e))

print("=" * 60)
if errors:
    print(f"\n[ERROR] {len(errors)} SYNTAX ERRORS FOUND:\n")
    for err in errors:
        print(err)
    sys.exit(1)
else:
    print("[OK] ALL FILES VALID - NO SYNTAX ERRORS")
    print("=" * 60)
