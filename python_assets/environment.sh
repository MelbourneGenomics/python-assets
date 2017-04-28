#!/usr/bin/env bash

ARGS=$(getopt -o p --long "proot" -n $(basename $0) -- "$@")
HERE=${BASH_SOURCE[0]}
eval set -- "$ARGS"

while true ; do
    case "$1" in
        -p|--proot)
        	# If we used the proot flag, just run proot in the current dir
        	proot -r . ${@}
          	exit 0;;
#        --usage|--help)
#          usage
#          exit 0;;
#        --)
#          	shift
#          	break ;;
        *)
			# If we didn't use proot, just set some environment variables
			export PATH=${HERE}/bin:${HERE}/maven/bin:${HERE}/bpipe/bin:${PATH}
			export CPATH="${HERE}/include"
			export CFLAGS="$CFLAGS -I${HERE}/include"
			export CPPFLAGS="$CPPFLAGS -I${HERE}/include"
			export LDFLAGS="$LDFLAGS -L${HERE}/lib"
			export LD_LIBRARY_PATH=${HERE}/lib:${LD_LIBRARY_PATH}
		;;
    esac
done
