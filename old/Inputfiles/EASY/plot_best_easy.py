#!/home/mdi0316/anaconda3/bin/python

import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

scripts_dir = '/home/mdi0316/FUNCTIONS'
sys.path.insert(0, scripts_dir)

from Functions import *

def create_subplot( tmp_rad, tmp_val, ax):
    
    sub_plt = ax.plot( tmp_rad, tmp_val )
    
    return sub_plt

work_dir = os.getcwd()

interaction = sys.argv[1]
dimer = work_dir.split('/')[-1]
month = work_dir.split('/')[4]
interac_dir = os.path.join( work_dir, interaction )

all_out = [ o for o in os.listdir( interac_dir ) if o.startswith( 'out_L1_' )]

min_obj = 1e6

for out_name in all_out:
  out_file = os.path.join( interac_dir, out_name )
  out_lines = open( out_file, 'r' ).readlines()
  out_lines = [ line for line in out_lines if not line.startswith('#') ]
  for line in out_lines:
    obj = float(line.split()[0])
    var = line.split()[1:]
    if obj < min_obj:
       min_obj = obj
       min_var = var
       
if interaction == 'LJ_nm_coul' and len(min_var) == 12:
  l1, l2, ang, e1, e2, e3, e4, s1, s2, s3, s4, n = [ float(v) for v in min_var ]
elif interaction == 'LJ_nm' and len(min_var) == 12:
  l1, l2, ang, e1, e2, e3, e4, s1, s2, s3, s4, n = [ float(v) for v in min_var ]

csv_dir = '/home/mdi0316/WORK/{}/DIMERS/{}/CSV/N311/B3LYP/SCAN_from_ISOLATED'.format(month, dimer)
dft_csv = os.path.join( csv_dir, 'scan_dft.csv' )
mp2_csv = os.path.join( csv_dir, 'scan_mp2.csv' )
dft_df  = pd.read_csv( dft_csv, index_col = 0 )
mp2_df  = pd.read_csv( mp2_csv, index_col = 0 )

ener_df = pd.merge( dft_df, mp2_df, on=['Radius', 'Theta', 'Phi'], how='inner' )

r_list = list(set(ener_df['Radius'].values )) 
r_list.sort()
t_list = list(set(ener_df['Theta'].values )) 
t_list.sort()
p_list = list(set(ener_df['Phi'].values )) 
p_list.sort()  

num_rows = len(t_list)
num_cols = len(p_list)

fig, ax = plt.subplots(num_cols, num_rows, sharex='col', sharey='row', figsize=(12,6))

column_list = ['DISP.EN._y', 'DISP.EN._x', 'INT.EN._x', 'INT.EN._y']
color_list = ['m', 'r', 'b', 'c']


for pp, P in enumerate(p_list):
  for tt, T in enumerate(t_list):
    tmp_df = ener_df.loc[ ener_df['Theta'] == T ].loc[ ener_df['Phi'] == P ]
    tmp_rad = tmp_df['Radius']
    max_rad = tmp_df.max()['Radius']
    for column, color in zip( column_list, color_list ):
      max_col = tmp_df.loc[ tmp_df['Radius'] == max_rad ][column]
      tmp_col = tmp_df[column] - float(max_col)
      tmp_rad, tmp_col = zip(*sorted(zip(tmp_rad, tmp_col)))
      ax.plot( tmp_rad, tmp_col, label = column, color = color )
      min_en = tmp_df[column].min()
      min_rad = tmp_df.loc[ tmp_df[column] == min_en ]['Radius'].values[0]
      xx = np.linspace(1,20,1e3)
      yy = LJ_nm_energy( xx, min_en, min_rad, n, 12 )
      ax.plot( xx, yy, color = color )
    ax.axhline(y=0.0, color = 'k', ls='--')
    ax.set_ylim( [-10,1] )
plt.legend()
plt.show()

           
