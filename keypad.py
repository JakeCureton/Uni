import RPi.GPIO as GPIO
import Keypad      
ROWS = 4       
COLS = 4      
keys =  [   '1','2','3','A',    
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [12,16,18,22]        
colsPins = [19,15,13,11]       

def loop():
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    
    keypad.setDebounceTime(50)      
    while(True):
        key = keypad.getKey()       
        if(key != keypad.NULL):     
            print (key)
            
if __name__ == '__main__':    
    try:
        loop()
    except KeyboardInterrupt: 
        GPIO.cleanup()
        
        
#experiment with this 
'''
code=""
pin="45"

def keypadpin(key):
    global code 
    global pin
    code += key
    print(code)
    if (len(code) == len(pin)):
        if(code == pin):
            unlock()
        else:
            print("Invalid code")

keypad.registerKeyPressHandler(keypadpin)'''


#and this
'''from pad4pi import rpi_gpio

KEYPAD = [
        [   '1','2','3','A',    
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
]

ROW_PINS = [12,16,18,22] 
COL_PINS = [19, 15, 13, 11] 

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_4_by_4_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

def printKey(key):
    print(key)

keypad.registerKeyPressHandler(printKey)'''
