

import os
from IPython.display import clear_output
from os import listdir
from os.path import isfile
import subprocess
  
PT=""

Session_Name = "WholeBiscuit27022023" 
Session_Name=Session_Name.replace(" ","_")
WORKSPACE='/Users/mentxaka/Github/TFG-DatasetGenerator/investigation/Fast-Dreambooth'
INSTANCE_NAME=Session_Name
OUTPUT_DIR="/content/models/"+Session_Name
SESSION_DIR=WORKSPACE+'/'+Session_Name
INSTANCE_DIR=SESSION_DIR+'/instance_images'
CONCEPT_DIR=SESSION_DIR+'/concept_images'
CAPTIONS_DIR=SESSION_DIR+'/captions'
MDLPTH=str(SESSION_DIR+"/"+Session_Name+'.ckpt')
MODEL_NAME="stabilityai/stable-diffusion-2-base"

if os.path.exists(str(SESSION_DIR)) and not os.path.exists(MDLPTH):
  print('[1;32mLoading session with no previous model, using the original model or the custom downloaded model')
  if MODEL_NAME!="":
    print('[1;32mSession Loaded, proceed to uploading instance images')

elif os.path.exists(MDLPTH):
  print('[1;32mSession found, loading the trained model ...')
  command = ["python", 
             "/content/convertodiff.py", 
             MDLPTH, 
             OUTPUT_DIR,
             "--v2", 
             "--reference_model",
             "stabilityai/stable-diffusion-2-1-base"
             ]
  subprocess.run(command, shell=True)
  if os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
    resume=True
    clear_output()
    print('[1;32mSession loaded.')
  else:     
    if not os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
      print('[1;31mConversion error, if the error persists, remove the CKPT file from the current session folder')

elif not os.path.exists(str(SESSION_DIR)):
    os.mkdir(SESSION_DIR)
    os.mkdir(INSTANCE_DIR)
    os.mkdir(CONCEPT_DIR)
    print('[1;32mCreating session...')
    if MODEL_NAME!="":
      print('[1;32mSession created, proceed to uploading instance images')

import shutil
import cv2
import os

Remove_existing_instance_images= False 
Remove_existing_concept_images= False 
Same_concept_images = True 
IMAGES_FOLDER="/Users/mentxaka/Github/TFG-DatasetGenerator/investigation/Biscuits"
CONCEPT_IMAGES="" 


if os.path.exists(INSTANCE_DIR+"/.ipynb_checkpoints"):
  os.rmdir(INSTANCE_DIR+"/.ipynb_checkpoints")

if Remove_existing_instance_images:
  if os.path.exists(str(INSTANCE_DIR)):
    os.rmdir(INSTANCE_DIR)

if Remove_existing_concept_images:
  if os.path.exists(str(CONCEPT_DIR)):
    os.rmdir(CONCEPT_DIR)

if Same_concept_images:
  CONCEPT_IMAGES = IMAGES_FOLDER

#check format of the images
try:
    # loop through all the files in the directory
    for filename in os.listdir(IMAGES_FOLDER):
        # check if the file is an image
        if filename.endswith(".png") or filename.endswith(".DS_Store"):
            if filename.endswith(".DS_Store"):
                os.remove(os.path.join(IMAGES_FOLDER, filename))
                print(f"{filename} has been deleted.")
                continue            
            # load the image
            img = cv2.imread(os.path.join(IMAGES_FOLDER, filename))
            # get the size of the image
            height, width, _ = img.shape
            # check if the image is 512x512
            if height == 512 and width == 512:
                print(f"\n - {filename} is a valid PNG image of size 512x512.")
            else:
                raise ValueError(f"{filename} is not a valid size. It is {width}x{height}.")
        else:
            raise ValueError(f"{filename} is not a PNG image.")
except Exception as e:
    print("An error occurred:", e)

if IMAGES_FOLDER!="":
  for filename in os.listdir(IMAGES_FOLDER):
    shutil.copy(IMAGES_FOLDER+"/"+filename, INSTANCE_DIR)

#CONCEPT IMAGES IMAGENES PARA CONCEPTOS O ESTILOS... VER SI SE PUEDEN BORRAR Y TENER EN CUENTA TODAS. No lo haria porque da mas freedom al usuario.

if CONCEPT_IMAGES!="":
  for filename in os.listdir(CONCEPT_IMAGES):
        shutil.copy(CONCEPT_IMAGES+"/"+filename, CONCEPT_DIR)

print('\n[1;32mDone, proceed to the training cell')

# #@ Start DreamBooth Training

# import os
# from IPython.display import clear_output
# import time
# import random

# if os.path.exists(INSTANCE_DIR+"/.ipynb_checkpoints"):
#   os.rmdir(INSTANCE_DIR+"/.ipynb_checkpoints")

# if os.path.exists(CONCEPT_DIR+"/.ipynb_checkpoints"):
#   os.rmdir(CONCEPT_DIR+"/.ipynb_checkpoints")

