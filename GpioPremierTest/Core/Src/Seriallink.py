import serial
import time


PortAPinAvailable=[0, 1,2, 4, 5, 6, 7, 8, 9, 10, 11, 12,13, 14, 15]

PortBPinAvailable=[0, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15]

PortCPinAvailable=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

PortDPinAvailable=[0,1]

PortHPinAvailable=[0, 1]
#Lien série avec la carte

serialInst=serial.Serial('COM6',115200)

while True:
    CommandInput= input("Hello! Enter the desire command among these ones: PA_2 out, PA_2 in...")
    [PortAndPin, SpaceSeparator, Direction]=CommandInput.partition(' ')
    [PortLetter, DashSeparator, PinNumber] = PortAndPin.partition('_')
    



    #Conversion

    PinNumber = int(PinNumber)

    #Verification direction

    if (Direction == "in" or Direction == "out"):
        print("The direction entered correct.Proceed... ")



    #About the port and Pin Number

    if (PortLetter == "PA"):
        PortLetterCode=1

        print("Port détecté")

        if PinNumber in PortAPinAvailable:
            
            if(Direction == "out"):
                DirectionCode=1

                print("Pin Number and Port well detected, output version A")

            elif(Direction == "in"):
                DirectionCode=0
                print("Pin Number and Port well detected, input version A")

        else:
            print("The PinNumber does not exist for the port A")


    
    elif(PortLetter == "PB"):
        PortLetterCode=2

        if PinNumber in PortBPinAvailable:

            if(Direction == "out"):
                DirectionCode=1

            elif(Direction == "in"):
                DirectionCode=0


        else:
            print("The PinNumber does not exist for this port")

    
    elif(PortLetter == "PC"):

        PortLetterCode=3
        
        if PinNumber in PortCPinAvailable:

            if(Direction == "out"):
                DirectionCode=1

            elif(Direction == "in"):
                DirectionCode=0


        else:
            print("The PinNumber does not exist for this port")

        

    elif(PortLetter == "PD"):

        PortLetterCode=4
        if PinNumber in PortDPinAvailable:
            if(Direction == "out"):
                DirectionCode=1

            elif(Direction =="in"):
                DirectionCode=0


        else:
            print("The PinNumber does not exist for this port")


    
    else:
        PortLetterCode=-1 #erreur

    

    #Trame to send

    key_start_1=18

    key_start_1 = key_start_1.to_bytes(1,'big')
   
    PortLetterCode = PortLetterCode.to_bytes(1,'big')
    PinNumber = (int(PinNumber)).to_bytes(1,'big')
    DirectionCode = DirectionCode.to_bytes(1,'big')

    print(PinNumber)

    trame = key_start_1 + key_start_1 + PortLetterCode + PinNumber + DirectionCode

    print("The trame is: ",trame)

    serialInst.write(trame)
    serialInst.write(trame)
    


    time.sleep(20)

    serialInst.close()


