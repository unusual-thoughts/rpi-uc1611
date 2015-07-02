#!/usr/bin/env python

import spidev as spi
import RPi.GPIO as GPIO

class UC1611(spi.SpiDev):

    def __init__(self):
        super().__init__()

    def open(self, *args, **kwargs):
        super().open(*args, **kwargs)
        self.mode = 3
        self.cshigh = True

        self.wrap_around = 0x1
        self.increment_page_first = 0x0
        self.page_increment_direction = 0x0

        self.mirror_y = 0x0
        self.mirror_x = 0x0
        self.ms_nibble_first = 0x0

    def cmd(self):
        raise NotImplementedError()

    def data(self):
        raise NotImplementedError()

    def set_col_addr(self, n):
        self.cmd(n & 0x0F)
        self.cmd(0x10 | (n >> 4))

    def set_temp_comp(self, n):
        self.cmd(0x24 | (n & 0x03))

    def set_panel_loading(self, n):
        self.cmd(0x28 | (n & 0x03))


    def set_pump_ctrl (self, n):
        self.cmd(0x2C | (n & 0x03))

    # undocumented
    def set_adv_ctrl (self, t, n):
        self.cmd(0x30 | (t & 0x01))
        self.cmd(n & 0xFF)

    def set_max_ca(self, n):
        self.cmd(0x32)
        self.cmd(n & 0xFF)

    def set_scroll_line(self, n):
        self.cmd(0x40 | (n & 0x0F))
        self.cmd(0x50 | (n >> 4))

    def set_page_addr(self, n):
        self.cmd(0x60 | (n & 0x0F))
        self.cmd(0x70 | (n >> 4))

    def set_v_bias_pot(self, n):
        self.cmd(0x81)
        self.cmd(n & 0xFF)

    def set_partial_display_ctrl(self, n):
        self.cmd(0x84 | (n & 0x03))

    def set_ram_addr_ctrl(self, n):
        self.cmd(0x88 | (n & 0x07))

    def set_wrap_around(self, n):
        self.wrap_around = 0x1 if n else 0x0
        self.set_ram_addr_ctrl(self.wrap_around | (self.increment_page_first << 1) | (self.page_increment_direction << 2))

    def set_increment_page_first(self, n):
        self.increment_page_first = 0x1 if n else 0x0
        self.set_ram_addr_ctrl(self.wrap_around | (self.increment_page_first << 1) | (self.page_increment_direction << 2))

    def set_page_increment_direction(self, n):
        self.page_increment_direction = 0x1 if n > 0 else 0x0
        self.set_ram_addr_ctrl(self.wrap_around | (self.increment_page_first << 1) | (self.page_increment_direction << 2))

    def set_fixed_lines(self, n):
        self.cmd(0x90 | (n & 0x0F))

    def set_line_rate(self, n):
        self.cmd(0xA0 | (n & 0x03))

    def set_all_pixel_on(self, n):
        self.cmd(0xA4 | (n & 0x01))

    def set_inverse_display(self, n):
        self.cmd(0xA6 | (n & 0x01))

    def set_display_enable(self, n):
        self.cmd(0xA8 | (n & 0x07))

    def set_lcd_mapping_ctrl(self, n):
        self.cmd(0xC0 | (n & 0x07))

    def set_mirror_x(self, n):
        self.mirror_x = 0x1 if n else 0x0
        self.set_lcd_mapping_ctrl(self.ms_nibble_first | (self.mirror_x << 1) | (self.mirror_y << 2))

    def set_mirror_y(self, n):
        self.mirror_y = 0x1 if n else 0x0
        self.set_lcd_mapping_ctrl(self.ms_nibble_first | (self.mirror_x << 1) | (self.mirror_y << 2))

    def set_ms_nibble_first(self, n):
        self.ms_nibble_first = 0x1 if n else 0x0
        self.set_lcd_mapping_ctrl(self.ms_nibble_first | (self.mirror_x << 1) | (self.mirror_y << 2))

    def set_gray_scale_mode(self, n):
        self.cmd(0xD0 | (n & 0x03))

    def set_gray_scale_bw(self):
        self.set_gray_scale_mode(0)

    def set_gray_scale_8(self):
        self.set_gray_scale_mode(1)

    def set_gray_scale_16(self):
        self.set_gray_scale_mode(2)

    def set_gray_scale_64(self):
        self.set_gray_scale_mode(3)

    def system_reset(self):
        self.cmd(0xE2)

    def nop(self):
        self.cmd(0xE3)

    # Undocumented
    def set_test_ctrl(self, t, n):
        self.cmd(0xE4 | (t & 0x03))
        self.cmd(n & 0xFF)

    def set_lcd_bias_ratio(self, n):
        self.cmd(0xE8 | (n & 0x03))

    def reset_cursor_update_mode(self):
        self.cmd(0xEE)

    def set_cursor_update_mode(self):
        self.cmd(0xEF)

    def set_com_end(self, n):
        self.cmd(0xF1)
        self.cmd(n & 0xFF)

    def set_partial_display_start(self, n):
        self.cmd(0xF2)
        self.cmd(n & 0xFF)

    def set_partial_display_end(self, n):
        self.cmd(0xF3)
        self.cmd(n & 0xFF)

    def send_img(self, pixels):
        i = 0
        buf = []
        for line in range(0, 160, 2):
            for col in range(240):
                if (i == 4095):
                    self.data(buf)
                    buf = []
                    i = 0
                buf.append(pixels[line * 240 + col] + (pixels[(line + 1) * 240 + col] << 4))
                i = i + 1
        self.data(buf)


class UC1611_4wire(UC1611):
    def __init__(self):
        super().__init__()
        self.cd_pin = 4

    def open(self, *args, **kwargs):
        super().open(*args, **kwargs)
        self.bits_per_word = 8
        # C/D pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.cd_pin, GPIO.OUT)

    def cmd(self, n):
        # pull CD low
        GPIO.output(self.cd_pin, GPIO.LOW)
        self.writebytes([n])

    # Takes a list
    def data(self, n):
        # pull CD high
        GPIO.output(self.cd_pin, GPIO.HIGH)
        self.writebytes(n)

class UC1611_3wire(UC1611):
    def __init__(self):
        super().__init__()

    def open(self, *args, **kwargs):
        super().open(*args, **kwargs)
        self.bits_per_word = 9

    def cmd(self, n):
        self.writebytes([0x100 | n])

    # Takes a list
    def data(self, n):
        self.writebytes(n)