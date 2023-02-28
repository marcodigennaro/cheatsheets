#!/home/mdi0316/anaconda3/bin/python

import os, sys, re
import numpy as np
import pandas as pd
import math
import shutil
from scipy import integrate
from datetime import datetime
import subprocess as sp
import shutil
from itertools import cycle

scripts_dir = '/home/mdi0316/FUNCTIONS'
classes_dir = '/home/mdi0316/CLASSES'
sys.path.insert(0, scripts_dir)
sys.path.insert(0, classes_dir)

from numpy.linalg import norm

import EASY 
import LAMMPS 

now = datetime.now()
month = now.strftime("%B") 
desktop_work_dir = '/home/mdi0316/WORK/{}'.format(month[:3].upper())

basis  = 'N311'
funct  = 'B3LYP'
dimer  = 'C1MIM_BF4'
csv_dir = os.path.join( desktop_work_dir, 'DIMERS', dimer, 'CSV', basis, funct, 'SCAN_from_ISOLATED' ) 
dft_csv_file = os.path.join( csv_dir, 'scan_dft.csv' )
mp2_csv_file = os.path.join( csv_dir, 'scan_mp2.csv' )

mp2_df = pd.read_csv( mp2_csv_file, index_col=0 )
mp2_df = mp2_df.astype( float )

radius_list = list( set( list(mp2_df['Radius'].values)))
theta_list  = list( set( list(mp2_df['Theta'].values)))
phi_list    = list( set( list(mp2_df['Phi'].values )))

#radius_list = np.arange( 2, 16, 1.0 )
theta_list  = [90]
phi_list    = [90] 

radius_list.sort()
theta_list.sort()
phi_list.sort()

easy_label  = 'lmps' #.format(dft_label)

tmp_label   = sys.argv[1]
interaction = sys.argv[2]
geometry    = sys.argv[3]

if tmp_label == 'NKK_MERLET':
  n_beads = 3
else:
  n_beads = int(tmp_label.replace('NKK_', ''))

