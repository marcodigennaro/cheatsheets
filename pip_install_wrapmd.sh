
conda install -c conda-forge jobflow packmol moltemplate lammps pandas

ext_pck_dir='/home/mdi0316/WORK_TME022/external_packages/'

cd $ext_pck_dir
for folder in jobflow-remote; do
    cd $folder
    git pull
    echo pip install $folder
    pip install .
    echo ---------------  DONE
    cd $ext_pck_dir
    done
