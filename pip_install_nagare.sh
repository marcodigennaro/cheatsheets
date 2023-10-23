# CLEAR PIP CACHE
# rm -r ~/.cache/pip/selfcheck/
# python -m pip install --upgrade pip

# CLEAN CONDA CACHE
# conda clean -a -y

# CREATE NEW CONDA ENVIRONMENT
# conda create -n nagare python=3.10 -y
# conda activate nagare
# conda install conda=23.9.0

pip_packages='
   monty==2023.8.8
   pydantic==1.10.9
   pymatgen==2023.9.2
   jobflow==0.1.13
   jupyterlab
   nbclassic'

for package in `echo $pip_packages`; do
  echo ===============  pip install $package
  pip install $package
  echo ---------------  DONE
  done


conda_packages='
mongodb=6.0.2
ipython
nglview
ase
'

for package in `echo $conda_packages`; do
  echo ===============  conda install $package
  conda install -y -c conda-forge $package
  echo ---------------  DONE
  done


ext_pck_dir='/home/mdi0316/WORK_TME022/external_packages/'

cd $ext_pck_dir
for folder in turbomoleio nagare jobflow-remote;
    do
    cd $folder
    git pull
    echo pip install $folder
    pip install .
    echo ---------------  DONE
    cd $ext_pck_dir
    done


pip freeze | grep -e monty -e pydantic -e pymatgen -e jobflow -e mongodb -e turbomoleio -e nagare -e jobflow-remote
