#!/usr/bin/sh


ev2ha=27.211
ang2bo=1.89

for bb in `cat all_mp2`; do
  echo begin
  echo comm
  cd $bb
  ene=`grep "TOT.EN. " tmp_log | awk '{print $2/27.211}'`
  cat atomic_coords_and_charges.csv | sed "s/,/ /g" | tail -5 | awk '{print atom"  "1.89*$4"  "1.89*$5"  "1.89*$6"  "$2"  "$8"  "0"  "0"  "0"  "0  }'
  echo energy $ene
  echo charge -1
  echo end
  cd /data/mdi0316/WORK/MONOMERS/BF4 
done
