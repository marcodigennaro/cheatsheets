# Initiate poetry and create pyproject.toml

### New project
poetry new poetry-demo

### Initialising a pre-existing project
cd pre-existing-project

poetry init

### Add Packages
poetry add numpy pandas ...

poetry config virtualenvs.in-project true
poetry new my-project

poetry init

poetry add numpy #and other dependencies
poetry install -vvv #install dependencies
poetry run python script.py # to run the shell

poetry env info
poetry update
poetry build
