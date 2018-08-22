#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sdk import UcloudApiClient
from config import *
import sys
import json
import time
import os
import argparse

def log_write(str_begin,str_end,*args):
    """日志函数"""
    if len(args) != 1:
        with open(LOG_FILE,"a+") as f:
            msg = " ".join(args)
            f.write(str_begin + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + msg + str_end)
    else:
        with open(LOG_FILE,"a+") as f:
            f.write(str_begin + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + args[0] + str_end)


def eip_apply():
    """EIP申请函数"""
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
        "Action":"AllocateEIP",
        "ProjectId": "org-tgfjdn",
        "Region": "cn-bj2",
        "OperatorName": "Bgp",
        "Bandwidth": "1",
        "ChargeType": "Month",
        "Count": "1",
        "Name": "EIP",
        "Remark": "XX项目",
        "Tag": "XX项目"
    }

    try:
        response = ApiClient.get("/", Parameters )
    except:
        log_write('', '\n', ' EIP申请失败')
        sys.exit(0)

    response_data = json.loads(json.dumps(response))
    #print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

    IPADDR = response_data["EIPSet"][0]["EIPAddr"][0]["IP"]
    IPUID =  str(response_data["EIPSet"][0]["EIPId"])

    log_write('', '\n', '', str(IPUID), str(IPADDR), 'EIP申请成功')

    eip_data = {}
    eip_data['IP'] = IPADDR
    eip_data['EIPId'] = IPUID

    return eip_data


def eip_describe(IPUID):
    """EIP 查看函数"""
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
        "Action":"DescribeEIP",
        "ProjectId": "org-tgfjdn",
        "Region":"cn-bj2",
        "EIPIds.1": IPUID,
    }

    try:
        response = ApiClient.get("/", Parameters )
    except:
        log_write('', '\n', '', str(IPUID), 'EIP查询权重失败')
        sys.exit(0)

    response_data = json.loads(json.dumps(response))
    #print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

    time.sleep(1)

    if response_data["RetCode"] == 0:
        #log_write('', '\n', '', str(response_data))
        WG = response_data["EIPSet"][0]["Weight"]
        log_write('', '\n', '', str(IPUID), 'EIP查询权重为['+ str(WG) + ']')
        return WG
    else:
        log_write('', '\n', '', str(IPUID), 'EIP查询权重失败')
        sys.exit(0)


def eip_Weight_modify(IPUID, WG):
    """修改EIP权重"""
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
        "Action":"ModifyEIPWeight",
        "ProjectId": "org-tgfjdn",
        "Region":"cn-bj2",
        "EIPId": IPUID,
        "Weight": WG
    }

    try:
        response = ApiClient.get("/", Parameters )
    except:
        log_write('', '\n', '', str(IPUID), 'EIP修改权重失败')
        sys.exit(0)

    response_data = json.loads(json.dumps(response))
    #print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

    if response_data["RetCode"] == 0:
        log_write('','\n', '', str(IPUID), 'EIP修改权重为[' + str(WG) + ']')
    else:
        log_write('', '\n', '', str(IPUID), 'EIP修改权重失败')
        sys.exit(0)


def eip_bind(IPUID, UHOSTID):
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
        "Action":"BindEIP",
        "EIPId": IPUID,
        "ResourceId": UHOSTID,
        "ResourceType":"uhost",
        "Region":"cn-bj2",
        "ProjectId":"org-tgfjdn"
    }

    try:
        response = ApiClient.get("/", Parameters )
    except:
        log_write('', '\n','', str(IPUID), str(UHOSTID), 'EIP绑定失败')
        sys.exit(0)

    response_data = json.loads(json.dumps(response))

    if response_data["RetCode"] == 0:
        log_write('','\n', '', str(IPUID), str(UHOSTID), 'EIP绑定成功')
    else:
        log_write('', '\n','', str(IPUID), str(UHOSTID), 'EIP绑定失败')
        sys.exit(0)


def eip_unbind(IPUID, UHOSTID):
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
        "Action":"UnBindEIP",
        "EIPId":IPUID,
        "ResourceId": UHOSTID,
        "ResourceType":"uhost",
        "Region":"cn-bj2",
        "ProjectId":"org-tgfjdn"
    }

    try:
        response = ApiClient.get("/", Parameters )
    except:
        log_write('', '\n', '', str(IPUID), str(UHOSTID), 'EIP解绑失败')
        sys.exit(0)

    response_data = json.loads(json.dumps(response))

    if response_data["RetCode"] == 0:
        log_write('', '\n', '', str(IPUID), str(UHOSTID), 'EIP解绑成功')
    else:
        log_write('', '\n', '', str(IPUID), str(UHOSTID), 'EIP解绑失败')
        sys.exit(0)


def eip_delete(IPUID):
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={"Action":"ReleaseEIP","EIPId":IPUID,"Region":"cn-bj2"}

    try:
        response = ApiClient.get("/", Parameters )
    except:
        log_write('', '\n', '', str(IPUID), 'EIP释放失败')
        sys.exit(0)

    response_data = json.loads(json.dumps(response))

    if response_data["RetCode"] == 0:
        log_write('', '\n', '', str(IPUID), 'EIP释放成功')
    else:
        log_write('', '\n', '', str(IPUID), 'EIP释放失败')
        sys.exit(0)


