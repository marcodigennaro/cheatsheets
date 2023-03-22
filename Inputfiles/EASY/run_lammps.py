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
from numpy import linalg as LA

scripts_dir = '/home/mdi0316/FUNCTIONS'
classes_dir = '/home/mdi0316/CLASSES'
sys.path.insert(0, scripts_dir)
sys.path.insert(0, classes_dir)

import EASY 
import LAMMPS 
from Functions import get_block_from_df 

now = datetime.now()
month = now.strftime("%B") 

def find_intersection_x_axis( df, column, x_axis='Radius' ):
    pos_energy_block = df.loc[ df[column] > 0 ] 
    neg_energy_block = df.loc[ df[column] < 0 ] 
    if neg_energy_block.empty:
      print('no negative energies in {}'.format(column))
      return 1e6
    elif pos_energy_block.empty:
      print('no positive energies in {}'.format(column))
      return 1e6
    else: 
      lowest_positive_line = pos_energy_block.loc[ pos_energy_block[x_axis] == pos_energy_block[x_axis].min() ] 
      highest_negative_line = neg_energy_block.loc[ neg_energy_block[x_axis] == neg_energy_block[x_axis].max() ] 
      x1 = lowest_positive_line[x_axis].values[0]
      y1 = lowest_positive_line[column].values[0]
      x2 = highest_negative_line[x_axis].values[0]
      y2 = highest_negative_line[column].values[0]
      slope = (y1-y2)/(x1-x2)
      offset = (x1*y2-x2*y1)/(x1-x2)
      intersection = -offset/slope
      return intersection

