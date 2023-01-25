from fastapi import FastAPI, File, UploadFile, Request, Form, Query
from typing import Union
import shutil
import os
import io
import cv2
from starlette.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pathlib import Path
from pydantic import BaseModel
from typing import List


relative = os.getcwd()

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

# HOME

@app.get("/", response_class=HTMLResponse)
async def uploadFile(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})

# LOGIN PAGE 

# UPLOADING IMAGES
@app.get("/uploadImages/", response_class=HTMLResponse)
async def uploadImages(request: Request):  
    link = "Cropping/cropImages.html" 
    return templates.TemplateResponse(link,{"request":request})

@app.post("/cropImages/", response_class=HTMLResponse)
async def cropImages(request: Request, files: List[UploadFile] = File(...)):
    print("paso el constructor")
    if files:
        session_dir = "static" + os.path.sep + "uploadedPictures" + os.path.sep + "prueba"
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        for f in files:
            filename = "static" + os.path.sep + "uploadedPictures" + os.path.sep + "prueba" + os.path.sep + f'{f.filename}'
            with open(filename, "wb") as buffer: 
                shutil.copyfileobj(f.file, buffer)        
        return JSONResponse(content={"message": "images uploaded successfully"})
    else:
        return JSONResponse(content={"message": "no images found"}, status_code=400)



@app.get("/upload/", response_class=HTMLResponse)
async def uploadImages(request: Request):  
    link = "Cropping/uploadImages.html" 
    return templates.TemplateResponse(link,{"request":request})
 
# PEDESTRIAN DETECTOR     

@app.get("/PedestrianDetector/", response_class=HTMLResponse)
async def pedestrianDetector(request: Request):
    '''! 
    Pedestrian Detector GET, this get function asks the user to upload a image file to upload.
    @link /PedestrianDetector/ \endlink 
    '''       
    return templates.TemplateResponse("PedestrianDetector/uploadImage.html",{"request":request})


