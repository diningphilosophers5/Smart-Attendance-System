"""
Main Script
Start the GUI of the application and calls the required modules for necessary functionality
Run this script to start the application
"""

from Tkinter import *
import tkFileDialog
from modules.training import *
from modules.predict import *

def browse_dir():
    """Opens a dialog box to browse to the required directory in the GUI
    Args: None
    Returns: The absolute path of the directory selected.
    """
    currdir = os.getcwd()
    Tk().withdraw()
    tempdir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print "You selected location : %s" % tempdir
    else:
        return browse_dir()
    return tempdir

def browse_file():
    """Opens a browse window to select a file
    :return: The absolute path of the file selected as a string
    """
    currdir = os.getcwd()
    Tk().withdraw()
    filepath = tkFileDialog.askopenfilename(parent = root, initialdir=currdir, title='Please select a file')
    if len(filepath) > 0:
        print "You selected file : %s" % filepath
    else:
        return browse_file()
    return filepath

def trainOnDataset(event):
    """Function get called on left click event on the button 'train'
        Opens a browse dialog to select the location of training data.
        Trains the LBP and Fisherfaces Recognisers on the given training set.
        Saves the configuration of the trained model in XML files for future use.
        Displays the result in the GUI.
    :param event: The function is bounded to the button train("Train on Data") and activated by left click event.
    """
    txt.delete(0.0, END)
    txt.insert(END, 'Training on dataset.\n')
    path = browse_dir()
    train_models(path)
    status.config(text='Training done successfully.')
    txt.delete(0.0, END)
    txt.insert(END, 'Prediction Models are ready.\n')



def processVideo(event):
    """Function get called on left click event on the button 'calculateVideo'
        Opens a browse dialog to select the video file.
        Processes the video for detecting faces and making predictions on them by loading the trained models.
        Displays the result in the GUI.
    :param event: The function is bounded to the button calculateVideo("Calculate Attendence from Video") and activated by left click event.
    """
    status.config(text='Processing Video...')
    txt.delete(0.0, END)
    txt.insert(END, 'Processing video.\n')
    path = browse_file()
    result = predict_video(path)
    status.config(text='Result computed successfully.')
    presentlist = list(result)
    txt.delete(0.0, END)
    txt.insert(END, 'Students present are:' + '\n')
    num = 1
    for name in presentlist:
        txt.insert(END, str(num) + '. ' + name + '\n')
        num += 1
    if num == 1:
        txt.delete(0.0, END)
        txt.insert(END, 'No persons found.' + '\n')
    #calculateVideo.configure(background=orig_color_calculatevideo)

def testImages(event):
    """Function get called on left click event on the button 'calculateImages'
        Opens a browse dialog to select the directory containing the images.
        Processes the images for detecting faces and making predictions on them by loading the trained models.
        Displays the result in the GUI.
    :param event: The function is bounded to the button calculateImages("Test on Images") and activated by left click event.
    """
    txt.delete(0.0, END)
    txt.insert(END, 'Processing images.\n')
    path = browse_dir()
    result = identify_images(path)
    status.config(text='Result computed successfully.')
    txt.delete(0.0, END)
    txt.insert(END, 'Persons identified are:\n')
    num = 1
    for label in result:
         txt.insert(END, str(num) + '. ' + result[label] + '\n')
         num += 1
    if num == 1:
        txt.delete(0.0, END)
        txt.insert(END, 'No persons found.' + '\n')
    #calculateImages.configure(background=orig_color_calculateimage)

def resetProgram():
    """Function bounded to the Reset option in the Options menu in the MenuBar.
        It clears the status of the status bar and the Text display in the GUI
    """
    status.config(text='Ready.')
    txt.delete(0.0, END)
    txt.insert(END, 'Ready.\n')

"""
    Main Script starts here.
"""
root = Tk()
root.wm_title("Smart Attendance System")

status = Label(root, text="Ready", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

topFrame = Frame(root, width=480, height=320)
topFrame.pack()

bottomFrame = Frame(root, width=480, height=320)
bottomFrame.pack(side=BOTTOM, fill="both", expand=True)
bottomFrame.grid_propagate(False)
bottomFrame.grid_rowconfigure(0, weight=1)
bottomFrame.grid_columnconfigure(0, weight=1)

# create a Text widget
txt = Text(bottomFrame, borderwidth=3, relief="sunken")
txt.config(font=("consolas", 12), undo=True, wrap='word')
txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
txt.insert(END, "Ready.")

# create a Scrollbar and associate it with txt
scrollb = Scrollbar(bottomFrame, command=txt.yview)
scrollb.grid(row=0, column=1, sticky='nsew')
txt['yscrollcommand'] = scrollb.set

train = Button(topFrame, text="Train on Data")
calculateVideo = Button(topFrame, text="Calculate Attendance from Video")
calculateImages = Button(topFrame, text="Test Model on Images")

train.bind("<Button-1>", trainOnDataset)
calculateVideo.bind("<Button-1>", processVideo)
calculateImages.bind("<Button-1>", testImages)

orig_color_train = train.cget("background")
orig_color_calculatevideo = calculateVideo.cget("background")
orig_color_calculateimage = calculateImages.cget("background")

train.pack(side=LEFT)
calculateVideo.pack(side=LEFT)
calculateImages.pack(side=LEFT)

menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="Options", menu=subMenu)
subMenu.add_command(label="Reset", command=resetProgram)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=root.quit)

root.mainloop()