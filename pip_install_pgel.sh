# CLEAR PIP CACHE
# rm -r ~/.cache/pip/selfcheck/
# python -m pip install --upgrade pip

# CLEAN CONDA CACHE
# conda clean -a -y

# CREATE NEW CONDA ENVIRONMENT
# conda create -n pgel python=3.10 -y
# conda activate pgel
# conda install conda=23.9.0

pip_packages='
    jupyterlab
    nbclassic'

for package in `echo $pip_packages`; do
    echo ===============  pip install $package
    pip install $package
    echo ---------------  DONE
    done

conda_packages='
    ase
    pymatgen
    nglview
    asap3
    gpaw
    openmpi
    tblite
    tblite-python
    xtb-python
    '

for package in `echo $conda_packages`; do
  echo ===============  conda install $package
  conda install -y -c conda-forge $package
  echo ---------------  DONE
  done
