#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sdk import UcloudApiClient
from config import *
import sys
import json
import time

def log_write(str_begin,str_end, *args):
    LOG_FILE = "/root/ucloud-sdk-python/log/eip.eip_polling_release_unbind"
    if len(args) != 1:
        with open(LOG_FILE,"a+") as f:
            msg = " ".join(args)
            f.write(str_begin + msg + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + str_end)
    else:
        with open(LOG_FILE,"a+") as f:
            f.write(str_begin + args[0] + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + str_end)


def eip_delete(IPUID):
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={"Action":"ReleaseEIP","EIPId":IPUID,"Region":"cn-bj2"}

    trynum = 0
    success = False
    while trynum < 3 and not success:
        try:
            response = ApiClient.get("/", Parameters )
            success = True
        except:
            trynum += 1
            if trynum != 3:
                time.sleep(5)
            else:
                log_write('\n', '\n', str(IPUID), '释放失败时间:')
                sys.exit(0)

    response_data = json.loads(json.dumps(response))

    if response_data["RetCode"] == 0:
        log_write('', '\n', '释放成功时间:')
    else:
        log_write('', '\n', '释放失败时间:')


def eip_list_relese(name):
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
        "Action":"DescribeEIP",
        "ProjectId":"org-tgfjdn",
        "Region":"cn-bj2",
        "Limit": 300
    }

    trynum = 0
    success = False
    while trynum < 3 and not success:
        try:
            response = ApiClient.get("/", Parameters )
            success = True
        except:
            trynum += 1
            if trynum != 3:
                time.sleep(5)
            else:
                log_write('\n', '\n', 'EIP获取列表失败时间:')
                sys.exit(0)

    response_data = json.loads(json.dumps(response))

    for eip_data in response_data["EIPSet"]:
       if eip_data["Status"] == "free":
           a = name.decode('utf-8').encode('unicode_escape')
           b = eip_data["Name"].encode('unicode_escape')
           c = eip_data["Bandwidth"]
           d = eip_data["EIPId"]
           e = eip_data["EIPAddr"][0]["IP"]
           f = eip_data["CreateTime"]
	   g = int(time.time() - 3600)

           if a == b and c == 1 and f < g:
              log_write('', ' ', str(e), str(d), '准备释放时间:')
              eip_delete(d)
       else:
           continue



if __name__=='__main__':
    name = "EIP"

    while True:
        eip_list_relese(name)
        time.sleep(600)
