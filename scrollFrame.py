import tkinter as tk
from tkinter import ttk

# ############################################################################################################################
# To make a scrollable frame, Scrollable frame class first creates a container tkinter frame, then adds another frame in it 
# called the Holder frame. Then a canvas is added to the Holder frame.
# Vertical and horizontal scrollbars are added to the holder frames and are attached to scroll the canvas
# Now since widgets CANNOT be placed directly on the canvas another frame is created. This is the frame on which the widgets
# are added.
# After creating the frame, a window is created inside the canvas, and the frame is set as the window for the canvas
# ############################################################################################################################


# MakeFrame class: creates a scrollable frame
class MakeFrame(tk.Frame):
    def __init__(self, root, width=None, height=None, container=False, xScroll=True, yScroll=True, bdThickness=0, bdColor=None):
        # root (tkinter widget): parent widget
        # width, height (integer value): dimensions of the frame
        # xScroll (boolean, default: True): allow horizontal Scrollbar
        # yScroll (boolean, default: True): allow vertical Scrollbar
        # bdThickness (integer value, default: 0): creates a border for the scrollable frame
        # bdColor (string value, defalut: "black"): color of the frame border
        
        
        # calling super class constrcutor and creating a tk.Frame, Holder frame
        super().__init__(root, width=width, height=height, highlightthickness=bdThickness)
        self.config(highlightbackground=bdColor, highlightcolor=bdColor) # applying container borders
        
        # intializing the parent widget refrence variable and dimensions
        self.root = root
        self.Width = width
        self.Height = height
        
        # creating a canvas to attach a scrollbar to, and place the final frame into
        self.canvas = tk.Canvas(self, width=self.master.winfo_reqwidth(), height=self.master.winfo_reqheight())
        
        # add horizontal scrollbar
        if(xScroll):
            # creating a scrollbar object for horizontal scrolling and attaching it to the canvas by setting 
            # its command to the xview of the canvas
            self.x_scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview) 
            self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X) # packing horizontal scrollbar on the holder frame
        
        # add vertical scrollbar
        if(yScroll):
            # creating a scrollbar object for vertical scrolling and attaching it to the canvas by setting 
            # its command to the yview of the canvas
            self.y_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
            self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # packing vertical scrollbar on the holder frame
        
        self.canvas.pack(side=tk.LEFT,fill=tk.BOTH, expand=tk.YES) # packing the canvas in the holder and filling it up
        
        # configuring the canvas to scroll when the scrollbars are moved
        if(xScroll):
            self.canvas.configure(xscrollcommand=self.x_scrollbar.set) # horizontal scrolling configuration
        if(yScroll):
            self.canvas.configure(yscrollcommand=self.y_scrollbar.set) # vertical scrolling configuration
        
        # setting a the scrollable area for the canvas to the whole canvas
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        
        # creating the frame to put the widgets in 
        self.frame = tk.Frame(self.canvas)
        
        # limitng the y scroll to 0, (this is done because the y scroll kept going in negative)
        def limY(event, prnt, chld):
            if not (prnt.winfo_rooty()-chld.winfo_rooty()) < 0:
                self.canvas.yview_scroll(-1, "units")
        
        # scrolling the frame using the mouse wheel when on Windows OS
        def windowWheel(event, prnt, child):
            if event.num == 5 or event.delta == -120:
                self.canvas.yview_scroll(1, "units")
                
            if event.num == 4 or event.delta == 120:
                limY(event, prnt, child)
                
        
        # binding mouse wheel events to the canvas, frame [for container frames(scrollable frames that contain other scrollable frames)]
        # when the cursor enters a frame or a canvas
        def eventBind():
            # binding to the canvas
            self.canvas.bind('<MouseWheel>', lambda event: windowWheel(event, self.frame.master, self.frame)) # MouseWheel event for Windows OS
            self.canvas.bind('<Button-4>', lambda event: limY(event, self.frame.master, self.frame)) # up scroll MouseWheel event for Linux
            self.canvas.bind('<Button-5>', lambda event: self.canvas.yview_scroll(1, "units")) # down scroll MouseWheel event for Linux
        
            # binding to the frame
            self.frame.bind('<MouseWheel>', lambda event: windowWheel(event, self.frame.master, self.frame))
            self.frame.bind('<Button-4>', lambda event: limY(event, self.frame.master, self.frame))
            self.frame.bind('<Button-5>', lambda event: self.canvas.yview_scroll(1, "units"))
        
        # binding mouse wheel events to the canvas and all the widgets in it(for a non container frame), when the cursor enters a non container frame
        def eventBindAll():
            self.canvas.bind_all('<MouseWheel>', lambda event: windowWheel(event, self.frame.master, self.frame))
            self.canvas.bind_all('<Button-4>', lambda event: limY(event, self.frame.master, self.frame))
            self.canvas.bind_all('<Button-5>', lambda event: self.canvas.yview_scroll(1, "units"))
            
        # removing all event bindings when the cursor leaves the scrollable frames, this prevents weird things from happening 
        # when multiple nested windows are created
        def eventRemove():
            self.canvas.unbind_all('<MouseWheel>')
            self.canvas.unbind_all('<Button-4>')
            self.canvas.unbind_all('<Button-5>')
          
        
        # mouse enter and leave events for the canvas to add remove the mouse wheel event bindings
        self.canvas.bind('<Enter>', lambda event: eventBindAll() if not container else eventBind())
        self.canvas.bind('<Leave>', lambda event: eventRemove())
        
        # mouse enter and leave events for the frame to add remove the mouse wheel event bindings
        #self.frame.bind('<Enter>', lambda event: eventBindAll() if not container else eventBind())
        #self.frame.bind('<Leave>', lambda event: eventRemove())
        
        # creating a "virtual" window in the canvas and setting the self.frame as the window
        self.canvas.create_window((0,0), window=self.frame, anchor="n")
        
        # when putting widgets in the scrollable frame, the widgets are actually being placed in self.frame


