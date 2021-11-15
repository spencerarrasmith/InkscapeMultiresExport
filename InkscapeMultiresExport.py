import subprocess
import os
import threading
import queue
import time
import datetime

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

        self.commandQueue = queue.Queue()
        self.alive = threading.Event()
        self.startCommandThread()


    def startCommandThread(self):
        self.cmd_thread = threading.Thread(target=self.thread_commands)
        self.cmd_thread.setDaemon(1)
        self.alive.set()
        self.cmd_thread.start()

    def thread_commands(self):
        while self.alive.isSet():
            time.sleep(0.1)
            command = self.commandQueue.get()
            if command:
                self.exportstatusvar.set("Exporting " + command.split(" ")[-1])
                subprocess.call(command, shell=True)
                self.exportstatusvar.set("Done")

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

        self.exportstatusvar = tk.StringVar()
        self.exportstatuslabel = tk.Label(self, textvariable=self.exportstatusvar, width=32, justify='left')
        self.exportstatuslabel.grid(row=0, column=4, sticky=tk.W, padx=10, pady=10)

        self.savebutton = tk.Button(self, text="Save Values", command=self.saveValues)
        self.savebutton.grid(row=0, column=5, sticky=tk.W, padx=10, pady=10)

        self.loadbutton = tk.Button(self, text="Load Values", command=self.loadValues)
        self.loadbutton.grid(row=0, column=6, sticky=tk.W, padx=10, pady=10)

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
            if row.isFilled():
                for res in row.lse_out.var.get().split(','):
                    outputfile = self.inkscapefile.split(".")[0] + "_export\\" + row.lse_name.var.get() + "_" + res.strip() + ".png"

                    command = "inkscape " + self.inkscapefile + " -z -a "
                    command += row.lse_x.var.get() + ":"
                    command += row.lse_y.var.get() + ":"
                    command += str(float(row.lse_x.var.get()) + float(row.lse_w.var.get())) + ":"
                    command += str(float(row.lse_y.var.get()) + float(row.lse_h.var.get()))
                    command += " -h " + res.strip()
                    command += " -e " + outputfile

                    print("")
                    print(command)
                    self.commandQueue.put(command)

                #row.configure(bg='green')

    def saveValues(self):
        out = ""
        for row in self.rows:
            out += row.getCSV()

        filename = "exportpreset_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
        f = open(filename, 'w+')
        f.write(out)
        f.close()

    def loadValues(self):
        loadfile = filedialog.askopenfilename(initialdir="/", title="Select File",
                                                       filetypes=(("Comma-Separated Values", "*.csv"), ("All Files", "*.*")))
        f = open(loadfile, 'r')
        csv = f.read()
        f.close()

        csvrows = csv.split('\n')
        for i, row in enumerate(self.rows):
            row.fillData(csvrows[i])


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

    def isFilled(self):
        if len(self.lse_name.var.get()) \
        and len(self.lse_x.var.get()) \
        and len(self.lse_y.var.get()) \
        and len(self.lse_w.var.get()) \
        and len(self.lse_h.var.get()) \
        and len(self.lse_out.var.get()):
            return True
        else:
            return False

    def getCSV(self):
        out =  self.lse_name.var.get() + ","
        out += self.lse_x.var.get() + ","
        out += self.lse_y.var.get() + ","
        out += self.lse_w.var.get() + ","
        out += self.lse_h.var.get() + ","
        out += self.lse_out.var.get() + "\n"

        return out

    def fillData(self, data=""):
        data = data.split(",")
        i = 0
        while len(data):
            val = data.pop(0)
            try:
                self.widgets[i].var.set(val)
                i += 1
            except:
                self.widgets[-1].var.set(self.widgets[-1].var.get() + ',' + val)



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