@app.post("/PedestrianDetector/response/", response_class=HTMLResponse)
async def pedestrianDetectorResponse(request: Request, file: UploadFile = File(...)):
    '''! 
    Pedestrian Detector POST, this post function processes the data uploaded by the client and calls the detectImage(path, model) function.
    @fn detectImage(path, model) of package PedestrianDetector processes the image passed throught parameter returns the number of detected images and the image with the detected objects.
    @link /PedestrianDetector/response/ \endlink 
    @param file image to process
    '''
    path = "static" + os.path.sep + "PedestrianDetector" + os.path.sep + "pictures" + os.path.sep + f'{file.filename}'
    with open( path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    path =  relative + os.path.sep + "static" + os.path.sep + "PedestrianDetector" + os.path.sep + "results" + os.path.sep + f'{file.filename}'
    path = "PedestrianDetector/results/"+ f'{file.filename}'    
    return templates.TemplateResponse("PedestrianDetector/returnImage.html",{"request":request, "path": path})

# FACE BLUR

@app.get("/FaceBlur/", response_class=HTMLResponse)
async def faceBlur(request: Request):
    '''! 
    Face Blur GET, this get function asks the user to upload a image file to upload.
    @link /FaceBlur/ \endlink 
    '''
    return templates.TemplateResponse("FaceBlur/uploadImage.html",{"request":request})


@app.post("/FaceBlur/select/", response_class=HTMLResponse)
async def faceBlurSelect(request: Request, file: UploadFile = File(...)):
    '''! 
    Face Blur POST, this post function asks the user to select the faces that wants to blur by clicking on them.
    @link /FaceBlur/select/ \endlink 
    @param file image to process
    '''
    path = "static" + os.path.sep + "FaceBlur" + os.path.sep + "pictures" + os.path.sep + f'{file.filename}'
    with open( path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    path = "FaceBlur" + os.path.sep + "pictures" + os.path.sep + f'{file.filename}'
    name =  f'{file.filename}'
    return templates.TemplateResponse("FaceBlur/selectRange.html",{"request":request, "path":path, "name":name})


@app.post("/FaceBlur/response/", response_class=HTMLResponse)
async def faceBlurResponse(request: Request, x: int = Form(...), y: int = Form(...), x2: int = Form(...), y2: int = Form(...), x3: int = Form(...), y3: int = Form(...), x4: int = Form(...), y4: int = Form(...),x5: int = Form(...), y5: int = Form(...), width: int = Form(...),height: int = Form(...), imgName: str = Form(...)): 
    '''! 
    Face Blur POST, this post function processes the data uploaded by the client, the image and the points selected.
    @fn faceBlur(path, model, r) of package FaceBlur processes the image passed throught parameter with the model and the points stored in array R. This function detects the faces and if the points passed match with the faces selected, returns the number of detected faces and the image with the blured objects.
    @link FaceBlur/response/ \endlink 
    @param x up to 5 points, in axis X
    @param y up to 5 points, in axis Y
    @param width witdth of the image on the screen of the client
    @param height height of the image on the screen of the client
    @param imageName name of the image on the system
    '''
    path =  relative + os.path.sep + "static" + os.path.sep + "FaceBlur" + os.path.sep + "pictures" + os.path.sep + f'{imgName}'
    nDetections=0
    r = [[x,y],[x2,y2],[x3,y3],[x4,y4],[x5,y5]]
    img=cv2.imread(path)
    originalHeight = img.shape[0]
    originalWidth = img.shape[1]
    for h in r:
        h[0] = int((originalWidth * h[0])/width)
        h[1] = int((originalHeight * h[1])/height)
    path =  relative + os.path.sep + "static" + os.path.sep + "FaceBlur" + os.path.sep + "results" + os.path.sep + f'{imgName}'
    cv2.imwrite(path,img)
    path = "FaceBlur/results/"+ f'{imgName}'    
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("FaceBlur/returnImage.html",{"request":request, "nDetections": nDetections, "path": path})

# IMAGE TRANSFORMATOR



@app.get("/ImageTransformator/", response_class=HTMLResponse)
async def imageTransformator(request: Request):
    '''! 
    Image Transformator GET, this get function asks the user to upload a image file to upload and the function the user wants to use.
    @link /ImageTransformator/ \endlink 
    @radioButtons 
    @li 1 Box Image
    @li 2 Clean Noise
    @li 3 Delete Lines
    @li 4 Rotator
    @li 5 Reader 
    '''
    return templates.TemplateResponse("ImageTransformator/uploadImage.html",{"request":request})


@app.post("/ImageTransformator/response/", response_class=HTMLResponse)
async def imageTransformatorResponse(request: Request, file: UploadFile = File(...), function: int = Form(...)):
    '''! 
    Image Transformator POST, this post function processes the uploaded image and the function to select
    @link /ImageTransformator/response/ \endlink 
    @fn 1 boxImage(path) boxes the object of an image \fn
    @fn 2 cleanNoise(path) cleans the possible noise of an image \fn
    @fn 3 deleteLines(path) deletes horizontal and vertical lines of an image \fn
    @fn 4 rotator(path) rotates the image dependign on the orientarion of the possible text and objects of the image \fn
    @fn 5 reader(path) reads the text of the image with an OCR provided by tesseract \fn
    '''
    if function == 1:
        function = "BoxImage"
        path = "static" + os.path.sep + "ImageTransformator" + os.path.sep + "pictures" + os.path.sep + function + os.path.sep + f'{file.filename}'
        with open( path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        path =  relative + os.path.sep + "static" + os.path.sep + "ImageTransformator" + os.path.sep + "results" + os.path.sep + function + os.path.sep + f'{file.filename}'
        path = "ImageTransformator/results/"+ function +"/"+ f'{file.filename}'  
    if function == 2:
        function = "CleanNoise"
        path = "static" + os.path.sep + "ImageTransformator" + os.path.sep + "pictures" + os.path.sep + function + os.path.sep + f'{file.filename}'
        with open( path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        path =  relative + os.path.sep + "static" + os.path.sep + "ImageTransformator" + os.path.sep + "results" + os.path.sep + function + os.path.sep + f'{file.filename}'
        path = "ImageTransformator/results/"+ function +"/"+ f'{file.filename}' 
    if function == 3:
        function = "DeleteLines"
        path = "static" + os.path.sep + "ImageTransformator" + os.path.sep + "pictures" + os.path.sep + function + os.path.sep + f'{file.filename}'
        with open( path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        path =  relative + os.path.sep + "static" + os.path.sep + "ImageTransformator" + os.path.sep + "results" + os.path.sep + function + os.path.sep + f'{file.filename}'
        path = "ImageTransformator/results/"+ function +"/"+ f'{file.filename}'  
    if function == 4:
        function = "Rotator"
        path = "static" + os.path.sep + "ImageTransformator" + os.path.sep + "pictures" + os.path.sep + function + os.path.sep + f'{file.filename}'
        with open( path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        path =  relative + os.path.sep + "static" + os.path.sep + "ImageTransformator" + os.path.sep + "results" + os.path.sep + function + os.path.sep + f'{file.filename}'
        path = "ImageTransformator/results/"+ function +"/"+ f'{file.filename}' 
    if function == 5:
        function = "Reader"
        path = "static" + os.path.sep + "ImageTransformator" + os.path.sep + "pictures" + os.path.sep + function + os.path.sep + f'{file.filename}'
        with open( path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        path = "static" + os.path.sep + "ImageTransformator" + os.path.sep + "results" + os.path.sep + function + os.path.sep + file.filename.split('.')[0] + '.txt'
        return templates.TemplateResponse("ImageTransformator/returnText.html",{"request":request})
    return templates.TemplateResponse("ImageTransformator/returnImage.html",{"request":request, "path": path})


