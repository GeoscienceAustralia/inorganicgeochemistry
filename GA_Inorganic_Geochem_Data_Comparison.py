"""
Date created: 14/08/2020
Lasted changed: 05/09/2020
Program to check if data uploaded to GA site is correct.
Input: Two excel files (Results from GA Site and original data sheets
Output: N/A only prints a response correct or incorrect
"""

import pandas as pd
import math

# variables
# lists used for results from downloaded spreadsheet
listXRF = []
listICPMS = []
listGRAV = []
listTITRE = []
listTemp = []


# lists used for results from original spreadsheet
listXRF2 = []
listICPMS2 = []
listGRAV2 = []
listTITRE2 = []

#holds data frames
dfGrav = '' #holds Grav data
dfXRF = '' #holds XRF data
dfICPMS = '' #holds icpms data
dfTitre = '' #holds Titre data
df_OG = '' #holds data downloaded from GA site

#used if a certain sheet doesnt exist the variable will be true and will skip code related to that data
skipXRF = False
skipICPMS = False
skipGrav = False
skipTitre = False

def looptillheaderOG(UploadedExcelFile):
    """loops until correct row is found and enters information from the excel file in a data frame.
    fails to find row with the required columns and keeps checking new rows to find one with the required information"""
    global df_OG
    row = 0
    #loops till correct row is found
    while True:
        try:
            df_OG = pd.read_excel(UploadedExcelFile, header=row,
                                  usecols=['SAMPLENO', 'SAMPLEID', 'TECHNIQUE', 'SiO2 [wt%]', 'TiO2 [wt%]',
                                           'Al2O3 [wt%]', 'Fe2O3TOT [wt%]', 'FeO [wt%]', 'MnO [wt%]',
                                           'MgO [wt%]', 'CaO [wt%]', 'Na2O [wt%]', 'K2O [wt%]',
                                           'P2O5 [wt%]', 'SO3 [wt%]', 'MLOI [wt%]',
                                           'Be [ppm]', 'Sc [ppm]', 'V [ppm]', 'Cr [ppm]',
                                           'Co [ppm]', 'Ni [ppm]', 'Cu [ppm]', 'Zn [ppm]',
                                           'Ga [ppm]', 'Ge [ppm]', 'As [ppm]'])
            break
        except:
            pass
        row += 1

def looptillheaderXRF(OriginalExcelFile): #same as above but specifically for the xrf data on the original data excel sheet
    global skipXRF
    global dfXRF
    XRF = ["XRF_Upload", "XRF_upload", "XRF"]
    exitLoop = False
    #loops for each probable sheet name
    for x in range(len(XRF)):
        row = 0
        #loops till correct row
        while True:
            try:
                dfXRF = pd.read_excel(OriginalExcelFile, sheet_name=XRF[x], header=row, usecols=['Sample No', 'SiO2 (%)',
                                                                                                    'TiO2 (%)', 'Al2O3 (%)',
                                                                                                    'Fe2O3tot (%)',
                                                                                                    'MnO (%)',
                                                                                                    'MgO (%)', 'CaO (%)',
                                                                                                    'Na2O (%)', 'K2O (%)',
                                                                                                    'P2O5 (%)', 'SO3 (%)'])
                exitLoop = True
                skipXRF = False
                break
            except:#this exception trys a second set of columns because Fe2O3 is has different column names depending on sheets
                try:
                    dfXRF = pd.read_excel(OriginalExcelFile, sheet_name=XRF[x], header=row, usecols=['Sample No', 'SiO2 (%)',
                                                                                                   'TiO2 (%)', 'Al2O3 (%)',
                                                                                                   'Fe2O3 (%)',
                                                                                                   'MnO (%)',
                                                                                                   'MgO (%)', 'CaO (%)',
                                                                                                   'Na2O (%)', 'K2O (%)',
                                                                                                   'P2O5 (%)', 'SO3 (%)'])
                    exitLoop = True
                    skipXRF = False
                    break
                except:
                    pass
            row += 1

            if row == 40:#allows to escape the while loop if too many fails in the row
                skipXRF= True
                break
        if exitLoop:
            break
    else:#if the loop continues to completion and no successful output is found assume a skip
        skipXRF = True

