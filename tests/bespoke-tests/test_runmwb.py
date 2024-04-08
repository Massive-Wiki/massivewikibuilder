import pytest
import sys
import io
import logging

# import the run MWB module
import run_mwb

# test cases
def test_mwb_with_valid_args():
    log_capture_string = io.StringIO()
    stream_handler = logging.StreamHandler(log_capture_string)
    logger = logging.getLogger()
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    # set sys.argv to mimic command-line arguments
    sys.argv = ['run_mwb.py', '-i', 'test-input', '-b', 'baseline']
    
    # Call the main function of run_mwb.py program
    run_mwb.main()
    
    # capture the logging output
    captured_output = log_capture_string.getvalue().strip()
    
    # assert captured and expected output equivalence
    expected_output = "args: Namespace(input='test-input', baseline='baseline', random=False, force=None, mwb_output='test-output', mwb_config='test-input/.massivewikibuilder/mwb.yaml', mwb_templates='test-input/.massivewikibuilder/this-wiki-themes/basso')\nRunning mwb.py...\nmwb.py executed successfully.\nComparing directories...\nComparison finished, no faults."
    
    assert captured_output == expected_output