# Resume_Training = False #@ {type:"boolean"}



# MODELT_NAME=MODEL_NAME

# UNet_Training_Steps=650 
# UNet_Learning_Rate = 1e-5 #@ ["2e-5","1e-5","9e-6","8e-6","7e-6","6e-6","5e-6", "4e-6", "3e-6", "2e-6"] {type:"raw"}
# untlr=UNet_Learning_Rate

# #@ - These default settings are for a dataset of 10 pictures which is enough for training a face, start with 650 or lower, test the model, if not enough, resume training for 150 steps, keep testing until you get the desired output, `set it to 0 to train only the text_encoder`.

# Text_Encoder_Training_Steps=250 

# #@ - 200-450 steps is enough for a small dataset, keep this number small to avoid overfitting, set to 0 to disable, `set it to 0 before resuming training if it is already trained`.

# Text_Encoder_Concept_Training_Steps=0 

# #@ - Suitable for training a style/concept as it acts as heavy regularization, set it to 1500 steps for 200 concept images (you can go higher), set to 0 to disable, set both the settings above to 0 to fintune only the text_encoder on the concept, `set it to 0 before resuming training if it is already trained`.

# Text_Encoder_Learning_Rate = 1e-6 #@ ["2e-6", "1e-6","8e-7","6e-7","5e-7","4e-7"] {type:"raw"}
# txlr=Text_Encoder_Learning_Rate

# #@ - Learning rate for both text_encoder and concept_text_encoder, keep it low to avoid overfitting (1e-6 is higher than 4e-7)

# trnonltxt=""
# if UNet_Training_Steps==0:
#    trnonltxt="--train_only_text_encoder"

# Seed=''

# External_Captions = False #@ {type:"boolean"}
# #@ - Get the captions from a text file for each instance image.
# external_captions=""
# if External_Captions:
#   external_captions="--external_captions"


# Style_Training = False #@ {type:"boolean"}

# #@ - Further reduce overfitting, suitable when training a style or a general theme, don't check the box at the beginning, check it after training for at least 1000 steps. (Has no effect when using External Captions)

# Style=""
# if Style_Training:
#   Style="--Style"

# Resolution = "512" #@ ["512", "576", "640", "704", "768", "832", "896", "960", "1024"]
# Res=int(Resolution)

# #@ - Higher resolution = Higher quality, make sure the instance images are cropped to this selected size (or larger).

# fp16 = True

# if Seed =='' or Seed=='0':
#   Seed=random.randint(1, 999999)
# else:
#   Seed=int(Seed)

# gradient_checkpointing="--gradient_checkpointing"

# if fp16:
#   prec="fp16"
# else:
#   prec="no"

# precision=prec

# resuming=""
# if Resume_Training and os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
#   MODELT_NAME=OUTPUT_DIR
#   print('[1;32mResuming Training...[0m')
#   resuming="Yes"
# elif Resume_Training and not os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
#   print('[1;31mPrevious model not found, training a new model...[0m')
#   MODELT_NAME=MODEL_NAME
#   while MODEL_NAME=="":
#     print('[1;31mNo model found, use the "Model Download" cell to download a model.')
#     time.sleep(5)

# Enable_text_encoder_training= True
# Enable_Text_Encoder_Concept_Training= True

# if Text_Encoder_Training_Steps==0 or External_Captions:
#    Enable_text_encoder_training= False
# else:
#   stptxt=Text_Encoder_Training_Steps

# if Text_Encoder_Concept_Training_Steps==0:
#    Enable_Text_Encoder_Concept_Training= False
# else:
#   stptxtc=Text_Encoder_Concept_Training_Steps

# #@ ---------------------------
# Save_Checkpoint_Every_n_Steps = False 
# Save_Checkpoint_Every=500 
# if Save_Checkpoint_Every==None:
#   Save_Checkpoint_Every=1
# #@ - Minimum 200 steps between each save.
# stp=0
# Start_saving_from_the_step=500 #
# if Start_saving_from_the_step==None:
#   Start_saving_from_the_step=0
# if (Start_saving_from_the_step < 200):
#   Start_saving_from_the_step=Save_Checkpoint_Every
# stpsv=Start_saving_from_the_step
# if Save_Checkpoint_Every_n_Steps:
#   stp=Save_Checkpoint_Every
# #@ - Start saving intermediary checkpoints from this step.

# Disconnect_after_training=False #@ {type:"boolean"}

# #@ - Auto-disconnect from google colab after the training to avoid wasting compute units.

# def dump_only_textenc(trnonltxt, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps):

