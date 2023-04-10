from flask import Flask
from flask import render_template
from flask import request
import json

app = Flask(__name__)

orderList = []
drinkList = ['Coca Cola (0.33L)', 'Fernandes (0.33L)', 'Fanta (0.33L)', 'Coca Cola Cherry (0.33L)', 'Amstel Radler 0.0 (0.33L)', 'Heineken 0.0 (0.33L)']

@app.route('/')
def main_Page():
    return render_template('index.html')

@app.route('/order_menu')
def order_Page():
    return render_template('orderscreen.html')

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
        
        orderList.pop(0)
        print(orderList)
        return json.dumps('received')

        

@app.route('/order_data', methods = ['POST'])
def order_data_proccessing():
    global orderList, drinkList

    receivedData = request.get_json()
    orderList.extend(receivedData['filteredOrderList'])

    while any(whileItem in orderList for whileItem in drinkList):
        for item in orderList:
            if item in drinkList:
                orderList.pop(orderList.index(item))
    
    print(orderList)
    return json.dumps('Received')
