#cp -r ./data/gam ./data/nnsrc

function resizeImage {
    echo grayscalling $1
    mogrify ./data/nnsrc/$1/*.jpg -depth 8 -colorspace gray
    echo resizing $1
    mogrify -resize 28x28 ./data/nnsrc/$1/*.jpg
}


function listFiles {
    echo listing $1
    pushd .
    # avoid list too long error
    cd data/nnsrc/$1
    for entry in `ls *.jpg`; do
	echo $entry $2 >> ../list_$1.txt
    done
    popd
}

resizeImage a
resizeImage c
resizeImage g
resizeImage z

rm data/nnsrc/list*.txt

listFiles "g" 0
listFiles "c" 1
listFiles "a" 2
listFiles "z" 3

rm -rf data/nnsrc/all
mkdir data/nnsrc/all

echo merging 1/4
find data/nnsrc/g -name "*.jpg" -print0 | xargs -0 -I{} mv {} data/nnsrc/all/
echo merging 2/4
find data/nnsrc/c -name "*.jpg" -print0 | xargs -0 -I{} mv {} data/nnsrc/all/
echo merging 3/4
find data/nnsrc/a -name "*.jpg" -print0 | xargs -0 -I{} mv {} data/nnsrc/all/
echo merging 4/4
find data/nnsrc/z -name "*.jpg" -print0 | xargs -0 -I{} mv {} data/nnsrc/all/

rm -rf data/nnsrc/g
rm -rf data/nnsrc/c
rm -rf data/nnsrc/a
rm -rf data/nnsrc/z

cat data/nnsrc/list_*.txt > data/nnsrc/list_all.txt
rm data/nnsrc/list_?.txt

