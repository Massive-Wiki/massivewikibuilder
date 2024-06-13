#!/usr/bin/env python3

import subprocess
import pytest
import filecmp

import logging                                                                                                       
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')                                         

#def run_mwb():
    # run bespoke-test_mwb.py with specific arguments and check return status
#    subprocess.run(["python", "bespoke-test_mwb.py", "-i", "test-input", "-b", "baseline"], check=True)

def run_mwb():
    """
    Runs mwb.py with the provided input directory and an output directory at the same level.
    Captures stdout and stderr, checks return code for success/fail.
    """
    try:
        cmd = [
            "./mwb.py",
            "-c", "tests/test-input/.massivewikibuilder/mwb.yaml",
            "-w", "tests/test-input",
            "-o", "tests/test-output",
            "-t", "tests/test-input/.massivewikibuilder/this-wiki-themes/basso"
        ]

        subprocess.run(cmd, check=True)

    except OSError as e:
        # OSError could be raised for issues related to file paths, directories, or if mwb.py doesn't exist
        logging.error(f"OS Error (file paths, directories, mwb.py doesn't exist?): {e}")
        return False
    except subprocess.CalledProcessError as e:
        # This will be raised if the called process returns a non-zero return code
        logging.error(f"CalledProcessError (called process returned a non-zero return code): {e}")
        return False
    except Exception as e:
        # Generic error handler for any other exceptions
        logging.error(f"Unexpected error occurred: {e}")
        return False

def compare_mwb_directories(output, baseline):
    comparison = filecmp.dircmp(output, baseline)
    if comparison.left_only or comparison.right_only or not ('build-results.json' in comparison.diff_files and len(comparison.diff_files) == 1):
        return False
    else:
        return True

@pytest.fixture(scope="module")
def run_and_verify():
    run_mwb()

def test_compare_output_with_baseline(run_and_verify):
    assert compare_mwb_directories("tests/test-output/", "tests/baseline/"), "Directory contents do not match."
