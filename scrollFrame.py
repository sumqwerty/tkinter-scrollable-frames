import tkinter as tk
from tkinter import ttk


class MakeFrame(tk.Frame):
    def __init__(self, root, width=None, height=None, xScroll=True, yScroll=True, bdThickness=0, bdColor=None):
        
        super().__init__(root, width=width, height=height, highlightthickness=bdThickness)
        self.config(highlightbackground=bdColor, highlightcolor=bdColor)
        
        self.root = root
        
        self.Width = width
        self.Height = height
        
        self.canvas = tk.Canvas(self, width=self.master.winfo_reqwidth(), height=self.master.winfo_reqheight())
        
        if(xScroll):
            self.x_scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
            self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        if(yScroll):
            self.y_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
            self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.pack(side=tk.LEFT,fill=tk.BOTH, expand=tk.YES)
        if(xScroll):
            self.canvas.configure(xscrollcommand=self.x_scrollbar.set)
        if(yScroll):
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

class ScrollableFrame(tk.Frame):
    def __init__(self,root,width=None,height=None, xScroll=True, yScroll=True, bdThickness=0, bdColor=None, label=None):
        super().__init__(root,width=width,height=height)
        scrollFrame = MakeFrame(self, xScroll=xScroll, yScroll=yScroll, bdThickness=bdThickness, bdColor=bdColor)
        scrollFrame.pack(side=tk.TOP,fill=tk.BOTH,expand=tk.YES, anchor="nw")
        self.frame = scrollFrame.frame
        if not label == None:
            tk.Label(self,text=label).pack()


if __name__ == "__main__":
    
    def AddManyWidgetsX(frm):
        lim = 20
        for i in range(1,lim):
            tk.Button(frm,text=f'{i}').grid(row=0,column=i,padx=20,pady=100)
            
    
    def AddManyWidgetsY(frm):
        lim = 20
        for i in range(0,lim):
            tk.Button(frm,text=f'{i}').grid(row=i,column=0,padx=100,pady=20)
            
    def AddManyWidgetsXY(frm):
        lim = 20
        for i in range(lim):
            for j in range(lim):
                tk.Button(frm,text=f'{i},{j}').grid(row=i,column=j,padx=5,pady=5)

    rt = tk.Tk()
    rt.title("Scrollable Frames")
    rt.geometry("600x600")
    
    superF = ScrollableFrame(rt,bdThickness=10, bdColor="maroon")
    superF.pack(fill=tk.BOTH, expand=tk.YES)
    
    paddingx = 50
    
    
    f1 = ScrollableFrame(superF.frame, width=300, height=300, bdThickness=4, bdColor="red", label="X Scrollbar")
    f1.grid(row=0, column=0, padx=paddingx, pady=20)
    AddManyWidgetsX(f1.frame)
    
    
    
    f2 = ScrollableFrame(superF.frame, width=300,height=300, bdThickness=4, bdColor="green", label="Y Scrollbar")
    f2.grid(row=1, column=0, padx=paddingx, pady=20)
    AddManyWidgetsY(f2.frame)
    
    f3 = ScrollableFrame(superF.frame, width=300,height=300, bdThickness=4, bdColor="blue", label="X and Y Scrollbar")
    f3.grid(row=2, column=0, padx=paddingx, pady=20)
    AddManyWidgetsXY(f3.frame)
    
    
    
    f4 = ScrollableFrame(superF.frame, 300, 300, bdThickness=4, bdColor="yellow", label="Empty frame")
    f4.grid(row=0, column=1, padx=paddingx, pady=20)
    
    f5 = ScrollableFrame(superF.frame, width=300,height=300, bdThickness=4, bdColor="cyan", label="No Scrollbar")
    f5.grid(row=1, column=1, padx=paddingx, pady=20)
    tk.Button(f5.frame,text="qwerty").pack(padx=100,pady=100)
    
    
    f6 = ScrollableFrame(superF.frame, 300,300, bdThickness=4, bdColor="indian red", label="Nested Frames")
    f6.grid(row=2, column=1, padx=paddingx, pady=20)
    ScrollableFrame(f6.frame, 200,200, bdThickness=4, bdColor="gold").pack(side=tk.TOP, anchor="nw", padx=50, pady=50)
    
    
    
    f7 = ScrollableFrame(superF.frame, 300,300, xScroll=False, bdThickness=4, bdColor="black", label="Only Y Scrollbar visible")
    f7.grid(row=0, column=2, padx=paddingx, pady=20)
    AddManyWidgetsY(f7.frame)
    
    f8 = ScrollableFrame(superF.frame, 300,300, yScroll=False, bdThickness=4, bdColor="orange", label="Only X Scrollbar visible")
    f8.grid(row=1, column=2, padx=paddingx, pady=20)
    AddManyWidgetsX(f8.frame)
    
    f9 = ScrollableFrame(superF.frame, 200,150, bdThickness=4, bdColor="dodger blue", label="Custom Sized")
    f9.grid(row=2, column=2, padx=paddingx, pady=20)
    AddManyWidgetsXY(f9.frame)
    
    rt.mainloop()