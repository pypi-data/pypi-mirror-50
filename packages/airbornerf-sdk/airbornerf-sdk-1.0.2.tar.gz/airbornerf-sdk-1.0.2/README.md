# AirborneRF Python SDK

## Release

When the pipeline successfully ran, release the package to PyPI:

```bash
rm -rf dist
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

Check the project page: https://pypi.org/project/airbornerf-sdk/
