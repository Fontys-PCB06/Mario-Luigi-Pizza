import sys, requests, time, json
from fhict_cb_01.CustomPymata4 import CustomPymata4

BUTTONPIN = 9
LED_PINS = [4, 5, 6, 7]

url = 'http://localhost:5000/check_list'
buttonLevel = 0

def Button_Changed(data):
    global level
    level = data[2]

def setup():
    global board
    board = CustomPymata4(com_port = 'COM4')
    board.displayOn()
    board.set_pin_mode_digital_input_pullup(BUTTONPIN, callback = Button_Changed)

    for pin in LED_PINS:
        board.set_pin_mode_digital_input(pin)


def loop():
    isAvailable = False

    response = requests.post(url, json = 'check_list')
    if response.status_code == 200 :
        isAvailable = json.loads(response.content)

        if isAvailable :
            while buttonLevel == 1:
                board.digital_pin_write(LED_PINS[1], 1)
                time.sleep(0.5)

            for i in range(260, -1, -1):
                board.displayShow(i)
                time.sleep(1) 
            
            response = requests.post(url, json = 'pizza_done')


setup()
while True:
    try:
        loop()
    except KeyboardInterrupt:
        print(' Shuttting down')
        board.shutdown()
        sys.exit(0)