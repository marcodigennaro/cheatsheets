VMD cheatsheet
==============

Create PBC
----------
pbc box

pbc set {50 50 50}

pbc box -centersel center

PBC wrap command in vmd to re-center a protein in a simulation box
-----------------------------------------------------------------
https://www.youtube.com/watch?v=IeBpVabqzy0

* to wrap a trajectory:
pbc wrap -centersel "protein" -center com -compound residue -all

* to write dcd:
animate write dcd mohamed.dcd

Visulaize LAMMPS data
---------------------
topo readlammpsdata "path/to/file.lmp"
topo readlammpsdata "path/to/file.data"

Write LAMMPS Data File with VMD Software
----------------------------------------
topo retypebonds

topo gussangles

topo guessdihedrals

pbc box

pbc set {50 50 50}

molinfo top set a 30.0

molinfo top set b 30.0

molinfo top set c 30.0

molinfo top set alpha 90.0

molinfo top set beta 90.0

molinfo top set gamma 90.0

topo writelammpsdata data.lammps full

Make movies
-----------
ffmpeg -i file.mpg out.mp4
