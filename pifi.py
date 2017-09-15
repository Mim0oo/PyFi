print "-------------------------------------"
print " PyFi - Python WiFi Monitor v1.0:10.09.2017"
print " This applications restarts WiFi adapter on fail"
print " By Martin Georgiev email: geeorgiev[at]gmail.com"
print " All rights reserved, GNU General Public License v3.0"
print "----------------------------------------------------"
print "loading assets...",
import subprocess
import requests
import logging
from time import sleep
from datetime import datetime
import threading
print " done"
print "------------------------------------------"

# Debug configuration
logging.basicConfig(filename="Wifi.log", level=logging.DEBUG)


def get_timestamp():
    # Current local time getter
    clock = datetime.now().strftime('[%Y-%m-%d %H:%M]')
    return clock


def run_win_cmd(cmd):
    result = []
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    for line in result:
        print(line)
	logging.debug(line)
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)


def ping_alive():
    clock = get_timestamp()
    try:
        r = requests.get('http://google.com')
    except Exception, e:
        logging.debug(clock+" WiFi connection test failed.")
        return 500
    logging.debug(clock+" WiFi test passed OK.")
    return r.status_code


def restart_wifi_adapter():
    run_win_cmd('netsh interface set interface "WiFi" admin=disable')
    sleep(3)
    run_win_cmd('net stop WlanSvc')
    sleep(3)
    run_win_cmd('net start WlanSvc')
    sleep(3)
    run_win_cmd('netsh interface set interface "WiFi" admin=enable')


def loop_mon():
    test = ping_alive()
    if test != 200:
        # Logging and restart
	clock = get_timestamp()
        logging.debug(clock+" Restarting adapter.")
        print clock+" Restarting adapter..."
        restart_wifi_adapter()
    threading.Timer(300, loop_mon).start()

loop_mon()
