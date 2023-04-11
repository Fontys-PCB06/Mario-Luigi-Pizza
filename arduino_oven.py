import sys, requests, time, json
from fhict_cb_01.CustomPymata4 import CustomPymata4

BUTTONPIN = 9
LED_PINS = [4,5,6,7]
TIMER = 5 # change cook time and last seconds time

url = 'http://localhost:5000/oven'
buttonLevel = 1
buttonPrevLevel = 1

def Button_Changed(data):
    global buttonLevel
    buttonLevel = data[2]

def setup():
    global board
    board = CustomPymata4(com_port = '/dev/ttyUSB0')
    board.displayOn()
    board.set_pin_mode_digital_input_pullup(BUTTONPIN, callback = Button_Changed)
    for pin in LED_PINS:
        board.set_pin_mode_digital_output(pin)


def loop():
    global buttonPrevLevel
    isAvailable = False
    board.digital_pin_write(5, 0)

    response = requests.post(url, json = 'check_list')
    if response.status_code == 200 :
        isAvailable = json.loads(response.content)
        print("OK")

        if isAvailable :
            buttonPrevLevel = 1
            print(buttonLevel)

            board.digital_pin_write(6, 1)
            while buttonPrevLevel == 1:
                if (buttonPrevLevel != buttonLevel):
                    buttonPrevLevel = buttonLevel
                time.sleep(0.1)

            board.digital_pin_write(6, 0)

            for i in range(TIMER, -1, -1):
                board.digital_pin_write(4, 1)
                if i <= 2: # CHANGE 2S TO 30S AFTER CHANGING TIMER
                    board.digital_pin_write(4, 0)
                    board.digital_pin_write(7, 1)
                board.displayShow(i)
                time.sleep(1) 
            board.digital_pin_write(7, 0)
            
            response = requests.post(url, json = 'pizza_done')
            if json.loads(response.content) == 'received':
                board.digital_pin_write(5, 1)
                time.sleep(1)


setup()
while True:
    try:
        loop()
    except KeyboardInterrupt:
        print(' Shuttting down')
        board.shutdown()
        sys.exit(0)
