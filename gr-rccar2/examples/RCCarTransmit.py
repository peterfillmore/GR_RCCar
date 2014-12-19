from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import gr
#from gnuradio import numpy
from gnuradio.eng_option import eng_option

import osmosdr
import rccar2

from time import sleep

#global samplerate
#i've set this to 500kHz
samp_rate = 0.5e6

#set the transmit frequency - i.e what the car is wired to receive
#RC_FREQUENCY = 27.253e6
RC_FREQUENCY = 47.6498e6

#command codes
RC_FORWARD = 1 
RC_FORWARD_TURBO = 2 
RC_TURBO = 3 
RC_TURBO_FORWARD_LEFT = 4 
RC_TURBO_FORWARD_RIGHT = 5 
RC_BACKWARD = 6 
RC_BACKWARD_RIGHT = 7 
RC_BACKWARD_LEFT = 8 
RC_LEFT = 9 
RC_RIGHT = 10 
RC_ENDCODE = 11
RC_NOTHING = 12

#create the flowgraph for transmission
class transmit_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
        #variables
        self.samp_rate = samp_rate
        self.direction = RC_NOTHING #no direction to start 
        #blocks 
        #define the gnuradio blocks
        #interpolator expands the input function - this creates long zeros and ones  
        self.interpolator = rccar2.functioninterpolator(samp_rate)
        #functioncoder takes a functioncode into it and creates the appropriate command stream 
        self.functioncoder = rccar2.functioncoder(samplerate=samp_rate, functioncode=1)
        #sink (the hackRF in this case), can be changed to your transmitting device of course
        self.hackrf = osmosdr.sink(args="numchan=" +str(1) + " " + "hackhf")
        self.hackrf.set_sample_rate(samp_rate)
        self.hackrf.set_center_freq(RC_FREQUENCY,0)
        self.hackrf.set_freq_corr(0,0)
        #enable the hackrf to transmit (need to set the gain to 14dB) 
        self.hackrf.set_gain(14,0)
        self.hackrf.set_if_gain(30,0)
        self.hackrf.set_bb_gain(20,0)
        self.hackrf.set_antenna("",0)
        self.hackrf.set_bandwidth(0,0)
        #conversion blocks 
        self.float_to_complex = blocks.float_to_complex(1)
        self.char_to_float = blocks.char_to_float(1,1)
        #vector source which sends the direction to the functioncoder 
        self.vector_source = blocks.vector_source_i([self.direction], False) 
        #connect it all up
        self.connect((self.char_to_float,0), (self.float_to_complex,0))
        self.connect((self.char_to_float,0), (self.float_to_complex,1)) 
        self.connect((self.interpolator,0), (self.char_to_float,0))
        self.connect((self.float_to_complex,0), (self.hackrf,0))
        self.connect((self.vector_source,0), (self.functioncoder,0))
        self.connect((self.functioncoder,0), (self.interpolator,0))
    def set_samp_rate(self):
        self.samp_rate = samp_rate
        self.hackrf.set_sample_rate(self.samp_rate)
    def get_samp_rate(self):
        return samp_rate
    def set_direction(self,direction):
        """update the command of the block"""
        self.direction = direction 
        self.vector_source.set_data([self.direction])
