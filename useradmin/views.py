from django.db.models.query_utils import RegisterLookupMixin
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from useradmin.models import ssh_useradmin, useradmin_user
import time
import psutil
import paramiko
import json

# Create your views here.


class GetMysqlData():
    '获取models的所有数据，并且以list的方式返回'
    Getuserdata = useradmin_user.objects.values_list()
    transGetuserdata = list(Getuserdata)


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def index(request):
    getdatajson = {}
    getdatajsoncount = 0
    Getdata = ssh_useradmin.objects.values_list()
    transdata = list(Getdata)
    for i in transdata:
        getdatajsoncount += 1
        getdatajson.update({'{}'.format(getdatajsoncount): i, })
    print(getdatajson)
    return render(request, 'index.html', {'data': getdatajson})

def datatables(request):
    mysql_list = []
    query_set = useradmin_user.objects.all()
    for i in query_set:
        mysql_list.append({
            'id': i.id,
            'user': i.user,
            'user_email': i.user_email,
            'user_level': i.user_level,
            'user_ip': i.user_ip,
            'user_passwd': i.user_passwd,
            'Merchant': i.user_Merchant,
            'Area': i.user_area,
            'status': i.user_status,
        })
    mysql_dic = {}
    mysql_dic['data'] = mysql_list

    return HttpResponse(json.dumps(mysql_dic))

def deletedata(request):
    deleteuserid = request.body.decode('utf-8')
    try:
        useradmin_user.objects.filter(id=deleteuserid).delete()
    finally:
        print("delete useradmin_user ID  {}".format(deleteuserid))
    jssp = ({'status_code': 200})
    return JsonResponse(jssp, safe=False)

def adddata(request):
    adddic = {}
    print("laile")
    preuserid = request.body.decode('utf-8')
    transpre = json.loads(preuserid)

    for i, l in transpre.items():
        if l == '' or l == None:
            print("transpre.value为null")
            errordata = ({'status_code': 400})
            return JsonResponse(errordata, safe=False)
        else:
            adddic.update({
                i: l,
            })
    useradmin_user.objects.create(**adddic)
    jssp = ({'status_code': 200})
    return JsonResponse(jssp, safe=False)

def addhost(request):
    adddic = {}
    outdata = []
    preuserid = request.body.decode('utf-8')
    transpre = json.loads(preuserid)

    ssh_ip = transpre['ssh_ip']
    ssh_rootname = transpre['ssh_root']
    ssh_password = transpre['ssh_passwd']
    ssh_port = transpre['ssg_hostport']
    ssh_command = """free -h |grep -v total |awk -F' ' '{print $2}' |head -n 1;df |awk '{if(NR>1)print}'|awk -F' ' '{print $2}'|awk '{sum+=$1} END {print sum/1024/1024}';
    uname -r;cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l;"""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ssh_ip, username=ssh_rootname,
                       password=ssh_password, port=ssh_port)
        stdin, stdout, stderr = client.exec_command(command=ssh_command)
        stdindata = stdout.read().decode('utf-8')
        liststdin = stdindata.split()
    finally:
        client.close()
    for i, l in transpre.items():
        if l == '' or l == None:
            print("transpre.value为null")
            errordata = ({'status_code': 400})
            return JsonResponse(errordata, safe=False)
        else:
            adddic.update({
                i: l,
            })
    adddic.update({
        'ssh_host_cpu': liststdin[3],
        'ssh_host_Memory': liststdin[0],
        'ssh_host_disk': liststdin[1],
        'ssh_host_system': str(liststdin[2])
    })
    print(adddic)
    ssh_useradmin.objects.create(**adddic)
    jssp = ({'status_code': 200})
    return JsonResponse(jssp, safe=False)

def deletehost(request):
    qedata = request.body.decode('utf-8')
    transpre = json.loads(qedata)
    deletetranspre = transpre['index']
    ssh_useradmin.objects.filter(ssh_ip=deletetranspre).delete()
    print("delete ip : {}".format(transpre))
    jssp = ({'status_code': 200})
    return JsonResponse(jssp, safe=False)

def findhostdate(request):
    query_setdic = []
    postdict = {}
    qedata = request.body.decode('utf-8')
    transpre = json.loads(qedata)
    data = transpre['index']
    query_set = ssh_useradmin.objects.all()
    try:
        if ssh_useradmin.objects.filter(ssh_host_cloud_merchant=data):
            query_set = ssh_useradmin.objects.filter(
                ssh_host_cloud_merchant=data).all()
            for i in query_set:
                query_setdic.append({
                    'ip': i.ssh_ip,
                })
            postdict['data'] = query_setdic
            return HttpResponse(json.dumps(query_setdic))
    except:
        if ssh_useradmin.objects.filter(ssh_host_in_the_area=data):
            query_set = ssh_useradmin.objects.filter(
                ssh_host_in_the_area=data).all()
            for i in query_set:
                query_setdic.append({
                    'ip': i.ssh_ip,
                })
            return HttpResponse(json.dumps(query_setdic))

    jssp = ({'status_code': 200})
    return JsonResponse(jssp, safe=False)

def ssh_login_command(ssh_host, ssh_usernmae, ssh_userpass, ssh_command, ssh_port):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 自动添加主机名和密钥信息
        client.connect(hostname=ssh_host, username=ssh_usernmae, password=ssh_userpass, port=ssh_port)
        stdin, stdout, stderr = client.exec_command(command=ssh_command)
        stdindata = stdout.read().decode('utf-8')
        if stdindata != '':
            return stdindata
        else:
            stdindata = stderr.read().decode('utf-8')
            return stdindata
    finally:
        client.close()

def getuserandpassword(self,sshcommand):
    strdata = ""
    if type(self) == list:
        ipdata = self
    else:
        ipdata = self.split(",")
    mysqlreturndata = []
    print(ipdata)
    for i in ipdata:
        loopdata = ssh_useradmin.objects.get(ssh_ip=i)
        mysqlreturndata.append({
            'ip':loopdata.ssh_ip,
            'user':loopdata.ssh_root,
            'userpasswd':loopdata.ssh_passwd,
            'hostport':loopdata.ssg_hostport
        })
    dumpsdata = json.dumps(mysqlreturndata)

    for i in json.loads(dumpsdata):
        strdata += ssh_login_command(i['ip'], i['user'], i['userpasswd'],sshcommand,i['hostport']) + i['ip'] + '\n' + '\n'
    return strdata

def ssh_command(request):
    requestdata = request.body.decode('utf-8')
    transrequest = json.loads(requestdata)
    sshcommand = transrequest['command']
    print(transrequest)
    if transrequest['statuscode']==1:
        for i in transrequest:
            if transrequest[i] == '':
                jssp = ({'status_code': 404})
                return JsonResponse(jssp, safe=False)
        hostip = transrequest['iphost']
        userdata = getuserandpassword(hostip,sshcommand)
        return HttpResponse(userdata, status='200')

    elif transrequest['statuscode']==2:
        needshift = transrequest['iphost']
        testdata = needshift.split(',')
        del(testdata[0])
        for i in transrequest:
            if transrequest[i] == '':
                jssp = ({'status_code': 404})
                return JsonResponse(jssp, safe=False)
        userdata = getuserandpassword(testdata,sshcommand)
        return HttpResponse(userdata , status='200')
    jssp = ({'status_code': 200})
    return JsonResponse(jssp, safe=False)
