#cp -r gam nnsrc

function resizeImage {
    mogrify ./nnsrc/$1/*.jpg -depth 8 -colorspace gray
    mogrify -resize 28x28 ./nnsrc/$1/*.jpg
}


function listFiles {
    for entry in `ls nnsrc/$1/*.jpg`; do
	echo $entry $2 >> list.txt
    done
}

#resizeImage a
#resizeImage c
#resizeImage g
#resizeImage z

echo > list.txt

listFiles "g" 0
listFiles "c" 1
listFiles "a" 2
listFiles "z" 3
