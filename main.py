from Display import *
from random import randint as rng
from time import time
from time import sleep as wait
from Logger import *

class Chip8:
    def __init__(self):
        self.memory = bytearray(0xfff)
        self.PC = 0x200
        self.Register = [0]*0x10
        self.I = 0x00
        self.TimeR = 0
        self.DelayR = 0
        
        self.Display = Display()
        
        self.Stack = []
        self.SP = -1


        self.targetTime = time()
        
        fonts = [ 
        0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
        0x20, 0x60, 0x20, 0x20, 0x70, # 1
        0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
        0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
        0x90, 0x90, 0xF0, 0x10, 0x10, # 4
        0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
        0xF0, 0x10, 0x20, 0x40, 0x40, # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90, # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
        0xF0, 0x80, 0x80, 0x80, 0xF0, # C
        0xE0, 0x90, 0x90, 0x90, 0xE0, # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
        0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]
        self.Load(fonts,start=0)

    def Main(self):
        while self.PC < 0x1000:
            #self.Display.ArrayOfKeys #list of keys

            #print(hex((self.memory[self.PC] << 8) | self.memory[self.PC + 1]))
            self.Opsecute((self.memory[self.PC] << 8) | self.memory[self.PC + 1])
            self.Display.update()
            self.PC += 2
            self.Restrict()
            

            if self.targetTime < time():
                self.DelayR -= 1
                self.DelayR = 0 if self.DelayR < 0 else self.DelayR
                self.targetTime = time()+(1/60)
            wait(1/500)
        print("Over")
        self.Display.canvas.mainloop()

    def Load(self,array,start=0x200):
        self.memory[start:start+len(array)-1]=array

    def Opsecute(self,Instruction):
        Command = f"{hex(Instruction)[2:]:0>4}"
        #output(f"{self.PC:>4} : {Command} : {self.Register}  {self.I} ")
        if Command[0:4] == "00e0": #0x0
            self.Display.cls()
        elif Command[0:4] == "00ee":#0x0
            self.PC = self.Stack.pop()

        
        elif Command[0] == "1":#0x1
            self.PC = int(f"0x{Command[1:]}",base=16) - 2
            
        elif Command[0] == "2":#0x2
            self.SP +=1
            self.Stack.append(self.PC) 
            self.PC = int(f"0x{Command[1:]}",base=16) - 2
        
        elif Command[0] == "3":#0x3
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB23 =  int(f"0x{Command[2:4]}",base=16)
            if self.Register[operandB1] == operandB23:
                self.PC += 2
        elif Command[0] == "4":#0x4
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB23 =  int(f"0x{Command[2:4]}",base=16)
            if self.Register[operandB1] != operandB23:
                self.PC += 2
        elif (Command[0],Command[3]) == ("5","0"):#0x5
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 =  int(f"0x{Command[2]}",base=16)
            if self.Register[operandB1] == self.Register[operandB2]:
                self.PC += 2
                
        elif Command[0] == "6":#0x6
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB23 =  int(f"0x{Command[2:4]}",base=16)
            self.Register[operandB1] = operandB23
            
        elif Command[0] == "7":#0x7
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB23 =  int(f"0x{Command[2:4]}",base=16)
            self.Register[operandB1] += operandB23
            
        elif (Command[0],Command[3]) == ("8","0"):#0x8xx0
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 =  int(f"0x{Command[2]}",base=16)
            self.Register[operandB1] = self.Register[operandB2]
        
        elif (Command[0],Command[3]) == ("8","1"):#0x8xx1
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 =  int(f"0x{Command[2]}",base=16)
            self.Register[operandB1] |= self.Register[operandB2]
            
        elif (Command[0],Command[3]) == ("8","2"):#0x8xx2
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 =  int(f"0x{Command[2]}",base=16)
            self.Register[operandB1] &= self.Register[operandB2]
            
        elif (Command[0],Command[3]) == ("8","3"):#0x8xx3
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 =  int(f"0x{Command[2]}",base=16)
            self.Register[operandB1] ^= self.Register[operandB2]
            
        elif (Command[0],Command[3]) == ("8","4"):#0x8xx4
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 =  int(f"0x{Command[2]}",base=16)
            
            value = self.Register[operandB1] + self.Register[operandB2]
            overflow = (value & 0b1_0000_0000)>>8
            value &= 0b1111_1111
            self.Register[0xf],self.Register[operandB1] = overflow,value
            
        elif (Command[0],Command[3]) == ("8","5"):#0x8xx5
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 =  int(f"0x{Command[2]}",base=16)
            
            value = abs(self.Register[operandB1] - self.Register[operandB2])
            overflow = self.Register[operandB1] > self.Register[operandB2]
            self.Register[0xf],self.Register[operandB1] = overflow,value
            
        elif (Command[0],Command[3]) == ("8","6"):#0x8xx6
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 =  int(f"0x{Command[2]}",base=16)
            
            if self.Register[operandB1]:
                self.Register[0xf] = 1
            else:
                self.Register[0xf] = 0
                self.Register[operandB1]>>=1
        
        elif (Command[0],Command[3]) == ("8","7"):#0x8xx7
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 =  int(f"0x{Command[2]}",base=16)
            
            value = abs(self.Register[operandB1] - self.Register[operandB2])
            overflow = self.Register[operandB1] < self.Register[operandB2]
            self.Register[0xf],self.Register[operandB1] = overflow,value
        
        elif (Command[0],Command[3]) == ("8","e"):#0x8xxe
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 = int(f"0x{Command[2]}",base=16)
            
            if (self.Register[operandB1] >> 16) & 0b1:
                self.Register[0xf] = 1
            else:
                self.Register[0xf] = 0
                self.Register[operandB1]<<=1
                
        elif (Command[0],Command[3]) == ("9","0"):#0x9
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 = int(f"0x{Command[2]}",base=16)
            
            if self.Register[operandB1] != self.Register[operandB2]:
                self.PC +=2
        
        elif Command[0] == "a":#0xa
            operandB123 =  int(f"0x{Command[1:4]}",base=16)
            self.I = operandB123

        elif Command[0] == "b":#0xb
            operandB123 =  int(f"0x{Command[1:4]}",base=16)
            self.PC = ((self.Register[0]+operandB123)&0b1111111111111111)

        elif Command[0] == "c":#0xc
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB23 = int(f"0x{Command[2:4]}",base=16)

            self.Register[operandB1] = rng(0,255)&operandB23

        elif Command[0] == "d":#0xd
            operandB1 =  int(f"0x{Command[1]}",base=16)
            operandB2 = int(f"0x{Command[2]}",base=16)
            operandB3 = int(f"0x{Command[3]}",base=16)


            self.Register[0xf] = self.Display.sprite(self.Register[operandB1],
                                self.Register[operandB2],
                                self.memory[self.I:self.I+operandB3])
            

        
        elif (Command[0],Command[2:4]) == ("e","9e"):#0xe           keybard
            operandB1 =  int(f"0x{Command[1]}",base=16)
            if self.Display.ArrayOfKeys[self.Register[operandB1]] == 1:
                self.PC += 2
                #print(f"== {self.Display.ArrayOfKeys[operandB1]}")
            
        elif (Command[0],Command[2:4]) == ("e","a1"):#0xe           keybard
            operandB1 =  int(f"0x{Command[1]}",base=16)
            if self.Display.ArrayOfKeys[self.Register[operandB1]] != 1:
                self.PC += 2
                #print(f"!= {self.Display.ArrayOfKeys[operandB1]}")

        elif Command[0] == "f":#0xf
            operandB1 =  int(f"0x{Command[1]}",base=16)
            if Command[2:4] == "07":
                self.Register[operandB1] = self.DelayR
            elif Command[2:4] == "0a": #0xfx0a                      keybard
                input = False
                while not input:
                    # Check for any key pressed (True in ArrayOfKeys)
                    if True in self.Display.ArrayOfKeys:
                        KeyDown = self.Display.ArrayOfKeys.index(True)  # Get the index of the first True value
                        self.Register[operandB1] = KeyDown  # Assign the key index to the register
                        input = True  # Set input to True to exit the loop

            elif Command[2:4] == "15":#0xfx15
                self.DelayR = self.Register[operandB1]
            elif Command[2:4] == "18":#0xfx18
                self.TimeR = self.Register[operandB1]
            elif Command[2:4] == "1e":#0xfx1e
                self.I += self.Register[operandB1]
            elif Command[2:4] == "29":#0xfx29
                self.I = (self.Register[operandB1]*5)
            elif Command[2:4] == "33":#0xfx33
                vx_value = self.Register[operandB1]
                self.memory[self.I] = vx_value // 100                 # Hundreds digit
                self.memory[self.I + 1] = (vx_value // 10) % 10       # Tens digit
                self.memory[self.I + 2] = vx_value % 10               # Ones digit
            elif Command[2:4] == "55":#0xfx55
                for Reg in range(operandB1):
                    self.memory[self.I + Reg] = self.Register[Reg]
            elif Command[2:4] == "65":#0xfx65
                for Reg in range(operandB1):
                    self.Register[Reg] = self.memory[self.I + Reg]
    
    def Restrict(self):
        """ The goal of this function is to keep the registers and 
        other stuff to the hardware's restrictions 
        like no negative numbers or numbers that are 16 bit cant go over 0xffff"""

        self.Register = [self.Register[i]%256 for i in range(16)] # 8 bit register
        if len(self.Stack)> 16:
            self.Stack.pop()


def file_to_byte_array(file_path):
    with open(file_path, 'rb') as file:
        byte_array = list(file.read())
    return byte_array
            
                
if __name__ == "__main__":
    wipeLog()
    test = Chip8()

    test.Load(file_to_byte_array("ROMs/SpaceInvaders.ch8"))
    test.Main()