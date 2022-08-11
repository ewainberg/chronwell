from tkinter import *
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
from pathlib import Path
import os
import csv

#upload file dialog command
def upload(event=None):
    global table, headers, filename, filepath, filenameDisplay 
    headers = []
    filetypes = (('csv files', '*.csv'),('All files', '*.*'))
    filename = filedialog.askopenfilename(filetypes=filetypes)
    pandasFile = pd.read_csv(filename)
    table = pandasFile.to_numpy()
    filepath = os.path.split(filename)[0]
    head = pandasFile.columns
    
    if delimiterInput.get() == '|':
        with open(filename) as fin:
            with open('output.csv', 'w', newline='') as fout:
                reader = csv.DictReader(fin, delimiter='|')
                writer = csv.DictWriter(fout, reader.fieldnames, delimiter=',')
                writer.writeheader()
                writer.writerows(reader)
        file = open('output.csv')
        csvfile = csv.reader(file)
        table = []
        for row in csvfile:
            table.append(row)
        head = table.pop(0)

    #creates header array for later, useful for indetifying indexes by string
    for i in range(0, len(head)):
        headers.append(head[i])

    filenameDisplay = tk.Label(delimiterInputFrame, text = 'Selected: ' + os.path.split(filename)[1])
    
    #makes delimiter input frame bigger to fit file name
    delimiterInputFrame.configure(height = 95, width = 150)
    filenameDisplay.place(relx = 0.5, rely = 0.86, anchor = "center")
    uploadButton.place(rely = 0.5)

    #sets values of row and column variables for scrollboxes
    rows.set(len(table))
    columns.set(len(table[0]))

    #sets scrollbox values and ungreys them
    rowsBox.configure(from_=0, to=len(table), state = NORMAL) 
    columnsBox.configure(from_=0, to=len(table[0]), state = NORMAL)

    #ungreys output button
    generateOutput.configure(state = NORMAL)

#function for generating an upload button, takes x, y coords, name of command function, and the window it should be in
def generateUploadButton(relx, rely, command, frame):
    global uploadButton
    uploadButton = tk.Button(frame, text="Upload File", command=command)
    if(delimiterInput.get() =='none'):
        uploadButton.configure(state = DISABLED)
    uploadButton.place(relx=relx, rely=rely, anchor="center")

#generate output delimiter frame with specified width, height, text, and a parameter to include an upload button
def generateDelimiterInputFrame(window, width, height, xpos, ypos, text, uploadButton):
    global delimiterInputFrame
    delimiterInputFrame = LabelFrame(window, width=width, height=height, text=text)
    pipelineInput = tk.Radiobutton(delimiterInputFrame, text='|', variable=delimiterInput, value = '|')
    commaInput = tk.Radiobutton(delimiterInputFrame, text=',', variable=delimiterInput, value = ',')
    commaInput.place(relx = 0.25, rely = 0.15, anchor = "center")
    pipelineInput.place(relx = 0.75, rely = 0.15, anchor = "center")
    delimiterInputFrame.place(relx = 0.5, rely = 0.17, anchor="center")
    if uploadButton:
        generateUploadButton(0.5, 0.6, upload, delimiterInputFrame)

def onDelimiterInputChange(*args):
    global flag
    if delimiterInput.get() == 'none':
        uploadButton.configure(state = tk.DISABLED)
    else:
        uploadButton.configure(state = tk.NORMAL)
        if(not flag):
            delimiterOutput.set(delimiterInput.get())
            flag = True

def generateDimensionFrm(window, width, height, xpos, ypos, text):
    global rowsBox, columnsBox
    dimensionFrm = LabelFrame(window, width=width, height=height, text=text)
    rowsLabel = tk.Label(dimensionFrm, text="Rows:")
    columnsLabel = tk.Label(dimensionFrm, text="Columns:")
    rowsBox = tk.Spinbox(dimensionFrm, state = DISABLED, textvariable=rows, wrap = True)
    columnsBox = tk.Spinbox(dimensionFrm, state = DISABLED, textvariable=columns, wrap = True)
    dimensionFrm.place(relx = xpos, rely = ypos, anchor="center")
    rowsLabel.place(relx = 0.05, rely = 0.05)
    columnsLabel.place(relx = 0.001, rely = 0.5)
    rowsBox.place(relx = 0.29, rely = 0.06)
    columnsBox.place(relx = 0.29, rely = 0.55)

def generateDelimiterOutputFrame(window, width, height, xpos, ypos, text):
    global generateOutput
    delimiterOutputFrame = LabelFrame(window, width=width, height=height, text=text)
    pipelineOutput = tk.Radiobutton(delimiterOutputFrame, text='|', variable=delimiterOutput, value = '|')
    commaOutput = tk.Radiobutton(delimiterOutputFrame, text=',', variable=delimiterOutput, value = ',')
    generateOutput = tk.Button(delimiterOutputFrame, text="Generate Output", command= lambda: main(table), state = DISABLED)
    commaOutput.place(relx = 0.1)
    pipelineOutput.place(relx = 0.6)
    generateOutput.place(relx = 0.5, rely = 0.6, anchor = "center")
    delimiterOutputFrame.place(relx = xpos, rely = ypos, anchor="center")

#finds the column of a specified header and returns it
def findHeader(inputHeader):
    if inputHeader in headers:
        return headers.index(inputHeader)
    else:
        return -1


#returns the sum of units of a specified program ID, takes a table and programID string as parameters
def getUnitSumOfID(table, programId):
    total = 0
    for row in table:
        if row[findHeader("ProgramID")] == programId:
            total = total + int(row[findHeader("Units")])
    return total

