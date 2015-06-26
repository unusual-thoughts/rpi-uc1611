#!/usr/bin/env python

import spidev

class UC1611(SpiDev):

    def __init__(self):
        SpiDev.init()

    def cmd(self):
        raise NotImplementedError()

    def data(self):
        raise NotImplementedError()

    def set_col_addr(n):
        self.cmd(n & 0x0F)
        self.cmd(n & 0xF0)

    def set_temp_comp(n):
        self.cmd(0x24 | (n & 0x03))

    def set_panel_loading (n):
        self.cmd(0x28 | (n & 0x03))


    def set_pump_ctrl (n):
        self.cmd(0x2C | (n & 0x03))

    # undocumented
    def set_adv_ctrl (b, n):
        self.cmd(0x30 | (b & 0x01))
        self.cmd(n & 0xFF)

    def set_max_ca(n):
        self.cmd(0x32)
        self.cmd(n & 0xFF)

    def set_scroll_line(n):
        self.cmd(0x40 | (n & 0x0F))
        self.cmd(0x50 | (n & 0xF0))

    def set_page_addr(n):
        self.cmd(0x60 | (n & 0x0F))
        self.cmd(0x70 | (n & 0xF0))

    def set_v_bias_pot(n):
        self.cmd(0x81)
        self.cmd(n & 0xFF)

    def set_partial_display_ctrl(n):
        self.cmd(0x84 | (n & 0x03))

    def set_ram_addr_ctrl(n):
        self.cmd(0x88 | (n & 0x07))

    def set_fixed_lines(n):
        self.cmd(0x90 | (n & 0x0F))

    def set_line_rate(n):
        self.cmd(0xA0 | (n & 0x03))

    def set_all_pixel_on(n):
        self.cmd(0xA4 | (n & 0x01))

    def set_inverse_display(n):
        self.cmd(0xA6 | (n & 0x01))

    def set_display_enable(n):
        self.cmd(0xA8 | (n & 0x07))

    def set_lcd_mapping_ctrl(n):
        self.cmd(0xC0 | (n & 0x07))

    def set_gray_scale_mode(n):
        self.cmd(0xD0 | (n & 0x03))

    def set_gray_scale_bw():
        set_gray_scale_mode(0)

    def set_gray_scale_8():
        set_gray_scale_mode(1)

    def set_gray_scale_16():
        set_gray_scale_mode(2)

    def gray_scale_64():
        set_gray_scale_mode(3)

    def system_reset():
        self.cmd(0xE2)

    def nop():
        self.cmd(0xE3)

    # Undocumented
    def set_test_ctrl(t, n):
        self.cmd(0xE4 | (t & 0x03))
        self.cmd(n & 0xFF)

    def set_lcd_bias_ratio(n):
        self.cmd(0xE8 | (n & 0x03))

    def reset_cursor_update_mode():
        self.cmd(0xEE)

    def set_cursor_update_mode():
        self.cmd(0xEF)

    def set_com_end(n):
        self.cmd(0xF1)
        self.cmd(n & 0xFF)

    def set_partial_display_start(n):
        self.cmd(0xF2)
        self.cmd(n & 0xFF)

    def set_partial_display_end(n):
        self.cmd(0xF3)
        self.cmd(n & 0xFF)


class UC1611_4wire(UC1611):