def main():
 
    lmps_run_dir = os.getcwd()

    easy_iter = EASY.EASY_RUN( lmps_run_dir )

    lmps_obj  = LAMMPS.LAMMPS_EASY( lmps_run_dir, easy_label, template_lmps_name = 'lammps_clusters.in' ) 

    ### WRITE AND RUN LAMMPS
    templ_lines = open( lmps_obj.lmp_template, 'r' ).readlines()
    lmps_lines = open( '{}_lammps.dat'.format(tmp_label), 'r' ).readlines()
    easy_lines = open( 'task.dat', 'r' ).readlines()[1:]  #read and remove heading


    # GEOMETRY
    if geometry:
       bonds = [ float(ii) for ii in easy_lines[:3] ]
       angle = float( easy_lines[3] )
       easy_lines = easy_lines[3:]  #remove geometry lines 

    # INTERACTION
    if interaction in ['LJ_nm', 'LJ_nm_coul'] :
       nn, mm = [ float(ii) for ii in easy_lines[-2:] ]
       easy_lines = easy_lines[:-2] #remove exponents lines
    else:
       nn, mm = 6, 12
    
    #lines left are epsilons and sigmas
    eps = [ float(ii) for ii in easy_lines[:n_beads+1] ] 
    sig = [ float(ii) for ii in easy_lines[1+n_beads:] ]
    
    #if interaction == 'LJ':
    #   int_ini_line = 'pair_style lj/cut 30.0\n'
    #   int_fin_line = 'pair_modify mix geometric\n'
    #elif interaction == 'LJ_coul':
    #   int_ini_line = 'pair_style jl/cut/long/coul 30.0\n'
    #   int_fin_line = '\n'
    #if interaction == 'LJ_nm':
    #   int_ini_line = 'pair_style nm/cut 30.0\n'
    #   int_fin_line = 'pair_modify mix geometric\n'
    #elif interaction == 'LJ_nm_coul':
    #   int_ini_line = 'pair_style nm/cut/coul/long 30.0\n'
    #   int_fin_line = '\n'


    with open( lmps_obj.inp_file, 'w+' ) as lmps_inp:
      for l1 in templ_lines:
        new_l1 = l1
        if l1.startswith( 'kspace' ) and interaction in [ 'LJ_nm', 'LJ_nm_coul' ]:
           new_l1 = ''
        if l1 == '## -- PROPERTY COMPUTE -- #\n':
           for l2 in lmps_lines:
             new_l2 = l2
            
             if geometry:
                if new_l2.startswith( 'bond_coeff  1' ):
                   new_l2 = 'bond_coeff  1 1.0 {}\n'.format(bonds[0])
                elif new_l2.startswith( 'bond_coeff  2' ):
                   new_l2 = 'bond_coeff  2 1.0 {}\n'.format(bonds[1])
                elif new_l2.startswith( 'angle_coeff 1' ):
                   new_l2 = 'angle_coeff 1 1.0 {}\n'.format(angle)

             ## LJ ( w/coul )
             if interaction in [ 'LJ', 'LJ_coul' ]:
                for ii, jj in zip( range(n_beads+1), range(n_beads+1) ):
                  ee = eps[ii]
                  ss = sig[ii]
                  if new_l2.startswith( 'pair_coeff {} {}'.format( ii+1, jj+1 ) ): 
                     new_l2 = 'pair_coeff {} {} {:4.8f} {:4.8f} 30.0\n'.format( ii + 1, jj + 1, ee, ss ) 

             ## LJ + NM ( w/coul )
             if interaction in [ 'LJ_nm', 'LJ_nm_coul' ]:
                for ii in range(n_beads+1):
                  for jj in range(ii,n_beads+1):
                    ee_ii, ee_jj = eps[ii], eps[jj]
                    ss_ii, ss_jj = sig[ii], sig[jj]
                    ee = math.sqrt( ee_ii * ee_jj )
                    ss = math.sqrt( ss_ii * ss_jj )
                    if new_l2.startswith( 'pair_coeff {} {}'.format( ii+1, jj+1 ) ): 
                       new_l2 = 'pair_coeff {} {} {:1.8e} {:1.8e} {:d} {:d}\n'.format( ii + 1, jj + 1, ee, ss, int(nn), int(mm) ) 

             lmps_inp.write( new_l2 )

        elif l1.startswith('fix frzring  ring'):
           new_l1 = '#\n'

        elif l1.startswith('variable dist   index   dist_values'):
           new_l1 = 'variable dist   index   {}\n'.format( [ float(rr) for rr in radius_list ] ).replace('[','').replace(']','').replace(',', ' ')
        elif l1.startswith('variable theta  index   theta_values'):
           new_l1 = 'variable theta  index   {}\n'.format( [ float(tt) for tt in theta_list ] ).replace('[','').replace(']','').replace(',', ' ') 
        elif l1.startswith('variable phi    index   phi_values'):
           new_l1 = 'variable phi    index   {}\n'.format( [ float(pp) for pp in   phi_list ] ).replace('[','').replace(']','').replace(',', ' ') 

        lmps_inp.write( new_l1 )

    sp.call( '/home/mdi0316/bin/lmp_src -in lmps.inp > out.lmps 2> err.lmps ', shell=True )

    ###
    ### lmps_obj.write_and_run( R_LIST = radius_list,  minimize_condition = 'T' )
    ###

    # easy writing DE, res and bakcup input files
    easy_iter.write_lmps_csv()
    lmps_pot_csv = easy_iter.lmps_pot_csv
    lmps_pot_df  = pd.read_csv( lmps_pot_csv, index_col = 0 )
 
    ref_col = 'MP2.EN.'

    delta_df = pd.DataFrame( columns = [ 'Radius', 'Theta', 'Phi', ref_col, 'LMP.INT.EN.', 'DELTA.EN.' ] )

    #if interaction in [ 'LJ_coul', 'LJ_nm_coul' ]:
    #   ref_col = 'MP2.EN.'
    #elif interaction in [ 'LJ', 'LJ_nm' ]:
    #   ref_col = 'DISP.EN.'

    for idx, mp2_row in mp2_df.iterrows():
     
      tmp_r, tmp_t, tmp_p, ref_en = mp2_row[['Radius', 'Theta', 'Phi', ref_col]]
      lmps_row = lmps_pot_df.loc[ lmps_pot_df['Radius'] == tmp_r ].loc[
                                  lmps_pot_df['Theta']  == tmp_t ].loc[
                                  lmps_pot_df['Phi']    == tmp_p ]
      if math.isnan( mp2_row[ref_col] ) or lmps_row.empty:
         pass
      else:
         lmps_en = lmps_row['LMP.INT.EN.'].values[0]
         delta_serie = pd.Series( { 'Radius' : tmp_r, 'Theta' : tmp_t, 'Phi' : tmp_p, 
                                    ref_col : ref_en, 'LMP.INT.EN.' : lmps_en, 'DELTA.EN.' : ref_en - lmps_en } )
         delta_df = delta_df.append( delta_serie, ignore_index=True )
         #tmp_idx = lmps_row.index.values[0]
         #delta_df.at[tmp_idx, ref_col] = mp2_row[ref_col]
         #delta_df.at[tmp_idx, 'DELTA'] = mp2_row[ref_col] - lmps_row['LMP.INT.EN.'].values 
#
    delta_df.to_csv( 'delta.csv' )

    min_lmp_e = delta_df['LMP.INT.EN.'].min()
    min_lmp_r = delta_df.loc[ delta_df['LMP.INT.EN.'] == min_lmp_e ]['Radius'].values[0] 

    min_mp2_e = delta_df[ref_col].min()
    min_mp2_r = delta_df.loc[delta_df[ref_col] == min_mp2_e ]['Radius'].values[0] 

    #delta_energy = delta_df['DELTA.EN.'].sum() /  max([ abs(dd) for dd in delta_df['DELTA.EN.'] ])
    delta_energy = sum([ abs(dd) for dd in delta_df['DELTA.EN.'] ]) / max([ abs(dd) for dd in delta_df['DELTA.EN.'] ])
    delta_radius = norm( np.array([min_lmp_r, min_lmp_e]) - np.array([min_mp2_r, min_mp2_e]) )
    print( [min_lmp_r, min_lmp_e] ) 
    print( [min_mp2_r, min_mp2_e] )

    sp.call( 'echo {} > task.res '.format(delta_energy), shell=True )
    sp.call( 'echo {} >> task.res '.format(delta_radius), shell=True )

if __name__ == "__main__":
  main()

