from rpi_uc1611 import *
from time import sleep
from PIL import Image

uc = UC1611_4wire()
uc.open(0,0)
#uc.max_speed_hz = 1000
bias = 0x0

uc.system_reset()

uc.set_display_enable(0x7)
uc.set_gray_scale_16()
uc.set_v_bias_pot(28)

uc.set_scroll_line(0)
uc.set_fixed_lines(0)

uc.set_mirror_x(True)

#moustique = list(Image.open("pokemon.png").getdata())

i = 0
uc.set_page_addr(0)
uc.set_col_addr(0)

uc.send_img(Image.open("pokemon_inverted.png").getdata())

# while i < len(moustique) - 240:
#     uc.data([0xF - moustique[i] + ((0xF - moustique[i + 240]) << 4)])
#     i = i + 1
#     if i % 240 == 0:
#         i = i + 240

# while i < len(moustique):
#     uc.set_page_addr(int(i / 480))
#     uc.set_col_addr(0)
#     uc.data(moustique[i:i + 480])
#     sleep(.1)
#     i = i + 480

# buf = list(range(256)) * 16
# for i in range(4):
#     uc.data(buf)

for i in range(160):
    uc.set_scroll_line(i)
    sleep(.3)

for page in range(80):
    buf = [page // 5 + (page // 5) * 16] * 240
    uc.data(buf)

# while i < len(moustique):
#     uc.data(moustique[i:i + 4096])
#     sleep(.1)
#     i = i + 4096


# while True:
#     #uc.set_all_pixel_on(0x0)
#     for bias in range(0xFF):
#         uc.set_v_bias_pot(bias)
#         print("OFF, " + str(bias))
#         sleep(.1)

    # uc.set_all_pixel_on(0x1)
    # for bias in range(0xFF):
    #     uc.set_v_bias_pot(bias)
    #     print("ON, " + str(bias))
    #     sleep(.1)

