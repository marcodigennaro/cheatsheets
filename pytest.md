PYTEST cheatsheet
=================

conda install -c conda-forge pytest pytest-cov pytest-html pytest-mock

Usage
-----
pytest --cov #get coverage report

pytest file.py::test_name #run one test only

pytest -s #print output to console

coverage html #generate html report

test explicit error
```
def test_to_fail() -> None:
    with pytest.raises(ValueError):
```

Custom options
--------------
pytest --turbomole-integration
