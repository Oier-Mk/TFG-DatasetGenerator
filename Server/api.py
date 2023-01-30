from fastapi import FastAPI, File, UploadFile, Request, Form, Response
import shutil
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import List

relative = os.getcwd()
users = {}
users["oime3564@gmail.com"] = ["Oier", "oime3564@gmail.com", "1234"]
users["oime6435@gmail.com"] = ["Oier", "oime6435@gmail.com", "1234"]

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
    return templates.TemplateResponse("home.html", {"request": request})

# LOGIN PAGE


@app.get("/login/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    link = "Login/login.html"
    return templates.TemplateResponse(link, {"request": request})


@app.get("/correct-login/{email}", response_class=HTMLResponse)
async def uploadImages(request: Request, email: str):
    return templates.TemplateResponse("Login/correctLogin.html", {"request": request, "name": users[email][0]})


@app.get("/correct-singup/{name}")
async def correct_singup(request: Request, name: str):
    return templates.TemplateResponse("login/correctSingup.html", {"request": request, "name": name})


@app.post("/check-password/", response_class=HTMLResponse)
async def uploadImages(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    # TODO gestionar base de datos con usuarios
    print(email + " " + password)
    if (name == "Name" and password2 == "Repeat your password"):
        print("login")
        if (email in users):
            if (users[email][2] == password):
                return "correct"
            else:
                return "incorrect"
        else:
            return "singup"
    else:
        users[email] = [name, email, password]
        print(users[email])
        return "correct"

# UPLOADING IMAGES


@app.get("/uploadImages/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    # TODO: comprobar que el usuario se ha logueado y de no ser asi mandarle loguearse
    userLoggedin = True
    if (userLoggedin):
        link = "Cropping/cropImages.html"
        return templates.TemplateResponse(link, {"request": request})
    else:
        # TODO pass message throw variable.
        link = "Utils/rejection.html"
        return templates.TemplateResponse(link, {"request": request})


@app.post("/cropImages/", response_class=HTMLResponse)
async def cropImages(request: Request, files: List[UploadFile] = Form(...), sessionName: str = Form(...)):
    if files:

        session_dir = "static" + os.path.sep + os.path.sep + \
            "uploadedPictures" + os.path.sep + "oime3564@gmail.com" + os.path.sep + sessionName + os.path.sep
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)

        for i in files:
            print(i.filename)
            with open(session_dir + i.filename, "wb") as buffer:
                buffer.write(i.file.read())
                buffer.close()
        link = "/Utils/confirmation.html"
    else:
        link = "Utils/rejection.html"
    # TODO añadir proceso de training de las fotos
    return templates.TemplateResponse(link, {"request": request})


# FILE EXPLORER

@app.get("/fileExplorer/{session}", response_class=HTMLResponse)
async def uploadImages(request: Request, session: str):

    # muestro las sesiones del usuario
    directory = os.path.join(os.getcwd(), "static",
                             "uploadedPictures", "oime3564@gmail.com")
    sessions = []
    for f in os.listdir(directory):
        if (f != ".DS_Store"):
            sessions.append(f)

    # por defecto muestro la primera sesion del usuario.
    if (session != "ftm"):
        for f in os.listdir(directory):
            if (f == session):
                folder_path = os.path.join(directory, f)
                folder = os.listdir(folder_path)
                break
    else:
        for f in os.listdir(directory):
            if (f != ".DS_Store"):
                folder_path = os.path.join(directory, f)
                folder = os.listdir(folder_path)
                break

    folder_path = folder_path.split("static/")[1]

    folder = [folder_path + os.path.sep + file for file in folder]

    for i in folder:
        if i.endswith('.DS_Store'):
            folder.remove(i)

    names = [string.split('/')[-1] for string in folder]

    n = 3
    folder = [folder[i:i+n] for i in range(0, len(folder), n)]

    names = [folder[i:i+n] for i in range(0, len(folder), n)]

    link = "FileExplorer/fileExplorer.html"
    return templates.TemplateResponse(link, {"request": request, "sessions": sessions, "folder": folder, "names": names})


@app.get("/download/{session}")
async def download_zip(request: Request, session: str):
    if (session == "ftm"):
        session = os.listdir(os.path.join(
            os.getcwd(), "static", "uploadedPictures", "oime3564@gmail.com"))[0]
    if (session != "ftm"):

        folder_path = os.path.join(
            os.getcwd(), "static", "uploadedPictures", "oime3564@gmail.com", session)

        zip_path = os.path.join(
            os.getcwd(), "static", "uploadedPictures", "compressed", "oime3564@gmail.com")
        if not os.path.exists(zip_path):
            os.makedirs(zip_path)
        zip_path = os.path.join(os.getcwd(
        ), "static", "uploadedPictures", "compressed", "oime3564@gmail.com", session)

        shutil.make_archive(zip_path, "zip", folder_path)

        return Response(content=open(zip_path+".zip", 'rb').read(), media_type="application/zip")

