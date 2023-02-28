#!/home/mdi0316/anaconda3/bin/python

import os
import pandas as pd
import shutil

label="C1MIM_BF4"
interaction="LJ_nm"

easy_dir='/home/mdi0316/WORK/SEP/EASY/'
int_dir =os.path.join( easy_dir, '3_BEADS', label, interaction )
int_csv =os.path.join( int_dir, 'easy.csv' )
if not os.path.exists( int_csv ):
   int_df = pd.DataFrame()
else:
   int_df = pd.read_csv(int_csv, index_col = 0 )

run_lmps=os.path.join(int_dir, "run_lammps.py")
inp_lmps=os.path.join(int_dir, "{}_lammps.dat".format(label) )

shutil.copy( run_lmps, "./" )
shutil.copy( inp_lmps, "./" )

import run_lammps

if __name__ == '__main__':
  df = run_lammps.main( label, interaction )
  if not df.empty:
    int_df = int_df.append( df, ignore_index = True )
    int_df.to_csv( int_csv )
