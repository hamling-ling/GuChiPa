# sub dir data/gam or data/tst should exist
# when arg $1 == t to use data/tst

#rm -rf data/nnsrc;cp -r ~/GitHub/GuChiPa/research/capture/gam data/nnsrc
#rm -rf data/nntst;cp -r ~/GitHub/GuChiPa/research/capture/tst data/nntst

sync
sync
sync

SRC_DIR="./data/nnsrc"

if [ "$1" == "-t" ]; then
    SRC_DIR="./data/nntst"
    echo SRC_DIR=$SRC_DIR
fi

function resizeImage {
    pushd $SRC_DIR/$1
    find . -size 0 | xargs --no-run-if-empty rm
    echo grayscalling $1
    mogrify -depth 8 -colorspace gray "*.jpg"
    
    sync;sync;sync
    
    echo resizing $1
    mogrify -resize 28x28 "*.jpg"

    sync;sync;sync;
    
    echo size>10k
    echo find . -size +30k
    find . -size +30k

    sync;sync;sync;
    popd
}

function listFiles {
    echo listing $1
    pushd .
    # avoid list too long error
    cd $SRC_DIR/$1
    for entry in `ls *.jpg`; do
	echo $entry $2 >> ../list_$1.txt
    done
    popd
}

resizeImage a
resizeImage c
resizeImage g
resizeImage z

rm $SRC_DIR/list*.txt

listFiles "g" 0
listFiles "c" 1
listFiles "a" 2
listFiles "z" 3

rm -rf $SRC_DIR/all
mkdir $SRC_DIR/all

echo merging 1/4
find $SRC_DIR/g -name "*.jpg" -print0 | xargs -0 -I{} mv {} $SRC_DIR/all/
echo merging 2/4
find $SRC_DIR/c -name "*.jpg" -print0 | xargs -0 -I{} mv {} $SRC_DIR/all/
echo merging 3/4
find $SRC_DIR/a -name "*.jpg" -print0 | xargs -0 -I{} mv {} $SRC_DIR/all/
echo merging 4/4
find $SRC_DIR/z -name "*.jpg" -print0 | xargs -0 -I{} mv {} $SRC_DIR/all/

#rm -rf $SRC_DIR/g
#rm -rf $SRC_DIR/c
#rm -rf $SRC_DIR/a
#rm -rf $SRC_DIR/z

sync;sync;sync;

cat $SRC_DIR/list_*.txt > $SRC_DIR/list_all.txt
rm $SRC_DIR/list_?.txt

echo resizing $1
mogrify -resize 28x28 "$SRC_DIR/all/*.jpg"
sync;sync;sync;

echo size>10k
echo find $SRC_DIR/all -size +30k
find $SRC_DIR/all -size +30k