from color import Color
from kmap16 import Kmap16 
import tkinter as tk
"""
GUI class for displaying a 4x4 Kavanaugh map. Gathers user input, and delivers a simplified
equation by calling Kmap16.
"""
class Gui:
    
    """
    Creates the window along with global variables and calls needed functions
    """
    def __init__(self):
        self.color = Color()
        self.k = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.label_list={}
        self.window = tk.Tk()
        self.nav_list = ["4x4"]
        self.window.geometry('500x400')
        self.create_nav()
        self.body = self.create_body()
        self.create_grid16()
        self.results = self.create_result_box()
        self.window.resizable(False, False) 
        #print(self.label_list) #for debugging
        self.window.mainloop()
    
    """
    Creates the Navigation bar
    """
    def create_nav(self):
        navbar = tk.Frame(master=self.window, width=500, height=50, bg="gray")
        navbar.pack(fill=tk.BOTH, side=tk.TOP, expand=False)
        navgrid = tk.Frame(master=navbar)
        
        for i in range(len(self.nav_list)):
            navgrid.grid(row=0, column=i)
            label = tk.Label(master=navgrid, text=f"{self.nav_list[i]}", padx=20, pady=20, bg="gray")
            label.pack(side=tk.LEFT)
    
    """
    Creates the Body of the app
    
    Returns: body Frame
    """
    def create_body(self):
        body = tk.Frame(master=self.window, width=500, height=350, bg="white")
        body.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)
        return body
    
    """
    Creates a 4x4 grid of labels for 4x4 kmaps
    """
    def create_grid16(self):
        for i in range(4):
            self.body.columnconfigure(i, weight=1, minsize=75)
            self.body.rowconfigure(i, weight=1, minsize=75)
            for j in range(4):
                frame = tk.Frame(
                    master=self.body,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j, padx=5, pady=5)
                label = tk.Label(master=frame, text=f"0", padx=20, pady=15)
                label.bind("<Button-1>", self.handle_click_grid)
                self.label_list[label] = (i, j)
                label.pack()
    
    """
    Handles clicks for labels in create_grid16
    """
    def handle_click_grid(self, event):
        caller = event.widget
        coords = self.label_list[caller]
        print("Clicked at coords: " + str(coords))
        row = coords[0]
        col = coords[1]
        if self.k[row][col] == 0:
            self.k[row][col] = 1
            caller["text"] = "1"
        else:
            self.k[row][col] = 0
            caller["text"] = "0"
    
    """
    Creates the result frame which holds the solve label and the result label
    
    Returns: result Label
    """
    def create_result_box(self):
        result_box = tk.Frame(master=self.window, width=500, height=100)
        result_box.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)
        label = tk.Label(master=result_box, text=f"Solve", padx=20, pady=20, bg=self.color.DARKGREEN)
        label.bind("<Button-1>", self.handle_click_solve)
        label.pack(side=tk.LEFT)
        results = tk.Label(master=result_box, text=f"", padx=20, pady=20)
        results.pack(side=tk.LEFT)
        
        return results
    
    """
    Handles clicks to the solve label. Calls Kmap16 for the creation, simplification,
    and returning of input data in string form. Sets result label to simplified
    equation
    """
    def handle_click_solve(self, event):
        caller = event.widget
        kmap = Kmap16()
        kmap.K = self.k
        kmap.start()
        self.results["text"] = kmap.simplify_equations(kmap.create_equations_from_boxes(kmap.create_boxes()))