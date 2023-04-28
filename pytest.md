PYTEST cheatsheet
=================

conda install -c conda-forge pytest

conda install -c conda-forge pytest-cov

conda install -c conda-forge pytest-html

conda install -c conda-forge pytest-mock

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
