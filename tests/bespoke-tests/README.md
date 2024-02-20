# Bespoke Tests

bespoke-test_mwb.py is a script that is used to test mwb.py.

The test script compares the known baseline files with the generated output files, and generates warning messages about anything that doesn't match.

In the Massive Wiki Builder repo:  
 -  `bespoke-test_mwb.py` is called like this:
```shell
cd tests/bespoke-tests
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r ../../requirements.txt
./bespoke-test_mwb.py -i test-input -b baseline
```

 - only if needed: to rebuild the `baseline` output directory:  
 ```shell
cd tests/bespoke-tests
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r ../../requirements.txt
../../mwb.py -c test-input/.massivewikibuilder/mwb.yaml -w test-input -o baseline -t test-input/.massivewikibuilder/this-wiki-themes/basso
```

When Massive Wiki Builder is installed in a wiki, bespoke-test_mwb.py is called like this:

```shell
cd YOURWIKIDIR/.massivewikibuilder/massivewikibuilder/tests/bespoke-tests
bespoke-test_mwb.py -i test-input -b baseline --mwb-config test-input/.massivewikibuilder/mwb.yaml --mwb-templates test-input/.massivewikibuilder/this-wiki-themes/basso
```

bespoke-test_mwb.py exits with a return code of 0 for success, or non-zero if there is a fault.

A successful test output looks like this:

```shell
INFO: args: Namespace(input='test-input', baseline='baseline', random=False, force=None, mwb_output='test-output', mwb_config='test-input/.massivewikibuilder/mwb.yaml', mwb_templates='test-input/.massivewikibuilder/this-wiki-themes/basso')
INFO: Running mwb.py...
INFO: mwb.py executed successfully.
INFO: Comparing directories...
INFO: Comparison finished, no faults.
```

## Scope and Limitations

The current test suite does not build or check the Lunr search files.
