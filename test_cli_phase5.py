#!/usr/bin/env python3
"""
Phase 5 CLI and integration verification tests for LootCode.
"""

import os
import subprocess
import sys
import tempfile


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(REPO_ROOT, 'adventurescript.py')
SAMPLE = os.path.join(REPO_ROOT, 'tests', '01_simple_adventure.adv')


def run_cmd(args, input_text=None, timeout=30):
    return subprocess.run(
        [sys.executable, ENTRY] + args,
        input=input_text,
        text=True,
        capture_output=True,
        cwd=REPO_ROOT,
        timeout=timeout,
    )


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def test_help_mode():
    result = run_cmd(['-h'])
    output = result.stdout + result.stderr
    assert_true(result.returncode == 0, 'help should exit with code 0')
    assert_true('--debug' in output and '--interactive' in output and '--output' in output, 'help text missing expected options')


def test_compile_and_run_mode():
    result = run_cmd([SAMPLE])
    output = result.stdout + result.stderr
    assert_true(result.returncode == 0, 'compile/run should exit with code 0')
    assert_true('[SUCCESS] Successfully compiled' in output, 'compile/run success marker missing')


def test_debug_mode():
    result = run_cmd([SAMPLE, '--debug'])
    output = result.stdout + result.stderr
    assert_true(result.returncode == 0, 'debug mode should exit with code 0')
    assert_true('PHASE 4: INTERMEDIATE CODE GENERATION' in output, 'debug output missing phase details')


def test_output_file_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = os.path.join(tmpdir, 'output.tac')
        result = run_cmd([SAMPLE, '-o', out_file])
        output = result.stdout + result.stderr
        assert_true(result.returncode == 0, 'output mode should exit with code 0')
        assert_true(os.path.exists(out_file), 'output TAC file was not created')
        with open(out_file, 'r', encoding='utf-8') as f:
            content = f.read()
        assert_true('Three-Address Code' in content, 'output TAC file missing expected header')
        assert_true('TAC written to:' in output, 'output mode missing confirmation message')


def test_interactive_mode():
    result = run_cmd(['--interactive'], input_text='exit\n', timeout=20)
    output = result.stdout + result.stderr
    assert_true(result.returncode == 0, 'interactive mode should exit with code 0 after exit command')
    assert_true('LootCode Interactive Mode' in output and 'Goodbye!' in output, 'interactive mode output mismatch')


def test_missing_file_error_handling():
    result = run_cmd(['does_not_exist.adv'])
    output = result.stdout + result.stderr
    assert_true(result.returncode != 0, 'missing file should return non-zero exit code')
    assert_true("[ERROR] File 'does_not_exist.adv' not found" in output, 'missing file error message mismatch')


def run_all():
    tests = [
        test_help_mode,
        test_compile_and_run_mode,
        test_debug_mode,
        test_output_file_mode,
        test_interactive_mode,
        test_missing_file_error_handling,
    ]

    passed = 0
    failed = 0

    print('=' * 70)
    print('PHASE 5 CLI/INTEGRATION VERIFICATION')
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
        print('[FAILED] CLI/integration verification has failures')
        return 1

    print('[SUCCESS] All CLI/integration verification tests passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(run_all())
