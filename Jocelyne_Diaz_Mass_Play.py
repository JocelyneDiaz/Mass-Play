#*****************************************************************************
#Arch 441//Medium//Fall 2021//Ericson
#
#Student Name:JOCELYNE DIAZ
#Date Modified
#Project Name: MASS PLAY
#*****************************************************************************
#imported Libraries
#
import rhinoscriptsyntax as rs
import Rhino as rh
import System
import scriptcontext as sc
import math
import random
import time
import Rhino
from math import radians
#
#*****************************************************************************
#Functions:

def GetCaptureView(Scale,FileName,NewFolder):
    #Source: https://github.com/mcneel/rhino-developer-samples/blob/6/rhinopython/SampleViewCaptureToFile.py
    #Modified by Mark Ericson to include file/folder directory and scale. 2.18.21

    #this function saves the current viewport to the desktop in a specified folder as a png.
    #Use scale to scale up or down the viewport size to inccrease/ecrease resolution
    #Will overwrite folders and files with same name. 


    view = sc.doc.Views.ActiveView;
    if view:
        view_capture = Rhino.Display.ViewCapture()
        view_capture.Width = view.ActiveViewport.Size.Width*Scale
        view_capture.Height = view.ActiveViewport.Size.Height*Scale
        view_capture.ScaleScreenItems = False
        view_capture.DrawAxes = False
        view_capture.DrawGrid = False
        view_capture.DrawGridAxes = False
        view_capture.TransparentBackground = False
        bitmap = view_capture.CaptureToBitmap(view)
        if bitmap:
            #locate the desktop and get path
            folder = System.Environment.SpecialFolder.Desktop
            path = System.Environment.GetFolderPath(folder)
            #convert foldername and file name sto string
            FName = str(NewFolder)
            File = str(FileName)
            #combine foldername and desktop path
            Dir = System.IO.Path.Combine(path,FName)
            #creat path to tje new folder
            NFolder = System.IO.Directory.CreateDirectory(Dir)
            Dir = System.IO.Path.Combine(Dir,FileName +".png")
            print (Dir)
            #save the file
            bitmap.Save(Dir, System.Drawing.Imaging.ImageFormat.Png);


def SaveObj(Objects,FileName,NewFolder):
    rs.SelectObjects(Objects)
    
    folder = System.Environment.SpecialFolder.Desktop
    path = System.Environment.GetFolderPath(folder)
    #convert foldername and file name sto string
    FName = str(NewFolder)
    File = str(FileName)
    #combine foldername and desktop path
    Dir = System.IO.Path.Combine(path,FName)
    NFolder = System.IO.Directory.CreateDirectory(Dir)
    Dir = System.IO.Path.Combine(Dir,FileName +".obj")
    cmd = "_-Export " + Dir + " _Enter PolygonDensity=1 _Enter"
    rs.Command(cmd)


####START#####


#GRID
def CreateGrid(Xnumber,Ynumber,Znumber,Distance):
    #Creates a 3D Grid
    Grid = []
    for i in range(0,Xnumber,Distance):
        x = i
        for j in range(0,Ynumber,Distance):
            y = j
            for p in range(0,Znumber,Distance):
                z = p

                Grid.append((x,y,z))
    return(Grid)

#Shere
def add_sphere_level(point, level, Radius):


    point_2 = rs.AddPoint(point)
    x, y, z = rs.PointCoordinates(point_2)
    
    new_point = x,y,level

    Sphere = rs.AddSphere(new_point,Radius)
    return Sphere
###create cue part of room and Cube
def add_cube_level(point, level, Radius):

    point_2 = rs.AddPoint(point)
    Cx = rs.PointCoordinates(point_2)[0]
    Cy = rs.PointCoordinates(point_2)[1]
    Cz = level
    #lower 4 points
    p1 = (Cx-Radius,Cy-Radius,Cz-Radius)
    p2 = (Cx+Radius,Cy-Radius,Cz-Radius)
    p3 = (Cx+Radius,Cy+Radius,Cz-Radius)
    p4 = (Cx-Radius,Cy+Radius,Cz-Radius)
    
    #upper 4 points
    p5 = (Cx-Radius,Cy-Radius,Cz+Radius)
    p6 = (Cx+Radius,Cy-Radius,Cz+Radius)
    p7 = (Cx+Radius,Cy+Radius,Cz+Radius)
    p8 = (Cx-Radius,Cy+Radius,Cz+Radius)
    
    #make a box
    Box = rs.AddBox([p1,p2,p3,p4,p5,p6,p7,p8])
    #return the box
    print(Cz)
    return Box

###create level and union all parts at one level
def create_level(level):
    room_number = rs.GetInteger("How many rooms would you like to create on the this level?")
    scale_factor = 1.25
    rooms = []
    for j in range(room_number):
        Radius = rs.GetReal("How many feet would you like the room to be ?")
        point = rs.GetPoint("Select a point on the plane to place the room")
        sphere = add_sphere_level(point, level,Radius*scale_factor)
        cube = add_cube_level(point, level,Radius)
        room = rs.BooleanUnion([sphere,cube])
        rooms.append(room)
    level =  rs.BooleanUnion(rooms)
    return level
def LinearColor(R,G,B,R2,G2,B2,ColorPercentage):
    
    #This function defines linear color gradient by treating R,G,B as coordinates on a 3D line.
    #The base color that will be altered by the percentage should be entered in the second R2,G2,B2 valu
    
    Rdiff = R2 - R
    Gdiff = G2 - G
    Bdiff = B2 - B


    t = ColorPercentage


    R3 = float(R + Rdiff*t)
    G3 = float(G + Gdiff*t)
    B3 = float(B + Bdiff*t)


    return (R3,G3,B3)


def color_objects(objects):
    
    length = len(objects)
    color_inc = 1.0/length
    color_step = 0
    for i in objects:
        color_step += color_inc
        color = LinearColor(255,0,0,30,144,255
        
        
        ,color_step)
        rhino_color = rs.CreateColor(color)
        rs.AddMaterialToObject(i)
        index = rs.ObjectMaterialIndex(i)
        rs.MaterialColor(index,rhino_color)
        rs.ObjectColor(i, rhino_color)


##main function
def main():
    rs.UnitSystem(9) #set units to feet 
    proceed = rs.MessageBox("This script produces a community center would you like to proceed?", 4)
    level_number = rs.GetInteger("How many levels should this building have?")
    level_height = 10
    top_floor_level = level_height*level_number
    for i in range(0,top_floor_level,level_height):
        create_level(i)
    objects = rs.ObjectsByType(16,select=True)
    color_objects(objects)


main()