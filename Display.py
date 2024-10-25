import tkinter as tk

class Display():
    def __init__(self,px:int=64,py:int=32,width:int= 640,outline:int = 0, name:str = "Display"):
        self.root = tk.Tk()
        self.SqrSize = width//px

        self.px = px
        self.py = py

        self.canvas = tk.Canvas(self.root, width = (px * self.SqrSize), height = (py * self.SqrSize))
        self.canvas.pack()


        self.ArrayOfKeys = [False]*16
        self.root.bind("<KeyPress>", self.getKeysD)
        self.root.bind("<KeyRelease>", self.getKeysU)
            
        self.PixelGrid = []
        self.root.title(name)
        self.PixelState = [0]*px*py
        self.PreviousState = [0]*px*py
        for i in range(px*py):
            self.PixelGrid.append(self.canvas.create_rectangle((i%px)*self.SqrSize, #x1
                                                               (i//px)*self.SqrSize,#y1
                                                               
                                                               ((i)%px)*self.SqrSize + self.SqrSize, #x2
                                                               ((i)//px)*self.SqrSize + self.SqrSize,#y2

                                                               fill=("#000000"),
                                                               width = outline))
            
        
        #self.update()

    

    def setColor(self,xy,color): #x + (y * xres) this is a little faster and cleaner
        self.canvas.itemconfig(self.PixelGrid[xy],fill = "#FFFFFF"if color else "#000000")

    def square(self,x1,y1,x2,y2,color):
        for y in range(y1,y2):
            for x in range(x1,x2):
                self.setColor(self.To1d(x,y),color)
        

    def To1d(self,x,y):
        return(((self.px * y) + (x % self.px)) % (self.py*self.px))

    def _from_rgb(self,rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb
    
    def fill(self,x1,y1   ,x2,y2):
        outOfRange = 0
        for y in range(y1,y2,1):
            for x in range(y1,x2,1):
                self.PixelState[self.To1d(x,y)] = not self.PixelState[self.To1d(x,y)]
                if not self.PixelState[self.To1d(x,y)]:
                    outOfRange = 1
        return outOfRange
    


    def cls(self):
        for i in range(self.px*self.py):
            self.PixelState[i] = 0

    def sprite(self, x, y, data):
        collision = 0
        for row_index, byte in enumerate(data):  # each row of sprite data
            for bit_index in range(8):  # each bit in the byte
                # Calculate the current pixel position, wrap-around enabled
                pixel_x = (x + bit_index) % self.px
                pixel_y = (y + row_index) % self.py
                pixel_index = self.To1d(pixel_x, pixel_y)

                checkingOutSize = ((x + bit_index) >= self.px or (y + row_index) >= self.py  or  (x + bit_index) < 0 or (x + bit_index)<0)
                drawing = (byte >> (7 - bit_index)) & 1
                #print(drawing,checkingOutSize)
                if drawing and checkingOutSize:
                    #print("Offscreen")
                    collision = 1
                
                # Determine if the pixel will toggle and set collision
                if self.PixelState[pixel_index] == 1 and ((byte >> (7 - bit_index)) & 1):
                    collision = 1
                
                # Toggle the pixel
                self.PixelState[pixel_index] ^= (byte >> (7 - bit_index)) & 1
        
        return collision

            
    def update(self):#send a request to update display

        for i in range(self.px*self.py):
            #print(f"{self.PreviousState[i]}:{self.PixelState[i]}   {self.PreviousState[i] != self.PixelState[i]}")
            if self.PreviousState[i] != self.PixelState[i]:
                self.setColor(i,self.PixelState[i])
                self.PreviousState[i] = self.PixelState[i]
            
        self.root.update()
        
    def getKeysD(self,event):
        if event.keysym == "1":
            self.ArrayOfKeys[0] = True
        elif event.keysym == "2":
            self.ArrayOfKeys[1] = True
        elif event.keysym == "3":
            self.ArrayOfKeys[2] = True
        elif event.keysym == "4":
            self.ArrayOfKeys[3] = True
        elif event.keysym == "q":
            self.ArrayOfKeys[4] = True
        elif event.keysym == "w":
            self.ArrayOfKeys[5] = True
        elif event.keysym == "e":
            self.ArrayOfKeys[6] = True
        elif event.keysym == "r":
            self.ArrayOfKeys[7] = True
        elif event.keysym == "a":
            self.ArrayOfKeys[8] = True
        elif event.keysym == "s":
            self.ArrayOfKeys[9] = True
        elif event.keysym == "d":
            self.ArrayOfKeys[10] = True
        elif event.keysym == "f":
            self.ArrayOfKeys[11] = True
        elif event.keysym == "z":
            self.ArrayOfKeys[12] = True
        elif event.keysym == "x":
            self.ArrayOfKeys[13] = True
        elif event.keysym == "c":
            self.ArrayOfKeys[14] = True
        elif event.keysym == "v":
            self.ArrayOfKeys[15] = True

    def getKeysU(self,event):
        if event.keysym == "1":
            self.ArrayOfKeys[0] = False
        elif event.keysym == "2":
            self.ArrayOfKeys[1] = False
        elif event.keysym == "3":
            self.ArrayOfKeys[2] = False
        elif event.keysym == "4":
            self.ArrayOfKeys[3] = False
        elif event.keysym == "q":
            self.ArrayOfKeys[4] = False
        elif event.keysym == "w":
            self.ArrayOfKeys[5] = False
        elif event.keysym == "e":
            self.ArrayOfKeys[6] = False
        elif event.keysym == "r":
            self.ArrayOfKeys[7] = False
        elif event.keysym == "a":
            self.ArrayOfKeys[8] = False
        elif event.keysym == "s":
            self.ArrayOfKeys[9] = False
        elif event.keysym == "d":
            self.ArrayOfKeys[10] = False
        elif event.keysym == "f":
            self.ArrayOfKeys[11] = False
        elif event.keysym == "z":
            self.ArrayOfKeys[12] = False
        elif event.keysym == "x":
            self.ArrayOfKeys[13] = False
        elif event.keysym == "c":
            self.ArrayOfKeys[14] = False
        elif event.keysym == "v":
            self.ArrayOfKeys[15] = False





if __name__ =="__main__":
    screen = Display()


    # Example sprite data (a 5-byte sprite)
    sprite_data = [0b11110000, 0b10010000, 0b10010000, 0b10010000, 0b11110000]

    # Draw the sprite at position (10, 5)
    print(screen.sprite(60, 27, sprite_data))

    while True:
        screen.update()
        print(screen.ArrayOfKeys)


    
