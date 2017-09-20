cat mnist_train.amat | sed -e "s/\s\s\s/\\n/g" > mnist_train_nl.txt
cat mnist_test.amat | sed -e "s/\s\s\s/\\n/g" > mnist_test_nl.txt
cat mnist_background_images_train.amat | sed -e "s/\s\s\s/\\n/g" > mnist_background_images_train_nl.txt
cat mnist_background_images_test.amat | sed -e "s/\s\s\s/\\n/g" > mnist_background_images_test_nl.txt

./amat2bin mnist_train_nl.txt mnist_train.bin
./amat2bin mnist_test_nl.txt mnist_test.bin
./amat2bin mnist_background_images_train_nl.txt mnist_background_images_train.bin
./amat2bin mnist_background_images_test_nl.txt mnist_background_images_test.bin

./dispimage mnist_test.bin 100
./dispimage mnist_train.bin 100
./dispimage mnist_background_images_train.bin 100
./dispimage mnist_background_images_test.bin 100
