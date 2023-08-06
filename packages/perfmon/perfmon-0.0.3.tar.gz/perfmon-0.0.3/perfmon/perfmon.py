# coding:utf-8
import os
import sys
import platform
import logging
import traceback
import subprocess
import datetime
import time
from threading import Thread



class PerfMon(object):
    '''
    docstring for perfmon
    pidcpu,totalcpu,pidmem,dalvikmem,nativemem,fps,sedtraffic,rcvtraffic
    '''
    def __init__(self):
        self.serial=''
        self.process=''
        self.model=''
        self.pid='0'
        self.uid = '0'
        self.fps_count=0
        self.fps_start_time=0
        self.fps_end_time=0
        self.fps_current_frame_num=0
        self.fps_last_frame_num=0
        self.root=0                 #root： 0： noroot  1： adb root 2 ： su -c   3: su root
        self.uid = 0
        self.sdk_version = 0
        self.adb_shell_root_pre = ''  # adb -s serial shell su -c , adb -s serial shell su root ,adb -s serial shell
        self.adb_shell_pre= ''  # adb -s serial shell
        self.grep= ''  #  window :findstr,linux :grep
        self.debug= False  #  debug

        self.idleCpuNow=[]
        self.idleCpuPre=[]
        self.totalCpuNow=[]
        self.totalCpuPre=[]
        self.processCpuNow=0
        self.processCpuPre=0
        self.str_platform = platform.system()

        self.processSedTraNow=0
        self.processRcvTraNow=0
        self.SedTraFirst=1
        self.RcvTraFirst=1
        self.processRcvTraInit=0
        self.processSedTraInit=0
        self.batteryFirst=1

        self.pidcpu = 0
        self.totalcpu = 0
        self.pidmem = 0
        self.totalmem = 0
        self.dalvikmem = 0
        self.nativemem = 0
        self.fps = 0
        self.sedtraffic = 0
        self.rcvtraffic = 0
        self.battery = 0

    #-----------------------------------------public define---------------------------------------------------------#
    def logging_info(self,*args):
        try:
            if self.debug:
                if args is not None:
                    logging.info(args)
                    print args
                return  True
        except Exception,ex:
            logging.error(Exception(ex))
            traceback.print_exc()
        return False

    def subprocess_cmd_v2(self,str_cmd):
        self.logging_info(sys._getframe().f_code.co_name, str_cmd)
        sub_result=''
        sub_proc = None
        try:
            if cmp(self.str_platform,'Windows')==0:
                sub_proc = subprocess.Popen(str_cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
            else:
                sub_proc = subprocess.Popen(str_cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True, close_fds=True)
            stdout,stderr = sub_proc.communicate()
            returncode = sub_proc.returncode
            self.logging_info("returncode=",returncode,",stdout=",stdout,",stderr=",stderr)
            sub_result = stdout
            self.logging_info("subprocess_cmd_v2 sub_result=",sub_result)
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
            self.logging_info(Exception(ex))
        return sub_result





    def get_adb_su(self):
        self.logging_info(sys._getframe().f_code.co_name)
        self.adb_shell_pre = 'adb -s ' + self.serial + ' shell '
        sub_result_adbroot = self.subprocess_cmd_v2(self.adb_shell_pre +  ' service call SurfaceFlinger 1013')
        if len(sub_result_adbroot) >0:
            if 'Error' not in sub_result_adbroot :
                self.root=1
                self.adb_shell_root_pre = self.adb_shell_pre
                return
        sub_result_suc = self.subprocess_cmd_v2(self.adb_shell_pre +  ' su -c service call SurfaceFlinger 1013')
        if len(sub_result_suc) >0:
            if ( 'Error' not in sub_result_suc) and ('Parcel' in  sub_result_suc) :
                self.root=2
                self.adb_shell_root_pre = self.adb_shell_pre +  ' su -c '
                return
        sub_result_suroot = self.subprocess_cmd_v2(self.adb_shell_pre +  ' su root service call SurfaceFlinger 1013')
        if len(sub_result_suroot) >0:
            if ('Error' not in sub_result_suroot) and ('Parcel' in  sub_result_suc) :
                self.root=3
                self.adb_shell_root_pre = self.adb_shell_pre + ' su root '
                return

    def get_sdk_version(self):
        self.logging_info(sys._getframe().f_code.co_name)
        sub_result = self.subprocess_cmd_v2(self.adb_shell_pre + ' getprop ro.build.version.sdk')
        if len(sub_result) > 0:
            self.sdk_version = int(sub_result)

    def set_grep(self):
        self.logging_info(sys._getframe().f_code.co_name)
        if cmp(self.str_platform, 'Windows')==0:
            self.grep = ' findstr '
        elif cmp(self.str_platform, 'Darwin')==0:
            self.grep = ' grep '
        elif cmp(self.str_platform, 'Linux')==0:
            self.grep = ' grep '
        else:
            self.grep = ' findstr '

    def get_pid_uid(self):
        self.logging_info(sys._getframe().f_code.co_name)
        for i in range(1,50):
            if self.sdk_version < 26:
                str_cpu = self.subprocess_cmd_v2(self.adb_shell_pre  + ' ps | '+ self.grep + self.process)
            else:
                str_cpu = self.subprocess_cmd_v2(self.adb_shell_pre  + ' ps -A | '+ self.grep + self.process)
            for it in str_cpu.split('\n'):
                it_list = filter(None, it.replace('\n','').replace('\t','').replace('\r','').split(' '))
                if len(it_list) > 0 and it_list[-1] ==self.process:
                    self.pid =  str(it_list[1])
                    self.uid = '100' + str(it_list[0].replace('u0_a',''))
                    return True
        return False

    def set_debug(self,_debug):
        self.logging_info(sys._getframe().f_code.co_name)
        self.debug = _debug

    def set_param(self,_serial,_process,_model):
        self.logging_info(sys._getframe().f_code.co_name)
        self.__init__()
        self.serial = _serial
        self.process = _process
        self.model = _model
        self.set_grep()
        self.get_adb_su()
        self.get_sdk_version()
        self.get_pid_uid()
        return self.pid

    def get_fps_frame_num(self,str_fps=''):
        self.logging_info(sys._getframe().f_code.co_name)
        frameNum = 0
        if 'Parcel' in str_fps:
            i1 = str_fps.index('(')
            i2 = str_fps.index('  ')
            frameNumString = str_fps[i1 + 1: i2]
            frameNum = int(frameNumString.upper(), 16)
        return frameNum

    def get_str_fps(self):
        self.logging_info(sys._getframe().f_code.co_name)
        return self.adb_shell_root_pre + ' service call SurfaceFlinger 1013'


    def cacl_pid_cpu_proc(self):# adb -s HT73A0203875 shell cat /proc/10099/stat
        self.logging_info(sys._getframe().f_code.co_name)
        str_pid_cpu = self.subprocess_cmd_v2(self.adb_shell_pre + ' cat /proc/' + self.pid + '/stat ')
        jef_list = filter(None, str_pid_cpu.split(' '))
        if len(jef_list)>14:
            self.processCpuNow = int(jef_list[13]) + int(jef_list[14])
        else:
            self.processCpuNow = 0

    def cacl_total_cpu_proc(self):
        self.logging_info(sys._getframe().f_code.co_name)
        str_total_cpu = self.subprocess_cmd_v2(self.adb_shell_pre + ' cat /proc/stat ')
        for line in str_total_cpu.split('\n'):
            if len(line) > 0 and 'cpu' in line:
                jef_list = filter(None, line.split(' '))
                self.idleCpuNow.append(int(jef_list[4]))
                self.totalCpuNow.append(int(jef_list[1]) + int(jef_list[2]) + int(jef_list[3]) + int(jef_list[4]) + int(jef_list[5]) + int(jef_list[6]) + int(jef_list[7]))

    def cacl_cpu_proc(self):
        self.logging_info(sys._getframe().f_code.co_name)
        self.idleCpuNow = []
        self.totalCpuNow = []
        self.cacl_pid_cpu_proc()
        self.cacl_total_cpu_proc()
        if (len(self.totalCpuPre) > 0):
            if (self.processCpuNow > self.processCpuPre) and (self.totalCpuNow[0] > self.totalCpuPre[0]):
                self.pidcpu = round(((self.processCpuNow -self.processCpuPre) * 1.00 /(self.totalCpuNow[0] - self.totalCpuPre[0]) ) * 100  ,2)
            else:
                self.pidcpu = 0
            if (self.totalCpuNow[0] > self.totalCpuPre[0]):
                total_cpu_up = (self.totalCpuNow[0] -self.idleCpuNow[0]) - (self.totalCpuPre[0] - self.idleCpuPre[0])
                total_cpu_down = self.totalCpuNow[0] - self.totalCpuPre[0]
                self.totalcpu = round(total_cpu_up * 1.00 / total_cpu_down  * 100,2)
            else:
                self.totalcpu = 0
        else:
            self.pidcpu = 0
            self.totalcpu = 0
            self.totalCpuPre = self.totalCpuNow
            self.processCpuPre = self.processCpuNow
            self.idleCpuPre = self.idleCpuNow

        self.totalCpuPre  = self.totalCpuNow
        self.processCpuPre = self.processCpuNow
        self.idleCpuPre  = self.idleCpuNow

    def cacl_ram(self):
        self.logging_info(sys._getframe().f_code.co_name)
        self.pidmem = 0
        self.dalvikmem = 0
        self.nativemem = 0
        str_ram = ''
        if self.model=='perfmon_native':
            str_ram = self.subprocess_cmd_v2(self.adb_shell_pre + ' dumpsys meminfo '+ self.process)
            for str_line in str_ram.split('\n'):
                str_line_list = filter(None, str_line.replace('\n','').replace('\t','').split(' '))
                if 'Native' in str_line and ':' not in str_line:
                    self.nativemem  =str_line_list[-2]
                elif 'Dalvik' in str_line and 'ther' not in str_line:
                    self.dalvikmem  =str_line_list[-2]
                elif 'TOTAL' in str_line and 'SWAP' not in str_line and 'Dirty'  not in str_line:
                    self.pidmem  =str_line_list[1]
                    break
                else:
                    pass
        else:
            if self.root !=0:
                str_ram = self.subprocess_cmd_v2(self.adb_shell_root_pre + ' cat /proc/' + self.pid + '/smaps | '+ self.grep + ' Pss')
                for str_line in str_ram.split('\n'):
                    if len(str_line) > 0:
                        str_line_list = filter(None, str_line.replace('\n','').replace('\t','').split(' '))
                        # print 'str_line_list=',str_line_list
                        self.pidmem += int(str_line_list[1])
            else:
                start_time = datetime.datetime.now()
                str_ram = self.subprocess_cmd_v2(self.adb_shell_pre + ' top -d 1 -n 1 | '+ self.grep +' ' + self.pid)
                for str_line in str_ram.split('\n'):
                    if len(str_line) > 0:
                        str_line_list = filter(None, str_line.replace('\n','').replace('\t','').split(' '))
                        if cmp(str_line_list[0],self.pid )==0:
                            if 'K' in str_line_list[5]:
                                self.pidmem = str_line_list[5].replace('K','')
                            elif 'M' in str_line_list[5]:
                                self.pidmem = int(str_line_list[5].replace('M','') ) * 1000
                            else:
                                self.pidmem = 0

    def cacl_fps(self):
        self.logging_info(sys._getframe().f_code.co_name)
        if self.root ==0:
            return
        self.fps = 0
        real_fps_cost_Time = 0
        self.fps_end_time = time.time()
        if self.fps_count != 0:
            real_fps_cost_Time = self.fps_end_time - self.fps_start_time
        self.fps_start_time =  time.time()
        if self.fps_count == 0:
            self.fps_last_frame_num = self.get_fps_frame_num(self.subprocess_cmd_v2(self.get_str_fps()))
        self.fps_current_frame_num = self.get_fps_frame_num(self.subprocess_cmd_v2(self.get_str_fps()))
        if real_fps_cost_Time > 0:
            self.fps = (int) ((self.fps_current_frame_num - self.fps_last_frame_num) / real_fps_cost_Time)
        self.fps_last_frame_num = self.fps_current_frame_num
        self.fps_count = self.fps_count + 1

    def cacl_traffic_sed(self):
        self.logging_info(sys._getframe().f_code.co_name)
        str_sed_traffic = self.subprocess_cmd_v2(self.adb_shell_root_pre + ' cat /proc/uid_stat/' + str(self.uid) + '/tcp_snd')
        for str_line in str_sed_traffic.split('\n'):
            if len(str_line) > 0:
                str_line_list = filter(None, str_line.replace('\n','').replace('\t','').split(' '))
                # print 'str_line_list',str_line_list
                if self.SedTraFirst == 1:
                    self.processSedTraInit = int(str_line_list[0])
                    self.SedTraFirst = 0
                else:
                    self.processSedTraNow = int(str_line_list[0])

    def cacl_traffic_rcv(self):
        self.logging_info(sys._getframe().f_code.co_name)
        str_rcv_traffic = self.subprocess_cmd_v2(self.adb_shell_root_pre + ' cat /proc/uid_stat/' + str(self.uid) + '/tcp_rcv')
        for str_line in str_rcv_traffic.split('\n'):
            if len(str_line) > 0:
                str_line_list = filter(None, str_line.replace('\n','').replace('\t','').split(' '))
                # print 'str_line_list',str_line_list
                if self.RcvTraFirst == 1:
                    self.processRcvTraInit = int(str_line_list[0])
                    self.RcvTraFirst = 0
                else:
                    self.processRcvTraNow = int(str_line_list[0])



    def cacl_traffic(self):
        self.logging_info(sys._getframe().f_code.co_name)
        self.cacl_traffic_sed()
        self.cacl_traffic_rcv()
        if (self.processSedTraNow > self.processSedTraInit)  and (self.processRcvTraNow > self.processRcvTraInit):
            self.sedtraffic = round((self.processSedTraNow - self.processSedTraInit) / 1024.0  / 1024.0, 3)
            self.rcvtraffic = round((self.processRcvTraNow - self.processRcvTraInit ) / 1024.0  / 1024.0, 3)

    # not support
    def cacl_battery(self):
        self.logging_info(sys._getframe().f_code.co_name)
        # if self.sdk_version >= 21:
        #     if self.batteryFirst == 1 :
        #         str_battery = self.subprocess_cmd_v2(self.adb_shell_pre + ' dumpsys batterystats –enable full-wake-history ')
        #         str_battery = self.subprocess_cmd_v2(self.adb_shell_pre + ' shell dumpsys batterystats --reset')
        #         str_battery = self.subprocess_cmd_v2(self.adb_shell_pre + ' shell  logcat -c')
        #         self.batteryFirst = 0
        #     str_battery = self.subprocess_cmd_v2(self.adb_shell_pre + ' bugreport >  bugreport.txt')
        #     str_battery = self.subprocess_cmd_v2(self.adb_shell_pre + ' dumpsys battery')
        #     for str_line in str_battery.split('\n'):
        #         if len(str_line) > 0 and 'level' in str_line:
        #             str_line_list = filter(None, str_line.replace('\n','').replace('\t','').split(' '))
        #             self.battery= str_line_list[2]

    def cacl_perf(self):
        self.logging_info(sys._getframe().f_code.co_name)
        if self.model=='perfmon_normal':
            self.cacl_cpu_proc()
            self.cacl_ram()
            self.cacl_fps()
        elif self.model=='perfmon_all':
            self.cacl_cpu_proc()
            self.cacl_ram()
            self.cacl_fps()
            self.cacl_traffic()
        elif self.model=='perfmon_cpu':
            self.cacl_cpu_proc()
        elif self.model=='perfmon_ram':
            self.cacl_ram()
        elif self.model=='perfmon_native':
            self.cacl_ram()
        elif self.model=='perfmon_fps':
            self.cacl_fps()
        elif self.model=='perfmon_traffic':
            self.cacl_traffic()
        elif self.model=='perfmon_battery':
            self.cacl_battery()
        perf_value = str(self.pidcpu) + ',' + str(self.totalcpu) +  ',' + str(self.pidmem)  + ',' + str(self.dalvikmem) + ',' + str(self.nativemem) + ',' + str(self.fps)+ ',' +  str(self.sedtraffic) + ',' + str(self.rcvtraffic) + ',' + str(self.battery)
        self.logging_info('perf_value',perf_value)
        return perf_value

if __name__ == '__main__':
    test = PerfMon()
    pro_pid = test.set_param(_serial='s25.btos.cn:7601',_process='com.autonavi.amapauto',_model='perfmon_normal')
    # test.set_debug(True)
    if pro_pid =='0':
        test.logging_info('error pro_pid')
        sys.exit(0)
    str_perf_file = time.strftime("%Y%m%d%H%M", time.localtime()) + '.txt'
    for i in range(0,1000):
        start_time = time.time()
        print test.cacl_perf()
        # print 4444,str(time.time() - start_time)