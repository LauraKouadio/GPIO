import serial
import time


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
                print("Pin Number and Port well detected, input version")

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
        
        if((self.pinNum in PortAPinAvailable) or (self.pinNum in PortBPinAvailable) or (self.pinNum in PortCPinAvailable) or (self.pinNum in PortDPinAvailable)):
            print("Okay")
        else:
            
            self.Message="Error, the pin number is incorrect."


    def Prepare_trame(self):
        key_start_1=18
        key_start_1 = key_start_1.to_bytes(1,'big')

        PinNumber = (CurrentPort.pinNum).to_bytes(1,'big')
        Direction = (CurrentPort.Direction).to_bytes(1,'big')
        PortLetterCode = (CurrentPort.PortLetterCode).to_bytes(1,'big')

        self.Trame = key_start_1 + key_start_1  + PinNumber+ Direction + PortLetterCode 
        #return(trame) 



            
#Lien série avec la carte

serialInst=serial.Serial('COM6',115200)

while True:
    CommandInput= input("""Hello! Enter the desire command among these ones:\n 
- io.PortLetter.CurrentPort.pinNumber.CurrentPort.modeOrState=out - io.PortLetter.CurrentPort.pinNumber.CurrentPort.modeOrState=in to set the CurrentPort.modeOrState of the pin.\n
- io.PortLetter.CurrentPort.pinNumber.Value=on - io.PortLetter.CurrentPort.pinNumber.Value=off to set the value of the pin (High=1 ou Low=0).\n
- io.PortLetter.CurrentPort.pinNumber.val? to read the value of the pin\n""") 
    
    CurrentPort = PortConfiguration()

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


#Current Port Handle

    if(CurrentPort.type == "io"):
        CurrentPort.Handle_PortLetter()
        CurrentPort.Handle_PinNumber()
        CurrentPort.Handle_modeOrState()

        print("The message is:",CurrentPort.Message)

        
        match(CurrentPort.Message):
            case 'Ready to send':

                CurrentPort.Prepare_trame()
                print(CurrentPort.Trame)
                serialInst.write(CurrentPort.Trame)
                time.sleep(5)
                if(CurrentPort.Direction==4):
                    print("Waiting for something to arrive...")
                    packet = serialInst.readline()
                    print(packet)

            case("Error, the Direction is incorrect."):
                print(CurrentPort.Message)
            
            case("Error, the port letter is incorrect."):
                print(CurrentPort.Message)
            
            case("Error, the pin number is incorrect."):
                print(CurrentPort.Message)
            case default:
                print("No match found")

        

serialInst.close()


