from flask import Flask
from flask import render_template
from flask import request
import json

app = Flask(__name__)

orderList = []

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

        for i in range(len(orderList) - 1):
            orderList[i] = orderList[i + 1]

        orderList = orderList[:-1]
        return json.dumps('received')
        print(orderList)

        

@app.route('/order_data', methods = ['POST'])
def order_data_proccessing():
    global orderList

    receivedData = request.get_json()
    orderList.extend(receivedData['filteredOrderList'])
    
    print(orderList)
    return json.dumps('Received')
