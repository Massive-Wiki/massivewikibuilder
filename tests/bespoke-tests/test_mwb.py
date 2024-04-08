#!/usr/bin/env python3

import subprocess
import pytest

def test_mwb():
    # run bespoke-test_mwb.py with specific arguments and check if the output is as expected
    expected_output = "INFO: args: Namespace(input='test-input', baseline='baseline', random=False, force=None, mwb_output='test-output', mwb_config='test-input/.massivewikibuilder/mwb.yaml', mwb_templates='test-input/.massivewikibuilder/this-wiki-themes/basso')\nINFO: Running mwb.py...\nINFO: mwb.py executed successfully.\nINFO: Comparing directories...\nINFO: Comparison finished, no faults."
    
    completed_process = subprocess.run(["python", "bespoke-test_mwb.py", "-i", "test-input", "-b", "baseline"], capture_output=True, text=True)
    result = completed_process.stderr.strip()
    assert result == expected_output
