import cv2
import numpy as np
import time
import random

char_map = {
    1: 'a',  2: 'b',  3: 'c',  4: 'd',
    5: 'e',  6: 'f',  7: 'g',  8: 'h',
    9: 'i',  10: 'j', 11: 'k', 12: 'l',
    13: 'm', 14: 'n', 15: 'o', 16: 'p',
    17: 'q', 18: 'r', 19: 's', 20: 't',
    21: 'u', 22: 'v', 23: 'w', 24: 'x',
    25: 'y', 26: 'z', 27: 'A', 28: 'B',
    29: 'C', 30: 'D', 31: 'E', 32: 'F',
    33: 'G', 34: '0', 35: '1', 36: '2',
    37: '3', 38: '4', 39: '5', 40: '6',
    41: '7', 42: '8', 43: '9', 44: '?',
    45: '/', 46: '^', 47: '%', 48: '$',
    49: '@', 50: '!', 51: '<', 52: '>',
    53: '}', 54: ';', 55: '[', 56: ']',
    57: '-', 58: '_', 59: '+', 60: '=',
    61: ')', 62: '(', 63: '&', 0 : '#',
    64: 'H', 65: 'I', 66: 'J', 67 : 'K',
    68: 'M', 69: 'N', 70: 'O', 71: 'P',
    72: 'Q', 73: 'R', 74: 'S', 75: 'T',
    76: 'U', 77: 'V', 78: 'W', 79: 'X',
    80: 'Y', 81: 'Z', 83: 'L', 84: ',', 85: '>', 86: ':'
}


def logisticmap(image, x0):
    lb = 3.99
    logisticVal = np.empty(len(image[0])*len(image[0])+300)
    
    logisticVal[0] = x0
    for i in range(1, len(logisticVal)-1):
        logisticVal[i] = lb*logisticVal[i-1]*(1-logisticVal[i-1])
    logisticVal = logisticVal[300:]
    return logisticVal

def readImages():
    image = cv2.imread("saturn.png")
    image = cv2.resize(image, (512,512))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("saturn0.png",image)
    return image

def getX():
    seconds = time.time()
    rand = random.randint(2,5)
    rand = seconds * rand
    random.seed(rand)
    x = random.random()
    return x

def generatePassword(valArr):
    strPass = ""
    for i in range(len(valArr)):
        strPass += str(char_map.get(valArr[i]%87, '-'))


    strPass_part = ""
    file = open("passwords.txt", "a")
    for i in range(16):
        offset = i*16
        strPass_part = strPass[0+offset:16+offset]
        file.write(strPass_part + "\n")
        print(strPass_part)
    file.close
    

def imageProcess(image, logisticVal0, logisticVal1):
    new_image = image.copy()
    sum = 0
    valArr = []

    logisticVal0 = np.argsort(logisticVal0)    
    logisticVal1 = np.argsort(logisticVal1)   
    for x in range(len(image[0])):
        for y in range(len(image)):
            new_image[x][y] = image[(logisticVal0[y*x])%512][(logisticVal1[x])%512]
            sum += int(new_image[x][y])
        sum %= 512
        valArr.append(sum)
        sum = 0 

    generatePassword(valArr)
    cv2.imwrite("new_saturn.png", new_image)

def generate():
    image = readImages()
    x0 = getX()
    x1 = getX()

    logisticVal0 = logisticmap(image, x0)
    logisticVal1 = logisticmap(image, x1)
    imageProcess(image, logisticVal0, logisticVal1)

for _ in range(25):
    generate()
