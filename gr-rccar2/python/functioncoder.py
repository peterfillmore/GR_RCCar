#/usr/bin/env python
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

#function codes based off TX-2B/RX-2B datasheet
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

#setup the raw bit information
RC_W1 = [1,0] 
RC_W2 = [1,1,1,0] 

#start code is W2 signal x 4
RC_STARTCODE = RC_W2 * 4

class functioncoder(gr.basic_block):
    """
    function coder creates the raw bit stream for a function
    this needs to be connected to the interpolator to create the stream to send to the hackrf 
    """
    #constants for functions
     
    #set_functioncode = 0 
    def __init__(self, samplerate, functioncode):
        """initialize a basic block - this has an input of an integer and outputs chars
        needs to be improved - pretty sure theres a better way of doing this 
        """ 
        gr.basic_block.__init__(self,name="functioncoder",in_sig=[numpy.int32],out_sig=[numpy.uint8])
        self.samplerate = samplerate 
        self.functioncode = functioncode 
        #create the commands 
        self.CMD_RC_RIGHT = (((RC_STARTCODE + (RC_W1 * 64)) ) ) * 3  
        self.CMD_RC_ENDCODE =  (RC_STARTCODE + (RC_W1 * 4))
        self.CMD_RC_FORWARD = (((RC_STARTCODE + (RC_W1 * 10))))
        self.CMD_RC_FORWARD_TURBO = (((RC_STARTCODE + (RC_W1 * 16)) ))  
        self.CMD_RC_TURBO = (((RC_STARTCODE + (RC_W1 * 22 )) ))  
        self.CMD_RC_TURBO_FORWARD_LEFT = (((RC_STARTCODE + (RC_W1 * 28)) ) ) * 3 
        self.CMD_RC_TURBO_FORWARD_RIGHT = (((RC_STARTCODE + (RC_W1 * 34))) )  
        self.CMD_RC_BACKWARD = (((RC_STARTCODE + (RC_W1 * 40))))  
        self.CMD_RC_BACKWARD_RIGHT = (((RC_STARTCODE + (RC_W1 * 46)) ) )  
        self.CMD_RC_BACKWARD_LEFT = (((RC_STARTCODE + (RC_W1 * 52)) ) )  
        self.CMD_RC_LEFT = (((RC_STARTCODE + (RC_W1 * 58)) ) )  
        self.CMD_RC_NOTHING = [0,0,0,0] * 64 
        #this tells gnuradio how long the output is
        #i need improve this calculation...  
        self.set_output_multiple(len(self.CMD_RC_RIGHT))
 
    def returnfunction(self,input_val): #return the encoded function
        """
        this function generates the returned command based off the input value
        """ 
        #switch statement to determine what to return 
        if(input_val == RC_ENDCODE): #end command
            #print "SENDING ENDCODE..." 
            return self.CMD_RC_ENDCODE * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_ENDCODE)) 
        if(input_val == RC_FORWARD): #forward
            #print "SENDING FORWARD..." 
            return self.CMD_RC_FORWARD * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_FORWARD)) 
        if(input_val == RC_FORWARD_TURBO):
            #print "SENDING FORWARD TURBO..." 
            return self.CMD_RC_FORWARD_TURBO * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_FORWARD_TURBO)) 
        if(input_val == RC_TURBO):
            #print "SENDING TURBO..." 
            return self.CMD_RC_TURBO * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_TURBO))
        if(input_val == RC_TURBO_FORWARD_LEFT):
            return self.CMD_RC_TURBO_FORWARD_LEFT * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_TURBO_FORWARD_LEFT))
        if(input_val == RC_TURBO_FORWARD_RIGHT):
            return self.CMD_RC_TURBO_FORWARD_RIGHT * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_TURBO_FORWARD_RIGHT))
        if(input_val == RC_BACKWARD):
            #print "SENDING BACKWARD..." 
            return self.CMD_RC_BACKWARD * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_BACKWARD)) 
        if(input_val == RC_BACKWARD_RIGHT):
            return self.CMD_RC_BACKWARD_RIGHT * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_BACKWARD_RIGHT))
        if(input_val == RC_BACKWARD_LEFT):
            return self.CMD_RC_BACKWARD_LEFT * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_BACKWARD_LEFT))
        if(input_val == RC_LEFT):
            return self.CMD_RC_LEFT * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_LEFT))
        if(input_val == RC_RIGHT): 
            return self.CMD_RC_RIGHT * (len(self.CMD_RC_RIGHT)/len(self.CMD_RC_RIGHT))
        if(input_val == RC_NOTHING):
            return self.CMD_RC_NOTHING * 10
  
    def forecast(self, noutput_items, ninput_items_required):
        """
            how many input items do we need to produce output, hardcoded to 1
        """ 
        return 1 
    
    def general_work(self, input_items, output_items):
        """
            heres where we do our work
            lots of the stuff here is hacked together to get to work
            so feel free to improve! 
        """ 
        if(input_items is None): #no inputs, then consume an input and continue
            self.consume(0,1)
            return 0 
        currentval = input_items[0][numpy.flatnonzero(input_items[0])] #get the input items
        if len(currentval) == 0: #if length is zero then consume and continue
            self.consume(0,1)
            return 0
        currentval = currentval[0] #get the input value
        if(currentval == 0): # if zero, consume and continue
            self.consume(0,1)
            return 0
        self.command = self.returnfunction(currentval) #lookup the command to return
        #nt output_items[0] 
        if(output_items is None): #check that output_items isn't null
            self.consume(0,1)
            return 0 
        if((len(output_items[0]) >= len(self.command))): #make sure we have space for the output 
            output_items[0][0:len(self.command)] = self.command #copy command into output
            self.consume(0,1) #consume 1 input int
            return len(self.command) #return the length of the output
        self.consume(0,1) #consume 1 input int - just in case
        return 0 
