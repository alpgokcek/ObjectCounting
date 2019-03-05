"""
Name Surname:   Alp Gökçek
Department:     Computer Engineering
Instructor:     Muhittin Gökmen
Course:         COMP204-Programming Studio
Date:           05/03/2019
"""
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import font  as tkfont
from tkinter.filedialog import *
from PIL import Image, ImageTk
import numpy
import time
import copy
import os
from createimage import create

#Global Variables
openedImage, resizedImage, binaryImage, framedImage = None, None, None, None
path=None
nCol, nRow, orNRow, orNCol = 0,0,0,0
pixelMapAsString=""

lev_iteration, lev_ncc=0,0
tsf_iteration, tsf_ncc=0,0

#GUI Creation
root=tk.Tk()

algorithm_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

def saveImgFunc(i=None):
    global path
    if i==None:
        path=createimagefunction.save_image(i)
    else:
        path=createimagefunction.saveas_image()
    openImage("s")
    writeBinaryToScreen()


#Create Image Frame
createimage_frame=Frame(root)
createimage_frame.grid(row=0, column=0, sticky="nsew")
createimagefunction=create(createimage_frame)

#utilities button frame
utilities_frame=Frame(createimage_frame,background='#EFEFEF')
utilities_frame.pack()

#homepage button
homepage_button = Button(utilities_frame, text="Go to the algorithms page", command=lambda: [controller(1), createimagefunction.discard_image()])
homepage_button.pack(side="left",padx="30",pady="20")

#Save button
save_button=Button(utilities_frame, text="Save", command=lambda:[saveImgFunc(None),messagebox.showinfo("Image Saved", "Image successfully saved to the directory.")])
save_button.pack(side="left", padx="20",pady="10")

#Save and Exit button
saveas_button=Button(utilities_frame, text="Save As", command=lambda:[saveImgFunc("s"),messagebox.showinfo("Image Saved", "Image successfully saved.")])
saveas_button.pack(side="left", padx="20",pady="10")

#Save and Continue button
saveandcont_button=Button(utilities_frame, text="Save and Continue", command=lambda:[saveImgFunc(None),controller(1)])
saveandcont_button.pack(side="left", padx="20",pady="10")
gui_frame = Frame(root)
gui_frame.grid(row=0, column=0, sticky="nsew")

#Showing iterations and ncc on the screen
levialdinccstr, levialdiiterstr, levialdidone=StringVar(),StringVar(),StringVar()
levialdinccstr.set(lev_ncc)
levialdiiterstr.set(lev_iteration)
tsfnccstr,tsfiterstr,tsfdone=StringVar(),StringVar(),StringVar()
tsfnccstr.set(tsf_ncc)
tsfiterstr.set(tsf_ncc)

TSF_Frame=Frame(gui_frame)
TSF_Frame.grid(row=2, column=0, sticky=N, pady=20)
Label(TSF_Frame, text="TSF Algorithm",font=algorithm_font).pack()

TSF_Frame1=Frame(TSF_Frame)
TSF_Frame1.pack()
TSF_Frame2=Frame(TSF_Frame)
TSF_Frame2.pack()

Label(TSF_Frame1, text="Number of Iterations:").pack(side="left")
Label(TSF_Frame1, textvariable=tsfiterstr).pack(side="right")
Label(TSF_Frame2, text="Number of Connected Components:").pack(side="left")
Label(TSF_Frame2, textvariable=tsfnccstr).pack(side="right")
Label(TSF_Frame,textvariable=tsfdone).pack()


LEV_Frame=Frame(gui_frame)
LEV_Frame.grid(row=2, column=1, sticky=N, padx=20, pady=20)
Label(LEV_Frame, text="Levialdi Algorithm",font=algorithm_font).pack()

LEV_Frame1=Frame(LEV_Frame)
LEV_Frame1.pack()
LEV_Frame2=Frame(LEV_Frame)
LEV_Frame2.pack()

