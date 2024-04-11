#!/usr/bin/env python3

import argparse
import os
import filecmp
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

import os
import subprocess
import logging

def run_mwb(args):
    """
    Runs mwb.py with the provided input directory and an output directory at the same level.
    Captures stdout and stderr, checks return code for success/fail.
    """
    try:
        output_directory = os.path.join(os.path.dirname(args.input), args.mwb_output)
        cmd = [
            "../../mwb.py",
            "-c", args.mwb_config,
            "-w", args.input,
            "-o", output_directory,
            "-t", args.mwb_templates
        ]

        logging.info("Running mwb.py...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.stdout:
            logging.info(result.stdout)
        if result.stderr:
            logging.error(result.stderr)

        if result.returncode != 0:
            logging.error("mwb.py script execution failed!")
            return False

        logging.info("mwb.py executed successfully.")
        return True

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

def compare_directories(baseline_output_dir, generated_output_dir):
    """
    Compares the contents of the known good output directory with the generated output directory.
    Prints warnings for any discrepancies.
    Returns True if directories are the same, False if not.
    """

    # Set flag to pass
    test_is_passing = True

    # Get the list of files in both directories
    baseline_output_files = set(os.listdir(baseline_output_dir))
    generated_output_files = set(os.listdir(generated_output_dir))
    
    # Are there any missing files?
    missing_files = baseline_output_files - generated_output_files
    if missing_files:
        test_is_passing = False
        for missing in missing_files:
            logging.warning(f"Missing file in generated output: {missing}")

    # Are there any extra files?
    extra_files = generated_output_files - baseline_output_files
    if extra_files:
        test_is_passing = False
        for extra in extra_files:
            logging.warning(f"Extra file in generated output: {extra}")

    # Compare files that are present in both directories
    for common_file in baseline_output_files.intersection(generated_output_files):
        baseline_file_path = os.path.join(baseline_output_dir, common_file)
        if os.path.isdir(baseline_file_path) or common_file == 'build-results.json':
            continue  # ignore build time difference
        generated_file_path = os.path.join(generated_output_dir, common_file)

        if not filecmp.cmp(baseline_file_path, generated_file_path, shallow=False):
            test_is_passing = False
            with open(baseline_file_path, 'r') as file1, open(generated_file_path, 'r') as file2:
                lines1 = file1.readlines()
                lines2 = file2.readlines()
                for i,lines2 in enumerate(lines2):
                    if lines2 != lines1[i]:
                        test_is_passing = False
                        print("line ",i," in ",generated_file_path," differs:")
                        print(lines2)
                        logging.warning(f"Mismatch in file content: {common_file}")

def setup_args():
    parser = argparse.ArgumentParser(description="Test the mwb.py script by comparing its output to known good outputs.")
    parser.add_argument('--input', '-i', required=True, help="Directory of source Markdown files.")
    parser.add_argument('--baseline', '-b', required=True, help="Directory of known good output files to compare against.")
    parser.add_argument('--random', '-r', action='store_true', help="Don't test, just return a random 0 or 1 exit code.")
    parser.add_argument('--force', '-f', choices=[0, 1], type=int, help="Don't test, just return 0 or 1 exit code as provided.")
    # arguments passed through to MWB
    parser.add_argument('--mwb-output', default="test-output", help="Directory of mwb.py-generated output files.")
    parser.add_argument('--mwb-config', default="test-input/.massivewikibuilder/mwb.yaml", help="Configuration file for mwb. Default is 'test-input/.massivewikibuilder/mwb.yaml'.")
    parser.add_argument('--mwb-templates', default="test-input/.massivewikibuilder/this-wiki-themes/basso", help="Templates directory for mwb. Default is 'test-input/.massivewikibuilder/this-wiki-themes-basso'.")
    return parser.parse_args()

def main():
    args = setup_args()
    logging.info(f"args: {args}")

    if args.force is not None:
        return args.force

    if args.random:
        import random
        return random.randint(0, 1)

    if not run_mwb(args):
        logging.error("Aborting tests due to mwb.py failure.")
        return 0

    logging.info("Comparing directories...")
    if compare_directories(args.baseline, args.mwb_output):
        logging.info("Comparison failed.")
        return 1
    else:
        logging.info("Comparison finished, no faults.")
        return 0

if __name__ == "__main__":
    exit(main())
