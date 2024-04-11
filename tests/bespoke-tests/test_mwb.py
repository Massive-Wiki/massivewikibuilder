#!/usr/bin/env python3

import subprocess
import pytest
import filecmp

def compare_mwb_directories(output, baseline):
    comparison = filecmp.dircmp(output, baseline)
    if comparison.left_only or comparison.right_only or not ('build-results.json' in comparison.diff_files and len(comparison.diff_files) == 1):
        return False
    else:
        return True

@pytest.fixture(scope="module")
def run_and_verify():
    # run bespoke-test_mwb.py with specific arguments and check return status
    subprocess.run(["python", "bespoke-test_mwb.py", "-i", "test-input", "-b", "baseline"], check=True)

def test_compare_output_with_baseline(run_and_verify):
    assert compare_mwb_directories("test-output/", "baseline/"), "Directory contents do not match."