#     command = [ "accelerate",
#             "launch", 
#             "/Users/mentxaka/Github/TFG-DatasetGenerator/investigation/diffusers/examples/dreambooth/train_dreambooth.py",
#             trnonltxt,
#             "--image_captions_filename",
#             "--train_text_encoder",
#             "--dump_only_text_encoder",
#             "--pretrained_model_name_or_path="+MODELT_NAME,
#             "--instance_data_dir="+INSTANCE_DIR,
#             "--output_dir="+OUTPUT_DIR,
#             "--instance_prompt="+PT,
#             "--seed="+str(Seed),
#             "--resolution=512",
#             "--mixed_precision="+precision,
#             "--train_batch_size=1",
#             "--gradient_accumulation_steps=1",
#             "--gradient_checkpointing",
#             "--use_8bit_adam",
#             "--learning_rate="+str(txlr),
#             "--lr_scheduler=polynomial",
#             "--lr_warmup_steps=0",
#             "--max_train_steps="+str(Training_Steps)
#     ]
#     subprocess.run(command, shell=True)
    
# def train_only_unet(stpsv, stp, SESSION_DIR, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, Res, precision, Training_Steps):
#     clear_output()
#     if resuming=="Yes":
#       print('[1;32mResuming Training...[0m')
#     print('[1;33mTraining the UNet...[0m')
#     command = [ "accelerate",
#             "launch",
#             "/Users/mentxaka/Github/TFG-DatasetGenerator/investigation/diffusers/examples/dreambooth/train_dreambooth.py",
#             Style,
#             external_captions,
#             "--stop_text_encoder_training="+str(Text_Encoder_Training_Steps),
#             "--image_captions_filename",
#             "--train_only_unet",
#             "--save_starting_step="+str(stpsv),
#             "--save_n_steps="+str(stp),
#             "--Session_dir="+SESSION_DIR,
#             "--pretrained_model_name_or_path="+MODELT_NAME,
#             "--instance_data_dir="+INSTANCE_DIR,
#             "--output_dir="+OUTPUT_DIR,
#             "--captions_dir="+CAPTIONS_DIR,
#             "--instance_prompt="+PT,
#             "--seed="+str(Seed),
#             "--resolution="+str(Res),
#             "--mixed_precision="+str(precision),
#             "--train_batch_size=1",
#             "--gradient_accumulation_steps=1 "+str(gradient_checkpointing),
#             "--use_8bit_adam",
#             "--learning_rate="+str(untlr),
#             "--lr_scheduler=polynomial",
#             "--lr_warmup_steps=0",
#             "--max_train_steps="+str(Training_Steps)
#             ]
#     subprocess.run(command, shell=True)


# if Enable_text_encoder_training :
#   print('[1;33mTraining the text encoder...[0m')
#   if os.path.exists(OUTPUT_DIR+'/'+'text_encoder_trained'):
#     os.rmdir(OUTPUT_DIR+"/text_encoder_trained")
#   dump_only_textenc(trnonltxt, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps=stptxt)

# if Enable_Text_Encoder_Concept_Training:
#   if os.path.exists(CONCEPT_DIR):
#     if os.listdir(CONCEPT_DIR)!=[]:
#       clear_output()
#       if resuming=="Yes":
#         print('[1;32mResuming Training...[0m')
#       print('[1;33mTraining the text encoder on the concept...[0m')
#       dump_only_textenc(trnonltxt, MODELT_NAME, CONCEPT_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps=stptxtc)
#     else:
#       clear_output()
#       if resuming=="Yes":
#         print('[1;32mResuming Training...[0m')
#       print('[1;31mNo concept images found, skipping concept training...')
#       Text_Encoder_Concept_Training_Steps=0
#       time.sleep(8)
#   else:
#       clear_output()
#       if resuming=="Yes":
#         print('[1;32mResuming Training...[0m')
#       print('[1;31mNo concept images found, skipping concept training...')
#       Text_Encoder_Concept_Training_Steps=0
#       time.sleep(8)

# if UNet_Training_Steps!=0:
#   train_only_unet(stpsv, stp, SESSION_DIR, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, Res, precision, Training_Steps=UNet_Training_Steps)

# if UNet_Training_Steps==0 and Text_Encoder_Concept_Training_Steps==0 and External_Captions :
#   print('[1;32mNothing to do')
# else:
#   if os.path.exists('/content/models/'+INSTANCE_NAME+'/unet/diffusion_pytorch_model.bin'):
#     prc="--fp16" if precision=="fp16" else ""
#     command = [ 
#       "python",
#        "/content/diffusers/scripts/convertosdv2.py",
#         prc,
#         OUTPUT_DIR,
#         SESSION_DIR+Session_Name+".ckpt"
#     ]
#     subprocess.run(command,shell=True)
#     clear_output()
#     if os.path.exists(SESSION_DIR+"/"+INSTANCE_NAME+'.ckpt'):
#       clear_output()
#       print("[1;32mDONE, the CKPT model is in your Gdrive in the sessions folder")
#     else:
#       print("[1;31mSomething went wrong")
#   else:
#     print("[1;31mSomething went wrong")

