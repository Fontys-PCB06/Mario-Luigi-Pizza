from flask import Flask
from flask import render_template
from flask import request
import json

app = Flask(__name__)

orderList = ["red", "blue", "yellow", "wasd", "a", "r"]

@app.route('/')
def Main_Page():
    return render_template('index.html')

@app.route('/oven', methods = ['POST'])
def arduino_contact():
    global orderList
    if request.get_json() == 'check_list':
        print("Connected ", orderList)
        if len(orderList) >= 1:
            return json.dumps(True)
        
        else:
            return json.dumps(False)        
    
    elif request.get_json() == 'pizza_done':
        #orderList.pop(0)

        for i in range(len(orderList) - 1):
            orderList[i] = orderList[i + 1]

        orderList = orderList[:-1]
        return json.dumps('received')
        

@app.route('/order_data', methods = ['POST'])
def order_data_proccessing():
    global orderList
    tempOrderList = []

    tempOrderList = request.get_json()
    for pizza in tempOrderList:
        orderList.append(pizza)
    
