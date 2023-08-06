import socket, os, sys, requests, json
import uuid, re
import subprocess
from crontab import CronTab
import requests, json

host_ip = ''
host_name = ''
host_mac = ''
all_jsons = {}

def ethtool_x_cp():
    
    f = open("ethtoolpyth.py", "w")
    f.write("import subprocess\n\r")
    f.write("import time\n\r")
    f.write("print('Running ethtool command')\n\r")
    f.write("subprocess.call(['sudo', 'ethtool', '-s','enp1s0', 'wol','g' ])\n\r")
    f.write("time.sleep(10)\n\r")
    f.write("subprocess.call(['sudo', 'ethtool', '-s','enp1s0', 'wol','g' ])\n\r")
    f.close()
    
    try:
        subprocess.call(["sudo", "chmod", "a+x", "ethtoolpyth.py"])
        print("Adding ethtoolpyth.py")
        print("yes or no")
        subprocess.call(["sudo", "cp", "-i", "ethtoolpyth.py", "/bin"])

    except:
        print(" Error while adding file to bin")


def cron_jobs():
    try:
        print("Running cron command")
        cron = CronTab(user='root')

        print("root access gained")

        for jobs in cron:
            print(jobs)
            if jobs.comment == 'run_it':
                cron.remove(jobs)
                cron.write()

        # **************** knowing python version **********************************
        __knowversion = ''
        if sys.version_info[0] < 3:
            __knowversion = 'python /bin/ethtoolpyth.py &'
        else :
            __knowversion = 'python3 /bin/ethtoolpyth.py &'
        # **************************************************************************

        # job = cron.new(command='python3 /bin/ethtoolpyth.py &', comment="run_it")
        job = cron.new(command=__knowversion , comment="run_it")
        job.every_reboot()

        cron.write()

        for jobs in cron:
            print(jobs)
    except:
        print("Unable to create in job")


def comp_info():
    try:
        global host_name
        global host_ip
        global host_mac
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print("Hostname :  ", host_name)
        print("IP : ", host_ip)
        print("The MAC address : ")
        print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
        host_mac = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
    except:
        print("Unable to get Hostname and IP")


def tool_run():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        ip_address_part = ip_address[0:11]
        ip_address_part += "1-"
        ip_address_part += ip_address[0:11]
        ip_address_part += "255"
        print(ip_address_part)
        s.close()
        print("Running Nbtscan ........")
        subprocess.call(["nbtscan", ip_address_part])
        f = open("output.txt", "w")
        p = subprocess.check_output(["nbtscan", ip_address_part]).decode("utf-8")
        f.write(p)
        f.close()
    except:
        print("Nbt scan failed ( Please check internet is connected!)")


def soft_install():
    try:
        print("installing ethtool")
        subprocess.call(["sudo", "apt-get", "install", "ethtool"])
        print("Ethtool installed")

    except:
        print("ethtool installation failed")

    try:
        print("Installing nbttool")
        subprocess.call(["sudo", "apt-get", "install", "nbtscan"])
        print("Nbtscan installed")

    except:
        print("Nbtscan installtion failed")


def checker(data, length=64):
    if len(data) <= 0 or len(data) > length :
        print("Not valid Input, length must be less than {0}".format(length))
        return True
    return False

def send_data():
    global host_name
    global host_mac
    try:
        with open('data.txt') as f:
            names = f.readlines()
        f.close()

        names = [x.strip() for x in names]

        with open('data.txt') as f:
            macs = f.readlines()
        f.close()

        macs = [x.strip() for x in macs]

        jsondata = []

        for i in range(1, len(macs)):
            list = [names[i], macs[i]]
            jsondata.append(list)

        # for x in jsondata:
        #     print(x)

        # *****clubing****************************************************
        check = input("Do you want to update computer list yes or no  : ")
        if check == 'no':
            return 0


        name = input("Enter Device ID  : ")
        while checker(name, length=12) :
            name = input("Enter Device ID  : ")


        userpass = input("Enter Password : ")
        while checker(userpass, length=64):
            userpass = input("Enter Password : ")

        wifi = input("Enter WiFi (Router's name)  : ")
        while checker(wifi, length=32):
            wifi = input("Enter WiFi (Router's name)  : ")

        password = input("Enter WiFi passowrd  : ")
        while checker(password, length=64):
            password = input("Enter WiFi passowrd  : ")

        check = input("Should sub network information need to be collected yes or no  : ")

        # ************************************************************************************
        all_jsons['wifi'] = [wifi, password]
        all_jsons['host_computer'] = [host_name, host_mac]

        if check == 'yes':
            all_jsons['sub_host'] = [jsondata]
        else:
            all_jsons['sub_host'] = []

        collect_json_data = json.dumps(all_jsons)

        # print(collect_json_data)

        send = "http://"
        send += name
        send += ":"
        send += userpass
        send += "@"
        # send += "127.0.0.1:8000/api/data"
        send += "192.168.61.180:5003/api/data"

        try:
            r = requests.post(send , data = collect_json_data)
            if r.status_code == 200 :
                print("Process completed successfully")
            else:
                print("FAILED to connect to server, Please check internet connection")

        except:
            print("FAILED to connect to server, Please check internet connection or Enter correct Device ID and password")
        # r = requests.post('http://username:userpass@127.0.0.1:8000/api/data', data=json.dumps(data))

        # ************************************************************************************

    except:
        print("error")


def format_data():
    print("Formating the output")

    try:
        f = open("data.txt", "w")
        p = subprocess.check_output(["sudo", "awk", "/server/ {print $2}", "output.txt"]).decode("utf-8")
        f.write(p)
        f.close()

        f = open("data.txt", "w")
        p = subprocess.check_output(["sudo", "awk", "/server/ {print $NF}", "output.txt"]).decode("utf-8")
        f.write(p)
        f.close()

    except:
        print("error in formatting")


def finder():
    if not os.geteuid() == 0:
        sys.exit("\nOnly root can run this script (Run with sudo on ubuntu)\n")

    comp_info()
    ethtool_x_cp()
    cron_jobs()
    soft_install()
    tool_run()
    format_data()
    send_data()
    
def main():
    finder()
    
if __name__=='__main__':
    finder()


