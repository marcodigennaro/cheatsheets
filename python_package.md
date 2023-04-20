HOW TO CREATE A PYTHON PACKAGE
==============================

# from https://www.youtube.com/watch?v=5KEObONUkik&t=6s #

pip install wheel
python setup.py bdist_wheel


# from https://www.youtube.com/watch?v=DhUpxWjOhME #

* Reorganize and run pytest
  * separate test/src
  * create setup.py
  * create toml file with poetry init
  * create cfg file
  * create requirements.txt file
  * Pip install -e . #install the package
* Mypy/flake8/autopep8
  * Create requirements_dev.txt
  * Modify setup.cfg for type hinting
  * Touch src/module/py.typed
  * Add configuration options to toml file
  * pip install -r requirements_dev.txt
  * Run mypy src # checks integrity of type hinting
  * Run flake8 src
* Multiple envs with tax
  * Create tox.ini
* GitHub actions

