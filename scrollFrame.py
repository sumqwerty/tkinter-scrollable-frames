import tkinter as tk
from tkinter import ttk


class MakeFrame(tk.Frame):
    def __init__(self, root, width=None, height=None, container=False, xScroll=True, yScroll=True, bdThickness=0, bdColor=None):
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
        
        def windowWheel(event, prnt, child):
            if event.num == 5 or event.delta == -120:
                self.canvas.yview_scroll(1, "units")
                
            if event.num == 4 or event.delta == 120:
                limY(event, prnt, child)
                
        
        def eventBind():
            self.canvas.bind('<MouseWheel>', lambda event: windowWheel(event, self.frame.master, self.frame))
            self.canvas.bind('<Button-4>', lambda event: limY(event, self.frame.master, self.frame))
            self.canvas.bind('<Button-5>', lambda event: self.canvas.yview_scroll(1, "units"))
        
            self.frame.bind('<MouseWheel>', lambda event: windowWheel(event, self.frame.master, self.frame))
            self.frame.bind('<Button-4>', lambda event: limY(event, self.frame.master, self.frame))
            self.frame.bind('<Button-5>', lambda event: self.canvas.yview_scroll(1, "units"))
        
        def eventBindAll():
            self.canvas.bind_all('<MouseWheel>', lambda event: windowWheel(event, self.frame.master, self.frame))
            self.canvas.bind_all('<Button-4>', lambda event: limY(event, self.frame.master, self.frame))
            self.canvas.bind_all('<Button-5>', lambda event: self.canvas.yview_scroll(1, "units"))

        def eventRemove():
            self.canvas.unbind_all('<MouseWheel>')
            self.canvas.unbind_all('<Button-4>')
            self.canvas.unbind_all('<Button-5>')
          
            
        self.canvas.bind('<Enter>', lambda event: eventBindAll() if not container else eventBind())
        self.canvas.bind('<Leave>', lambda event: eventRemove())
        
        self.frame.bind('<Enter>', lambda event: eventBindAll() if not container else eventBind())
        self.frame.bind('<Leave>', lambda event: eventRemove())
            
        self.canvas.create_window((0,0), window=self.frame, anchor="n")

class ScrollableFrame(tk.Frame):
    def __init__(self,root,width=None,height=None, container=False, xScroll=True, yScroll=True, bdThickness=0, innerbdThickness=0, bdColor="gray25", innerbdColor="black", label=None):
        super().__init__(root,width=width,height=height, highlightthickness=bdThickness)
        self.config(highlightbackground=bdColor, highlightcolor=bdColor)
        scrollFrame = MakeFrame(self, container=container, xScroll=xScroll, yScroll=yScroll, bdThickness=innerbdThickness, bdColor=innerbdColor)
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
    
    superF = ScrollableFrame(rt, container=True , bdThickness=10, bdColor="maroon")
    superF.pack(fill=tk.BOTH, expand=tk.YES)
    
    paddingx = 50
    
    
    f1 = ScrollableFrame(superF.frame, width=300, height=300, innerbdThickness=4, innerbdColor="red", label="X Scrollbar")
    f1.grid(row=0, column=0, padx=paddingx, pady=20)
    AddManyWidgetsX(f1.frame)
    
    
    
    f2 = ScrollableFrame(superF.frame, width=300,height=300, innerbdThickness=4, innerbdColor="green", label="Y Scrollbar")
    f2.grid(row=1, column=0, padx=paddingx, pady=20)
    AddManyWidgetsY(f2.frame)
    
    f3 = ScrollableFrame(superF.frame, width=300,height=300, innerbdThickness=4, innerbdColor="blue", label="X and Y Scrollbar")
    f3.grid(row=2, column=0, padx=paddingx, pady=20)
    AddManyWidgetsXY(f3.frame)
    
    
    
    f4 = ScrollableFrame(superF.frame, 300, 300, bdThickness=4, bdColor="yellow", innerbdThickness=4, innerbdColor="dark green", label="Empty frame with Frame and Container borders.")
    f4.grid(row=0, column=1, padx=paddingx, pady=20)
    
    f5 = ScrollableFrame(superF.frame, width=300,height=300, innerbdThickness=4, innerbdColor="cyan", label="No Scrollbar")
    f5.grid(row=1, column=1, padx=paddingx, pady=20)
    tk.Button(f5.frame,text="qwerty").pack(padx=100,pady=100)
    
    
    f6 = ScrollableFrame(superF.frame, 300,300, container=True, innerbdThickness=4, innerbdColor="indian red", label="Nested Frames")
    f6.grid(row=2, column=1, padx=paddingx, pady=20)
    ScrollableFrame(f6.frame, 200,200, bdThickness=4, bdColor="gold").pack(side=tk.TOP, anchor="nw", padx=50, pady=50)
    
    
    
    f7 = ScrollableFrame(superF.frame, 300,300, xScroll=False, innerbdThickness=4, innerbdColor="black", label="Only Y Scrollbar visible")
    f7.grid(row=0, column=2, padx=paddingx, pady=20)
    AddManyWidgetsY(f7.frame)
    
    f8 = ScrollableFrame(superF.frame, 300,300, yScroll=False, innerbdThickness=4, innerbdColor="orange", label="Only X Scrollbar visible")
    f8.grid(row=1, column=2, padx=paddingx, pady=20)
    AddManyWidgetsX(f8.frame)
    
    f9 = ScrollableFrame(superF.frame, 200,1500, innerbdThickness=4, innerbdColor="dodger blue", label="Custom Sized")
    f9.grid(row=2, column=2, padx=paddingx, pady=20)
    AddManyWidgetsXY(f9.frame)
    
    rt.mainloop()
