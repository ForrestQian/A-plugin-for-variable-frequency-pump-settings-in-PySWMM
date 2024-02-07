from swmm_api import SwmmInput
from datetime import timedelta
import pyswmm as pm
import os
import shutil

def movefile(srcfile, dstpath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.move(srcfile, dstpath + fname)  # 移动文件
        print("move %s -> %s" % (srcfile, dstpath + fname))

def swmm_write(time_step, start, end, in_filename, out_filename, pump_1, pump_2, pump_3, pump_in, pump_out, inner_loop):
    start_date = start.date()
    end_date = end.date()
    # 设置模拟的起始和终止时刻
    start_time = start.time()
    end_time = end.time()
    # 设置模拟的时间步长
    report_step = timedelta(seconds=time_step)
    report_step = str(report_step)
    # 将字符串格式化为00:00:00的格式
    report_step = report_step[-8:]

    inp = SwmmInput(str(in_filename))
    inp['OPTIONS']['START_DATE'] = start_date
    inp['OPTIONS']['START_TIME'] = start_time
    inp['OPTIONS']['REPORT_START_DATE'] = start_date
    inp['OPTIONS']['REPORT_START_TIME'] = start_time
    inp['OPTIONS']['END_DATE'] = end_date
    inp['OPTIONS']['END_TIME'] = end_time
    inp['OPTIONS']['REPORT_STEP'] = report_step
    if inner_loop == 0:
        inp['CONDUITS']['19'].to_node = 'Out'
    else:
        inp['CONDUITS']['19'].to_node = 'WSTJC'
        pump_in = 0.0
    for i in range(3):
        inp['CURVES']['PUMP_WS1'].points[i][1] = pump_1
        inp['CURVES']['PUMP_WS2'].points[i][1] = pump_2
        inp['CURVES']['PUMP_WS3'].points[i][1] = pump_3
        inp['CURVES']['PUMP_IN'].points[i][1] = pump_in
        inp['CURVES']['PUMP_OUT'].points[i][1] = pump_out

    inp.write_file(str(out_filename))

def swmm_run(data, time_set, step_hour, time_step, in_file):
    for j in range(len(data)):
        if j == 0:
            start_time = time_set
        else:
            start_time = end_time
        end_time = start_time + timedelta(hours=step_hour)
        pump_in = data.loc[j, 'PUMP_IN'] / 3600
        pump_out = data.loc[j, 'PUMP_OUT'] / 3600
        pump_1 = data.loc[j, 'PUMP_1'] / 3600
        pump_2 = data.loc[j, 'PUMP_2'] / 3600
        pump_3 = data.loc[j, 'PUMP_3'] / 3600
        inner_loop = int(data.loc[j, 'Inner_loop'])
        change_file = str('./swmm_inp/') + start_time.strftime('%Y-%m-%d_%H-%M-%S') + str('.inp')
        changed_file = str('./swmm_inp/') + end_time.strftime('%Y-%m-%d_%H-%M-%S') + str('.inp')
        in_hsf_file = str('./swmm_hsf/') + start_time.strftime('%Y-%m-%d_%H-%M-%S') + str('.hsf')
        out_hsf_file = str('./swmm_hsf/') + end_time.strftime('%Y-%m-%d_%H-%M-%S') + str('.hsf')
        rpt_file = str('./swmm_rpt/')
        out_file = str('./swmm_out/')
        if j == 0:
            change_file = in_file
        swmm_write(time_step=time_step, start=start_time, end=end_time, in_filename=change_file, out_filename=changed_file,
                   pump_1=pump_1, pump_2=pump_2, pump_3=pump_3, pump_out=pump_out, pump_in=pump_in, inner_loop=inner_loop)
        with pm.Simulation(changed_file) as sim:
            if j == 0:
                in_hsf_file = None
            else:
                sim.use_hotstart(in_hsf_file)
            for step in sim:
                while step.getCurrentSimulationTime() > end_time - timedelta(seconds=30):
                    sim.save_hotstart(out_hsf_file)
                    break
            sim.close()
        srcfile = changed_file.replace('.inp', '.out')
        dst_dir = out_file
        movefile(srcfile, dst_dir)  # 移动文件
        srcfile = changed_file.replace('.inp', '.rpt')
        dst_dir = rpt_file
        movefile(srcfile, dst_dir)  # 移动文件



