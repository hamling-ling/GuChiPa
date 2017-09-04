# sub dir data/gam or data/tst should exist
# when arg $1 == t to use data/tst

sync
sync
sync

SRC_DIR="./data/nnsrc"

if [ "$1" == "-t" ]; then
    SRC_DIR="./data/nntst"
    echo SRC_DIR=$SRC_DIR
    rm -rf data/nntst;cp -r ~/GitHub/GuChiPa/research/capture/tst data/nntst
else
    rm -rf data/nnsrc;cp -r ~/GitHub/GuChiPa/research/capture/gam data/nnsrc
fi

function resizeImage {
    pushd $SRC_DIR/$1
    find . -size 0 | xargs --no-run-if-empty rm
    echo grayscalling and resizing $1
    mogrify -depth 8 -colorspace gray -resize 28x28 -format png ephemeral:"*.jpg"
    
    #echo size more than 30k checking...
    #echo find . -name "*.png" -size +30k
    #find . -size +30k

    popd
}

function listFiles {
    echo listing $1
    pushd .
    # avoid list too long error
    cd $SRC_DIR/$1
    find . -name "*.png" -exec echo "{} $2" \; >> ../list_$1.txt
    popd
}

resizeImage a
resizeImage c
resizeImage g
resizeImage z

rm -f $SRC_DIR/list*.txt

listFiles "g" 0
listFiles "c" 1
listFiles "a" 2
listFiles "z" 3

rm -rf $SRC_DIR/all
mkdir $SRC_DIR/all

echo merging 1/4
find $SRC_DIR/g -name "*.png" -print0 | xargs -0 -I{} mv {} $SRC_DIR/all/
echo merging 2/4
find $SRC_DIR/c -name "*.png" -print0 | xargs -0 -I{} mv {} $SRC_DIR/all/
echo merging 3/4
find $SRC_DIR/a -name "*.png" -print0 | xargs -0 -I{} mv {} $SRC_DIR/all/
echo merging 4/4
find $SRC_DIR/z -name "*.png" -print0 | xargs -0 -I{} mv {} $SRC_DIR/all/

#rm -rf $SRC_DIR/g
#rm -rf $SRC_DIR/c
#rm -rf $SRC_DIR/a
#rm -rf $SRC_DIR/z

cat $SRC_DIR/list_*.txt > $SRC_DIR/list_all.txt
rm -f $SRC_DIR/list_?.txt

#echo resizing all
#mogrify -resize 28x28 "$SRC_DIR/all/*.png"
#sync;sync;sync;

#echo finding not procecced files
#echo find $SRC_DIR/all -size +30k
#find $SRC_DIR/all -size +30k
