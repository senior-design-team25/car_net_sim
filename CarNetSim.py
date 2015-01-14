#!/usr/bin/env python2

import Tkinter as tk
import io
import sys

from World import World


# Top level window for the simulator

class CarNetSim(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        
        self.master.title('Car Network Simulator')
        
        self.pack(fill=tk.BOTH, expand=True)
        self.hw = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.vw = tk.PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.hw.pack(fill=tk.BOTH, expand=True)
        self.hw.add(self.vw)
        
        self.vw.add(self.init_canvas())
        self.vw.add(self.init_console_frame())
        self.hw.add(self.init_control_frame())
        
        self.initialized = False
        self.hw.bind('<Configure>', self.onresize)
        
        
    def init_canvas(self):
        self.canvas = tk.Canvas(self)
        self.canvas.width = 0
        self.canvas.height = 0
        
        self.canvas.bind('<Button-2>', self.onm2down)
        self.canvas.bind('<B2-Motion>', self.onm2move)
        self.canvas.bind('<Button-3>', self.onm2down)
        self.canvas.bind('<B3-Motion>', self.onm2move)
        self.canvas.bind_all('<MouseWheel>', self.onmwheel)
        self.canvas.bind_all('<Button-4>', self.onmwheel)
        self.canvas.bind_all('<Button-5>', self.onmwheel)
        
        self.world = World(self.canvas)
        
        return self.canvas
        
    def init_console_frame(self):
        self.console = tk.Frame(self)
        scroll = tk.Scrollbar(self.console)
        text = tk.Text(self.console, state=tk.DISABLED, yscrollcommand=scroll.set)
        scroll.config(command=text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(fill=tk.BOTH, expand=True)
        
        def write(m):
            text.configure(state=tk.NORMAL)
            text.insert(tk.END, m)
            text.yview(tk.END)
            text.configure(state=tk.DISABLED)
            
        sys.stdout = io.IOBase()
        sys.stdout.write = write
        
        return self.console
        
    def init_control_frame(self):
        self.control = tk.Frame(self)
        
        def hello():
            print "Hello World!"
            
        def error():
            raise Error("Error!")
            
        tk.Button(self.control, text='Hello', command=hello).pack(fill=tk.X)
        tk.Button(self.control, text='Error', command=error).pack(fill=tk.X)
        tk.Button(self.control, text='Quit', command=self.quit).pack(fill=tk.X)
        
        return self.control
        
    def onresize(self, event):
        hoff, voff = None, None
    
        if not self.initialized:
            hoff, voff = 200, 100
            self.initialized = True
            
            scale = event.width/100.0
            self.world.scale((0,0), event.width/100)
        else:
            hoff = self.canvas.width - self.hw.sash_coord(0)[0]
            voff = self.canvas.height - self.vw.sash_coord(0)[1]
            
            scale = event.width/float(self.canvas.width)
            self.world.scale((0,0), event.width/float(self.canvas.width))
        
        def place_sash(x, y):
            self.hw.sash_place(0, x, 1)
            self.vw.sash_place(0, 1, y)
        
        self.hw.config(width=event.width)
        self.vw.config(height=event.height)
        self.after_idle(place_sash, event.width-hoff, event.height-voff)
        
        self.canvas.width = event.width
        self.canvas.height = event.height
        
    def onm2down(self, event):
        self.mx = event.x
        self.my = event.y
        
    def onm2move(self, event):
        self.world.move((event.x - self.mx, event.y - self.my))
        self.mx = event.x
        self.my = event.y
        
    def onmwheel(self, event):
        if event.x > self.hw.sash_coord(0)[0] or \
           event.y > self.vw.sash_coord(0)[1]:
            return
        elif event.num == 4 or event.delta > 0:
            self.world.scale((event.x, event.y), 1.2)
        elif event.num == 5 or event.delta < 0:
            self.world.scale((event.x, event.y), 1/1.2)
        
        
        
# Entry point for the simulator    

def main():
    root = tk.Tk()
    root.geometry("800x600+50+50")
    sim = CarNetSim(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()