Label(LEV_Frame1, text="Number of Iterations:").pack(side="left")
Label(LEV_Frame1, textvariable=levialdiiterstr).pack(side="right")
Label(LEV_Frame2, text="Number of Connected Components:").pack(side="left")
Label(LEV_Frame2, textvariable=levialdinccstr).pack(side="right")
Label(LEV_Frame,textvariable=levialdidone).pack()



def outputstring():
    global lev_ncc
    global lev_iteration
    global tsf_ncc
    global tsf_iteration
    global path
    global openedImage
    global framedImage
    global createimagefunction

    output=""

    #if image created via the create image function, output is changed
    if path!="created-image.png":
        output="Image Path:"+path+"\nImage Size: "+str(os.path.getsize(path))+" bytes\n-------------------------------------------\n"

    else:
        output+="Created Object Size: "+str(createimagefunction.created_obj_size)+"pixel^2\n-------------------------------------------\n"
    output+="Original Image Dimensions:"+str(openedImage.size[0])+"x"+str(openedImage.size[1])+"\nFramed Image Dimensions:"+str(framedImage.size[0])+"x"+str(framedImage.size[1])+" \n-------------------------------------------\nTSF Algorithm \n"+ "NCC: " +str(tsf_ncc) + "\nIteration: "+str(tsf_iteration)+ "\n-------------------------------------------\nLevialdi Algorithm \n"+ "NCC: " +str(lev_ncc) + "\nIteration: "+str(lev_iteration)
    file=open("output.txt","w+")
    file.write(output)

#Save button for output.txt
save_button=Button(gui_frame, text="Save", command=lambda:[outputstring(),messagebox.showinfo("Output Saved", "Output successfully saved to the directory.")])
save_button.grid(row=2, column=1, sticky=NE, padx=20, pady=20)


xSize,ySize = 900,650
max_width,max_height=int(xSize*3/9), int(ySize*3/6)
size = str(xSize)+"x"+str(ySize)
root.geometry(size)
root.title("COMP204 Project 1 || Alp Gökçek")
root.configure(bg="white")
root.resizable(0, 0)



"""
this method is for making the program multipage.
if input is 0, create image frame shows up
if input is 1, algorithm page a.k.a. homepage shows up
"""
def controller(sel):
    if sel==0:
        createimage_frame.tkraise()
        root.geometry("1150x650")
    if sel==1:
        gui_frame.tkraise()
        root.geometry("900x650")

#selecting gui frame as home page
controller(1)


#Main GUI Grid Partioning
for r in range(3):
    for c in range(3):
        if r == 0:
            Label(gui_frame, bg='white').grid(row=r, column=c, padx=(xSize/6)-15, pady=20)
        else:
            Label(gui_frame, bg='white', text=" ").grid(row=r, column=c, padx=(xSize*2/9)-15, pady=(ySize*2/6))


#################
# TSF ALGORITHM #
#################

# Checking 3 or more consecutive zeros
def lengthofzeros(a,i,j): #a=array , i=row, j=column
    b1,b2,b3=int(a[i-1][j-1]),int(a[i-1][j]),int(a[i-1][j+1])
    b4,b5,b6=int(a[i][j-1]), int(a[i][j]),int(a[i][j+1])
    b7,b8,b9=int(a[i+1][j-1]),int(a[i+1][j]), int(a[i+1][j+1])


    iter_arr=[b1,b2,b3,b6,b9,b8,b7,b4]

    for b in range(0,8):
        if iter_arr[b-2]==0 and iter_arr[b-1]==0 and iter_arr[b]==0:
            return True
    return False


