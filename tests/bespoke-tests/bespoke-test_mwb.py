#!/usr/bin/env python3

import argparse
import os
import filecmp

def compare_directories(good_output_dir, generated_output_dir):
    """
    Compares the contents of the known good output directory with the generated output directory.
    Prints warnings for any discrepancies.
    """
    # Get the list of files in both directories
    good_output_files = set(os.listdir(good_output_dir))
    generated_output_files = set(os.listdir(generated_output_dir))
    
    # Find missing and extra files
    missing_files = good_output_files - generated_output_files
    extra_files = generated_output_files - good_output_files

    for missing in missing_files:
        print(f"WARNING: Missing file in generated output: {missing}")

    for extra in extra_files:
        print(f"WARNING: Extra file in generated output: {extra}")

    # Compare files that are present in both directories
    for common_file in good_output_files.intersection(generated_output_files):
        good_file_path = os.path.join(good_output_dir, common_file)
        generated_file_path = os.path.join(generated_output_dir, common_file)

        if not filecmp.cmp(good_file_path, generated_file_path, shallow=False):
            print(f"WARNING: Mismatch in file content: {common_file}")


def main():
    parser = argparse.ArgumentParser(description="Test the mwb.py script by comparing its output to known good outputs.")

    # Directories arguments
    parser.add_argument('--test-files-dir', required=True, help="Directory of static test files.")
    parser.add_argument('--generated-output-dir', required=True, help="Directory of generated output files from mwb.py.")
    parser.add_argument('--good-output-dir', required=True, help="Directory of known good output files to compare against.")

    args = parser.parse_args()

    compare_directories(args.good_output_dir, args.generated_output_dir)


if __name__ == "__main__":
    main()
