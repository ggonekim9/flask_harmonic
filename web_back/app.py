import numpy as np
from flask import Flask, render_template, request, jsonify
from wl_model import wl_model
import ttide as ttide
import json

app = Flask(__name__)

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

@app.route('/waterLevel',methods = ['POST', 'GET'])
def mean_water_level():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data)
        head_q = json_data.get("head_q")
        foot_r = json_data.get("foot_r")
        wl_day = json_data.get("wl_day")
        param = wl_model.t_q_res(head_q,wl_day,foot_r)
        dic_t = {'org':'org'}
        dic_t['Costant'] = param.tolist()[0]
        dic_t['Q'] = param.tolist()[1]
        dic_t['Q2'] = param.tolist()[2]
        dic_t['R'] = param.tolist()[3]
        print(dic_t)
        return jsonify(dic_t)
    else:
        return 'error'

@app.route('/fitting',methods = ['POST', 'GET'])
def tide_fit():
    if request.method == 'POST':
        # 获取前端json数据
        # request.get_data()获取字符串，json.loads()转化为json
        data = request.get_data()
        # print(data)
        json_data = json.loads(data)
        # print(json_data)
        wl_hour = json_data.get("water")
        # print(type(np.array(wl_hour)))
        wl_hour = np.array(wl_hour)
        tfit_e = ttide.t_tide(wl_hour)
        tide_out = tfit_e['xout'].tolist()

        # 给前端传输json数据
        dic = {'org':'org'} # 创建字典
        if(tide_out[0][0]=='nan'):
            print(tide_out)
            dic['water'] = tide_out
        return jsonify(dic)
    else:
        return 'error'


@app.route('/login', methods=['POST'])
def login():
    # 获取前端json数据
    # request.get_data()获取字符串，json.loads()转化为json
    data = request.get_data()
    print(data)
    json_data = json.loads(data)
    print(json_data)

    Id = json_data.get("userId")
    password = json_data.get("password")
    print("userId is " + Id)
    print("password is " + password)

    # 给前端传输json数据
    info = dict()   # 创建字典
    info['status'] = 'success'
    return jsonify(info)

if __name__ == '__main__':
    #默认为5000端口
    # app.run()
    app.run(port=8000)