# ScrollableFrame class: creates the frame container and calls MakeFrame class to create a scrollable frame class
class ScrollableFrame(tk.Frame):
    def __init__(self,root,width=None,height=None, container=False, xScroll=True, yScroll=True, bdThickness=0, innerbdThickness=0, bdColor="gray25", innerbdColor="black", label=None):
        # root (tkinter widget, REQURIED): parent widget
        # width, height (integer value, OPTINAL WHEN MAKING A FULL ROOT WINDOW SIZED FRAME): dimensions of the frame
        # container (boolean, default: False): if the scrollable frame will contain another scrollable frame, 
        #                                      for e.g a full window frame that contains other frames
        # xScroll (boolean, default: True, OPTIONAL): allow horizontal Scrollbar
        # yScroll (boolean, default: True, OPTIONAL): allow vertical Scrollbar
        # bdThickness (integer value, default: 0, OPTIONAL): creates a border for the frame container (encloses the label)
        # innerbdThickness (integer value, default: 0, OPTIONAL): creates a border for the frame (not enclosing the label)
        # bdColor (string value, defalut: "gray25", OPTIONAL): color of the continer border
        # innerbdColor (string value, defalut: "black", OPTIONAL): color of the frame border
        # label (string value, OPTIONAL): text label for the frame
        
        
        # calling super class constrcutor and creating a tk.Frame, Container frame
        super().__init__(root,width=width,height=height, highlightthickness=bdThickness) 

        self.config(highlightbackground=bdColor, highlightcolor=bdColor) # applying container borders
        
        # CALLING MakeFrame CLASS TO CREATE A SCROLLABLE FRAME IN THE CONTAINER
        scrollFrame = MakeFrame(self, container=container, xScroll=xScroll, yScroll=yScroll, bdThickness=innerbdThickness, bdColor=innerbdColor)
        scrollFrame.pack(side=tk.TOP,fill=tk.BOTH,expand=tk.YES, anchor="nw") 
        
        self.frame = scrollFrame.frame # frame object on which widgets will be placed,
        # IT IS TO NOTE THAT, WIDGETS CAN'T BE PLACED DIRECTLY ON THE ScrollableFrame OBJECT, IT IS TO BE PLACED ON THE 
        # frame ATTRIBUTE OF THE ScrollableFrame OBJECT LIKE, tk.widget(ScrollableFrameObj.frame)
        
        # creating a label for the scrollable frame
        if not label == None:
            tk.Label(self,text=label).pack()


