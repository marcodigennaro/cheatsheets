#from  http://chembytes.wikidot.com/grocnt

fname=$1

cp /home/mdi0316/WORK/09_SEP/MWCNT/Inputfiles/${fname}.pdb .
cp /home/mdi0316/WORK/09_SEP/MWCNT/Inputfiles/*mdp .

gmx editconf -f ${fname}.pdb -o ${fname}.gro -box 4 4 5  -angles 90 90 90
gmx x2top -f ${fname}.gro -o topol.top  -ff cnt_oplsaa -name CNT -noparam -pbc
sed -i~ '/\[ dihedrals \]/,/\[ system \]/s/1 *$/3/' topol.top

gmx grompp -f em.mdp -c ${fname}.gro -p topol.top -o em.tpr > em.out 2> em.err
gmx mdrun -v -deffnm em -g em.log
printf  "8\n0\n" | gmx energy -f em.edr -o potential.xvg

gmx grompp -f nvt.mdp -c em.gro    -p topol.top -o nvt.tpr -r em.gro > nvt.out 2> nvt.err
gmx mdrun  -deffnm nvt -g nvt.log
printf "13\n0\n" | gmx energy -f nvt.edr -o temperature.xvg

gmx grompp -f npt.mdp -c nvt.gro   -p topol.top -o npt.tpr -r nvt.gro -t nvt.cpt > npt.out 2> npt.err
gmx mdrun  -deffnm npt -g npt.log
printf "15\n0\n" | gmx energy -f npt.edr -o pressure.xvg

gmx grompp -f md.mdp -c npt.gro  -p topol.top -o  md.tpr -t npt.cpt > md.out 2> md.err
gmx mdrun  -deffnm md -g md.log
printf "20\n0\n" | gmx energy -f md.edr -o density.xvg

printf "0\n0\n" | gmx trjconv -s  em.tpr -f  em.xtc -o  em_noPBC.xtc -pbc mol -center
printf "0\n0\n" | gmx trjconv -s nvt.tpr -f nvt.xtc -o nvt_noPBC.xtc -pbc mol -center
printf "0\n0\n" | gmx trjconv -s npt.tpr -f npt.xtc -o npt_noPBC.xtc -pbc mol -center
printf "0\n0\n" | gmx trjconv -s  md.tpr -f  md.xtc -o  md_noPBC.xtc -pbc mol -center

# mkdir stretch
# cd stretch
# ln ../md* .
# ln ../npt.gro .
# gmx grompp -f stretch.mdp -c npt.gro -p topol.top -o stretch.tpr -t md.cpt
# gmx mdrun  -deffnm stretch -g stretch.log
