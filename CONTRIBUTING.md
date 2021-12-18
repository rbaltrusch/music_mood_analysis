# Contributions to Music Mood Analysis

Welcome to Music Mood Analysis and thanks for considering to contribute to this repository! Every contribution is welcome, no matter how small or large.

## Open points

Currently there are no large plans for this repository, but contributions of any kind are always welcome!
Simply submit an issue that details your contribution idea and submit a pull request to fix that issue.

## Setting up your branch

To setup your local development environment, open a terminal and run the following:

```
git clone https://github.com/rbaltrusch/music_mood_analysis
python -m pip install -r requirements.txt
python -m pip install -r tests/requirements.txt
```

### Using Conda env

If you are using conda, you could setup your development virtual environment using the following command:

```
conda env update --file environment.yml --name test-env
```

### Tests

To run all tests, run the following commands:
```
cd tests
python run_tests.py --all
```

All other test options can be listed using:
```
python run_tests.py -h
```

Please make sure that all tests still pass after your contribution. If code changes are implemented on your branch, please also commit new tests or update existing tests, if applicable.

### Github Actions

After pushing to your branch, you should be able to see whether the existing workflows still pass. Make sure that all workflows that passed before your changes are still passing, otherwise your pull request will need to fix those failures first after being submitted.

### Pre-commit hooks

To be consistent with coding guidelines, it would be desireable to also set up pre-commit hooks using the pre-commit module:

```
pip install pre-commit
pre-commit install
```

All commits will now be checked before being accepted. Some of the tests may automatically fix your files if they fail. These will not be staged and have to be added to the staging index before re-attempting the commit.

As the pre-commit pylint has issues importing external modules, it is acceptable to ignore pylint failures after reviewing that nothing else fails, using:

```
git commit --no-verify
```

## Pull requests

The general procedure for submitting pull requests that can be easily reviewed and accepted is detailed in the [pull request template](.github/pull_request_template.md).
Please go through the points specified in the template before submitting your pull request to avoid a lengthy back-and-forth between reviews and refactoring your changes.

### Pull requests without issues

If what you are improving on in your pull request is not detailed in any issue, it would be great if you could submit an issue first and then submit your pull request, referencing that issue.

## Contact

For any questions or feedback, please raise an issue or reach out to me by email: richard@baltrusch.net.