# DEMO ##################################################################################################################
if __name__ == "__main__":
    
    def AddManyWidgetsX(frm): # creating 20 button widgets in a single row
        lim = 20
        for i in range(1,lim):
            tk.Button(frm,text=f'{i}').grid(row=0,column=i,padx=20,pady=100)
            
    
    def AddManyWidgetsY(frm): # creating 20 button widgets in a single column
        lim = 20
        for i in range(0,lim):
            tk.Button(frm,text=f'{i}').grid(row=i,column=0,padx=100,pady=20)
            
    def AddManyWidgetsXY(frm): # creating a grid of 400 button widgets a 20x20 grid
        lim = 20
        for i in range(lim):
            for j in range(lim):
                tk.Button(frm,text=f'{i},{j}').grid(row=i,column=j,padx=5,pady=5)


    rt = tk.Tk() # root window
    rt.title("Scrollable Frames") # window title
    rt.geometry("600x600") # initial size of the window
    
    # creating a frame for the whole window
    # this frame will act the the root for all the widgets that will be added, it is the same size as the window.
    # this gives an effect of a scrollable window
    superF = ScrollableFrame(rt, container=True , bdThickness=10, bdColor="maroon") # no size provided since it will expand to
    # window size, when ever the window is resized. Since its a frame for the whole window and it will contain some other scrollable frame
    # the container attribute is set to True.
    
    superF.pack(fill=tk.BOTH, expand=tk.YES) # adding the scrollable frame to the root window and allowing it to take all the window space
    
    
    paddingx = 50
    
    # Scrollable frame with only horizonal scroll bar active
    # ####################################################################################
    # ################################################################################## #
    #                                                                                    #
    # f1 SCROLLABLE FRAME IS ADDED TO superF.frame AND NOT DIRECTLY TO superF.           #
    #                                                                                    #
    # ANY WIDGET THAT IS TO BE ADDED ON THE SCROLLABLE FRAME SHOULD BE ADDED TO THE      #
    # "frame" ATTRIBUTE OF THE ScrollableFrame object.                                   #
    #                                                                                    #
    # ################################################################################## #
    # ####################################################################################
    f1 = ScrollableFrame(superF.frame, width=300, height=300, innerbdThickness=4, innerbdColor="red", label="X Scrollbar") # f1 is added to superF.frame and not directly on superF
    f1.grid(row=0, column=0, padx=paddingx, pady=20)
    AddManyWidgetsX(f1.frame)
    
    
    # Scrollable frame with only vertical scroll bar active
    f2 = ScrollableFrame(superF.frame, width=300,height=300, innerbdThickness=4, innerbdColor="green", label="Y Scrollbar") # f2 is added to superF.frame and not directly on superF
    f2.grid(row=1, column=0, padx=paddingx, pady=20)
    AddManyWidgetsY(f2.frame)
    
    # Scrollable frame with both horizontal and vertical scroll bars active
    f3 = ScrollableFrame(superF.frame, width=300,height=300, innerbdThickness=4, innerbdColor="blue", label="X and Y Scrollbar") # f3 is added to superF.frame and not directly on superF
    f3.grid(row=2, column=0, padx=paddingx, pady=20)
    AddManyWidgetsXY(f3.frame)
    
    
    # An Empty frame with both horizontal and vertical scroll inactive, and having double borders, one on the frame and other on the container
    f4 = ScrollableFrame(superF.frame, 300, 300, bdThickness=4, bdColor="yellow", innerbdThickness=4, innerbdColor="dark green", label="Empty frame with Frame and Container borders.") # f4 is added to superF.frame and not directly on superF
    f4.grid(row=0, column=1, padx=paddingx, pady=20)
    
    
    # A Non empty scrollbar but with inactive horizonal and vertical scrollbars
    f5 = ScrollableFrame(superF.frame, width=300,height=300, innerbdThickness=4, innerbdColor="cyan", label="No Scrollbar") # f5 is added to superF.frame and not directly on superF
    f5.grid(row=1, column=1, padx=paddingx, pady=20)
    tk.Button(f5.frame,text="qwerty").pack(padx=100,pady=100)
    
    # A frame containg another frame, Nested Frames
    f6 = ScrollableFrame(superF.frame, 300,300, container=True, innerbdThickness=4, innerbdColor="indian red", label="Nested Frames") # f6 is added to superF.frame and not directly on superF
    f6.grid(row=2, column=1, padx=paddingx, pady=20)
    ScrollableFrame(f6.frame, 200,200, bdThickness=4, bdColor="gold").pack(side=tk.TOP, anchor="nw", padx=50, pady=50)
    
    
    # Frame with horizonal scroll disabled all together, providing only a vertical scrollbar
    f7 = ScrollableFrame(superF.frame, 300,300, xScroll=False, innerbdThickness=4, innerbdColor="black", label="Only Y Scrollbar visible") # f7 is added to superF.frame and not directly on superF
    f7.grid(row=0, column=2, padx=paddingx, pady=20)
    AddManyWidgetsY(f7.frame)
    
    # Frame with vertical scroll disabled all together, providing only a horizontal scrollbar
    f8 = ScrollableFrame(superF.frame, 300,300, yScroll=False, innerbdThickness=4, innerbdColor="orange", label="Only X Scrollbar visible") # f8 is added to superF.frame and not directly on superF 
    f8.grid(row=1, column=2, padx=paddingx, pady=20)
    AddManyWidgetsX(f8.frame)
    
    # Frame with non rectangular dimension (its possible to size the scrollable frame) 
    f9 = ScrollableFrame(superF.frame, 200,150, innerbdThickness=4, innerbdColor="dodger blue", label="Custom Sized") # f9 is added to superF.frame and not directly on superF
    f9.grid(row=2, column=2, padx=paddingx, pady=20)
    AddManyWidgetsXY(f9.frame)
    
    rt.mainloop()
