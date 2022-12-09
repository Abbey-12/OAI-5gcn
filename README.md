# OAI-5gcn
Openairinterface 5gcn with ueransim

Pulling the images from Docker Hub\
$ ./pull_oai_5gnc_images.sh 

Build UERANSIM docker image\
$ cd UERANSIM\
$  docker build --target ueransim --tag ueransim:latest -f docker/Dockerfile.ubuntu.18.04 .\
$  sudo python3 oai_5gcn_deployment.py 
