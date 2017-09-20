#!/bin/bash

PROCESS_AUG="TRUE"
PROCESS_TST="TRUE"
PROCESS_SRC="TRUE"
PROCESS_DBG="FALSE"

for OPT in "$@"PT in "$@"
do
    if [ "$OPT" = "-ns" ] ; then
	PROCESS_SRC="FALSE"
	break;
    fi
done

for OPT in "$@"PT in "$@"
do
    if [ "$OPT" = "-nt" ] ; then
	PROCESS_TST="FALSE"
	break;
    fi
done

for OPT in "$@"PT in "$@"
do
    if [ "$OPT" = "-naug" ] ; then
	PROCESS_AUG="FALSE"
	break;
    fi
done

for OPT in "$@"PT in "$@"
do
    if [ "$OPT" = "-dbg" ] ; then
	PROCESS_DBG="TRUE"
	break;
    fi
done

function resizeImage {
    pushd .
    cd $1

    XARGS_NO_RUN=''
    if [ `uname` = 'Linux' ]; then
	XARGS_NO_RUN='--no-run-if-empty';
    fi
    find . -size 0 | xargs $XARGS_NO_RUN rm
    echo grayscalling and resizing $1
    mogrify -depth 8 -colorspace gray -resize 28x28 -format png "*.jpg"
    find . -name "*.jpg" | xargs $XARGS_NO_RUN rm

    popd
}

function listFiles {
    echo listing $1
    pushd .
    cd $1
    echo "entering $1"
    # avoid list too long error
    echo "find . -name "*.png" -exec echo "{} $2" \; >> ../list_$2.txt"
    find . -name "*.png" -exec echo "{} $2" \; >> ../list_$2.txt
    popd
}

function mergeDir {
    echo merging $1 into $3 for $2

    pushd .
    cd $1
    echo "entering $1"
    find . -name "*.png" -print0 | xargs -0 -I{} mv {} ../../$3/

    cd ../
    echo "cd $(pwd) for $2"
    echo "cat list_$2.txt > list_all.txt"
    cat list_$2.txt >> list_all.txt
    echo "rm -f list_$2.txt"
    rm -f list_$2.txt
    popd

    rm -rf $1
}

function processDir {
    echo "processing $1"
    
    resizeImage "$1/g"
    resizeImage "$1/c"
    resizeImage "$1/a"
    resizeImage "$1/z"
    
    rm -f $1/list*.txt

    listFiles "$1/g" 0
    listFiles "$1/c" 1
    listFiles "$1/a" 2
    listFiles "$1/z" 3

    mkdir -p $1/all
    mergeDir "$1/g" 0 "$1/all"
    mergeDir "$1/c" 1 "$1/all"
    mergeDir "$1/a" 2 "$1/all"
    mergeDir "$1/z" 3 "$1/all"

    rm -rf g c a z
}

if [ "$PROCESS_DBG" == "TRUE" ] ; then

    # do something for debug
    exit 0
fi

if [ "$PROCESS_AUG" == "TRUE" ] ; then
    rm -rf flp rot scl trs crp cnt gam tst

    # x2
    python flip.py raw flp
    # x3
    python rot.py flp rot
    rm -rf flp
    # x3
    python scale.py rot scl
    rm -rf rot
    # x9
    python trans.py scl trs
    rm -rf scl
    # x1
    python crop.py trs crp
    rm -rf trs
    # x3
    python contrast.py crp cnt
    rm -rf crp
    # x3
    python gamma.py cnt gam
    rm -rf cnt
    # x2
    #python gaussnoise.py
    # x3
    #python saltnoise.py
    
    ./takesample.sh 10000 gam tst
    #./takesample.sh 1 gam tst
fi

if [ "$PROCESS_SRC" == "TRUE" ] ; then
    processDir "gam"
    echo "removing nnsrc"
    rm -rf nnsrc
    echo "rename gam -> nnsrc"
    mv gam nnsrc
fi

if [ "$PROCESS_TST" == "TRUE" ] ; then
    processDir "tst"
    echo "removing nntst"
    rm -rf nntst
    echo "rename tst -> nntst"
    mv tst nntst
fi
