#!/usr/bin/env python2

import Tkinter as tk
import io
import sys
import types


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
		self.hw.bind('<Configure>', self.on_resize)
		
		
	def init_canvas(self):
		self.canvas = tk.Canvas(self)
		self.canvas.width = 0
		self.canvas.height = 0
		
		def onresize(canvas, event):
			canvas.width = event.width
			canvas.height = event.height
			canvas.create_line(0,0,event.width,event.height)
			canvas.create_line(0,event.height,event.width,0)
			
		self.canvas.onresize = types.MethodType(onresize, self.canvas)
		
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
			
		def error(m):
			write(m)
			
		sys.stdout = io.IOBase()
		sys.stdout.write = write
		sys.stderr = sys.stdout
		
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
		
	def on_resize(self, event):
		hoff, voff = None, None
	
		if not self.initialized:
			hoff, voff = 200, 100
			self.initialized = True
		else:
			hoff = self.canvas.width - self.hw.sash_coord(0)[0]
			voff = self.canvas.height - self.vw.sash_coord(0)[1]
		
		self.canvas.onresize(event)
		
		def place_sash(x, y):
			self.hw.sash_place(0, x, 1)
			self.vw.sash_place(0, 1, y)
			
		self.after_idle(place_sash, event.width-hoff, event.height-voff)
		
		
		
# Entry point for the simulator	

def main():		
	root = tk.Tk()
	root.geometry("800x600+50+50")
	sim = CarNetSim(root)
	root.mainloop()
	
if __name__ == "__main__":
	main()