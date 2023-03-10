import serial
import time

#################################################################################################   STM32F103XX GPIO Driver ###########################################################################################
# 
# This driver allows the user to control the I/O, following a simple protocol.
#   - The user enters a simple command
#   - According to the command which has been entered, an instance of the class PortConfiguration is created and configured with the method PortConfig.
#   - The methods Handle_modeOrState, Handle_PortLetter and Handle_PinNumber encode the configuration.
#   - Unless an error has been detected, the method Prepare_trame will prepare a trame corresponding to the input command and send it to the STM32 board.
#   - The STM32 will send back a message to confirm that the command has been executed properly. 
# #

PortAPinAvailable=[0, 1,2 , 4, 5, 6, 7, 8, 9, 10, 11, 12,13, 14, 15]
PortBPinAvailable=[0, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15]
PortCPinAvailable=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
PortDPinAvailable=[2]
PortHPinAvailable=[0, 1]


class PortConfiguration:
    "Définition de la configuration du port."

    def __init__(self):
        self.Direction =0
        self.PortLetterCode=0
        self.Trame=0
        self.Message ='Ready to send'
        self.Receive=[0,0,0,0,0]

    def Handle_modeOrState(self):

        match(self.modeOrState):
            case "in":
                self.Direction=0
                
            case "out":
                self.Direction=1
                
            case "on":
                self.Direction=2

            case "off":
                self.Direction=3

            case "?":
                self.Direction=4
                

            case default:
                self.Direction=-1
                self.Message= "Error, the Direction is incorrect."
        
    def Handle_PortLetter(self):

        match(self.portLetter):
            case 'A':
                self.PortLetterCode=1
            case 'B':
                self.PortLetterCode=2
            case 'C':
                self.PortLetterCode=3
            case 'D':
                self.PortLetterCode=4

            case default:
                self.PortLetterCode=-1
                self.Message="Error, the port letter is incorrect."



    def Handle_PinNumber(self):

        self.pinNum = int(self.pinNum)

        match(self.PortLetterCode):
            case 1:
                if(self.pinNum in PortAPinAvailable):
                    print("Okay port A")
                else:
                    self.Message='Error the pin number is incorrect.'
            case 2:
                if(self.pinNum in PortBPinAvailable):
                    print("Okay port B")
                else:
                    self.Message='Error the pin number is incorrect.'

            case 3:
                if(self.pinNum in PortCPinAvailable):
                    print("Okay port C")
                else:
                    self.Message='Error the pin number is incorrect.'

            case 4:
                if (self.pinNum in PortDPinAvailable):
                    print("Okay pour port D")
                else:
                    self.Message='Error the pin number is incorrect.'
            
            case default:
                self.Message='Error the port letter code is incorrect.'
        


    def Prepare_trame(self):
        key_start_1=18
        key_start_1 = key_start_1.to_bytes(1,'big')

        PinNumber = (CurrentPort.pinNum).to_bytes(1,'big')
        Direction = (CurrentPort.Direction).to_bytes(1,'big')
        PortLetterCode = (CurrentPort.PortLetterCode).to_bytes(1,'big')

        self.Trame = key_start_1 + key_start_1  + PinNumber+ Direction + PortLetterCode 
        #return(trame) 

    def Decode_received(self):
        packet = serialInst.readline()
        
        CurrentPort.Receive[0]=ord((packet.decode("utf-8"))[0])
        CurrentPort.Receive[1]=ord((packet.decode("utf-8"))[1])
        CurrentPort.Receive[2]=ord((packet.decode("utf-8"))[2])
        CurrentPort.Receive[3]=ord((packet.decode("utf-8"))[3])
        CurrentPort.Receive[4]=ord((packet.decode("utf-8"))[4])

        match(CurrentPort.Receive):
            case [0,0,0,0,0]:
                print("This GPIO is in mode INPUT. Its value is equal to 0.")
            case [0,0,0,0,1]:
                print("This GPIO is in mode OUTPUT PUSH PULL. Its value is equal to 0.")
            case [1,0,0,0,1]:
                print("This GPIO is in mode OUTPUT PUSH PULL. Its value is equal to 1.")

            case [3,3,3,3,3]:
                print("You are trying to set the value 'ON' or 'OFF' to a GPIO which is not in output mode. Turn the mode to output mode and try again.")
            
            case [1,1,0,0,0]:
                print("This GPIO is in mode Input pull up pull down with a value equal to 1.")

            case [0,1,0,0,0]:
                print("This GPIO is in mode Input pull up pull down with a value equal to 0.")


        print(CurrentPort.Receive)

    def PortConfig(self,CommandInput):
        [Type,PointSeparator,Remain] = CommandInput.partition('.')
        [PortLetter,PointSeparator,Remain] = Remain.partition('.')
        [PinNumber,PointSeparator,Remain]=Remain.partition('.')
        [Action,EqualSeparator,ModeOrState] = Remain.partition('=')


        if(Action =="val?"):
            
            [Action,QuestionSeparator,Void] = Action.partition('?')   
            CurrentPort.type = Type
            CurrentPort.portLetter=PortLetter
            CurrentPort.pinNum=PinNumber
            CurrentPort.action=Action
            CurrentPort.modeOrState= QuestionSeparator


        else:
            CurrentPort.type = Type
            CurrentPort.portLetter=PortLetter
            CurrentPort.pinNum=PinNumber
            CurrentPort.action=Action
            CurrentPort.modeOrState= ModeOrState




            
#Lien série avec la carte

serialInst=serial.Serial('COM6',115200)
serialInst.timeout =1

while True:
    CommandInput= input("""Hello! Enter the desire command among these ones:\n 
- io.PortLetter.pinNumber.dir=out - io.PortLetter.pinNumber.dir=in to set the CurrentPort.modeOrState of the pin.\n
- io.PortLetter.pinNumber.val=on - io.PortLetter.pinNumber.val=off to set the value of the pin (High=1 ou Low=0).\n
- io.PortLetter.pinNumber.val? to read the value of the pin\n""") 
    
    CurrentPort = PortConfiguration()
    CurrentPort.PortConfig(CommandInput)


#Current Port Handle

    if(CurrentPort.type == "io"):
        CurrentPort.Handle_PortLetter()
        CurrentPort.Handle_PinNumber()
        CurrentPort.Handle_modeOrState()
        
        match(CurrentPort.Message):
            case 'Ready to send':

                CurrentPort.Prepare_trame()
                print(CurrentPort.Trame)
                serialInst.write(CurrentPort.Trame)
                time.sleep(1)

                if(CurrentPort.Direction==4):
                    print("Waiting for something to arrive...")
                    CurrentPort.Decode_received()

                elif(CurrentPort.Direction==2):
                    print("Waiting for something to arrive...")
                    CurrentPort.Decode_received()

                elif(CurrentPort.Direction==3):
                    print("Waiting for something to arrive...")
                    CurrentPort.Decode_received()
                    
            case("Error, the Direction is incorrect."):
                print(CurrentPort.Message)
            
            case("Error, the port letter is incorrect."):
                print(CurrentPort.Message)
            
            case('Error the pin number is incorrect.'):
                print(CurrentPort.Message)
            case default:
                print("No match found")

        

serialInst.close()


