# coding:utf-8
import os
import sys
from perfmon import *

global perfMon
global ret_flag


@async
#get perf sync
def perf_monitor_7(case_name=''):
    logging_info(sys._getframe().f_code.co_name)
    global ret_flag
    while ret_flag:
        perf_value =  perfMon.cacl_perf()
        logging_info('perf_value',perf_value)
        write_fun_file(file_name=case_name,funtxt=perf_value)

# start monitor
def perfmon_start_monitor(dir_case_file):
    logging_info(sys._getframe().f_code.co_name, dir_case_file)
    global ret_flag
    ret_flag = True
    perf_monitor_7(dir_case_file)

# stop monitor
def perfmon_stop_monitor():
    logging_info(sys._getframe().f_code.co_name)
    global ret_flag
    ret_flag = False

#init
def perfmon_init(serial,process,model):
    logging_info(sys._getframe().f_code.co_name,serial,process,model)
    global perfMon
    global ret_flag
    ret_flag = False
    perfMon = PerfMon()
    perfMon.set_param(serial,process,model)


#unint
def perfmon_uninit():
    logging_info(sys._getframe().f_code.co_name)
    global perfMon
    perfMon = None
    global ret_flag
    ret_flag = False

if __name__ == '__main__':
    pass