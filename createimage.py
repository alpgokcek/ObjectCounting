"""
Name Surname:   Alp Gökçek
Department:     Computer Engineering
Instructor:     Muhittin Gökmen
Course:         COMP204-Programming Studio
Date:           05/03/2019
"""

from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.colorchooser import askcolor
import tkinter
from PIL import Image, ImageDraw,ImageFont, ImageTk
import cv2
import os
import subprocess
import io, math, random


class create:

        #rgb and hex color
        black=((0,0,0),"#000000")
        white=((255,255,255),"#FFFFFF")

        file_directory=None

        canvas,scale=None,None

        initial_thickness=5
        initial_color=white[1]
        initial_tool="pen"

        tools=["pen","rectangle","circle","line","eraser"]

        mouse_state="r" #r for released, c for clicked

        x_pos, y_pos = None,None
        x1,y1,x2,y2=None,None,None,None

        created_obj_size=0

        def choose_color(self):
            self.initial_color=askcolor()
            self.initial_color=self.initial_color[1]
            #print(self.initial_color)

        def setTool(self,toolName,frame):
            if toolName in self.tools:
                self.initial_tool=toolName
            self.thickness(frame)

        def mouse_clicked(self,event):
            self.mouse_state="c"
            try:
                self.x1=event.x
                self.y1=event.y

            except Exception as e:
                print(e)

        def mouse_released(self, event):
            self.mouse_state="r"

            self.x_pos,self.y_pos=None,None

            self.x2=event.x
            self.y2=event.y


            if self.initial_tool == "line": self.line_tool(event)
            elif self.initial_tool == "circle": self.circle_tool(event)
            elif self.initial_tool == "rectangle": self.rectangle_tool(event)


        def motion(self,event=None):
            try:
                if self.initial_tool in ("pen", "eraser"):
                    self.pen_tool(event)
            except Exception as e:
                print(e)

        def line_tool(self, event):
            try:
                event.widget.create_line(self.x1,self.y1,self.x2,self.y2, width=self.scale.get(),fill=self.initial_color, tags="object")
                self.created_obj_size+=abs((((self.x2-self.x1)**2 + (self.y2-self.y1)**2)**0.5)*self.scale.get())
            except Exception as e:
                print(e)

        def pen_tool(self, event):
            color=None
            try:
                if self.mouse_state == "c":
                    if self.x_pos is not None and self.y_pos is not None:
                        r=self.scale.get()
                        if self.initial_tool=="eraser":
                            color=self.black[1]
                        else:
                            color=self.initial_color
                        event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y, fill = color, width=r, capstyle=ROUND, smooth=TRUE, splinesteps=36, tags="object")
                        self.created_obj_size+=abs((((event.x-self.x_pos)**2 + (event.y-self.y_pos)**2)**0.5)*self.scale.get())

                    self.x_pos = event.x
                    self.y_pos = event.y
            except Exception as e:
                print(e)

        def rectangle_tool(self, event):
            try:
                event.widget.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill= self.initial_color,outline=self.initial_color, tags="object")
                self.created_obj_size+=abs((self.x2-self.x1)*(self.y2-self.y1))

            except Exception as e:
                print(e)

        def circle_tool(self, event):
            try:
                event.widget.create_oval(self.x1,self.y1,self.x2,self.y2,fill= self.initial_color,outline=self.initial_color, tags="object")
                self.created_obj_size+=abs(((self.x2-self.x1)/2)*((self.y2-self.y1)/2)*math.pi)
            except Exception as e:
                print(e)

        def saveas_image(self):
            self.file_directory=filedialog.asksaveasfilename(initialdir="/", title = "Select file",filetypes = (("png files","*.png"),("jpeg files","*.jpg"),("all files","*.*")))
            self.save_image(self.file_directory)
            return self.file_directory

        def random_image(self):
            for i in range(0,int(self.scale.get())):
                random_number=random.randint(0,3)
                x1,y1,x2,y2=random.randint(10,1000),random.randint(10,500),random.randint(10,1000),random.randint(10,500)
                while abs(x2-x1)<10 or abs(y2-y1)<10 or x1==y1 or x2==y2:
                    x1,y1,x2,y2=random.randint(10,1000),random.randint(10,500),random.randint(10,1000),random.randint(10,500)
                if random_number==0:
                    self.canvas.create_rectangle(x1,y1,x2,y2,fill= self.initial_color,outline=self.initial_color, tags="object")
                    self.created_obj_size+=abs((x2-x1)*(y2-y1))
                elif random_number==1:
                    self.canvas.create_oval(x1,y1,x2,y2,fill= self.initial_color,outline=self.initial_color, tags="object")
                    self.created_obj_size+=abs(((x2-x1)/2)*((y2-y1)/2)*math.pi)
                else:
                    self.canvas.create_line(x1,y1,x2,y2, width=5,fill=self.initial_color, tags="object")
                    self.created_obj_size+=abs((((x2-x1)**2 + (y2-y1)**2)**0.5)*5)



        def save_image(self,file_name):
            if not file_name:
                self.file_directory="created-image.png"

            canvas_postscript = self.canvas.postscript(colormode='color')
            Image.open(io.BytesIO(canvas_postscript.encode('utf-8'))).crop((0,1,1000,501)).save(self.file_directory)
            return self.file_directory


        def discard_image(self):
            #self.image=Image.new("RGB", (1000,500),self.white)
            self.canvas.delete("object")
            #self.canvas.create_rectangle((self.canvas.winfo_rootx()),(self.canvas.winfo_rooty()),(self.canvas.winfo_rootx()+1000),(self.canvas.winfo_rooty()+600),outline=self.black[1],fill= self.black[1])


        def thickness(self,frame):
            if self.initial_tool in ("pen", "line","eraser") and not self.scale:
                self.scale=Scale(frame,from_=1, to=10, tickinterval=1,orient=HORIZONTAL,background='#EFEFEF',length=180)
                self.scale.set(5)
                self.scale.pack()
            elif self.scale and self.initial_tool not in ("pen", "line","eraser"):
                self.scale.pack_forget()
                self.scale=None



        def __init__(self,frame):

            text=Label()

            tools_frame=Frame(frame)
            tools_frame.pack(side="top")

            self.canvas = Canvas(frame,width="1000",height="500",bd=0, highlightthickness=0,highlightbackground="black",background="black")
            self.canvas.configure(cursor="crosshair")
            self.canvas.pack(padx="20")
            self.canvas.create_rectangle((self.canvas.winfo_rootx()),(self.canvas.winfo_rooty()),(self.canvas.winfo_rootx()+1100),(self.canvas.winfo_rooty()+600),outline=self.black[1],fill= self.black[1])

            #canvas events
            self.canvas.bind("<ButtonPress-1>", self.mouse_clicked)
            self.canvas.bind("<ButtonRelease-1>", self.mouse_released)
            self.canvas.bind("<Motion>", self.motion)
            self.canvas.update()

            #circle button
            circle_button=Button(tools_frame, text="Circle", command=lambda:self.setTool("circle",tools_frame))
            circle_button.pack(side="left", padx="20",pady="10")

            #rectangle button
            rectangle_button=Button(tools_frame, text="Rectangle", command=lambda:self.setTool("rectangle",tools_frame))
            rectangle_button.pack(side="left", padx="20",pady="10")

            #line button
            line_button=Button(tools_frame, text="Line", command=lambda:self.setTool("line",tools_frame))
            line_button.pack(side="left", padx="20",pady="10")

            #pen button
            pen_button=Button(tools_frame, text="Pen", command=lambda:self.setTool("pen",tools_frame))
            pen_button.pack(side="left",padx="20",pady="10")

            #eraser button
            eraser_button=Button(tools_frame, text="Eraser", command=lambda:(self.setTool("eraser",tools_frame),print("clicked")))
            eraser_button.pack(side="left",padx="20",pady="10")

            #color button
            color_button=Button(tools_frame, text="Color", command=self.choose_color)
            color_button.pack(side="left", padx="20",pady="10")

            #clear button
            clear_button=Button(tools_frame, text="Clear", command=lambda:self.discard_image())
            clear_button.pack(side="left", padx="20",pady="10")

            #random image button
            randomimg_button=Button(tools_frame, text="Random Image", command=lambda:self.random_image())
            randomimg_button.pack(side="left", padx="20",pady="10")

            frame.configure(background='#EFEFEF')
            tools_frame.configure(background='#EFEFEF')
            self.setTool(self.initial_tool,tools_frame)
