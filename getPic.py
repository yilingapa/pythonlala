# -*- coding:utf-8 -*-
import subprocess,os,sys,time
globalStartupInfo = subprocess.STARTUPINFO()
globalStartupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
def runCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd(), shell=False, startupinfo=globalStartupInfo)
    p.wait()
    re=p.stdout.read().decode()
    return re
curdir=os.getcwd()
#连接的手机列表
mobiles=[]
cmd=[curdir +'/adb.exe','devices']
mobilelist=runCmd(cmd)
mobilelist=mobilelist.split('\r\n')[1:]
# print(mobilelist)
for x in mobilelist:
    if x:
        mobiles.append(x)
if mobiles:
    print(mobiles)
else:
    print(['no devices\t no devices'])
#取第一个手机的序列号
xuliehao='';
if mobiles:
    #取第一个手机设备
    device=mobiles[0].split('\t')
    xuliehao=device[0]
    print(device)
#有手机连接上就截图
if xuliehao:
    #保存到本地电脑的图片路径
    timestamp = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    jietupath=r'd:\_code\pythonla\venv\venv\static\lala-'+timestamp+'.png'
    sdcardpath='/sdcard/screenshot-'+timestamp+'.png'
    if os.path.exists(jietupath):
        os.remove(jietupath)
    print('it is screenshoting to mobile.....')
    jtcmd=curdir +'/adb.exe   -s '+xuliehao+' shell /system/bin/screencap -p '+sdcardpath
    # print(jtcmd)
    result=runCmd(jtcmd)
    print('it is screenshot success.....')
    # print(result)
    print('it is moving screenshot to pc.....')
    jtcmd=curdir +'/adb.exe  -s  '+xuliehao+' pull '+sdcardpath+' '+jietupath
    print(jietupath)
    # print(jtcmd)
    result=runCmd(jtcmd)
    # print(result)
    #删除sd图片
    jtcmd=curdir +'/adb.exe   -s '+xuliehao+' shell rm  '+sdcardpath
    # print(jtcmd)
    result=runCmd(jtcmd)
    print(result)
    print('it is moved screenshot to pc success.....')
else:
    print('no device!')