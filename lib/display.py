#from ST7735 import TFT, TFTColor
import ST7735
from sysfont import sysfont
from framebuf2 import FrameBuffer, RGB565
import config
from bmp import bmp
from microfont import MicroFont

class CoinSortDisplay:
    def __init__(self, spi):
        #self.display = TFT(spi,aDC=config.DISPLAY_DC_PIN, aReset=config.DISPLAY_RST_PIN, aCS=config.DISPLAY_CS_PIN)
        #self.display.initr()
        #self.display.rgb(True)
        #self.display.fill(TFT.WHITE)
        #self.display.rotation(3)
        self.display = ST7735.ST7735(spi, rst=config.DISPLAY_RST_PIN, ce=config.DISPLAY_CS_PIN, dc=config.DISPLAY_DC_PIN)
        self.display.reset()
        self.display.begin()
        self.display.set_rotation(1)
        self.display._bground = 0xffff
        self.display._color = 0x0000
        self.display.fill_screen(self.display._bground)
        self.buffer = bytearray(128*160*2)

    def show_message(self, message, color=0x0, font=sysfont, background_color=0xffff):
        """
        Display a message on the TFT screen with optional customization.

        :param message: The message to display.
        :param color: The color of the text (default: TFT.BLACK).
        :param font: The font to use for the text (default: sysfont).
        :param background_color: The background color to fill the screen (default: TFT.WHITE).
        """

        fb = FrameBuffer(self.buffer, 160, 128, RGB565)
        fb.fill(0xffff)
        fb.rect(0,0,160,60,self.display.rgb_to_565(10,0,18),True)
        fb.large_text('100.00', 8, 22, 3, 0xffff)

        fb.rect(0,60,160,16,self.display.rgb_to_565(21,21,43),True)
        fb.text('100x0.01', 8, 65, color)
        fb.text('100x0.20', 88, 65, color)

        fb.text('100x0.02', 8, 81, color)
        fb.text('100x0.02', 88, 81, color)
        
        fb.rect(0,92,160,16,self.display.rgb_to_565(21,21,43),True)
        fb.text('100x0.05', 8, 97, color)
        fb.text('100x0.10', 88, 97, color)

        fb.text('100x1.00', 8, 113, color)
        fb.text('100x2.00', 88, 113, color)

        font = MicroFont("victor_B_32.mfnt",cache_index=True)
        color = 1 # Color must be in the framebuffer color mode format.
        angle = 0
        font.write("100.00€", fb, RGB565, 160, 128, 0, 0, color, rot=angle, x_spacing=0, y_spacing=0)

        self.display.draw_bmp(0,0,160,128,self.buffer)

        #self.display.fill_screen(self.display.rgb_to_565(21,21,43))

    def clear(self):
        self.display.fill_screen(0x0)
    
    def show_amount(self):
        self.display.fill_screen(0xffff)
        self.display.p_string(0,0,"Hello World")
        bmp('Bosch_Logo.bmp',self.display,10,10,1)
