#!/usr/bin/env python3
"""
LootCode Compiler - Main Entry Point
Run this file to use the LootCode compiler for adventure game development
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Import and run the compiler
from compiler import main

if __name__ == "__main__":
    main()
