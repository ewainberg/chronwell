import tkinter as tk
from tkinter import *
from tkinter import filedialog
import csv
import numpy as np
import os

#initiate main window
window = tk.Tk()
window.title("CSV Manipulation")
window.geometry("400x360")

#initiate output variables
delimiterInput = tk.StringVar()
delimiterOutput = tk.StringVar()
rows = tk.IntVar()
columns = tk.IntVar()

#initiate and configure delimiter choosing frame
delimiterFrm = LabelFrame(window, width=200, height=110, text='Input Delimiter')
delimiterFrm.pack(pady=10)
delimiterFrm.grid_propagate(0)
delimiterFrm.update()

#initiate radio buttons
commaInput = tk.Radiobutton(delimiterFrm, text=',', variable=delimiterInput)
commaInput.config(indicatoron=0, bd=4, width=12, value=",")
commaInput.grid(row=1, column=0)

pipelineInput = tk.Radiobutton(delimiterFrm, text='|', variable=delimiterInput)
pipelineInput.config(indicatoron=0, bd=4, width=12, value="|")
pipelineInput.grid(row=1, column=1)

def close():
   window.destroy()

#initiate upload file button and function
def UploadAction(event=None):
    filetypes = (('csv files', '*.csv'),('All files', '*.*'))
    global filename
    global table
    table = []
    filename = filedialog.askopenfilename(filetypes=filetypes)
    filenameDisplay = tk.Label(delimiterFrm, text = 'Selected: ' + os.path.split(filename)[1])
    filenameDisplay.place(x=100, y=75, anchor="center")
    if delimiterInput.get() == ",":
        file = open(filename)
        csvfile = csv.reader(file)
    else:
        with open(filename) as fin:
            with open('output.csv', 'w', newline='') as fout:
                reader = csv.DictReader(fin, delimiter='|')
                writer = csv.DictWriter(fout, reader.fieldnames, delimiter=',')
                writer.writeheader()
                writer.writerows(reader)
        file = open('output.csv')
        csvfile = csv.reader(file)
    for row in csvfile:
        table.append(row)
    global rowsBox
    global columnsBox
    rowsBox = tk.Spinbox(dimensionFrm, from_=0, to=len(table), textvariable=rows, wrap=True)
    columnsBox = tk.Spinbox(dimensionFrm, from_=0, to=len(table[0]), textvariable=columns, wrap=True)
    rowsBox.grid(row=0, column=1)
    columnsBox.grid(row=1, column=1)
uploadFile = tk.Button(delimiterFrm, text="Upload File", command=UploadAction)
uploadFile.place(x=100, y=50, anchor="center")

#--------------------------------------------------#

#initiate and configure dimension choosing frame
dimensionFrm = LabelFrame(window, width=200, height=100, text='Choose Dimensions')
dimensionFrm.pack(pady=5)
dimensionFrm.grid_propagate(0)
dimensionFrm.update()

#initiate rows text display and entry box
rowsLabel = tk.Label(dimensionFrm, text="Rows:")
rowsLabel.grid(row=0, column=0)

#initiate columns text display and entry box
columnsLabel = tk.Label(dimensionFrm, text="Columns:")
columnsLabel.grid(row=1, column=0)
#--------------------------------------------------#

#initiate delimiter output choosing frame
delimiterOutputFrm = LabelFrame(window, width=200, height=100, text='Output Delimiter')
delimiterOutputFrm.pack(pady=10)
delimiterOutputFrm.grid_propagate(0)
delimiterOutputFrm.update()

#initiate radio buttons
commaInput = tk.Radiobutton(delimiterOutputFrm, text=',', variable=delimiterOutput)
commaInput.config(indicatoron=0, bd=4, width=12, value=",")
commaInput.grid(row=1, column=0)

pipelineInput = tk.Radiobutton(delimiterOutputFrm, text='|', variable=delimiterOutput)
pipelineInput.config(indicatoron=0, bd=4, width=12, value="|")
pipelineInput.grid(row=1, column=1)

#initiate upload file button
outputFile = tk.Button(delimiterOutputFrm, text="Generate Output", command = close)
outputFile.place(x=100, y=50, anchor="center")

#program loop
window.mainloop()

#debug
rowLimit = rows.get()
columnLimit = columns.get()
chosenDelimiter = delimiterOutput.get()

#manipulation
newTable = []
newRow = []


for row in table:
    for element in range(0, columnLimit):
        newRow.append(row[element])
    newTable.append(newRow)
    newRow = []
for row in range(len(newTable)-1, rowLimit, -1):
    newTable.pop(row)

numpyArray = np.array(newTable)

if chosenDelimiter == ",":
    np.savetxt('output.csv', numpyArray, delimiter=',', fmt='%s')
else:
    np.savetxt('output.csv', numpyArray, delimiter='|', fmt='%s')
