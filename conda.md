CONDA cheatsheet
================

# show environment
echo $CONDA_DEFAULT_ENV

conda clean --all 

conda update --all

conda update pip

Solving environment takes too long 
----------------------------------

conda config --remove channels conda-forge

conda config --add channels conda-forge

conda config --set channel_priority flexible/strict

# change PS1 default

conda config --set changeps1 True

# deactivate default base

conda config --set auto_activate_base false


# CREATE ENV.yml

$ conda env export ENVNAME>ENV.yml

# UPDATE AND PRUNE

$ conda env update --prefix ./env --file environment.yml  --prune
