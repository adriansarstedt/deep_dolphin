[![adriansarstedt](https://circleci.com/gh/adriansarstedt/deep_dolphin.svg?style=shield&circle-token=5f49fde881ddd893225b4fb0e2efe5af4f38222e)](https://app.circleci.com/pipelines/github/adriansarstedt/deep_dolphin)
[![codecov](https://codecov.io/gh/adriansarstedt/deep_dolphin/branch/master/graph/badge.svg?token=A918ZGR2WN)](https://codecov.io/gh/adriansarstedt/deep_dolphin)

# DeepDolphin

DeepDolphin is a library produced for the Austin Hospital of Melbourne.

It provides a work flow for automated brain tumour segmentation using neural network technology.

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
