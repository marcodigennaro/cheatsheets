# CLEAR PIP CACHE
# rm -r ~/.cache/pip/selfcheck/
# python -m pip install --upgrade pip

# CLEAN CONDA CACHE
# conda clean -a -y

# CREATE NEW CONDA ENVIRONMENT

conda create -n pgel-abinit python=3.10 -y
conda activate pgel-abinit
conda install conda=23.10.0

conda install -y -c conda-forge \
    ase           \
    pymatgen      \
    nglview       \
    openmpi       \
    abinit 
    #tblite        \
    #tblite-python \
    #xtb-python    \
    #jupyterlab    \
    #ffmpeg        \
    #imageio       \

    #statsmodels   \
    #asap3         \

    #gpaw          \
    #lammps        \

    #pipreqs       \
    #pre_commit    \
    #autopep8      \

    ## needed for ANI-ASE
    #fortran-compiler \
    #libcublas        \
   

pip install matgl

ext_pck_dir='/home/mdi0316/WORK_TME022/external_packages/'
cd $ext_pck_dir
git clone git@github.com:ehermes/ased3.git

for folder in ase ; do
    cd $ext_pck_dir/$folder
    echo pip install $folder
    git pull
    pip install .
    done