#calculating number of connected ones around the central-pixel b5
def calc_cp(a,i,j): #a=array , i=row, j=column
    b1,b2,b3=int(a[i-1][j-1]),int(a[i-1][j]),int(a[i-1][j+1])
    b4,b5,b6=int(a[i][j-1]), int(a[i][j]),int(a[i][j+1])
    b7,b8,b9=int(a[i+1][j-1]),int(a[i+1][j]), int(a[i+1][j+1])

    cp_arr=[b1,b2,b3,b6,b9,b8,b7,b4] #array for circular iteration
    if (b4==1 and b2==1): cp_arr[0]=1
    if (b2==1 and b6==1): cp_arr[2]=1
    if (b6==1 and b8==1): cp_arr[4]=1
    if (b8==1 and b4==1): cp_arr[6]=1

    cp=0 #cp counter

    #calculating tp over cp_arr
    sum=cp_arr[0]+cp_arr[1]+cp_arr[2]+cp_arr[3]+cp_arr[4]+cp_arr[5]+cp_arr[6]+cp_arr[7]

    #checking if every neigbor is equal to 1
    if sum == 8:
        return 1
    for b in range(0,8):
        if cp_arr[b-1]==0 and cp_arr[b]==1:
            cp+=1
    return cp



def tsf_algorithm():
    #number of connected components and number of iterations counter
    global tsf_ncc
    global tsf_iteration
    global binaryImage
    global tsfnccstr #displaying on screen
    global tsfiterstr #displaying on screen
    global tsfdone

    tsf_ncc,tsf_iteration=0,0
    tsfnccstr.set(0) #this is for showing ncc on gui
    tsfiterstr.set(0) #this is for showing iterations on gui
    tsfdone.set("") #this is for showing if iterations are done

    nrow,ncolumn = len(binaryImage),len(binaryImage[0]) #image size

    buffer=numpy.copy(binaryImage) #buffer array
    temp=copy.deepcopy(buffer) #temp array for copying

    flag=True #flag for checking if there is any change in the picture


    while flag:
        flag=False

        #subfield-1
        for row in range(1,nrow-1,2):
            for column in range(1,ncolumn-1,2):
                cp=int(buffer[row][column]) #center pixel
                lp=int(buffer[row][column-1]) #left pixel
                clp=int(buffer[row+1][column-1]) # cross-left pixel
                bp=int(buffer[row+1][column]) #below pixel
                neighborhood_8 = int(buffer[row-1][column-1] + buffer[row-1][column] + buffer[row-1][column+1] + buffer[row][column+1] + buffer[row+1][column+1]+lp+clp+bp)

                b_p=int(neighborhood_8) #number of 1’s in cp’s 8-neighborhood
                c_p=calc_cp(buffer,row,column) #number of connected 1's

                if cp==1:
                    if b_p==0:
                        #isolated point detection
                        temp[row][column]=0
                        tsf_ncc+=1
                        tsfnccstr.set(tsf_ncc)
                        flag=True
                    if (c_p==1 and (b_p!=1 or (buffer[row+1][column-1]==0 and buffer[row-1][column-1]==0)) and lengthofzeros(buffer,row,column)):
                        #deletion condition
                        temp[row][column]=0
                        flag=True
                if cp==0:
                    #augmentation condition
                    if c_p==1 and ((buffer[row][column-1]==1 and buffer[row-1][column]==1) or (buffer[row][column-1]==1 and buffer[row+1][column]==1)):
                        temp[row][column]=1
                        flag=True

        for row in range(2,nrow-1,2):
            for column in range(2,ncolumn-1,2):
                cp=int(buffer[row][column]) #center pixel
                lp=int(buffer[row][column-1]) #left pixel
                clp=int(buffer[row+1][column-1]) # cross-left pixel
                bp=int(buffer[row+1][column]) #below pixel
                neighborhood_8 = int(buffer[row-1][column-1] + buffer[row-1][column] + buffer[row-1][column+1] + buffer[row][column+1] + buffer[row+1][column+1]+lp+clp+bp)

                b_p=neighborhood_8 #number of 1’s in cp’s 8-neighborhood
                c_p=calc_cp(buffer,row,column) #number of connected 1's

                if cp==1:
                    if b_p==0:
                        #isolated point detection
                        temp[row][column]=0
                        tsf_ncc+=1
                        tsfnccstr.set(tsf_ncc)
                        flag=True
                    if (c_p==1 and (b_p!=1 or (buffer[row+1][column-1]==0 and buffer[row-1][column-1]==0)) and lengthofzeros(buffer,row,column)):
                        #deletion condition
                        temp[row][column]=0
                        flag=True
                if cp==0:
                    #augmentation condition
                    if c_p==1 and ((buffer[row][column-1]==1 and buffer[row-1][column]==1) or (buffer[row][column-1]==1 and buffer[row+1][column]==1)):
                        temp[row][column]=1
                        flag=True

        #updating buffer after subfield-1
        buffer=copy.deepcopy(temp)

        #subfield-2

        for row in range(2,nrow-1,2):
            for column in range(1,ncolumn-1,2):
                cp=int(buffer[row][column]) #center pixel
                lp=int(buffer[row][column-1]) #left pixel
                clp=int(buffer[row+1][column-1]) # cross-left pixel
                bp=int(buffer[row+1][column]) #below pixel
                neighborhood_8 = int(buffer[row-1][column-1] + buffer[row-1][column] + buffer[row-1][column+1] + buffer[row][column+1] + buffer[row+1][column+1]+lp+clp+bp)

                b_p=neighborhood_8 #number of 1’s in cp’s 8-neighborhood
                c_p=calc_cp(buffer,row,column) #number of connected 1's

                if cp==1:
                    if b_p==0:
                        #isolated point detection
                        temp[row][column]=0
                        tsf_ncc+=1
                        tsfnccstr.set(tsf_ncc)
                        flag=True
                    if (c_p==1 and (b_p!=1 or (buffer[row+1][column-1]==0 and buffer[row-1][column-1]==0)) and lengthofzeros(buffer,row,column)):
                        #deletion condition
                        temp[row][column]=0
                        flag=True
                if cp==0:
                    #augmentation condition
                    if c_p==1 and ((buffer[row][column-1]==1 and buffer[row-1][column]==1) or (buffer[row][column-1]==1 and buffer[row+1][column]==1)):
                        temp[row][column]=1
                        flag=True


        for row in range(1,nrow-1,2):
            for column in range(2,ncolumn-1,2):
                cp=int(buffer[row][column]) #center pixel
                lp=int(buffer[row][column-1]) #left pixel
                clp=int(buffer[row+1][column-1]) # cross-left pixel
                bp=int(buffer[row+1][column]) #below pixel
                neighborhood_8 = int(buffer[row-1][column-1] + buffer[row-1][column] + buffer[row-1][column+1] + buffer[row][column+1] + buffer[row+1][column+1]+lp+clp+bp)

                b_p=neighborhood_8 #number of 1’s in cp’s 8-neighborhood
                c_p=calc_cp(buffer,row,column) #number of connected 1's

                if cp==1:
                    if b_p==0:
                        #isolated point detection
                        temp[row][column]=0
                        tsf_ncc+=1
                        tsfnccstr.set(tsf_ncc)
                        flag=True
                    if (c_p==1 and (b_p!=1 or (buffer[row+1][column-1]==0 and buffer[row-1][column-1]==0)) and lengthofzeros(buffer,row,column)):
                        #deletion condition
                        temp[row][column]=0
                        flag=True
                if cp==0:
                    #augmentation condition
                    if c_p==1 and ((buffer[row][column-1]==1 and buffer[row-1][column]==1) or (buffer[row][column-1]==1 and buffer[row+1][column]==1)):
                        temp[row][column]=1
                        flag=True

        buffer=copy.deepcopy(temp)

        if flag:
            tsf_iteration+=1
            tsfiterstr.set(tsf_iteration)
            binarytoString(buffer)
            writeBinaryToScreen()
        else:
            binarytoString(buffer)
            writeBinaryToScreen()
            tsfdone.set("Done!")


    print("\nTSF Algorithm")
    print("Shape Count: ", tsf_ncc)
    print("Iteration Count: ", tsf_iteration)


