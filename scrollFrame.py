import tkinter as tk
from tkinter import ttk

rt = tk.Tk()
rt.geometry("500x500")
class ScrollableFrame():
    def __init__(self, root, _width, _height, xScroll=True, yScroll=True):
        self.root = root
        
        self.Width = _width
        self.Height = _height
        
        self.holderFrame = tk.Frame(self.root, width=self.Width, height=self.Height)
        #self.xFrame = tk.Frame(self.holderFrame, pady=0)
        #self.xFrame.pack(side=tk.BOTTOM, fill=tk.X, expand=1,pady=0)
        
        self.canvas = tk.Canvas(self.holderFrame,bg="red")
        
        
        if(xScroll):
            self.x_scrollbar = ttk.Scrollbar(self.holderFrame, orient=tk.HORIZONTAL, command=self.canvas.xview)
            self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        if(yScroll):
            self.y_scrollbar = ttk.Scrollbar(self.holderFrame, orient=tk.VERTICAL, command=self.canvas.yview)
            self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        self.frame = tk.Frame(self.canvas)
        
        def limY(event, prnt, chld):
            if not (prnt.winfo_rooty()-chld.winfo_rooty()) < 0:
                self.canvas.yview_scroll(-1, "units")
                
        self.canvas.bind('<Button-4>', lambda event: limY(event, self.frame.master, self.frame))
        self.canvas.bind('<Button-5>', lambda event: self.canvas.yview_scroll(1, "units"))
        self.frame.bind('<Button-4>', lambda event: limY(event, self.frame.master, self.frame))
        self.frame.bind('<Button-5>', lambda event: self.canvas.yview_scroll(1, "units"))        
        
        
        self.canvas.create_window((0,0), window=self.frame, anchor="n")
    
    def pack(self, side=tk.TOP, fill=tk.NONE, expand=tk.NO, anchor="n", padx=0, pady=0):
        sd = side
        fl = fill
        exp = expand
        anc = anchor
        pdx=padx
        pdy=pady
        self.holderFrame.pack(side=sd,fill=fl,expand=exp,anchor=anc,padx=pdx,pady=pdy)



superF = ScrollableFrame(rt,rt.winfo_width(), rt.winfo_height())
superF.pack(anchor="nw",fill=tk.BOTH,expand=tk.YES)

f = ScrollableFrame(superF.frame,100,100)
f.pack(anchor="nw",pady=10)


f2 = ScrollableFrame(superF.frame,100,100)
f2.pack(pady=10,side=tk.RIGHT)



for thing in range(100):
    tk.Button(superF.frame, text=f'Button {thing} Yo!').pack()
for thing in range(100):
    tk.Button(f.frame, text=f'Button {thing} Yo!').grid(row=thing, column=0, pady=20, padx=10)
	
    tk.Button(f2.frame, text=f'Button {thing} Yo!').grid(row=thing, column=0, pady=20, padx=10)
    
    


rt.mainloop()