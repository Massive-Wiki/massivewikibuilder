import sys
import pytest
from io import StringIO

# Import your foo.py module here
import run_mwb

# Fixture to capture the stdout
@pytest.fixture
def capture_stderr(monkeypatch):
    buffer = StringIO()
    monkeypatch.setattr(sys, 'stderr', buffer)
    yield buffer
    buffer.close()

# Test cases
def test_mwb_with_valid_args(capture_stderr):
    # Set the sys.argv to mimic command-line arguments
    sys.argv = ['run_mwb.py', '-i', 'test-input', '-b', 'baseline']
    
    # Call the main function of your foo.py program
    run_mwb.main()
    
    # Get the captured stderr
    captured_output = capture_stderr.getvalue()
    
    # Assert the expected output
    expected_output = "args: Namespace(input='test-input', baseline='baseline', random=False, force=None, mwb_output='test-output', mwb_config='input-dir/.massivewikibuilder/mwb.yaml', mwb_templates='input-dir/.massivewikibuilder/this-wiki-themes/basso')\nRunning mwb.py...\nmwb.py executed successfully.\nComparing directories...\nComparison finished, no faults.\n"
    
    assert captured_output == expected_output

