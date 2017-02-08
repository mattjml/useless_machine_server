docker build -t test_image .
docker rm -f test_image
docker run --rm --name test_runner -u root -t test_image nosetests test 
