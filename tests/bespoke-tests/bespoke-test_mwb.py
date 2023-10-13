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

def run_mwb(input_directory):
    """
    Runs mwb.py with the provided input directory and an output directory at the same level.
    Captures stdout and stderr, checks return code for success/fail.
    """
    try:
        output_directory = os.path.join(os.path.dirname(input_directory), "output")
        cmd = [
            "./mwb.py",
            "-c", "../mwb.yaml",
            "-w", input_directory,
            "-o", output_directory,
            "-t", "../this-wiki-themes/basso",
            "--lunr"
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

def compare_directories(good_output_dir, generated_output_dir):
    """
    Compares the contents of the known good output directory with the generated output directory.
    Prints warnings for any discrepancies.
    Returns True if directories are the same, False if not.
    """

    # Set flag to pass
    compare_pass = True

    # Get the list of files in both directories
    good_output_files = set(os.listdir(good_output_dir))
    generated_output_files = set(os.listdir(generated_output_dir))
    
    # Find missing and extra files
    missing_files = good_output_files - generated_output_files
    extra_files = generated_output_files - good_output_files

    for missing in missing_files:
        compare_pass = False
        logging.warning(f"Missing file in generated output: {missing}")

    for extra in extra_files:
        compare_pass = False
        logging.warning(f"Extra file in generated output: {extra}")

    # Compare files that are present in both directories
    for common_file in good_output_files.intersection(generated_output_files):
        good_file_path = os.path.join(good_output_dir, common_file)
        generated_file_path = os.path.join(generated_output_dir, common_file)

        if not filecmp.cmp(good_file_path, generated_file_path, shallow=False):
            compare_pass = False
            logging.warning(f"Mismatch in file content: {common_file}")

def setup_args():
    parser = argparse.ArgumentParser(description="Test the mwb.py script by comparing its output to known good outputs.")
    parser.add_argument('--input', '-i', required=True, help="Directory of source Markdown files.")
    parser.add_argument('--output', '-o', required=True, help="Directory of mwb.py-generated output files.")
    parser.add_argument('--baseline', '-b', required=True, help="Directory of known good output files to compare against.")
    parser.add_argument('--random', '-r', action='store_true', help="Don't test, just return a random 0 or 1 exit code.")
    parser.add_argument('--force', '-f', choices=[0, 1], type=int, help='Force flag: 0 or 1')

    return parser.parse_args()

def main():
    args = setup_args()
    logging.info(f"args: {args}")

    if args.force is not None:
        return args.force

    if args.random:
        import random
        return random.randint(0, 1)

    if not run_mwb(args.input):
        logging.error("Aborting tests due to mwb.py failure.")
        return 0

    logging.info("Comparing directories...")
    if compare_directories(args.baseline, args.output):
        return 1
    else:
        return 0
    logging.info("Comparison finished.")

if __name__ == "__main__":
    exit(main())