######################
# LEVIALDI ALGORITHM #
######################

def levialdi_algorithm():
    global binaryImage
    global lev_iteration
    global lev_ncc
    global levialdinccstr
    global levialdiiterstr
    global levialdidone

    levialdidone.set("")
    levialdinccstr.set(0)
    levialdiiterstr.set(0)

    lev_iteration,lev_ncc=0,0

    nrow,ncolumn = len(binaryImage),len(binaryImage[0])
    array=numpy.copy(binaryImage)
    flag=True #flag for checking if there is any change in the picture
    buffer=numpy.copy(binaryImage) #buffer array
    temp=copy.deepcopy(buffer) #temp array for copying



    while flag:
        flag=False
        for row in range(1,nrow-1):
            for column in range(1,ncolumn-1):
                cp=buffer[row][column] #center pixel
                lp=buffer[row][column-1] #left pixel
                clp=buffer[row+1][column-1] # cross-left pixel
                bp=buffer[row+1][column] #below pixel

                #sum of all pixels excluding center pixel
                neighborhood_8 = buffer[row-1][column-1] + buffer[row-1][column] + buffer[row-1][column+1] + buffer[row][column+1] + buffer[row+1][column+1]+lp+clp+bp

                #isolated point detection
                if cp==1 and neighborhood_8 == 0:
                    lev_ncc += 1
                    levialdinccstr.set(lev_ncc)
                    temp[row][column]=0
                    flag=True

                if cp==1 and lp==0 and clp==0 and bp==0:
                    temp[row][column]=0
                    flag=True

                if cp==0 and lp==1 and bp==1:
                    temp[row][column]=1
                    flag=True

        if flag:
            lev_iteration+=1
            levialdiiterstr.set(lev_iteration)
            buffer=copy.deepcopy(temp)
            binarytoString(buffer)
            writeBinaryToScreen()
        else:
            buffer=copy.deepcopy(temp)
            binarytoString(buffer)
            writeBinaryToScreen()
            levialdidone.set("Done!")


    print("\nLevialdi Algorithm")
    print("Shape Count: ", lev_ncc)
    print("Iteration Count: ", lev_iteration)



