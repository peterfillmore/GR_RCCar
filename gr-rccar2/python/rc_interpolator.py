#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class rc_interpolator(gr.interp_block):
    """
    docstring for block rc_interpolator
    """
    def __init__(self, samplerate):
        self.samplerate = samplerate
        self.interpolatefactor = int(samplerate/500) 
        gr.interp_block.__init__(self,
            name="rc_interpolator",
            in_sig=[numpy.uint8],
            out_sig=[numpy.uint8],
            interp = self.interpolatefactor)

    def work(self, input_items, output_items):
        print len(input_items[0]) 
        output_items[0] = input_items[0] 
        #for i in xrange(len(input_items[0])):
        #    for j in xrange(self.interpolatefactor):
        #        output_items[0][j] = input_items[0][i]
        #output_items[0][:] = input_items[0] * self.interpolatefactor 
        # <+signal processing here+>
        return len(output_items[0])

