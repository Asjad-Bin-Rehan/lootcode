"""
Test Runner for LootCode Compiler
Runs all adventure game test files and reports results
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from compiler import run_file

def main():
    """Run all test files"""
    test_files = [
        '01_simple_adventure.adv',
        '02_basic_arithmetic.adv',
        '03_simple_loop.adv',
        '04_conditional.adv',
        '05_combine_items.adv',
        '06_equip_stats.adv',
        '07_rest_operation.adv',
        '08_nested_control.adv',
        '09_combat_scenario.adv',
        '10_inventory.adv',
        '11_full_game.adv',
        '12_optimization.adv',
    ]
    
    print("=" * 60)
    print("LootCode Compiler - Adventure Game Test Suite")
    print("=" * 60)
    
    results = []
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n{'=' * 60}")
            print(f"Running: {test_file}")
            print(f"{'=' * 60}")
            success = run_file(test_file)
            results.append((test_file, success))
        else:
            print(f"\n[ERROR] Test file not found: {test_file}")
            results.append((test_file, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_file, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} - {test_file}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed!")
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed")

if __name__ == "__main__":
    main()
