# Bespoke Tests

bespoke-test_mwb.py is a script that is used to test mwb.py.

The test script compares the known baseline files with the generated output files, and generates warning messages about anything that doesn't match.

When Massive Wiki Builder is installed in a wiki, bespoke-test_mwb.py is called like this:

```shell
# cd YOURWIKIDIR/.massivewikibuilder/massivewikibuilder/tests/bespoke-tests
./bespoke-test_mwb.py -i test-input -o output -b baseline
```

bespoke-test_mwb.py exits with a return code of 0 for success, or non-zero if there is a fault.

a successful test output looks like this:

```shell
INFO: args: Namespace(input='test-input', output='output', baseline='baseline', random=False, force=None)
INFO: Running mwb.py...
INFO: mwb.py executed successfully.
INFO: Comparing directories...
```
