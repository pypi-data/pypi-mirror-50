# coding:utf-8
import os
import sys
from perfmon import *

global perfMon
perfMon = PerfMon()
global ret_flag
ret_flag = False

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def write_fun_file(file_name='',funtxt=''):
    try:
        file_object=None
        if os.path.isfile(file_name):
            with open(file_name, 'a+') as file_object:
                file_object.write(funtxt + '\n')   #加\n换行显示
        else:
            file_object = open(file_name,'w')
            file_object.write('pidcpu,totalcpu,pidmem,dalvikmem,nativemem,fps,sedtraffic,rcvtraffic,battery\n')
        return True
    except Exception,ex:
        print (Exception(ex))
    return False


@async
#get perf sync
def perf_monitor_7(case_name=''):
    global ret_flag
    while ret_flag and perfMon is not None:
        start_time = time.time()
        perf_value =  perfMon.cacl_perf()
        write_fun_file(file_name=case_name,funtxt=perf_value)
        print 4444,str(time.time() - start_time)
# start monitor
def perfmon_start_monitor(dir_case_file):
    global ret_flag
    ret_flag = True
    perf_monitor_7(dir_case_file)

# stop monitor
def perfmon_stop_monitor():
    global ret_flag
    ret_flag = False

#init
def perfmon_init(serial,process,model):
    global perfMon
    perfMon.set_param(serial,process,model)

#init
def perfmon_debug(debug):
    global perfMon
    perfMon.set_debug(debug)

#unint
def perfmon_uninit():
    global perfMon
    perfMon = None
    global ret_flag
    ret_flag = False

if __name__ == '__main__':
    perfmon_init(serial='8XV5T15A23005494',process='com.autonavi.amapauto',model='perfmon_normal')
    perfmon_debug(False)
    perfmon_start_monitor(dir_case_file='D:/6.txt')
    time.sleep(60)
    perfmon_stop_monitor()
    perfmon_uninit()