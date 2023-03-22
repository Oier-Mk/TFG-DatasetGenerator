from stable_diffusion.train import train, train2
from stable_diffusion.inference import infereDataset, infereTest
import os 
import shutil
import threading

def train_model(session_data, envMail, input_Dataset, input_Session_Name, input_Concept, input_Resume_Training, input_UNet_Training_Steps, input_UNet_Learning_Rate, input_Text_Encoder_Training_Steps, input_Text_Encoder_Concept_Training_Steps, input_Text_Encoder_Learning_Rate, input_Save_Checkpoint_Every, input_Start_saving_from_the_step):
    t = threading.Thread(target=train2, args=(session_data, envMail, input_Dataset, input_Session_Name, input_Concept, input_Resume_Training, input_UNet_Training_Steps, input_UNet_Learning_Rate, input_Text_Encoder_Training_Steps, input_Text_Encoder_Concept_Training_Steps, input_Text_Encoder_Learning_Rate, input_Save_Checkpoint_Every, input_Start_saving_from_the_step))
    t.start()

def test_model(session_data, temp_folder, model, prompt, nSteps, element, scheduler):
    infereTest(model, temp_folder = temp_folder,prompt = prompt, nSteps = nSteps, element = element, nImages = 1, scheduler = scheduler,)
    
def generate_dataset(username, envMail, name, model, prompt, nSteps, element, nImages, scheduler):
    t = threading.Thread(target=infereDataset, args=(username, envMail, name, model, prompt, nSteps, element, nImages, scheduler))
    t.start()

def get_sessions(session, directory):
    sessions = []
    for f in os.listdir(directory):
        if (f != ".DS_Store"):
            sessions.append(f)
    return sessions

def show_results(session, directory):
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

    n = 3
    return [folder[i:i+n] for i in range(0, len(folder), n)]

def get_results(session, session_data):
        if (session == "ftm"):
            directory = os.path.join(os.getcwd(), "static", "users", session_data.username, "datasets")
            session = [file for file in os.listdir(directory) if file != ".DS_Store"][0]

        if (session != "ftm"):

            folder_path = os.path.join(
                os.getcwd(), "static", "users", session_data.username, "datasets", session)

        zip_path = os.path.join(
            os.getcwd(), "static", "users", session_data.username, "compressed")
        if not os.path.exists(zip_path):
            os.makedirs(zip_path)
        zip_path = os.path.join(os.getcwd(
        ), "static", "users", session_data.username, "compressed", session)

        shutil.make_archive(zip_path, "zip", folder_path)

        return zip_path + ".zip"
