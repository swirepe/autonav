#!/bin/bash

DIR_NAME=$(dirname $BASH_SOURCE)


if [[ x"${BASH_SOURCE[0]}" == x"$0" ]]
then    
    echo "ERROR: autonav.sh needs to be sourced, not executed." 1>&2
    exit
fi


function set_confs {
    if [[ "$@" ]]
    then
        CONFS="$@"
    else
        CONFS="$DIR_NAME/autonav.ini"
    fi
    
}


function check_helper_script {
    # this program cannot run without autonav.py
    if [ ! -e $DIR_NAME/autonav.py ]
    then
        echo "ERROR: Required helper script missing: autonav.py" 1>&2
        return
    fi
      
}



check_helper_script
set_confs $@

NAV_FILE="$(python $DIR_NAME/autonav.py $CONFS)"
source "$NAV_FILE"
rm "$NAV_FILE"
