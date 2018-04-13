from flask import Flask
from flask import render_template
from flask import request
import os
import subprocess,os,sys,time
globalStartupInfo = subprocess.STARTUPINFO()
globalStartupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
curdir = os.getcwd()
xuliehao=''
def runCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd(), shell=False, startupinfo=globalStartupInfo)
    p.wait()
    re=p.stdout.read().decode()
    return re

app = Flask(__name__)

@app.route('/')
def hello(name=None):
    global xuliehao
    # 连接的手机列表
    mobiles = []
    cmd = [curdir + '/adb.exe', 'devices']
    mobilelist = runCmd(cmd)
    mobilelist = mobilelist.split('\r\n')[1:]
    for x in mobilelist:
        if x:
            mobiles.append(x)
    if mobiles:
        print(mobiles)
    else:
        print(['no devices\t no devices'])
    if mobiles:
        device = mobiles[0].split('\t')
        xuliehao = device[0]
        print(device)
    return render_template('getDistance.html', name=name)

@app.route('/picname',methods=['GET'])
def picName():
    os.chdir(r'D:\_Code\pythonla\venv\venv\static')
    path=os.getcwd()
    return os.listdir(path)[-1]

@app.route('/pullimg',methods=['GET'])
def pullimg():
    global xuliehao
    timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    jietupath = r'd:\_code\pythonla\venv\venv\static\\' + timestamp + '.png'
    sdcardpath = '/sdcard/screenshot-' + timestamp + '.png'
    if os.path.exists(jietupath):
        os.remove(jietupath)
    print('screenshoting to mobile.....')
    jtcmd = curdir + '/adb.exe   -s ' + xuliehao + ' shell /system/bin/screencap -p ' + sdcardpath
    # print(jtcmd)
    result = runCmd(jtcmd)
    print('mobile screenshot success.....')
    # print(result)
    print('moving screenshot to pc.....')
    jtcmd = curdir + '/adb.exe  -s  ' + xuliehao + ' pull ' + sdcardpath + ' ' + jietupath
    print(jietupath)
    # print(jtcmd)
    result = runCmd(jtcmd)
    # print(result)
    # 删除sd图片
    jtcmd = curdir + '/adb.exe   -s ' + xuliehao + ' shell rm  ' + sdcardpath
    # print(jtcmd)
    result = runCmd(jtcmd)
    print(result)
    print('moved to pc success.....')
    return 'pull success'


@app.route('/gettime',methods=['GET'])
def gettime():
    time = request.args.get('time', '')
    print('time:'+time)
    cmdorder=curdir + '/adb.exe   -s ' + xuliehao +' shell input swipe 30 30 30 30 '+time
    result = runCmd(cmdorder)
    print(result)
    return ''
if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
