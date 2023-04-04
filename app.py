from flask import Flask
from flask import render_template
from flask import request
import json

app = Flask(__name__)

order_list = ["red", "blue", "yellow"]

@app.route('/')
def Main_Page():
    return render_template('index.html')

@app.route('/oven', methods = ['POST'])
def arduino_contact():
    global order_list
    if request.get_json() == 'check_list':
        print("Connected")
        if len(order_list) >= 1:
            return json.dumps(True)
        
        else:
            return json.dumps(False)
        print(len(order_list))
    elif request.get_json() == 'pizza_done':
        order_list.pop(0)

        for i in range(len(order_list) - 1):
            order_list[i] = order_list[i + 1]

        order_list = order_list[:-1]
        
    