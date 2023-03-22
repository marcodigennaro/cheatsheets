#!/bin/bash
# Spread the tasks evenly among the nodes
# Want the node exlusively
#SBATCH --job-name=500K_80
#SBATCH -p nodeshiq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is `pwd`"

#module add mpich/ge/gcc

mpirun lmp_mpi -in in.merlet
