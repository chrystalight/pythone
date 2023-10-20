#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
from datetime import datetime
from string import ascii_uppercase


def getSerial(value):
    year = (datetime.now().year)%10
    month = ascii_uppercase[datetime.now().month-1]

    if len(value) == 1:
        value = '00'+value
    if len(value) == 2: 
        value = '0'+value
    return(str(year)+month+value)

def getSerialsArray(initialValue, parts):
    initialValue_int = int(initialValue)
    parts_int = int(parts)

    serials = []
    i = 0
    while i<parts_int:
        serials.append(getSerial(str(initialValue_int+i)))
        i=i+1
    return(serials)

def replaceSerial(newSerial): 
    for component in adsk.core.Application.get().activeProduct.allComponents:
        for sketch in component.sketches:
            for sketchText in sketch.sketchTexts:
                sketchText.text = newSerial

def run(context):
    ui = None

    try:
        app :adsk.core.Application = adsk.core.Application.get()
        ui :adsk.core.UserInterface = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent

        # inputbox
        # https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-110bf712-8527-4ccd-a11d-f7266d69773e
        initialValue, cancelled = ui.inputBox(
            'What is the three digit code for your first part?',
            'Enter Initial Serial Number',
            '001')

        if cancelled:
            ui.messageBox('Cancel')
            return

        ##ui.messageBox('Your first serial number is '+getSerial(initialValue))

        partsNumber, cancelled = ui.inputBox(
            'Your first serial number is '+getSerial(initialValue)+'. How many idential parts would you like to generate?',
            'Enter number of parts',
            '1'
        )

        serialsArray = getSerialsArray(initialValue, partsNumber)
        ui.messageBox('You are trying to generate '+partsNumber+' parts. Your serial numbers will be: '+ str(serialsArray))

        defaultInputFolder = r'C:\\\\'
        folderInput = ui.inputBox('Input path to save folder: ', 'Define Save Folder', defaultInputFolder)
        folder = folderInput[0]

        for i in serialsArray: 
            replaceSerial(i)
            filename = f'{folder}\\Test File ({i})'
            ui.messageBox(f'Check model appearance')

            exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
            stlOptions = exportMgr.createSTLExportOptions(rootComp)
            stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            stlOptions.filename = filename
            exportMgr.execute(stlOptions)
            ##save file as stl with a good name

        #add a confirm serials number and that parameters are correctly set button
        #with a loop that tuns partsNumber times, do the following: 
            #change the sketch string input to serial number
            #nameOH WE NAED A NAME

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# def run(context):
#     ui = None
#     try:
#         app = adsk.core.Application.get()
#         ui = app.userInterface
#         ui.messageBox('Hello addin')
#     except:
#         if ui:
#             ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
 
# def stop(context):
#     ui = None
#     try:
#         app = adsk.core.Application.get()
#         ui = app.userInterface
#         ui.messageBox('Stop addin')
#     except:
#         if ui:
#             ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