def main(dimer_label, interaction):

    csv_dir = '/home/mdi0316/WORK/SEP/DIMERS/{}/CSV/N311/B3LYP/SCAN_from_ISOLATED/'.format(dimer_label)
    dft_csv_file = os.path.join( csv_dir, 'scan_dft.csv' )
    mp2_csv_file = os.path.join( csv_dir, 'scan_mp2.csv' )
    
    dft_df = pd.read_csv( dft_csv_file, index_col=0 )
    mp2_df = pd.read_csv( mp2_csv_file, index_col=0 )
    
    tot_df = pd.merge( dft_df, mp2_df, on=['Radius', 'Theta', 'Phi'] )
    
    dft_ene     = tot_df['MP2.EN.'].values
    dft_coul    = tot_df['COUL.EN._y'].values
    radius_list = tot_df['Radius'].values
    radius_list = list(set(list(tot_df['Radius'].values)))
    theta_list  = list(set(list(tot_df['Theta'].values)))
    phi_list    = list(set(list(tot_df['Phi'].values)))
    radius_list.sort()
    theta_list.sort()
    phi_list.sort()

 
    lmps_dat_file = '{}_lammps.dat'.format(dimer_label)
    lmps_run_dir = os.getcwd()

    easy_iter = EASY.EASY_RUN( lmps_run_dir )
    easy_iter.dat_to_csv_file()

    lmps_obj = LAMMPS.LAMMPS_EASY( lmps_run_dir, 'lmps', template_lmps_name = 'lammps_clusters.in' ) 

    ### WRITE AND RUN LAMMPS
    templ_lines = open( lmps_obj.lmp_template, 'r' ).readlines()
    lmps_dat_lines = open( lmps_dat_file, 'r' ).readlines()
    task_dat_lines = open( easy_iter.dat_file, 'r' ).readlines()

    if interaction in ['LJ_nm', 'LJ_nm_coul'] :
       nn, mm = [ float(ii) for ii in task_dat_lines[-2:] ]
       task_dat_lines = task_dat_lines[:-2]

    if len(task_dat_lines) == 5: #NKK = 1
       ee1, ee2, ss1, ss2 = [ float(ii) for ii in task_dat_lines[1:len(task_dat_lines)] ]
       ees = cycle([ee1, ee2])
       sss = cycle([ss1, ss2])

    elif len(task_dat_lines) == 8: #NKK = 2
       bond1, ee1, ee2, ee3, ss1, ss2, ss3 = [ float(ii) for ii in task_dat_lines[1:len(task_dat_lines)] ]
       bonds = cycle([bond1])
       ees = cycle([ee1, ee2, ee3])
       sss = cycle([ss1, ss2, ss3])

    elif len(task_dat_lines) == 12: #NKK = 3
       bond1, bond2, angle1, ee1, ee2, ee3, ee4, ss1, ss2, ss3, ss4 = [ float(ii) for ii in task_dat_lines[1:len(task_dat_lines)] ]
       bonds = cycle([bond1, bond2])
       angles = cycle([angle1])
       ees = cycle([ee1, ee2, ee3, ee4])
       sss = cycle([ss1, ss2, ss3, ss4])

    with open( lmps_obj.inp_file, 'w+' ) as lmps_inp:
      for l1 in templ_lines:
        new_l1 = l1
        if l1 == '## -- PROPERTY COMPUTE -- #\n':
           for l2 in lmps_dat_lines:
             new_l2 = l2
             if new_l2.startswith( 'bond_coeff' ):
                new_l2_list = new_l2.split() 
                new_l2_list[-1] = str(next(bonds))
                new_l2_list.append( '\n' )
                new_l2 = ' '.join(new_l2_list)
             elif new_l2.startswith( 'angle_coeff' ):
                new_l2_list = new_l2.split() 
                new_l2_list[-1] = str(next(angles))
                new_l2_list.append( '\n' )
                new_l2 = ' '.join(new_l2_list)
             elif new_l2.startswith( 'pair_coeff' ):
                new_l2_list = new_l2.split() 
                new_l2_list[3] = str(next(ees))
                new_l2_list[4] = str(next(sss))
                if interaction in ['LJ_nm', 'LJ_nm_coul'] :
                   new_l2_list[5] = str(nn)
                   new_l2_list.append( str(mm) )
                new_l2_list.append( '\n' )
                new_l2 = ' '.join(new_l2_list)
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

    ### POST PROCESSING
    
    ## write task.res
    if interaction in [ 'LJ', 'LJ_nm' ]:
       column = 'DISP.EN._y'
    elif interaction in [ 'LJ_coul', 'LJ_nm_coul' ]:
       column = 'MP2.EN.'
    lmps_df = easy_iter.write_lmps_csv()
    dist_Emin = 0 #distance between two minima
    dist_E0   = 0 #distance between two intersections with x axix
    delta_E   = 0 #difference of all energies

    for T in theta_list:
      for P in phi_list:
        tmp_lmps_df = get_block_from_df( lmps_df, [ ('Theta', T), ('Phi', P) ] )
        tmp_tot_df = get_block_from_df( tot_df, [ ('Theta', T), ('Phi', P) ] )

        # find minimum of energy curve 
        min_lmps_ener = tmp_lmps_df['LMP.INT.EN.'].min() 
        max_lmps_ener = tmp_lmps_df['LMP.INT.EN.'].max() 
        min_lmps_line = tmp_lmps_df.loc[ tmp_lmps_df['LMP.INT.EN.'] == min_lmps_ener ]
        min_lmps_rad  = min_lmps_line['Radius']

        min_mp2_ener = tot_df[column].min() 
        max_mp2_ener = tot_df[column].max() 
        min_mp2_line = tot_df.loc[ tot_df[column] == min_mp2_ener ]
        min_mp2_rad  = min_mp2_line['Radius']

        min_lmps = np.array([ min_lmps_ener/max_lmps_ener, min(min_lmps_rad.values) ]) ## there could be degenerate values on the tail
        min_gms  = np.array([ min_mp2_ener/max_mp2_ener, min_mp2_rad.values[0] ])
        dist_Emin += LA.norm( [min_lmps - min_gms] )

        # find intersection with x axis
        mp2_E0 = find_intersection_x_axis( tot_df, column )
        lmps_E0 = find_intersection_x_axis( lmps_df, 'LMP.INT.EN.' )
        dist_E0 += abs( mp2_E0 - lmps_E0 )

        # difference of all energies
        delta_E += sum( [ abs( lmps_en-mp2_en ) for (lmps_en, mp2_en) in zip( lmps_df['LMP.INT.EN.'], tot_df[column]) ] )

    sp.call( 'echo {} >  task.res '.format(dist_Emin), shell=True )
    sp.call( 'echo {} >> task.res '.format(dist_E0), shell=True )
    sp.call( 'echo {} >> task.res '.format(delta_E), shell=True )

    ## write easy.csv 

    new_task_dat = open( lmps_obj.task_dat, 'r' ).read().split()
    task_id = open( lmps_obj.task_id, 'r' ).read().split()
    
    task_dict = { 'id' : task_id[0], 'dist.Emin.': dist_Emin, 'dist.E0': dist_E0, 'delta.E': delta_E }

    if len(new_task_dat) == 14: #NKK = 3
      task_dict['l1']  = new_task_dat[1]
      task_dict['l2']  = new_task_dat[2]
      task_dict['ang'] = new_task_dat[3]
      task_dict['e1']  = new_task_dat[4]
      task_dict['e2']  = new_task_dat[5]
      task_dict['e3']  = new_task_dat[6]
      task_dict['e4']  = new_task_dat[7]
      task_dict['s1']  = new_task_dat[8]
      task_dict['s2']  = new_task_dat[9]
      task_dict['s3']  = new_task_dat[10]
      task_dict['s4']  = new_task_dat[11]
      task_dict['n']   = new_task_dat[12]
      task_dict['m']   = new_task_dat[13]
    else:
      print( unknown_task_dat )

    return( pd.DataFrame( [task_dict] ))

if __name__ == "__main__":
  main(dimer_label, interaction)

