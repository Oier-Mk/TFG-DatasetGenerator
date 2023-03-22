from fastapi import FastAPI, Depends, UploadFile, Request, Form, Response
import base64
import time
import json
import os
import tempfile
import shutil
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import List
from uuid import uuid4
from mail_sender.sender import *
from user_management.sessions import *
from database.database import *

from stable_diffusion.stable_diffusion import show_results, get_sessions, get_results, train_model, test_model, generate_dataset


#delete_database()

# CREATE APP

app = FastAPI()

# STATIC FILES

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

#LOAD TEMPLATES

templates = Jinja2Templates(directory="templates") 

# LOAD EMAIL CONFIG

envMail = ".env"

envDDBB = "/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB"

# HOME

@app.get("/", response_class=HTMLResponse)
async def home(request: Request): return templates.TemplateResponse("home.html", {"request": request})

# LOGIN PAGE


@app.get("/login/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def getLogin(request: Request, session_data: SessionData = Depends(verifier)):
    try: 
        session_data.username
        logout(request, session_data)
    except: pass 
    return templates.TemplateResponse("Login/login.html", {"request": request})


@app.post("/login/", response_class=HTMLResponse)
async def postLogin(request: Request, response: Response, name: str = Form(...), email: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    print(email + " - " + password)
    if user_exists(envDDBB, email):
        if (get_password(envDDBB, email) == password):
            session = uuid4()
            data = SessionData(username=email)
            await backend.create(session, data)
            cookie.attach_to_response(response, session) #TODO get User
            return "correct"
        else:
            return "incorrect"
    else:
        if name == "Name":
            return "singup"
        else:
            if (password != password2):
                return "incorrect"
            else:
                time.sleep(1)
                session = uuid4()
                data = SessionData(username=email)
                await backend.create(session, data)
                cookie.attach_to_response(response, session)
                print(data.username)
                insert_user(envDDBB, email, name, password)
                os.mkdir("static" + os.path.sep + "users" + os.path.sep + email)
                os.mkdir("static" + os.path.sep + "users" + os.path.sep + email + os.path.sep + "inputs")
                os.mkdir("static" + os.path.sep + "users" + os.path.sep + email + os.path.sep + "models")
                os.mkdir("static" + os.path.sep + "users" + os.path.sep + email + os.path.sep + "datasets")
                os.mkdir("static" + os.path.sep + "users" + os.path.sep + email + os.path.sep + "compressed")
                return "correct"


@app.get("/correct-login/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def correctLogin(request: Request, session_data: SessionData = Depends(verifier)):
    try: 
        print(session_data.username)
        return templates.TemplateResponse("Login/correctLogin.html", {"request": request, "name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})


@app.get("/correct-singup/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def correctSingup(request: Request, session_data: SessionData = Depends(verifier)):
    try: return templates.TemplateResponse("Login/correctSingup.html", {"request": request, "name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

# LOGOUT

@app.post("/logout/")
async def logout(response: Response, session_id: UUID = Depends(cookie)):
    try:
        await backend.delete(session_id)
        cookie.delete_from_response(response)
    except Exception as e:
        e.printstack()

# UPLOADING IMAGES

@app.get("/uploadImages/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def uploadImages(request: Request, session_data: SessionData = Depends(verifier)):
    try: return templates.TemplateResponse("Cropping/cropImages.html", {"request": request, "name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})


@app.post("/cropImages/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def cropImages(request: Request, session_data: SessionData = Depends(verifier), files: List[UploadFile] = Form(...), sessionName: str = Form(...)):
    if files:
        session_dir = "static" + os.path.sep + \
            "users" + os.path.sep + session_data.username + \
            os.path.sep + "inputs" + os.path.sep + sessionName + os.path.sep
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)

        for i in files:
            print(i.filename)
            with open(session_dir + i.filename, "wb") as buffer:
                buffer.write(i.file.read())
                buffer.close()
        return templates.TemplateResponse("/Cropping/correctCrop.html", {"request": request})
    else:
        return templates.TemplateResponse("Utils/rejection.html", {"request": request})


# FILE EXPLORER

@app.get("/fileExplorer/{session}", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def fileExplorer(request: Request, session: str, session_data: SessionData = Depends(verifier)):
    try:
        try:
            # muestro las sesiones del usuario

            directory = os.path.join(os.getcwd(), "static",
                                    "users", session_data.username, "datasets")
                
            sessions = get_sessions(session, directory)
            
            folder = show_results(session, directory)

            return templates.TemplateResponse("FileExplorer/fileExplorer.html", {"request": request, "sessions": sessions, "folder": folder, "user_name": session_data.username})
        except: 
            import traceback
            traceback.print_exc()
            return templates.TemplateResponse("Utils/noFiles.html", {"request": request, "user_name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

# DOWNLOAD BUTTON


@app.get("/download/{session}", dependencies=[Depends(cookie)])
async def download(request: Request, session: str, session_data: SessionData = Depends(verifier)):
    try:
        zip_path = get_results(session, session_data)
        return Response(content=open(zip_path, 'rb').read(), media_type="application/zip")
    except: 
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

# TRAINING PHASE


@app.get("/train/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def getTrain(request: Request, session_data: SessionData = Depends(verifier)):
    try:
        try:
            # muestro las sesiones del usuario
            directory = os.path.join(
                os.getcwd(), "static", "users", session_data.username, "inputs")
            sessions = []
            for f in os.listdir(directory):
                if (f != ".DS_Store"):
                    sessions.append(f)
            return templates.TemplateResponse("Training/training.html", {"request": request, "sessions": sessions})
        except: return templates.TemplateResponse("Utils/noFiles.html", {"request": request, "user_name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})


@app.post("/train/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def postTrain(request: Request, session_data: SessionData = Depends(verifier), 
session : str = Form(...), 
resume_training : str = Form(...),  
unet_training : str = Form(...), 
unet_learning : str = Form(...), 
encoder_training : str = Form(...), 
concept_training : str = Form(...), 
encoder_learning : str = Form(...), 
style : str = Form(...)):
    try:
        session_data.username
        try:
            train_model(session_data, envMail, session, session, session, resume_training, unet_training, unet_learning, encoder_training, concept_training, encoder_learning, 0, 0)
            return "correct" 
        except: return "incorrect"
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

@app.get("/infere/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def getInfere(request: Request, session_data: SessionData = Depends(verifier)):
    try:
        try:
            # muestro las sesiones del usuario
            directory = os.path.join(
                os.getcwd(), "static", "users", session_data.username, "models")
            models = []
            for f in os.listdir(directory):
                if (f != ".DS_Store"):
                    models.append(f)
            return templates.TemplateResponse("Infering/infering.html", {"request": request, "models": models})
        except: return templates.TemplateResponse("Utils/noFiles.html", {"request": request, "user_name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

@app.post("/infere/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def postTrain(request: Request, session_data: SessionData = Depends(verifier), 
model : str = Form(...), 
prompt : str = Form(...), 
nIterations : str = Form(...), 
element : str = Form(...),
scheduler : str = Form(...)
): 
    try:
        session_data.username
        try:

            temp_folder = tempfile.mkdtemp()

            test_model(session_data, 
                       temp_folder,
                       os.path.join(os.getcwd(), "static", "users", session_data.username, "models", model), #add the path of the model in question
                       prompt, 
                       int(nIterations), 
                       element, 
                       scheduler, 
                       )

            with open(temp_folder+"/test.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

            shutil.rmtree(temp_folder)

            return json.dumps({"image": encoded_string})
        except: "incorrecto"
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})


@app.get("/generate/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def getGenerate(request: Request, session_data: SessionData = Depends(verifier)):
    try:
        try:
            # muestro las sesiones del usuario
            directory = os.path.join(
                os.getcwd(), "static", "users", session_data.username, "models")
            models = []
            for f in os.listdir(directory):
                if (f != ".DS_Store"):
                    models.append(f)
            return templates.TemplateResponse("Infering/generatingDataset.html", {"request": request, "models": models})
        except: return templates.TemplateResponse("Utils/noFiles.html", {"request": request, "user_name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

@app.post("/generate/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def postGenerate(request: Request, session_data: SessionData = Depends(verifier), 
name : str = Form(...), 
model : str = Form(...), 
prompt : str = Form(...), 
nIterations : str = Form(...), 
nImages : str = Form(...), 
element : str = Form(...),
scheduler : str = Form(...)
): 
    try:
        session_data.username
        print(session_data.username)
        try:
            generate_dataset(
                session_data.username, 
                envMail,
                name, 
                os.path.join(os.getcwd(), "static","users", session_data.username, "models", model), #add the path of the model in question
                prompt, 
                int(nIterations), 
                element, 
                int(nImages),
                scheduler, 
            )
            return "correct"
        except: return "incorrect"
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

@app.get("/correct-generation/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def correctGeneration(request: Request, session_data: SessionData = Depends(verifier)):
    try: return templates.TemplateResponse("Infering/correctGeneration.html", {"request": request, "user_name": session_data.username})
    except: 
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

@app.get("/correct-training/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def correctGeneration(request: Request, session_data: SessionData = Depends(verifier)):
    try: return templates.TemplateResponse("Training/correctTraining.html", {"request": request, "user_name": session_data.username})
    except: 
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

