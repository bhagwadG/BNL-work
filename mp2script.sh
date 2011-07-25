#!/bin/sh

export PWD=`pwd`
# File containing ring secret
export MPD_CONF_FILE=~/.mpd.conf

# Condor environment
_PWD=$PWD
_CONDOR_PROCNO=$_CONDOR_PROCNO
_CONDOR_NPROCS=$_CONDOR_NPROCS

CONDOR_SSH=`condor_config_val libexec`
CONDOR_SSH=$CONDOR_SSH/condor_ssh

SSHD_SH=`condor_config_val libexec`
SSHD_SH=$SSHD_SH/sshd.sh

# source Condor sshd script (creates the contact file, among other things)
. $SSHD_SH $_CONDOR_PROCNO $_CONDOR_NPROCS 

# If not the head node, just sleep forever, to let the
# sshds run
if [ $_CONDOR_PROCNO -ne 0 ]
then
                wait
                sshd_cleanup
                exit 0
fi

# Expect the working directory and name of the executable as
# arguments to the script
_WDIR=$1
shift
EXECUTABLE=$1
shift

# Set MPDIR to the bin directory of MPICH installation (only set one)
# if the gcc compiler was used
# MPDIR=/opt/lsst/SL44/mpich2-1.2/bin
# if the Intel compiler was used
# MPDIR=/opt/lsst/SL44/mpich2-1.2-intel/bin
MPDIR=/opt/lsst/SL53/mpich2-1.2-intel/bin
PATH=$MPDIR:.:$PATH
export PATH

export P4_RSHCOMMAND=$CONDOR_SSH

CONDOR_CONTACT_FILE=$_CONDOR_SCRATCH_DIR/contact
export CONDOR_CONTACT_FILE

env
echo $PWD

# The second field in the contact file is the machine name
# that condor_ssh knows how to use
# sort -n +0 < $CONDOR_CONTACT_FILE | awk '{print $2}' > machines
sort -k 1n,1 < $CONDOR_CONTACT_FILE | awk '{print $2}' > machines

## run the actual mpijob, passing the Working directory _WDIR
mpiexec -machinefile machines -wdir $_WDIR -np $_CONDOR_NPROCS $EXECUTABLE $@

sshd_cleanup
rm -f machines

echo 0 > jobStatus

exit $?

