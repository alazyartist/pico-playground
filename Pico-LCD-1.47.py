
from machine import Pin,SPI,PWM
import framebuf
import time
import os

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch47(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 320
        self.height = 172
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.RED   =   0x07E0
        self.GREEN =   0x001f
        self.BLUE  =   0xf800
        self.WHITE =   0xffff
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x13)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xF0)
        self.write_data(0x00)
        self.write_data(0x04)
        self.write_data(0x04)
        self.write_data(0x05)
        self.write_data(0x29)
        self.write_data(0x33)
        self.write_data(0x3E)
        self.write_data(0x38)
        self.write_data(0x12)
        self.write_data(0x12)
        self.write_data(0x28)
        self.write_data(0x30)

        self.write_cmd(0xE1)
        self.write_data(0xF0)
        self.write_data(0x07)
        self.write_data(0x0A)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x07)
        self.write_data(0x28)
        self.write_data(0x33)
        self.write_data(0x3E)
        self.write_data(0x36)
        self.write_data(0x14)
        self.write_data(0x14)
        self.write_data(0x29)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3f)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x22)
        self.write_data(0x00)
        self.write_data(0xCD)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    def write_text(self,text,x,y,size,color):
        ''' Method to write Text on OLED/LCD Displays
            with a variable font size
            Args:
                text: the string of chars to be displayed
                x: x co-ordinate of starting position
                y: y co-ordinate of starting position
                size: font size of text
                color: color of text to be displayed
        '''
        background = self.pixel(x,y)
        info = []
        # Creating reference charaters to read their values
        self.text(text,x,y,color)
        for i in range(x,x+(8*len(text))):
            for j in range(y,y+8):
                # Fetching amd saving details of pixels, such as
                # x co-ordinate, y co-ordinate, and color of the pixel
                px_color = self.pixel(i,j)
                info.append((i,j,px_color)) if px_color == color else None
        # Clearing the reference characters from the screen
        self.text(text,x,y,background)
        # Writing the custom-sized font characters on screen
        for px_info in info:
            self.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2])   
  
if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch47()
    #color BRG
    # LCD.fill(LCD.WHITE)
    LCD.fill(0x0000)
    LCD.show()
    
    # LCD.fill_rect(0,0,320,30,LCD.RED)
    # LCD.ellipse(86,43,43,43,LCD.RED,True)
    # LCD.show()
    # LCD.write_text("Message From:",10,8,2,LCD.WHITE)
    # LCD.show()
    x,y = 0,0 
    # LCD.fill_rect(0,30,320,30,LCD.BLUE)
    # LCD.write_text("Dylan",x,28,2,LCD.WHITE)
  
    LCD.write_text("Dylan",10,38,2,LCD.WHITE)
#     while x < 160:
#         LCD.fill_rect(0,20,320,30,LCD.BLUE)
#         x += 1
        # LCD.write_text("Dylan",x,28,2,LCD.WHITE)
    LCD.show()
#         time.sleep(0.01)

#     # LCD.fill_rect(0,60,320,30,LCD.GREEN)
# #     LCD.rect(0,40,160,20,LCD.GREEN)
#     mx,my = 320,0
#     while mx > 0:
#         LCD.fill_rect(0,40,320,30,0x000000)
#         mx -= 1
#         LCD.write_text("Thanks,Mom",mx,68,2,LCD.WHITE)
#         LCD.show()
#         time.sleep(0.01)
    
    # LCD.fill_rect(0,90,320,30,0X07FF)
    # LCD.fill_rect(0,120,320,60,0xF81F)
    # LCD.fill_rect(0,150,320,30,0xFF1F)
    

#framebufer
    byte_data = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

    fb = framebuf.FrameBuffer(byte_data, 20, 20, framebuf.RGB565)

    LCD.blit(fb,50,30)
    LCD.show()
  # Screen dimensions
    # WIDTH = 320
    # HEIGHT = 172

    # # Create a buffer for the screen

    # # Pixel position and velocity
    # x, y = 0, 0
    # dx, dy = 1, 1

    # # Main loop
    
    # while True:

    #     # Draw the pixel
    #     LCD.pixel(x, y, LCD.RED)

    #     # Update the screen
    #     # Your code to update the screen goes here, e.g., lcd.write(fb)
    #     # LCD.blit(fb,0,0)
    #     # LCD.show()
    #     LCD.show()
        
    #     # Move the pixel
    #     x += dx
    #     y += dy

    #     # Check for collisions with the boundaries
    #     if x <= 0 or x >= WIDTH - 1:
    #         dx = -dx
    #     if y <= 0 or y >= HEIGHT - 1:
    #         dy = -dy

    #     # Delay to control the speed of the animation
    #     time.sleep(0.01)





    # while True:
    # #show current time
    #     time.sleep(1)
    #     LCD.fill_rect(0,120,320,60,0xF81F)
    #     now = time.localtime()
    #     time_string = "{:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5])
    #     LCD.write_text(time_string,10,128,4,0x0000)
    #     LCD.show()




