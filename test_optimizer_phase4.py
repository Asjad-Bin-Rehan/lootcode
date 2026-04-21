#!/usr/bin/env python3
"""
Phase 4 Optimizer verification tests for LootCode.
Validates optimizer alignment with current TAC operations and unit-safe behavior.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from optimizer import Optimizer
from intermediate_code import TACInstruction


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def test_constant_folding_numeric():
    optimizer = Optimizer()
    instructions = [
        TACInstruction('add', '2', '3', 'score'),
    ]
    optimized = optimizer.optimize(instructions)
    assert_true(len(optimized) == 1, 'Expected single folded instruction')
    assert_true(optimized[0].op == 'assign', 'Expected add to fold into assign')
    assert_true(str(optimized[0].arg1) in ('5', '5.0'), 'Expected folded value 5')


def test_constant_folding_units():
    optimizer = Optimizer()
    instructions = [
        TACInstruction('add', '50 hp', '25 hp', 'player_hp'),
    ]
    optimized = optimizer.optimize(instructions)
    assert_true(len(optimized) == 1, 'Expected single folded unit instruction')
    assert_true(optimized[0].op == 'assign', 'Expected unit add to fold into assign')
    assert_true('75' in str(optimized[0].arg1) and 'hp' in str(optimized[0].arg1), 'Expected folded unit value 75 hp')


def test_no_invalid_unit_fold():
    optimizer = Optimizer()
    instructions = [
        TACInstruction('add', '10 hp', '5 qty_unit', 't0'),
    ]
    optimized = optimizer.optimize(instructions)
    assert_true(optimized[0].op == 'add', 'Mismatched units should not fold')


def test_quest_boundary_alignment():
    optimizer = Optimizer()
    instructions = [
        TACInstruction('begin_quest', None, None, 'q1'),
        TACInstruction('add', '1', '2', 'quest_score'),
        TACInstruction('end_quest', None, None, 'q1'),
    ]
    optimized = optimizer.optimize(instructions)
    assert_true(optimized[0].op == 'begin_quest', 'begin_quest should remain unchanged')
    assert_true(optimized[1].op == 'assign', 'folding should still work inside quest body')
    assert_true(optimized[2].op == 'end_quest', 'end_quest should remain unchanged')


def test_constant_propagation():
    optimizer = Optimizer()
    instructions = [
        TACInstruction('assign', '10', None, 'x'),
        TACInstruction('add', 'x', '5', 'score'),
    ]
    optimized = optimizer.optimize(instructions)

    # The second instruction may be folded after propagation.
    assert_true(len(optimized) >= 1, 'Expected optimized instruction stream')
    has_expected = any(
        (instr.op == 'assign' and str(instr.arg1) in ('15', '15.0')) or
        (instr.op == 'add' and str(instr.arg1) in ('10', '10.0'))
        for instr in optimized
    )
    assert_true(has_expected, 'Expected either propagated add or fully folded assign result')


def run_all():
    tests = [
        test_constant_folding_numeric,
        test_constant_folding_units,
        test_no_invalid_unit_fold,
        test_quest_boundary_alignment,
        test_constant_propagation,
    ]

    passed = 0
    failed = 0

    print('=' * 70)
    print('PHASE 4 OPTIMIZER VERIFICATION')
    print('=' * 70)

    for test in tests:
        try:
            test()
            print(f'[PASS] {test.__name__}')
            passed += 1
        except Exception as e:
            print(f'[FAIL] {test.__name__}: {e}')
            failed += 1

    print('-' * 70)
    print(f'Total: {passed}/{len(tests)} passed')

    if failed:
        print('[FAILED] Optimizer verification has failures')
        return 1

    print('[SUCCESS] All optimizer verification tests passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(run_all())
