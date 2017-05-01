#!/usr/bin/env bash

# Find out parent directory
if [[ -z $_ ]]; then
	HERE=$_
else
	HERE=$0
fi
HERE=$(dirname $(readlink -f $HERE))

# Parse arguments
ARGS=$(getopt -o p --long "proot" -n $(basename $0) -- "$@")
eval set -- "$ARGS"

# Build up arguments for proot
PROOT_ARGS=''
IS_PROOT=false

while [[ -n $1 ]] ; do
    case "$1" in
        -p|--proot)
        	# If we used the proot flag, just run proot in the current dir
        	shift
        	IS_PROOT=true
		;;
        --)
        	# When we hit --, we're done parsing arguments, so now we can run what the user requested
        	if [[ $IS_PROOT = true ]] ; then
        		shift
        		proot -r . ${@}
				exit 0
        	else
				# If we didn't use proot, just set some environment variables
				export PATH=${HERE}/bin:${HERE}/maven/bin:${HERE}/bpipe/bin:${PATH}
				export CPATH="${HERE}/include"
				export CFLAGS="$CFLAGS -I${HERE}/include"
				export CPPFLAGS="$CPPFLAGS -I${HERE}/include"
				export LDFLAGS="$LDFLAGS -L${HERE}/lib"
				export LD_LIBRARY_PATH=${HERE}/lib:${LD_LIBRARY_PATH}

				shift
				break
			fi
        ;;
        *)
        	PROOT_ARGS="$1 ${PROOT_ARGS}"
		;;
    esac
done
