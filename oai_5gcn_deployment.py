#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller


if __name__ == "__main__":

    AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

    setLogLevel("info")

    prj_folder="/home/vagrant/comnetsemu_oai5g/oai-cn5g-fed"
   
    env = dict()

    net = Containernet(controller=Controller, link=TCLink)

    info("*** Adding Host for  mysql\n")
    env={"TZ":"Europe/Paris", 
        "MYSQL_DATABASE":"oai_db",
        "MYSQL_USER":"test",
        "MYSQL_PASSWORD":"test",
        "MYSQL_ROOT_PASSWORD":"linux"
        }
    mysql = net.addDockerHost(
        "mysql",
        dimage="mysql:latest",
        # ip="192.168.0.131/24",
        docker_args= {
            "environment":env,
            "volumes": {
                prj_folder + "/database/oai_db1.sql": {
                    "bind": "/docker-entrypoint-initdb.d/oai_db.sql",
                    "mode":"rw",
                    },
                
                }
            
            }
       
    )
    info("*** Adding Host for  oai-nrf\n")
    env={"NRF_INTERFACE_NAME_FOR_SBI":"eth0",
        "NRF_INTERFACE_PORT_FOR_SBI":"80",
        "NRF_INTERFACE_HTTP2_PORT_FOR_SBI":"9090",
        "NRF_API_VERSION":"v1",
        "INSTANCE":"0",
        "PID_DIRECTORY":"/var/run"
       }
    oai_nrf =net.addDockerHost(
        "oai-nrf",
        dimage="oai-nrf:v1.4.0",
        # ip="192.168.0.130/24",
        docker_args= {
            "environment":env,
              

        }
    )

    info("*** Adding Host for oai-amf\n")
    env={"TZ":"Europe/paris",
        "INSTANCE":"0",
        "PID_DIRECTORY":"/var/run",
        "MCC":"208",
        "MNC":"95",
        "REGION_ID":"128",
        "AMF_SET_ID":"1",
        "SERVED_GUAMI_MCC_0":"208",
        "SERVED_GUAMI_MNC_0":"95",
        "SERVED_GUAMI_REGION_ID_0":"128",
        "SERVED_GUAMI_AMF_SET_ID_0":"1",
        "SERVED_GUAMI_MCC_1":"460",
        "SERVED_GUAMI_MNC_1":"11",
        "SERVED_GUAMI_REGION_ID_1":"10",
        "SERVED_GUAMI_AMF_SET_ID_1":"1",
        "PLMN_SUPPORT_MCC":"208",
        "PLMN_SUPPORT_MNC":"95",
        "PLMN_SUPPORT_TAC":"0xa000",
        "SST_0":"1",
        "SD_0":"0xFFFFFF",
        "SST_1":"1",
        "SD_1":"1",
        "SST_2":"222",
        "SD_2":"123",
        "AMF_INTERFACE_NAME_FOR_NGAP":"oai_amf-s1",
        "AMF_INTERFACE_NAME_FOR_N11":"eth0",
        "SMF_INSTANCE_ID_0":"1",
        "SMF_FQDN_0":"oai-smf",
        "SMF_IPV4_ADDR_0":"172.17.0.5/16",
        "SMF_HTTP_VERSION_0":"v1",
        "SELECTED_0":"true",
        "SMF_INSTANCE_ID_1":"2",
        "SMF_FQDN_1":"oai-smf",
        "SMF_IPV4_ADDR_1":"0.0.0.0",
        "SMF_HTTP_VERSION_1":"v1",
        "SELECTED_1":"false",
        "MYSQL_SERVER":"172.17.0.2/16",
        "MYSQL_USER":"root",
        "MYSQL_PASS":"linux",
        "MYSQL_DB":"oai_db",
        "NRF_IPV4_ADDRESS":"172.17.0.3/16",
        "NRF_PORT":"80",
        "EXTERNAL_NRF":"no",
        "NF_REGISTRATION":"yes",
        "SMF_SELECTION":"yes",
        "USE_FQDN_DNS":"yes",
        "EXTERNAL_AUSF":"no",
        "EXTERNAL_UDM":"no",
        "EXTERNAL_NSSF":"no",
        "USE_HTTP2":"no",
        "NRF_API_VERSION":"v1",
        "NRF_FQDN":"oai-nrf",
        "AUSF_IPV4_ADDRESS":"0.0.0.0",
        "AUSF_PORT":"80",
        "AUSF_API_VERSION":"v1",
        "AUSF_FQDN":"localhost",
        "UDM_IPV4_ADDRESS":"0.0.0.0",
        "UDM_PORT":"80",
        "UDM_API_VERSION":"v2",
        "UDM_FQDN":"localhost",
        "INT_ALGO_LIST":["NIA1" , "NIA2"],
        "CIPH_ALGO_LIST":["NEA1" , "NEA2"]

    }
    
    oai_amf= net.addDockerHost(
        "oai-amf",
        dimage="oai-amf:v1.4.0",
        ip="192.168.0.111/24",
        docker_args= {
            "environment":env, 
            },
        
    )

    info("*** Adding Host for  oai-smf\n")
    env={"TZ":"Europe/Paris",
        "INSTANCE":"0",
        "PID_DIRECTORY":"/var/run",
        "SMF_INTERFACE_NAME_FOR_N4":"eth0",
        "SMF_INTERFACE_NAME_FOR_SBI":"eth0",
        "SMF_INTERFACE_PORT_FOR_SBI":"80",
        "SMF_INTERFACE_HTTP2_PORT_FOR_SBI":"9090",
        "SMF_API_VERSION":"v1",
        "DEFAULT_DNS_IPV4_ADDRESS":"172.21.3.100",
        "DEFAULT_DNS_SEC_IPV4_ADDRESS":"8.8.8.8",
        "AMF_IPV4_ADDRESS":"172.17.0.4",
        "AMF_PORT":"80",
        "AMF_API_VERSION":"v1",
        "AMF_FQDN":"localhost",
        "UDM_IPV4_ADDRESS":"0.0.0.0",
        "UDM_PORT":"80",
        "UDM_API_VERSION":"v2",
        "UDM_FQDN":"localhost",
        "UPF_IPV4_ADDRESS":"172.17.0.6/16",
        "UPF_FQDN_0":"oai-spgwu",
        "NRF_IPV4_ADDRESS":"172.17.0.3/16",
        "NRF_PORT":"80",
        "NRF_API_VERSION":"v1",
        "NRF_FQDN":"oai-nrf",
        "REGISTER_NRF":"yes",
        "DISCOVER_UPF":"yes",
        "USE_FQDN_DNS":"yes",
        "USE_NETWORK_INSTANCE":"no",
        "USE_LOCAL_SUBSCRIPTION_INFO":"yes",
        "DNN_RANGE1":"12.1.1.51 - 12.1.1.150",
        "DNN_RANGE0":"12.2.1.2 - 12.2.1.128",
        "DNN_NI1":"oai.ipv4",
        "TYPE1":"IPv4",
        "NSSAI_SST1":"1",
        "NSSAI_SD1":"1",
        "SESSION_AMBR_UL1":"100Mbps",
        "SESSION_AMBR_DL1":"200Mbps",
        "DNN_NI2":"default",
        "TYPE2":"IPv4",
        "DNN_RANGE2":"12.1.1.2 - 12.1.1.50",
        "NSSAI_SST2":"222",
        "NSSAI_SD2":"123",
        "SESSION_AMBR_UL2":"50Mbps",
        "SESSION_AMBR_DL2":"100Mbps",
        "DNN_NI3":"ims",
        "TYPE3":"IPv4v6",
        "DNN_RANGE3":"14.1.1.2 - 14.1.1.253",
        "DEFAULT_CSCF_IPV4_ADDRESS":"127.0.0.1",
        "ENABLE_USAGE_REPORTING":"no",
        }
    oai_smf= net.addDockerHost(
        "oai-smf",
        dimage="oai-smf:v1.4.0", 
        # ip="192.168.0.133/24",
        docker_args={
            "environment":env, 
            
        }
    )

    info("*** Adding Host for  oai-spgwu\n")
    env={"TZ":"Europe/Paris",
        "PID_DIRECTORY":"/var/run",
        "SGW_INTERFACE_NAME_FOR_S1U_S12_S4_UP":"oai_spgwu-s2",
        "SGW_INTERFACE_NAME_FOR_SX":"eth0",
        "PGW_INTERFACE_NAME_FOR_SGI":"oai_spgwu-s2",
        "NETWORK_UE_NAT_OPTION":"yes",
        "NETWORK_UE_IP":"12.1.1.0/24",
        "SPGWC0_IP_ADDRESS":"172.17.0.5/16",
        "BYPASS_UL_PFCP_RULES":"no",
        "THREAD_S1U_PRIO":"80",
        "S1U_THREADS":"8",
        "THREAD_SX_PRIO":"81",
        "SX_THREADS":"1",
        "THREAD_SGI_PRIO":"80",
        "SGI_THREADS":"8",
        "MCC":"208",
        "MNC":"95",
        "MNC03":"095",
        "TAC":"40960",
        "GW_ID":"1",
        "REALM":"openairinterface.org",
        "ENABLE_5G_FEATURES":"yes",
        "REGISTER_NRF":"yes",
        "USE_FQDN_NRF":"yes",
        "UPF_FQDN_5G":"oai-spgwu",
        "NRF_IPV4_ADDRESS":"172.17.0.3/16",
        "NRF_PORT":"80",
        "NRF_API_VERSION":"v1",
        "NRF_FQDN":"oai-nrf",
        "NSSAI_SST_0":"1",
        "NSSAI_SD_0":"0xFFFFFF",
        "DNN_0":"oai",
        "NSSAI_SST_1":"1",
        "NSSAI_SD_1":"1",
        "DNN_1":"oai.ipv4",
        "NSSAI_SST_2":"222",
        "NSSAI_SD_2":"123",
        "DNN_2":"default"

       }
    # permission=["NET_ADMIN","SYS_ADMIN"]
    oai_spgwu=net.addDockerHost(
        "oai-spgwu",
        dimage="oai-spgwu-tiny:v1.4.0",
        ip="192.168.0.134/24",
        privilege="true",
        docker_args= {
            "environment":env,
            "cap_add":["NET_ADMIN","SYS_ADMIN"],
            "cap_drop":["ALL"],
            "sysctls": {"net.ipv4.ip_forward": 1},
        }
    
    )

    oai_ext_dn =net.addDockerHost(
        "oai-ext-dn",
        dimage="trf-gen-cn5g:latest",
        ip="192.168.0.135/24",
        privileged="true",
        entrypoint="/bin/bash -c \
                   iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE;\
                   ip route add 12.1.1.0/24 via 192.168.0.201 dev eth0; sleep infinity",

        docker_args= {
            "environment":"",

        }
    )

    info("*** Adding Host for  ueransim\n")
    env={ 
        # GNB Congig Parameters
            "MCC":"208",
            "MNC":"95",
            "NCI":"0x000000010",
            "TAC":"0xa000",
            "LINK_IP":"192.168.0.141",
            "NGAP_IP":"192.168.0.141",
            "GTP_IP":"192.168.0.141",
            "NGAP_PEER_IP":"172.168.0.111",
            "SST":"222",
            "SD":"123",
            "IGNORE_STREAM_IDS":"true",
            # UE Config Parameters
            "NUMBER_OF_UE":"1",
            "IMSI":"208950000000031",
            "KEY":"0C0A34601D4F07677303652C0462535B",
            "OP":"63bfa50ee6523365ff14c1f45f88737d",
            "OP_TYPE":"OPC",
            "AMF_VALUE":"8000",
            "IMEI":"356938035643803",
            "IMEI_SV":"0035609204079514",
            "GNB_IP_ADDRESS":"192.168.0.141",
            "PDU_TYPE":"IPv4",
            "APN":"default",
            "SST_C":"222",
            "SD_C":"123",
            "SST_D":"222",
            "SD_D":"123"
       }
    ueransim=net.addDockerHost(
        "ueransim",
        dimage="ueransim:latest",
        ip="192.168.0.141/24",
        privilege="true",
        docker_args= {
            "environment":env,
                
        }
    
    )
    # info("*** Adding gNB\n")
    # env["COMPONENT_NAME"]="gnb"
    # gnb = net.addDockerHost(
    #     "gnb", 
    #     dimage="myueransim_v3-2-6",
    #     ip="192.168.0.131/24",
    #     # dcmd="",
    #     dcmd="bash /mnt/ueransim/open5gs_gnb_init.sh",
    #     docker_args={
    #         "environment": env,
    #         "volumes": {
    #             prj_folder + "/ueransim/config": {
    #                 "bind": "/mnt/ueransim",
    #                 "mode": "rw",
    #             },
    #             prj_folder + "/log": {
    #                 "bind": "/mnt/log",
    #                 "mode": "rw",
    #             },
    #             "/etc/timezone": {
    #                 "bind": "/etc/timezone",
    #                 "mode": "ro",
    #             },
    #             "/etc/localtime": {
    #                 "bind": "/etc/localtime",
    #                 "mode": "ro",
    #             },
    #             "/dev": {"bind": "/dev", "mode": "rw"},
    #         },
    #         "cap_add": ["NET_ADMIN"],
    #         "devices": "/dev/net/tun:/dev/net/tun:rwm"
    #     },
    # )

    # info("*** Adding UE\n")
    # env["COMPONENT_NAME"]="ue"
    # ue = net.addDockerHost(
    #     "ue", 
    #     dimage="myueransim_v3-2-6",
    #     ip="192.168.0.132/24",
    #     # dcmd="",
    #     dcmd="bash /mnt/ueransim/open5gs_ue_init.sh",
    #     docker_args={
    #         "environment": env,
    #         "volumes": {
    #             prj_folder + "/ueransim/config": {
    #                 "bind": "/mnt/ueransim",
    #                 "mode": "rw",
    #             },
    #             prj_folder + "/log": {
    #                 "bind": "/mnt/log",
    #                 "mode": "rw",
    #             },
    #             "/etc/timezone": {
    #                 "bind": "/etc/timezone",
    #                 "mode": "ro",
    #             },
    #             "/etc/localtime": {
    #                 "bind": "/etc/localtime",
    #                 "mode": "ro",
    #             },
    #             "/dev": {"bind": "/dev", "mode": "rw"},
    #         },
    #         "cap_add": ["NET_ADMIN"],
    #         "devices": "/dev/net/tun:/dev/net/tun:rwm"
    #     },
    # )

    info("*** Add controller\n")
    net.addController("c0")

    info("*** Adding switch\n")
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")
    s3 = net.addSwitch("s3")

    info("*** Adding links\n")
    net.addLink(s1,  s2, bw=1000, delay="10ms", intfName1="s1-s2",  intfName2="s2-s1")
    net.addLink(s2,  s3, bw=1000, delay="50ms", intfName1="s2-s3",  intfName2="s3-s2")
    
    # net.addLink(ue,  s1, bw=1000, delay="1ms", intfName1="ue-s1",  intfName2="s1-ue")
    # net.addLink(gnb, s1, bw=1000, delay="1ms", intfName1="gnb-s1", intfName2="s1-gnb")
    net.addLink(ueransim, s1, params1={"delay":"1ms", "bw" : 1000, "ip" : "192.168.0.141/24" }, intfName1="ueransim-s1",  intfName2="s1-ueransim")
    net.addLink(oai_amf,s1,params1={"delay":"1ms", "bw" : 1000, "ip" : "192.168.0.111/24" } , intfName1="oai_amf-s1", intfName2="s1-oai_amf")
    # net.addLink(mysql,s1, params1={"delay":"1ms", "bw" : 1000, "ip" : "192.168.0.131/24" } , intfName1="mysql-s1", intfName2="s1-mysql")
    # net.addLink(oai_nrf,s2,  params1={"delay":"1ms", "bw" : 1000, "ip" : "192.168.0.130/24" } , intfName1="oai_nrf-s1", intfName2="s1-oai_nrf")
    # net.addLink(oai_smf,  s2, params1={"delay":"1ms", "bw" : 1000, "ip" : "192.168.0.133/24" }, intfName1="oai_smf-s2",  intfName2="s2-oai_smf")
    net.addLink(oai_spgwu,s2,params1={"delay":"1ms", "bw" : 1000, "ip" : "192.168.0.134/24" } , intfName1="oai_spgwu-s2", intfName2="s2-oai_spgwu")
    net.addLink(oai_ext_dn, s3, bw=1000, delay="1ms", intfName1="oai_ext_dn-s3",  intfName2="s3-oai_ext_dn")
   
    info("\n*** Starting network\n")
    net.start()

    if not AUTOTEST_MODE:
        # spawnXtermDocker("open5gs")
        # spawnXtermDocker("gnb")
        CLI(net)

    net.stop()