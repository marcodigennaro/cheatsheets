# CLEAR PIP CACHE
# rm -r ~/.cache/pip/selfcheck/
# python -m pip install --upgrade pip

# CLEAN CONDA CACHE
# conda clean -a -y

# CREATE NEW CONDA ENVIRONMENT
# conda create -n pgel python=3.10 -y
# conda activate pgel
# conda install conda=23.10.0

conda install -y -c conda-forge \
    ase           /
    pymatgen      /
    nglview       /
    asap3         /
    gpaw          /
    openmpi       /
    tblite        /
    tblite-python /
    xtb-python    /
    jupyterlab    /
    ffmpeg        /
    lammps


pip install matgl

ext_pck_dir='/home/mdi0316/WORK_TME022/external_packages/'

for folder in ase; do
    cd $ext_pck_dir/$folder
    echo pip install $folder
    git pull
    pip install .
    done