#Opening an image
def openImage(sel):
    global path
    if not sel:
        openFileFormats = (("all files", "*.*"), ("png files", "*.png"))  # File formats for easy search
        path = askopenfilename(parent=gui_frame, filetypes=openFileFormats)  # Basic file pick gui
    fp = open(path, "rb")  # Read file as a byte map
    print(path)

    global openedImage
    global resizedImage
    global max_height
    global max_width
    global levialdidone
    global tsfdone

    levialdidone.set("")
    tsfdone.set("")
    levialdinccstr.set("0")
    levialdiiterstr.set("0")
    tsfnccstr.set("0")
    tsfiterstr.set("0")

    openedImage = Image.open(fp).convert('1', dither=Image.NONE)  # Convert byte map to Image then grayscaling of the image
    (ncol,nrow)=openedImage.size
    resizedImage=openedImage
    if ncol>500 or nrow>500:
        ratio=max((ncol/max_height), (nrow/max_width))
        print("Ratio: ", ratio, ", i:", int(ncol/ratio), ", j:",int(nrow/ratio) )
        resizedImage=openedImage.resize((int(ncol/ratio), int(nrow/ratio)))


    imageProcess()

def binarytoString(binaryImgArray):
    global pixelMapAsString
    global resizedImage

    nCol, nRow = resizedImage.size

    #Create binary image according to pixel map
    if pixelMapAsString!="": pixelMapAsString=""
    for r in range(nRow):
        for c in range(nCol):
            pixelMapAsString +=  str(binaryImgArray[r][c])
        pixelMapAsString += "\n"
    #print(pixelMapAsString)