#returns the sum of all elements in a column
def getSumOfColumn(table, column):
    total = 0
    for row in table:
        total = total + int(row[column])
    return total

#saves sheets into an xls file, with paremeters of a string and two arrays.
#the string should be the file name of the xls
#the first array should be a list of the data tables
#The second array should be a list of the names of the sheets, respective to the order of the first array
def saveSheets(fileName, sheetData, sheetNames):
    counter = 0
    writer = pd.ExcelWriter(fileName)
    if len(sheetData) != len(sheetNames):
        print("Please make sure sheets and sheetNames arrays are same size!")
    for element in range(0, len(sheetData)):
        sheetData[element].to_excel(writer, sheet_name=sheetNames[element], index=False)
    writer.save()
    writer.handles = None

#returns a list of all unique elements in specified column
def uniquesInColumn(table, column):
    uniques = []
    for row in table:
        if row[column] not in uniques:
            uniques.append(row[column])
    return uniques

#takes original value and a percentage user wishes to deduct from original, returns original with percentage deducted
def deductPercent(originalAmount, percentage):
    return originalAmount - (originalAmount*(percentage/100))

#if directory does not exist, create specified directory
def create_dir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

#main function, with a specified array as an input
def main(table):
    global filename, filenameDisplay, generateOutput
    generateOutput.configure(state = DISABLED)
    csvTable = table
    #gets practice type from file name
    practiceType = Path(filename).stem

    #initiates tempTable variable of iteration of original table
    tempTable = []

    #inserts revenue column into table, finding the header indexes for the salary and bill columns automatically, only if table is type A1
    if practiceType == "A1":
        headers.append("Revenue")
        for row in table:
            row = np.append(row, row[findHeader("Salary")] - row[findHeader("Bills")])
            tempTable.append(row.tolist())
        table = tempTable

    #applies salary and appends extra column, only if table is type B1
    if practiceType == "B1":
        headers.append("Salary after tax")
        for row in table:
            row = np.append(row, deductPercent(row[findHeader("Salary")], findHeader("Tax %")))
            tempTable.append(row.tolist())
        table = tempTable

    #compares revenue to car price and appens extra columns, only if table is type C1
    if practiceType == "C1":
        headers.append("Can Afford Car")
        for row in table:
            if row[findHeader("Car Price")] <= (row[findHeader("Salary")] - row[findHeader("Bills")]):
                row = np.append(row, "True")
            else:
                row = np.append(row, "False")
            tempTable.append(row.tolist())
        table = tempTable
                

    #finds all unique program ids for later iteration
    programIDs = uniquesInColumn(table, findHeader("ProgramID"))
    programIDs.sort() #sorts the IDs for aesthetic pleasure

    #initiates summary array
    summary = []

    #iterates through IDs, finds its unit sum, and appends its to the table
    for ID in programIDs:
        summary.append([ID, getUnitSumOfID(table, ID)])
    summary.append(["Total Units", getSumOfColumn(table, findHeader("Units"))])
    summaryDataFrame = pd.DataFrame(summary, columns = ["Program IDs","Sum of Units"])

    #calls savesheets function to save sheets into file, converts array into numpy array then into pandas dataframe to be exported into xls
    dataFrame = pd.DataFrame(table, columns = headers)
    create_dir(filepath + '/Outputs/XLS Outputs/')
    create_dir(filepath + '/Outputs/CSV Outputs/')
    if practiceType in ["A1", "B1", "C1"]:
        saveSheets(filepath + '/Outputs/XLS Outputs/' + practiceType + '_Output.xls', [dataFrame, summaryDataFrame], ['Data', 'Summary'])

    newRow = []
    newCsvTable = []
    newHeaders = []
    for row in table:
        for element in range(0, columns.get()):
            newRow.append(row[element])
        newCsvTable.append(newRow)
        newRow = []

    for element in range(0, columns.get()):
        newHeaders.append(headers[element])
        
    if rows.get() != 0: 
        for row in range(len(newCsvTable)-1, rows.get()-1, -1):
            newCsvTable.pop(row)
        csvTable = np.insert(newCsvTable, 0, newHeaders, 0)
    else:
        newCsvTable = []
        newCsvTable.append(newHeaders)
        csvTable = newCsvTable
        

    if delimiterOutput.get() == ",":
        np.savetxt(filepath + '/Outputs/CSV Outputs/Output.csv', csvTable, delimiter=',', fmt='%s')
    else:
        np.savetxt(filepath + '/Outputs/CSV Outputs/Output.csv', csvTable, delimiter='|', fmt='%s')

    filenameDisplay.configure(text = "Selected: None")
    

if __name__ == "__main__":
    
    #creates window for upload button (not necessary but easy for debugging)
    window = tk.Tk()
    window.title("CSV to XLS / Manipulation")
    window.geometry("300x290")
    window.resizable(False, False)

    #tk variables for radiobuttons and dimension scrollers
    global rows, columns, delimiterOutput, delimiterInput, filenameDisplay
    delimiterInput = tk.StringVar(value = 'none')
    delimiterOutput = tk.StringVar(value = 'none')
    rows = tk.IntVar()
    columns = tk.IntVar()
    delimiterInput.trace_add('write', onDelimiterInputChange)
    flag = False

    #sets up graphical interface
    generateDelimiterInputFrame(window, 100, 85, 0.5, 0.2, "Input Delimiter", True)
    generateDimensionFrm(window, 200, 70, .5, .46, "Output Dimensions")
    generateDelimiterOutputFrame(window, 110, 85, .5, .75, "Output Delimiter")
        
    window.mainloop()
