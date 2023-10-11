bespoke-test_mwb.py is script that is used to test mwb.py.

mwb.py is called like this:

./mwb.py -c ../mwb.yaml -w ../.. -o ../output -t ../this-wiki-themes/basso --lunr

the -w flag specifies an input directory with various markdown files.

the -o flag specifies an output directory with transformed files.

the input flags to the test script should specify a directory of static test files, a directory of the generated output files, and a directory of known good output files to compare against.

the test script should compare the known good output files with the generated output files, and generate warning messages about anything that doesn't match

bespoke-test_mwb.py is called like this:

```shell
./test_mwb.py --test-files-dir [path_to_test_files] --generated-output-dir [path_to_generated_outputs] --good-output-dir [path_to_known_good_outputs]
```