def imageProcess():
    global resizedImage
    global openedImage
    nCol, nRow = resizedImage.size
    print("-------------------------------------------")
    print("Image size : \nHorizontal : ",openedImage.size[0],"\nVertical : ", openedImage.size[1])
    print("-------------------------------------------")

    #openedImage
    colorMap = resizedImage.load() # Images to pixel map because of converting return average of RGB

    global framedImage
    # Creates an image with 2 additional columns and rows for framing edges
    framedImage = Image.new('RGB', ((nCol+2), (nRow+2)), color='black').convert('1', dither=Image.NONE)
    #convert 1 : black white image
    #convert L : gray scaled image
    reset()
    for r in range(1,nRow+1):
        for c in range(1,nCol+1):
            framedImage.putpixel((c,r), colorMap[c-1,r-1]) #Coloring framed image

    colorMap = framedImage.load() # Images to pixel map
    orNCol,orNRow=nCol,nRow

    nCol, nRow = framedImage.size
    print("-------------------------------------------")
    print("Framed Image size : \nHorizontal : ", nCol, "\nVertical : ", nRow)
    print("-------------------------------------------")

    global binaryImage
    binaryImage = [[0 for x in range(nCol)] for y in range(nRow)]  # Set pixelValue sizes

    global pixelMapAsString

    #Create binary image according to pixel map
    if pixelMapAsString!="": pixelMapAsString=""
    for r in range(nRow):
        for c in range(nCol):
            if colorMap[c,r] > 200:
                binaryImage[r][c] = 1
            else:
                binaryImage[r][c] = 0
            pixelMapAsString +=  str(binaryImage[r][c])
        pixelMapAsString += "\n"


    # Putting image to screen
    global img1
    global max_width
    global max_height

    (ncol,nrow)=openedImage.size
    ratio=max((ncol/max_height), (nrow/max_width))
    print("Ratio: ", ratio, ", i:", int(ncol/ratio), ", j:",int(nrow/ratio) )


    defImg = ImageTk.PhotoImage(framedImage.resize((int(ncol/ratio), int(nrow/ratio))))
    img1.config(image=defImg)
    img1.image = defImg
    img1.update()


#reseting the canvas
def reset():
    global openedImage
    global pixelMapAsString
    global binaryCanvas
    if pixelMapAsString!="": pixelMapAsString=""
    binaryCanvas.delete("binary")



#writing binary image and iterations of algorithms on screen
def writeBinaryToScreen():
    global binaryCanvas
    global pixelMapAsString
    global openedImage
    binaryCanvas.delete("binary")
    fontSize=1
    if openedImage.size[0]>299 or openedImage.size[1]>299:
        fontSize = 1
    elif openedImage.size[0]>199 or openedImage.size[1]>199:
        fontSize=2
    elif openedImage.size[0]>100 or openedImage.size[1]>100:
        fontSize = 3
    else:
        fontSize=4
    try:
        w=binaryCanvas.winfo_width()
        h=binaryCanvas.winfo_height()

        binaryCanvas.create_text(w/2,h/2, text=pixelMapAsString, font=("Ariel", fontSize, "bold"), tag="binary", anchor=CENTER)

        binaryCanvas.update()

    except:
        pass

    binaryCanvas.update()



selectButton = Button(gui_frame, text='Open', borderwidth=1, command=lambda:[openImage(None),writeBinaryToScreen()], relief=RAISED)
selectButton.grid(row=0, column=0, sticky=NW, padx=20, pady=20)

createButton = Button(gui_frame, text='Create Image', borderwidth=1, command=lambda:controller(0), relief=RAISED)
createButton.grid(row=0, column=0, sticky=NE, padx=20, pady=20)

levButton = Button(gui_frame, text='Levialdi', borderwidth=1, command=levialdi_algorithm, relief=RAISED)
levButton.grid(row=0, column=1, sticky=NE, padx=20, pady=20)

tsfButton = Button(gui_frame, text='TSF', borderwidth=1, command=tsf_algorithm, relief=RAISED)
tsfButton.grid(row=0, column=1, sticky=NW, padx=20, pady=20)

binaryCanvas = Canvas(gui_frame, borderwidth=2, bg="white", bd=3, relief="groove")
binaryCanvas.grid(row=1, column=1, sticky=W + E + N + S, padx=10)

img1 = Label(gui_frame, borderwidth=2, bg="white", fg="black", bd=3, relief="groove")
img1.grid(row=1, column=0, sticky=W + E + N + S, padx=10)

gui_frame.mainloop()
