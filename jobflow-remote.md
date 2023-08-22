JOBFLOW REMOTE
==============

*show job/flow list:

jf job list

jf job info -db 17 -err

jf -fe job info -db 17 -err

*generate new project

jf project generate --full NAME

*reset admin database:

jf runner status

jf admin reset  #if more than 25 jobs use `jf admin reset -max 0`

jf runner start

jf runner check

<<<<<<< HEAD
*
=======
export $JFREMOTE_PROJECT='PGEL'
>>>>>>> d1ce282a9451848f81f75538ad78c4ade1a00693
