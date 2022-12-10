# OAI-5gcn
Openairinterface 5gcn with ueransim

Pulling the images from Docker Hub\
$ ./pull_oai_5gnc_images.sh 

Build UERANSIM docker image\
$ git clone -b docker_support https://github.com/orion-belt/UERANSIM.git
$ cd UERANSIM\
$  docker build --target ueransim --tag ueransim:latest -f docker/Dockerfile.ubuntu.18.04 .

Run topology

$  sudo python3 oai_5gcn_deployment.py 