def looptillheaderTITRE(OriginalExcelFile):#same as above but specifically for the titre data on the original data excel sheet
    global skipTitre
    global dfTitre
    TITRE = ["FeO", "FeO_Upload", "FeO_upload"]
    exitLoop = False
    for x in range(len(TITRE)):
        row = 0
        while True:
            try:
                dfTitre = pd.read_excel(OriginalExcelFile, sheet_name=TITRE[x], header=row, usecols=['Sample No', 'FeO (%)'])
                exitLoop = True
                skipTitre = False
                break
            except:
                pass

            row += 1
            if row == 40:
                skipTitre = True
                break
        if exitLoop:
            break
    else:
        skipTitre = True

def looptillheaderGrav(OriginalExcelFile):#same as above but specifically for the grav data on the original data excel sheet
    global skipGrav
    global dfGrav
    Grav = ["LOI"]
    exitLoop = False
    for x in range(len(Grav)):
        row = 0
        while True:
            try:
                dfGrav = pd.read_excel(OriginalExcelFile, sheet_name=Grav[x], header=row, usecols=['Sample No', 'MLOI (%)'])
                exitLoop = True
                skipGrav = False
                break
            except:
                pass
            row += 1
            if row == 40:
                skipGrav = True
                break
        if exitLoop:
            break
    else:
        skipGrav = True