def uhost_describe(UHOSTID):
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
        "Action": "DescribeUHostInstance",
        "ProjectId": "org-tgfjdn",
        "Region": "cn-bj2",
        "Zone": "cn-bj2-04",
        "UHostIds.1": UHOSTID
    }

    try:
        response = ApiClient.get("/", Parameters )
    except:
        log_write('', '\n', '', str(UHOSTID), '获取主机IP信息失败')
        sys.exit(0)

    response_data = json.loads(json.dumps(response))
    #print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

    if response_data["RetCode"] == 0:
        IPLIST = response_data["UHostSet"][0]["IPSet"]
        log_write('','\n', '', str(UHOSTID), '获取主机IP信息成功')
        return IPLIST
    else:
        log_write('','\n', '', str(UHOSTID), '获取主机IP信息失败')
        sys.exit(0)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Crawler EIP Polling')
    parser.add_argument('-i', '--uhost-id', type = str, default = None)
    parser.add_argument('-a', '--uhost-ip', type = str, default = None)
    parser.add_argument('-t', '--time', type = int, default = 600)
    args = parser.parse_args()
    
    UHOSTID = args.uhost_id
    UHOSTIP = args.uhost_ip
    TIME = args.time

    LOG_PATH = str('/root/ucloud-sdk-python/log')
    #LOG_TIME = str(time.strftime('%Y%m%d',time.localtime(time.time())))
    #LOG_FILE = LOG_PATH + '/' + LOG_TIME + '/' + str('eip.' + UHOSTIP)
    LOG_FILE = LOG_PATH + '/' + str('eip.' + UHOSTIP)

    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)


    while True:
        IPADDRS = uhost_describe(UHOSTID)

        if len(IPADDRS) == 1:
            eip_data_1 = eip_apply()
            time.sleep(1)
            eip_id_1 = eip_data_1['EIPId']
            eip_wg_1 = eip_describe(eip_id_1)

            if eip_wg_1 != 100:
                eip_Weight_modify(eip_id_1, 100)

            time.sleep(1)
            eip_bind(eip_id_1, UHOSTID)

	    log_write('','\n','')
	    log_write('','\n','')
            time.sleep(TIME)

        elif len(IPADDRS) == 2:
            for IPS in IPADDRS:
                if IPS.has_key("IPId"):
                    eip_id_1 = IPS["IPId"]
                    eip_wg_1 = eip_describe(eip_id_1)
                    if eip_wg_1 != 100:
                        eip_Weight_modify(eip_id_1, 100)

                    eip_data_2 = eip_apply()
                    time.sleep(1)
                    eip_id_2 = eip_data_2['EIPId']
                    eip_wg_2 = eip_describe(eip_id_2)
                    if eip_wg_2 != 50:
                        eip_Weight_modify(eip_id_2, 50)
                    time.sleep(1)
                    eip_bind(eip_id_2, UHOSTID)

                    time.sleep(15)
                    eip_unbind(eip_id_1, UHOSTID)
                    time.sleep(15)
                    eip_delete(eip_id_1)
                    time.sleep(1)
                    eip_Weight_modify(eip_id_2, 100)

            time.sleep(1)
	    log_write('','\n','')
	    log_write('','\n','')
            time.sleep(TIME)
        elif len(IPADDRS) == 3:
            WGLIST = {}
            for IPS in IPADDRS:
                if IPS.has_key("IPId"):
                    eip_id = IPS["IPId"]
                    eip_wg = eip_describe(eip_id)
                    WGLIST[eip_id] = eip_wg

            WGARR = WGLIST.values()

            if WGARR.count(100) == 1:
                for key in WGLIST.keys():
                    if WGLIST[key] == 100:
                        eip_id_1 = key
                        eip_unbind(eip_id_1, UHOSTID)
                        time.sleep(15)
                        eip_delete(eip_id_1)
                        time.sleep(1)

                for key in WGLIST.keys():
                    if WGLIST[key] != 100:
                        eip_id_2 = key
                        eip_Weight_modify(eip_id_2, 100)
            else:
                eip_id_1 = WGLIST.keys()[0]
                eip_id_2 = WGLIST.keys()[1]
                eip_wg_1 = WGLIST[eip_id_1]
                eip_wg_2 = WGLIST[eip_id_2]
                if eip_wg_1 != 100:
                    eip_Weight_modify(eip_id_1, 100)

                time.sleep(1)
                eip_unbind(eip_id_2, UHOSTID)
                time.sleep(15)
                eip_delete(eip_id_2)
                time.sleep(1)

                eip_data_3 = eip_apply()
                eip_id_3 = eip_data_3['EIPId']
                eip_wg_3 = eip_describe(eip_id_3)
                if eip_wg_3 != 50:
                    eip_Weight_modify(eip_id_3, 50)
                time.sleep(1)
                eip_bind(eip_id_3, UHOSTID)

                time.sleep(15)
                eip_unbind(eip_id_1, UHOSTID)
                time.sleep(15)
                eip_delete(eip_id_1)
                time.sleep(1)
                eip_Weight_modify(eip_id_3, 100)

	    log_write('','\n','')
	    log_write('','\n','')
            time.sleep(TIME)
        else:
            for IPS in IPADDRS:
                if IPS.has_key("IPId"):
                    eip_id = IPS["IPId"]
                    eip_unbind(eip_id, UHOSTID)
                    time.sleep(15)
                    eip_delete(eip_id)
                    time.sleep(1)

            log_write('','\n', ' 云主机绑定了太多的EIP,请检查!')
            sys.exit(0)
