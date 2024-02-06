from read_out import read_out
from Swmm_code import swmm_run
import pandas as pd
from datetime import datetime
import os

# 设置需要读取的节点
nodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '21',
         'Out', 'WSTJC', 'SOURCE', '20', 'WSMDC']
# 设置需要读取的管段
links = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', 'outpipe',
         '19', 'WS1', 'WS2', 'WS3', 'out_pump', '21', '20', 'weir1']
# 设置泵站运行曲线
data = pd.read_csv('curve.csv', encoding='gbk')
# 设置模拟的时间步长
time_step = 300  # 单位为秒
# 设置每一段swmm模拟时间
step_hour = 1    # 单位为小时
# 设置模拟的起始时间
time_set = datetime(2024, 2, 5, 0, 0, 0)
## 注意：需要保证每一段swmm模拟时间与泵站运行曲线的间隔一致！！
# 监测生成需要文件夹
if not os.path.exists('swmm_inp'):
    os.makedirs('swmm_inp')
if not os.path.exists('swmm_out'):
    os.makedirs('swmm_out')
if not os.path.exists('swmm_hsf'):
    os.makedirs('swmm_hsf')
if not os.path.exists('swmm_rpt'):
    os.makedirs('swmm_rpt')
# 自动由原始框架swmm文件生成按小时序列运行swmm文件
# swmm_run(data=data, time_set=time_set, step_hour=step_hour, time_step=time_step, in_file='v1.inp')
# 读取数据并用plotly绘图
read_out(nodes=nodes, links=links)
