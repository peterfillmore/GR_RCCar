#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Fri Dec 19 11:43:48 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import rccar2
import wx

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")

        ##################################################
        # Variables
        ##################################################
        self.variable_control = variable_control = 1
        self.samp_rate = samp_rate = 0.5e6
        self.freq_change = freq_change = -52e3
        self.amp_const = amp_const = 0.1
        self.RC_FREQUENCY = RC_FREQUENCY = 45.6498e6
        self.RC_DIRECTION = RC_DIRECTION = 1

        ##################################################
        # Blocks
        ##################################################
        _amp_const_sizer = wx.BoxSizer(wx.VERTICAL)
        self._amp_const_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_amp_const_sizer,
        	value=self.amp_const,
        	callback=self.set_amp_const,
        	label="amp const",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._amp_const_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_amp_const_sizer,
        	value=self.amp_const,
        	callback=self.set_amp_const,
        	minimum=0,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_amp_const_sizer)
        self._RC_FREQUENCY_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.RC_FREQUENCY,
        	callback=self.set_RC_FREQUENCY,
        	label="Transmission Frequency",
        	choices=[27.253e6, 45.6498e6, 49e6],
        	labels=["27 MHz", "45.6498 Mhz", "49 MHz"],
        	style=wx.RA_HORIZONTAL,
        )
        self.Add(self._RC_FREQUENCY_chooser)
        self._RC_DIRECTION_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.RC_DIRECTION,
        	callback=self.set_RC_DIRECTION,
        	label="Select Direction",
        	choices=[11,1, 2,6,12],
        	labels=["ENDCODE","FORWARD","FORWARD TURBO","BACKWARDS","NOTHING"],
        )
        self.Add(self._RC_DIRECTION_chooser)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0.win)
        _variable_control_sizer = wx.BoxSizer(wx.VERTICAL)
        self._variable_control_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_variable_control_sizer,
        	value=self.variable_control,
        	callback=self.set_variable_control,
        	label="direction",
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._variable_control_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_variable_control_sizer,
        	value=self.variable_control,
        	callback=self.set_variable_control,
        	minimum=1,
        	maximum=6,
        	num_steps=6,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_variable_control_sizer)
        self.rccar_rc_interpolator_0 = rccar2.functioninterpolator(samp_rate)
        self.rccar_functioncoder_0 = rccar2.functioncoder(samplerate=samp_rate,functioncode=1)
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "hackrf" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(RC_FREQUENCY, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(14, 0)
        self.osmosdr_sink_0.set_if_gain(30, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        _freq_change_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_change_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_change_sizer,
        	value=self.freq_change,
        	callback=self.set_freq_change,
        	label="freq_change",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_change_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_change_sizer,
        	value=self.freq_change,
        	callback=self.set_freq_change,
        	minimum=-2e6,
        	maximum=2e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_change_sizer)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((amp_const, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_const_source_x_0 = analog.sig_source_i(0, analog.GR_CONST_WAVE, 0, 0, RC_DIRECTION)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.rccar_rc_interpolator_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.rccar_functioncoder_0, 0))
        self.connect((self.rccar_functioncoder_0, 0), (self.rccar_rc_interpolator_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_float_to_complex_0, 1))



    def get_variable_control(self):
        return self.variable_control

    def set_variable_control(self, variable_control):
        self.variable_control = variable_control
        self._variable_control_slider.set_value(self.variable_control)
        self._variable_control_text_box.set_value(self.variable_control)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)

    def get_freq_change(self):
        return self.freq_change

    def set_freq_change(self, freq_change):
        self.freq_change = freq_change
        self._freq_change_slider.set_value(self.freq_change)
        self._freq_change_text_box.set_value(self.freq_change)

    def get_amp_const(self):
        return self.amp_const

    def set_amp_const(self, amp_const):
        self.amp_const = amp_const
        self._amp_const_slider.set_value(self.amp_const)
        self._amp_const_text_box.set_value(self.amp_const)
        self.blocks_multiply_const_vxx_0.set_k((self.amp_const, ))

    def get_RC_FREQUENCY(self):
        return self.RC_FREQUENCY

    def set_RC_FREQUENCY(self, RC_FREQUENCY):
        self.RC_FREQUENCY = RC_FREQUENCY
        self._RC_FREQUENCY_chooser.set_value(self.RC_FREQUENCY)
        self.osmosdr_sink_0.set_center_freq(self.RC_FREQUENCY, 0)

    def get_RC_DIRECTION(self):
        return self.RC_DIRECTION

    def set_RC_DIRECTION(self, RC_DIRECTION):
        self.RC_DIRECTION = RC_DIRECTION
        self.analog_const_source_x_0.set_offset(self.RC_DIRECTION)
        self._RC_DIRECTION_chooser.set_value(self.RC_DIRECTION)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
