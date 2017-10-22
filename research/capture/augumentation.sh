#!/bin/bash

PROCESS_AUG="TRUE"
PROCESS_TST="TRUE"
PROCESS_SRC="TRUE"
PROCESS_DBG="FALSE"
MOGRIFY_OPT="-define jpeg:size=227x227 -resize 64x64"

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

for OPT in "$@"PT in "$@"
do
    if [ "$OPT" = "-gray" ] ; then
	MOGRIFY_OPT="-depth 8 -colorspace gray -resize 28x28"
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
    mogrify $MOGRIFY_OPT -format jpg "*.jpg"
    #find . -name "*.jpg" | xargs $XARGS_NO_RUN rm

    popd
}

function listFiles {
    echo listing $1
    pushd .
    cd $1
    echo "entering $1"
    # avoid list too long error
    echo "find . -name "*.jpg" -exec echo "{} $2" \; >> ../list_$2.txt"
    find . -name "*.jpg" -exec echo "{} $2" \; >> ../list_$2.txt
    popd
}

function mergeDir {
    echo merging $1 into $3 for $2

    pushd .
    cd $1
    echo "entering $1"
    find . -name "*.jpg" -print0 | xargs -0 -I{} mv {} ../../$3/

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
    echo "debuging mode"
fi

if [ "$PROCESS_AUG" == "TRUE" ] ; then
    echo "processing augumentation"
    rm -rf rot scl trs crp cnt src tst dbg

    if [ "$PROCESS_DBG" == "FALSE" ] ; then
 
	# x3
	python rot.py raw rot
	# x3
	python scale.py rot scl
	rm -rf rot
	# x5
	python trans.py scl trs
	rm -rf scl
   
	# x1
	python crop.py trs crp
	rm -rf trs
	# x3
	python contrast.py crp cnt
	rm -rf crp
	# x3
	#python gamma.py cnt gam
	#rm -rf cnt
	# x2
	#python gaussnoise.py
	# x3
	#python saltnoise.py
	mv cnt src
	./takesample.sh 5000 src tst
	./takesample.sh 10 src dbg
	#./takesample.sh 10 src tst
	#./takesample.sh 10 src dbg
    else
	echo "not actually augumenting for debug"
	# x1
	python crop.py raw crp
	#rm -rf trs
	# x3
	python contrast.py crp cnt
	#rm -rf crp
	mv cnt src
	./takesample.sh 1 src tst
	echo taking 1 smple for debug
	./takesample.sh 1 src dbg
    fi
fi

processDir "src"
echo "removing nnsrc"
rm -rf nnsrc
echo "rename src -> nnsrc"
mv src nnsrc

processDir "tst"
echo "removing nntst"
rm -rf nntst
echo "rename tst -> nntst"
mv tst nntst

rm -rf nndbg
mv dbg nndbg
