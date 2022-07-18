from tkinter import *
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
from pathlib import Path
import os

#upload file dialog command
def upload(event=None):
    global table
    global headers
    global filename
    global filepath
    headers = []
    filetypes = (('csv files', '*.csv'),('All files', '*.*'))
    filename = filedialog.askopenfilename(filetypes=filetypes)
    pandasFile = pd.read_csv(filename)
    table = pandasFile.to_numpy()
    filepath = os.path.split(filename)[0]
    head = pandasFile.columns
    #creates header array for later, useful for indetifying indexes by string
    for i in range(0, len(head)):
        headers.append(head[i])
    window.destroy()

#function for generating an upload button, takes x, y coords, name of command function, and the window it should be in
def generateUploadButton(relx, rely, command, frame):
    uploadFile = tk.Button(frame, text="Upload File", command=command)
    uploadFile.place(relx=relx, rely=rely, anchor="center")

#finds the column of a specified header and returns it
def findHeader(inputHeader):
    return headers.index(inputHeader)


#returns the sum of units of a specified program ID, takes a table and programID string as parameters
def getUnitSumOfID(table, programId):
    total = 0
    for row in table:
        if row[findHeader("ProgramID")] == programId:
            total = total + row[findHeader("Units")]
    return total

#returns the sum of all elements in a column
def getSumOfColumn(table, column):
    total = 0
    for row in table:
        total = total + row[column]
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
    create_dir(filepath + '/Outputs')
    saveSheets(filepath + '/Outputs/' + practiceType + '_Output.xls', [dataFrame, summaryDataFrame], ['Data', 'Summary'])

if __name__ == "__main__":
    #creates window for upload button (not necessary but easy for debugging)
    window = tk.Tk()
    window.title("CSV to XLS / Manipulation")
    window.geometry("200x100")

    #calls to generate an upload button
    generateUploadButton(0.5, 0.5, upload, window)
    window.mainloop()

    #runs main function with input table as parameter
    main(table)