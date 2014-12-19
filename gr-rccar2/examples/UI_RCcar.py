import wx
from RCCarTransmit import transmit_block 
from time import sleep

#create button id's
ID_BUTTON_FORWARD = wx.NewId()
ID_BUTTON_RIGHT = wx.NewId()
ID_BUTTON_LEFT = wx.NewId()
ID_BUTTON_BACK = wx.NewId()
ID_BUTTON_STOP = wx.NewId()
ID_BUTTON_FORWARD_LEFT = wx.NewId()
ID_BUTTON_FORWARD_RIGHT = wx.NewId()
ID_BUTTON_BACKWARD_RIGHT = wx.NewId()
ID_BUTTON_BACKWARD_LEFT = wx.NewId()
ID_EXIT = wx.NewId()

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

#create the UI
class MyFrame(wx.Frame):
 
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent,title=title, style=wx.DEFAULT_FRAME_STYLE | wx.WANTS_CHARS, size=(300,500))
        self.InitUI()
        self.Centre()
        self.Show()
        self.running = False 
    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File') 
        self.SetMenuBar(menubar) 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        gs = wx.GridSizer(3, 3)
        gs.AddMany([
(wx.Button(self,ID_BUTTON_FORWARD_LEFT, label='FORWARD LEFT'), 0,wx.EXPAND),
(wx.Button(self,ID_BUTTON_FORWARD, label='^'), 0,wx.EXPAND),  
(wx.Button(self,ID_BUTTON_FORWARD_RIGHT, label='FORWARD RIGHT'), 0,wx.EXPAND),  
(wx.Button(self,ID_BUTTON_LEFT, label='<'), 0,wx.EXPAND),
(wx.Button(self,ID_BUTTON_STOP, label='.'), 0,wx.EXPAND),
(wx.Button(self,ID_BUTTON_RIGHT, label='>'), 0,wx.EXPAND),
(wx.Button(self,ID_BUTTON_BACKWARD_LEFT, label='BACKWARD LEFT'), 0,wx.EXPAND),
(wx.Button(self, ID_BUTTON_BACK,label='#'), 0,wx.EXPAND), 
(wx.Button(self,ID_BUTTON_BACKWARD_RIGHT, label='BACKWARD RIGHT'), 0,wx.EXPAND)])
        sizer.Add(gs, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)  
        self.Bind(wx.EVT_BUTTON, self.set_forward, id=ID_BUTTON_FORWARD)
        self.Bind(wx.EVT_BUTTON, self.set_backward, id=ID_BUTTON_BACK)
        self.Bind(wx.EVT_BUTTON, self.set_stop, id=ID_BUTTON_STOP)
        self.Bind(wx.EVT_BUTTON, self.set_forward_left, id=ID_BUTTON_FORWARD_LEFT)
        self.Bind(wx.EVT_BUTTON, self.set_forward_right, id=ID_BUTTON_FORWARD_RIGHT)
        self.Bind(wx.EVT_BUTTON, self.set_backward_right, id=ID_BUTTON_BACKWARD_RIGHT)
        self.Bind(wx.EVT_BUTTON, self.set_backward_left, id=ID_BUTTON_BACKWARD_LEFT)
        self.Bind(wx.EVT_BUTTON, self.set_left, id=ID_BUTTON_LEFT)
        self.Bind(wx.EVT_BUTTON, self.set_right, id=ID_BUTTON_RIGHT)
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.panel.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.panel.SetFocus() 
        self.SetFocus()
        self.tb = transmit_block() 
        self.currentkey = 0 
    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        print key 
        if (key == self.currentkey):
            return 
        if(key == 314): #Left key
            self.tb.stop()
            self.running = False 
            self.tb.wait()
            self.tb.set_direction(RC_TURBO_FORWARD_LEFT)
            self.currentkey = key
            self.running = True 
            self.tb.start()
        elif(key == 315): #up key
            self.tb.stop()
            self.running = False 
            self.tb.wait()
            self.tb.set_direction(RC_FORWARD)
            self.currentkey = key
            self.running = True 
            self.tb.start()
        elif(key == 316): #right key
            self.tb.stop()
            self.running = False 
            self.tb.wait()
            self.tb.set_direction(RC_TURBO_FORWARD_RIGHT)
            self.currentkey = key
            self.running = True 
            self.tb.start()
        elif(key == 317): #back key
            self.tb.stop()
            self.running = False 
            self.tb.wait()
            self.tb.set_direction(RC_BACKWARD)
            self.currentkey = key
            self.running = True 
            self.tb.start()
             
    def OnKeyUp(self,event):
        print "KEY UP" 
        self.tb.stop()
        self.tb.wait()
        self.tb.set_direction(RC_ENDCODE)
        self.running = True 
        self.tb.start()
        sleep(0.1) 
        self.tb.stop()
        self.currentkey = 0 
        self.running = False

    def set_forward(self,event):
        print "Forward Clicked" 
        if(self.running == True):
            self.tb.stop()
            self.tb.wait()
            self.running = False
        self.tb.set_direction(RC_FORWARD)
        self.running = True 
        self.tb.start()
    
    def set_forward_left(self,event):
        print "Forward Left Clicked" 
        if(self.running == True):
            self.tb.stop()
            self.tb.wait()
            self.running = False
        self.tb.set_direction(RC_TURBO_FORWARD_LEFT)
        self.running = True 
        self.tb.start()
    
    def set_forward_right(self,event):
        print "Forward Right Clicked" 
        if(self.running == True):
            self.tb.stop()
            self.tb.wait()
            self.running = False
        self.tb.set_direction(RC_TURBO_FORWARD_RIGHT)
        self.running = True 
        self.tb.start()
    
    def set_left(self,event):
        print "Left Clicked"
        if(self.running == True):
            self.tb.stop()
            self.tb.wait()
            self.running = False
        self.running = True 
        self.tb.set_direction(RC_LEFT)
        self.tb.start()
     
    def set_right(self,event):
        print "Right Clicked"
        if(self.running == True):
            self.tb.stop()
            self.tb.wait()
            self.running = False
        self.running = True 
        self.tb.set_direction(RC_RIGHT)
        self.tb.start()
     
    def set_backward(self,event):
        print "Backwards Clicked"
        if(self.running == True):
            self.tb.stop()
            self.tb.wait()
            self.running = False
        self.running = True 
        self.tb.set_direction(RC_BACKWARD)
        self.tb.start()
     
    def set_backward_right(self,event):
        print "backward right clicked"
        if(self.running == True):
            self.tb.stop()
            self.tb.wait()
            self.running = False
        self.running = True 
        self.tb.set_direction(RC_BACKWARD_RIGHT)
        self.tb.start()
    
    def set_backward_left(self,event):
        print "backward left clicked"
        if(self.running == True):
            self.tb.stop()
            self.tb.wait()
            self.running=False
        self.running = True 
        self.tb.set_direction(RC_BACKWARD_LEFT)
        self.tb.start()

    def set_stop(self,event):
        if(self.running == True):
            self.tb.stop()
            self.tb.wait()
            self.runnning = False
        self.tb.set_direction(RC_ENDCODE)
        self.running = True 
        self.tb.start()
        sleep(1) #sleep for 1 second 
        self.tb.stop()
        self.tb.wait()
        self.running = False

    def OnQuit(self,event):
        self.tb.stop()
        self.running = False 
        self.Close(True)

def main():
    ex = wx.App()
    MyFrame(None, title="RC Remote")
    ex.MainLoop()

if __name__ == '__main__':
    main()

