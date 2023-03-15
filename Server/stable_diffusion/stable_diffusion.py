from stable_diffusion.train import train
from stable_diffusion.inference import infere
from mail_sender.sender import send_email
import os 
import shutil

async def train_model(session_data, envMail, input_Dataset, input_Session_Name, input_Concept, input_Resume_Training, input_UNet_Training_Steps, input_UNet_Learning_Rate, input_Text_Encoder_Training_Steps, input_Text_Encoder_Concept_Training_Steps, input_Text_Encoder_Learning_Rate, input_Save_Checkpoint_Every, input_Start_saving_from_the_step):
    #session en este caso es el valor del dataset
    train(
        input_Dataset, \
        input_Session_Name, \
        input_Concept, \
        input_Resume_Training, \
        input_UNet_Training_Steps, \
        input_UNet_Learning_Rate, \
        input_Text_Encoder_Training_Steps, \
        input_Text_Encoder_Concept_Training_Steps, \
        input_Text_Encoder_Learning_Rate, \
        input_Save_Checkpoint_Every, \
        input_Start_saving_from_the_step
    )
    await send_email(envMail, session_data.username, "Training completed", "Your training has been completed. You can now use the application.")


def test_model(session, session_data, envMail, model, prompt, nSteps, element, scheduler):
    infere(
        model, 
        prompt = prompt, 
        nSteps = nSteps, 
        element = element, 
        nImages = 1, 
        scheduler = scheduler,
        test=True
    )
    
def generate_dataset(session, model, prompt, nSteps, element, nImages, scheduler):
    return infere(
        model, 
        prompt = prompt, 
        nSteps = nSteps, 
        element = element, 
        nImages = nImages, 
        scheduler = scheduler
    )

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
