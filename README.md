[![adriansarstedt](https://circleci.com/gh/adriansarstedt/deep_dolphin.svg?style=svg)](https://app.circleci.com/pipelines/github/adriansarstedt/deep_dolphin)

# DeepDolphin

DeepDolphin is a library of work produced for the Austin Hospital of Melbourne.

It focuses on providing a work flow for automated brain tumour segmentation using neural network technology.

## Setup

In order to import the library locally and thereby test it, the project directory must be added to the `$PYTHONPATH`:

```
export PYTHONPATH="$PYTHONPATH:$PWD"
```

## Testing

Testing is implemented using [nosetests](https://nose.readthedocs.io/en/latest/usage.html). Full test suite can be run using:

```
make test
```
