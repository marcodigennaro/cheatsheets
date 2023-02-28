#!/bin/sh

month="09_SEP"
main_dir="/home/mdi0316/WORK/${month}/MWCNT"
inpf_dir="/home/mdi0316/WORK/${month}/MWCNT/Inputfiles"
run_dir="/home/mdi0316/WORK/${month}/MWCNT/RUNS/${1}"
mkdir -p $run_dir
cd $run_dir

cp ${inpf_dir}/${1}.pdb .
cp ${inpf_dir}/em.mdp .
cp ${inpf_dir}/md.mdp .
cp -r ${main_dir}/${1}_oplsaa.ff .
echo  ${main_dir}/${1}_oplsaa.ff 

gmx x2top -f ${1}.pdb -o topol.top -ff ${1}_oplsaa -name ${1} -noparam
sed -i~ '/\[ dihedrals \]/,/\[ system \]/s/1 *$/3/' topol.top

gmx editconf -f ${1}.pdb -o boxed.gro -bt dodecahedron -d 1

gmx grompp -f em.mdp -c boxed.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em

gmx grompp -f md.mdp -c em.gro -p topol.top -o md.tpr
gmx mdrun -v -deffnm md

printf "0\n0\n" | gmx trjconv -s  md.tpr -f md.xtc -o  md_noPBC.xtc -pbc mol -center
#gmx trjconv -f md.xtc -s md.tpr -o md_centered.xtc -pbc mol -center
#gmx trjconv -s md.tpr -f md_centered.xtc -o md_fit.xtc -fit rot+trans
#vmd em.gro md_fit.xtc