def looptillheaderICPMS(OriginalExcelFile):#same as above but specifically for the icpms data on the original data excel sheet
    global skipICPMS
    global dfICPMS
    ICPMS = ["ICPMS_Upload", "ICPMS_upload", "ICP-MS", ]
    exitLoop = False
    for x in range(len(ICPMS)):
        row = 0
        while True:
            try:
                dfICPMS = pd.read_excel(OriginalExcelFile, sheet_name=ICPMS[x], header=row,
                                    usecols=['Sample No', 'Sample ID', 'Comments'])
                #uses numbers for columns cause the column names for the data is a couple rows too early
                dfICPMS = pd.read_excel(OriginalExcelFile, sheet_name=ICPMS[x], header=row,#
                                    usecols=[1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
                exitLoop = True
                skipICPMS = False
                break
            except:#this exception trys a second set of columns because ICPMS sheets sometimes has an extra columns for comments before the data
                try:
                    dfICPMS = pd.read_excel(OriginalExcelFile, header=row,
                                        usecols=['Sample No', 'Sample ID'])
                    dfICPMS = pd.read_excel(OriginalExcelFile, sheet_name=ICPMS[x], header=row,
                                        usecols=[1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
                    exitLoop = True
                    skipICPMS = False
                    break
                except:
                    pass
            row += 1
            if row == 40:
                skipICPMS = True
                break
        if exitLoop:
            break
    else:
        skipICPMS = True


def variablesetup(input1, input2):
    global df_OG
    global dfGrav
    global dfXRF
    global dfICPMS
    global dfTitre

    UploadedExcelFile = pd.ExcelFile(input1) #first file path inputted uploaded data
    OriginalExcelFile = pd.ExcelFile(input2) #second file path inputted original data
    looptillheaderOG(UploadedExcelFile) #finds data in uploaded excel file
    looptillheaderXRF(OriginalExcelFile) #finds xrf data in original excel file
    looptillheaderICPMS(OriginalExcelFile) #finds icpms data in orginal excel file
    looptillheaderGrav(OriginalExcelFile)   #finds grav data in orginal excel file
    looptillheaderTITRE(OriginalExcelFile) #finds titre data in orginial excel file


def convert_to_list_database():  # sorts downloaded sheet into 3 lists for each technique
    global listGRAV
    global listXRF
    global listICPMS
    global listGRAV2
    global listXRF2
    global listICPMS2
    global listTITRE
    global listTITRE2
    global listTemp
    #converts all the data frames to lists
    if skipGrav == False:
        listGRAV2 = dfGrav.values.tolist()
    if skipXRF == False:
        listXRF2 = dfXRF.values.tolist()
    if skipICPMS == False:
        listICPMS2 = dfICPMS.values.tolist()
    if skipTitre == False:
        listTITRE2 = dfTitre.values.tolist()
    listTemp = df_OG.values.tolist()
    #runs through the list containing data from uploaded data and puts all the data in their seperate lists
    for i in range(len(listTemp)):
        if listTemp[i][2] == 'XRF':
            if math.isnan(listTemp[i][3]):
                pass
            else:
                listXRF.append((listTemp[i][0],listTemp[i][3],listTemp[i][4],listTemp[i][5],listTemp[i][6], listTemp[i][8],
                               listTemp[i][9],listTemp[i][10],listTemp[i][11],listTemp[i][12], listTemp[i][13], listTemp[i][14]))
        if listTemp[i][2] == 'TITR':
            if math.isnan(listTemp[i][7]):
                pass
            else:
                listTITRE.append((listTemp[i][0],listTemp[i][7]))
        if listTemp[i][2] == 'ICPMS':
            if math.isnan(listTemp[i][16]):
                pass
            else:
                listICPMS.append((listTemp[i][0],listTemp[i][25],listTemp[i][19],listTemp[i][18],
                               listTemp[i][21],listTemp[i][23],listTemp[i][24],listTemp[i][20],listTemp[i][16],listTemp[i][17],
                                listTemp[i][22], listTemp[i][26]))
        if listTemp[i][2] == 'GRAV':
            if math.isnan(listTemp[i][15]):
                pass
            else:
                listGRAV.append((listTemp[i][0], listTemp[i][15]))

    x = 0
    while x <= 10: #runs multiple times to remove invalid lines
        x += 1
        if skipXRF == False:
            removeInvalidLines(listXRF)
            removeInvalidLines(listXRF2)

        if skipTitre == False:
            removeInvalidLines(listTITRE)
            removeInvalidLines(listTITRE2)

        if skipGrav == False:
            removeInvalidLines(listGRAV)
            removeInvalidLines(listGRAV2)

        if skipICPMS == False:
            removeInvalidLines(listICPMS)
            removeInvalidLines(listICPMS2)

def removeExtra():
    global listXRF2
    global listICPMS2
    global listGRAV2
    global listTITRE2

    if skipXRF == False:
        removeStrings(listXRF)
        removeStrings(listXRF2)
    if skipICPMS == False:
        removeStrings(listICPMS)
        removeStrings(listICPMS2)
    if skipGrav == False:
        removeStrings(listGRAV)
        removeStrings(listGRAV2)
    if skipTitre == False:
        removeStrings(listTITRE)
        removeStrings(listTITRE2)

def removeInvalidLines(lists): #get rid of extra lines
    #runs for each index in the lists checks if sample No is invalid either a string, nan, 0
    for i in range(len(lists)):
        try:
            if isinstance(lists[i][0], int) and lists[i][0] < 10000 or isinstance(lists[i][0], float) and lists[i][0] < 10000:
               del lists[i]
        except:
            pass
        try:
            if isinstance(lists[i][0], str):
                try:
                    float(lists[i][0])
                except ValueError:
                    del lists[i]
        except:
            pass
        try:
            if math.isnan(lists[i][0]):
                del lists[i]
        except:
            pass
        try:
            if lists[i][0] == 0:
                del lists[i]
        except:
            pass



def removeStrings(lists): #gets rid of < in data
    print("removestrings has occured")
    list(lists)
    temporaryList = lists

    for x in range(len(temporaryList)):#runs for each index
        for i in range(len(temporaryList[x])):#runs for each index of nestes list
            try:
                if isinstance(lists[x][i], str):#checks if it is a str
                    tempValue = temporaryList[x][i] #had a not subscriptable issue
                    if "<" in temporaryList[x][i]: #some data has < when data was below a threshold changes to - to match uploaded data
                        tempValue = (float((tempValue).replace("<", "-")))

                    else:
                        try:
                            tempValue = float(temporaryList[x][i]) #some numbes were stored as text
                        except ValueError:
                            tempValue = 0.111111 #other strings are changes to this random number to be identified later
                    temporaryList[x][i] = tempValue
            except ValueError:
                pass
    return(temporaryList) #returns the list





def checkCorrect(a, b):  # calculates error percent (as a decimal) that is used in checkList
    try:
        if (a-b) == 0:
            return True
        elif -0.05 <= (a - b) / b <= 0.05:
            return True
    except TypeError:
        print(a, b)


def checkCorrectGrav(a, b):
    """ calculates error percent (as a decimal) that is used in checkList grav and titre have higher allowed percentage
    since data is much smaller and rounding affects the resutls much more
    e.g. original data = 0.15 uploaded = 0.2"""
    if (a-b) == 0:
        return True
    elif -0.15 <= (a - b) / b <= 0.15:
        return True

def listSort():
    """icpms since the order is different due to how the data is sometimes orders makes it
    from largest to smallest to make sure everything is in order"""
    global listICPMS
    global listICPMS2

    if skipICPMS == False:
        listICPMS = nestedListSort(listICPMS)
        listICPMS2 = nestedListSort(listICPMS2)

def nestedListSort(nestedList): # sort from biggest to smallest values inside the nested lists
    list(nestedList)
    nestedListTemp = []
    listTemp = []
    for x in range(len(nestedList)):
        for i in range(len(nestedList[x])):
            nestedListTemp.append(nestedList[x][i])
        nestedListTemp.sort(reverse=True)
        listTemp.append((nestedListTemp[0], nestedListTemp[1], nestedListTemp[2], nestedListTemp[3], nestedListTemp[4],
                         nestedListTemp[5], nestedListTemp[6], nestedListTemp[7], nestedListTemp[8], nestedListTemp[9],
                         nestedListTemp[10], nestedListTemp[11], ))
        nestedListTemp.clear()
    return(listTemp)

def findequivalent(id, listSearch): #finds all sampleNos that are the same gets their indexs so they can be checked
    possibleValues = []
    for x in range(len(listSearch)):
        if id == listSearch[x][0]:
            possibleValues.append(x)
    return possibleValues

def checkList(listone, listtwo): #compares the two lists and checks if the values are within the allowed limit
    #list one is the uploaded data sheet list two is the original data sheet

    i = 0
    totalTrue = 0
    total = 0
    for i in range(len(listtwo)):
        total += 1
        if listone == listXRF or listone == listICPMS:
            if math.isnan(listtwo[i][0]) or listtwo[i][0] <= 10000 or 0.111111 in listtwo[i]:
                pass
            else:
                possibleValues = findequivalent(listtwo[i][0], listone)

                for x in range(len(possibleValues)):
                    value = possibleValues[x]

                    if checkCorrect(listone[value][1], listtwo[i][1]) and checkCorrect(listone[value][2], listtwo[i][2]) \
                            and checkCorrect(listone[value][3], listtwo[i][3]) and checkCorrect(listone[value][4], listtwo[i][4]) \
                            and checkCorrect(listone[value][5], listtwo[i][5]) and checkCorrect(listone[value][6], listtwo[i][6]) \
                            and checkCorrect(listone[value][7], listtwo[i][7]) and checkCorrect(listone[value][8], listtwo[i][8]) \
                            and checkCorrect(listone[value][9], listtwo[i][9]) and checkCorrect(listone[value][10], listtwo[i][10]):
                        totalTrue += 1
                        break
                else:#if none of the possible values worked the is some incorrect data
                    print("Wrong")
                    print(listtwo[i])#prints the original data so you can go check manually if needed
                possibleValues.clear()


        elif listone == listGRAV or listone == listTITRE:
            if math.isnan(listtwo[i][0]) or listtwo[i][0] <= 10000 or 0.111111 in listtwo[i]:
                pass
            else:
                possibleValues = findequivalent(listtwo[i][0], listone)

                for x in range(len(possibleValues)):
                    value = possibleValues[x]

                    if checkCorrectGrav(listone[value][1], listtwo[i][1]):
                        totalTrue += 1
                        break
                else:#if none of the possible values worked the is some incorrect data
                    print("\nWrong")
                    print(listtwo[i])#prints the original data so you can go check manually if needed
                possibleValues.clear()


    if totalTrue == total:
        print("This sheet is accurate!")
    else:
        print("Sheet is inaccurate!")


def clearlist(): #clears all the lists
    listXRF.clear()
    listXRF2.clear()
    listGRAV.clear()
    listGRAV2.clear()
    listICPMS.clear()
    listICPMS2.clear()
    listTITRE.clear()
    listTITRE2.clear()

def optionQuit(): #allows the users to quit or continue the program
    userInput = input("Press q to quit or y to continue")
    if userInput == 'q' or userInput == 'Q':
        quit()
    else:
        main()

def main():  # main function of program
    
    variablesetup(r"{}".format(input("Enter GA SITE downloaded excel path").replace('"', ''))
                  , r"{}".format(input("Enter original file").replace('"', '')))
    convert_to_list_database()
    removeExtra()
    listSort()

    print(len(listXRF),len(listXRF2),len(listGRAV),len(listGRAV2),len(listICPMS),len(listICPMS2),len(listTITRE),len(listTITRE2))
    if skipXRF == False:
        checkList(listXRF, listXRF2)
    if skipICPMS == False:
        checkList(listICPMS, listICPMS2)
    if skipTitre == False:
        checkList(listTITRE, listTITRE2)
    if skipGrav == False:
        checkList(listGRAV, listGRAV2)
    clearlist()
    optionQuit()

main()
