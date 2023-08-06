#-*- coding:utf-8 -*-
import os
import subprocess
import traceback
import platform
import sys
import logging
import time
import datetime
from threading import Thread
str_platform = platform.system()


def logging_info(*args):
    try:
        if args is not None:
            logging.info(args)
        return  True
    except Exception,ex:
        logging.error(Exception(ex))
        traceback.print_exc()
    return False

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper


def subprocess_cmd_v2(str_cmd=''):
    sub_result = ''
    try:
        logging_info('subprocess_cmd str_cmd= ' + str_cmd)
        if cmp(str_platform,'Windows')==0:
            sub_proc = subprocess.Popen(str_cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        else:
            sub_proc = subprocess.Popen(str_cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True, close_fds=True)
        stdout,stderr = sub_proc.communicate()
        returncode = sub_proc.returncode
        logging_info('returncode=',returncode,',stdout=',stdout,',stderr=',stderr)
        sub_result = stdout
        logging_info('subprocess_cmd_v2 sub_result=',sub_result)
        if sub_proc.stdin:
            sub_proc.stdin.close()
        if sub_proc.stdout:
            sub_proc.stdout.close()
        if sub_proc.stderr:
            sub_proc.stderr.close()
        try:
            sub_proc.kill()
        except OSError:
            pass
    except Exception,ex:
        logging_info(Exception(ex))
        traceback.print_exc()
    return sub_result


def write_fun_file(file_name='',funtxt=''):
    logging_info(sys._getframe().f_code.co_name, file_name, funtxt)
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
        print Exception(ex)
    return False


if __name__ == '__main__':
    logging_info(sys._getframe().f_code.co_name)
    logging_info('aa',{})