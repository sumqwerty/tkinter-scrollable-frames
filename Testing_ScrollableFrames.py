import tkinter as tk
from scrollFrame import *


root = tk.Tk() # creating root window

root.geometry("500x500") # Initial size of the window


windowFrame = ScrollableFrame(root) # creating a scrollable frame, since its for the whole window, size is not requried, the frame will just expand and fill the
# whole window
windowFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES) # always pack() the scrollable frame, it its a frame for the whole window, so that "fill" and "expand" options
# can be used to set the frame equal to the window


# adding alot of widgets to windowFrame


for i in range(20):
    for j in range(20):
        tk.Button(windowFrame.frame, text=f"{i},{j}", bg="yellow").grid(row=i, column=j, padx=10, pady=10) 
        ''' note that the button is added to the "frame" attribute of the
        windowFrame object(windowFrame.frame) and not directly on the windowFrame'''

root.mainloop()
