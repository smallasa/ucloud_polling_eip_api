# ucloud_polling_eip_api
### 1.下载软件包
```bash
git clone https://github.com/smallasa/ucloud_polling_eip_api.git

mv ucloud_polling_eip_api/ucloud-sdk-python /root/ucloud-sdk-python
```

### 2.系统安装supervisor
```bash
yum -y install supervisor

systemctl staart supervisord && systemctl enable supervisord
```

### 3.脚本说明
```text
supervisor管理脚本:
ucloud_polling_eip_api/eip_supervisor_polling_init.sh
ucloud_polling_eip_api/eip_supervisor_polling_release_unbind.sh
ucloud_polling_eip_api/eip_supervisor_restart.sh

Ulcoud API 配置文件:
ucloud_polling_eip_api/ucloud-sdk-python/config.py

Ucloud API EIP 轮询脚本:
ucloud_polling_eip_api/ucloud-sdk-python/eip_uhost_polling.py

Ucloud API EIP 释放未被绑定的脚本:
ucloud_polling_eip_api/ucloud-sdk-python/eip_polling_release_unbind.py
```

### 4.修改API配置文件
```bash
ucloud-sdk-python/config.py:

#-*- encoding: utf-8 -*-
#配置公私钥"""
public_key  = ""
private_key = ""

#有外网IP主机使用
base_url    = "https://api.ucloud.cn"
```

### 5.手动执行脚本
```bash
删除已经申请,但未被使用的EIP:
cd /root/ucloud-sdk-python && python eip_polling_release_unbind.py

自动轮询切换EIP:
cd /root/ucloud-sdk-python && python eip_uhost_polling.py --uhost-id {xx} --uhost-ip {xx} --time 600

注意: 后面--time表示多久轮询切换一次EIP
```

### 6.推荐使用supervisor进行管理
```bash
配置supervisor 释放EIP配置:
sh eip_supervisor_polling_release_unbind.sh

配置supervisor 轮询EIP配置:
sh eip_supervisor_polling_init.sh {uhost-ip} {uhost-id}

重启supervisor管理的服务：
sh eip_supervisor_restart.sh
```

### 7.结束语
```text
请各位合理参考，进行修改！
```