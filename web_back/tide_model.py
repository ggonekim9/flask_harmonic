import time
import math
import ttide as tt
import pandas as pd
import numpy as np

def read_tidelevle(path):

    frame = pd.read_excel(path,usecols=[0,1,2])
    datat = frame.values
    return datat;

def get_mean_waterlevel_hour(datat):

    return ;

def harmonic_analysis(mean_waterlevel_hour):

    return ;

def interpolation(datat):
    timet = []
    watert = []
    t2014 = "2014-01-01 00:00:00"
    t2014y = time.strptime(t2014, "%Y-%m-%d %H:%M:%S")  # 转时间元组
    t2014ym = time.mktime(t2014y)  # 转时间戳
    for i in range(0, len(datat)):
        time1 = str(datat[i][0])
        time2 = str(datat[i][2])
        time3 = time1[:11] + time2
        date_time = time.strptime(time3, "%Y-%m-%d %H:%M:%S")  # 转时间元组
        timeStamp = time.mktime(date_time)  # 转时间戳
        timet.append((timeStamp - t2014ym) / 60 / 60);  # 转为小时
        watert.append(datat[i][1])
    length = len(datat)
    x1 = timet
    y1 = watert
    x2 = np.linspace(0, 365 * 24, 365 * 24)
    y2 = []
    flag = 1
    for j in range(0, len(x2)):
        for t in range(1, length):
            if (x2[j] < x1[t]):
                flag = t
                break
        tem = function_interpolation(x1[flag - 1], x1[flag], y1[flag - 1], y1[flag], x2[j]);
        y2.append(tem)
    # plt.plot(x1, y1, '+', x2, y2, 'r')
    # plt.xlim(0, 200)
    # plt.show();
    return y2

# 正弦波插值
def function_interpolation(x1,x2,y1,y2,x):
    if(y1<y2):
        q=1
    else:
        q=0
    y = (abs(y1-y2)/2)*math.sin(math.pi*(x-x1)/(x2-x1)+(0.5+q)*math.pi)+(y1+y2)/2
    return y

if __name__ == '__main__':

    path_t = 'baozhen.xlsx'
    datat = read_tidelevle(path_t)
    data_hour = interpolation(datat) # 高低潮数据插值为逐时水位
    points = np.array(data_hour, dtype=np.float32) # 列表转数组
    # temp = np.array([1,2,5,34,456,45,6,4])
    tfit_e = tt.t_tide(points)
    tide_out = tfit_e['xout']
    # x1 = range(0,tide_out.shape[0])
    # y1 = tuple(map(tuple, tide_out))
    # plt.plot(x1, y1, color='red', linestyle="-.", label='data')
    # plt.show();

