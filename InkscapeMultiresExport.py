import subprocess
import os

import tkinter as tk
from tkinter import ttk, Tk
from tkinter import filedialog




class MultiresExportWindow(tk.Frame):
    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)

        tk.Frame.__init__(self, master=self.root)

        self.inkscapefile = ""

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.filebutton = tk.Button(self, text="Select File", command=self.openFileDialog)
        self.filebutton.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        self.openfilevar = tk.StringVar()
        self.openfilelabel = tk.Label(self, textvariable=self.openfilevar, width=32, justify='left')
        self.openfilelabel.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)

        self.addrowbutton = tk.Button(self, text="Add Row", command=self.addRow)
        self.addrowbutton.grid(row=0, column=2, sticky=tk.W, padx=10, pady=10)

        self.exportbutton = tk.Button(self, text="Export", command=self.exportFile)
        self.exportbutton.grid(row=0, column=3, sticky=tk.W, padx=10, pady=10)

        self.rows = []

        self.addRow()

    def addRow(self):
        newrow = ExportObjectRow(master=self)
        self.rows.append(newrow)
        newrow.grid(row=len(self.rows), column=0, columnspan=10, sticky=tk.W, padx=10, pady=10)


    def openFileDialog(self):
        self.inkscapefile = filedialog.askopenfilename(initialdir = "/",title = "Select File",filetypes = (("Inkscape File","*.svg"),("All Files","*.*")))

        os.chdir("\\".join(self.inkscapefile.split("/")[:-1]))
        self.inkscapefile = self.inkscapefile.split("/")[-1]

        self.openfilevar.set(self.inkscapefile)

        if not os.path.isdir(self.inkscapefile.split(".")[0] + "_export"):
            os.mkdir(self.inkscapefile.split(".")[0] + "_export")

    def exportFile(self):
        for row in self.rows:
            for res in row.lse_out.var.get().split(','):
                outputfile = self.inkscapefile.split(".")[0] + "_export\\" + row.lse_name.var.get() + "_" + res + ".png"

                command = "inkscape " + self.inkscapefile + " -z -a "
                command += row.lse_x.var.get() + ":"
                command += row.lse_y.var.get() + ":"
                command += str(float(row.lse_x.var.get()) + float(row.lse_w.var.get())) + ":"
                command += str(float(row.lse_y.var.get()) + float(row.lse_h.var.get()))
                command += " -h " + res.strip()
                command += " -e " + outputfile

                print("")
                print(command)
                subprocess.call(command, shell=True)

            row.configure(bg='green')


class BaseFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.grid()

        self.widgets = []

    def addWidgetHorizontal(self, widget=None):
        if widget:
            widget.grid(row=0, column=len(self.widgets), sticky=tk.W, padx=10, pady=10)
            self.widgets.append(widget)


class ExportObjectRow(BaseFrame):
    def __init__(self, master=None):
        super().__init__(master=master)

        self.configure(borderwidth=2, relief=tk.RAISED)

        self.lse_name = LabeledStringEntry(self, text="Name: ", width=16)
        self.addWidgetHorizontal(self.lse_name)
        self.lse_x = LabeledStringEntry(self, text="X Coord: ", width=10)
        self.addWidgetHorizontal(self.lse_x)
        self.lse_y = LabeledStringEntry(self, text="Y Coord: ", width=10)
        self.addWidgetHorizontal(self.lse_y)
        self.lse_w = LabeledStringEntry(self, text="Width: ", width=10)
        self.addWidgetHorizontal(self.lse_w)
        self.lse_h = LabeledStringEntry(self, text="Height: ", width=10)
        self.addWidgetHorizontal(self.lse_h)
        self.lse_out = LabeledStringEntry(self, text="Resolutions: ", width=16)
        self.addWidgetHorizontal(self.lse_out)


class LabeledStringEntry(BaseFrame):
    def __init__(self, master=None, text="", width=6):
        super().__init__(master=master)

        self.label = tk.Label(master=self, text=text)
        self.addWidgetHorizontal(self.label)
        self.var = tk.StringVar()
        self.entry = tk.Entry(master=self, textvariable=self.var, width=width, justify='left')
        self.addWidgetHorizontal(self.entry)



if __name__ == "__main__":
    app = MultiresExportWindow()
    app.root.title("Inkscape Multi-Resolution Export")
    app.mainloop()

