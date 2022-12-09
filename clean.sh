
#!/bin/bash

sudo mn -c

docker stop $(docker ps -aq)

docker container prune -f

if [ "$1" == "log" ]; then
    cd log && sudo rm *.log 
fi
udo ip link delete s1-ueransim
sudo ip link delete s2-s3
sudo ip link delete s2-s1
sudo ip link delete oai_amf-s1
sudo ip link delete s1-oai_amf
sudo ip link delete oai_spgwu-s2
sudo ip link delete s2-oai_spgwu
sudo ip link delete oai_ext_dn-s3
