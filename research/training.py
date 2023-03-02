from subprocess import getoutput
import time
import os
import cv2
import shutil
from IPython.display import clear_output
import subprocess
  
def train(
  input_Dataset, \
  input_Session_Name, \
  input_Concept = "", \
  input_Resume_Training = False, \
  input_UNet_Training_Steps = 650, \
  input_UNet_Learning_Rate = 1e-5, \
  input_Text_Encoder_Training_Steps = 250, \
  input_Text_Encoder_Concept_Training_Steps = 0, \
  input_Text_Encoder_Learning_Rate = 1e-6, \
  input_Save_Checkpoint_Every = 500, \
  input_Start_saving_from_the_step = 500
):
  
  def chek_format(Images_folder):
    #check format of the images
    try:
        # loop through all the files in the directory
        for filename in os.listdir(Images_folder):
            # check if the file is an image
            if filename.endswith(".png") or filename.endswith(".DS_Store"):
                if filename.endswith(".DS_Store"):
                    os.remove(os.path.join(Images_folder, filename))
                    print(f"{filename} has been deleted.")
                    continue            
                # load the image
                img = cv2.imread(os.path.join(Images_folder, filename))
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

  def upload_images( 
      Images_folder,
      Concept_folder = "", 
      Remove_existing_instance_images = False, 
      Remove_existing_concept_images = False, 
      Same_concept_images = True,
      chek_format_flag = False,
  ):
    
    nonlocal INSTANCE_DIR
    nonlocal CONCEPT_DIR

    if os.path.exists(INSTANCE_DIR+"/.ipynb_checkpoints"):
      os.rmdir(INSTANCE_DIR+"/.ipynb_checkpoints")

    if Remove_existing_instance_images:
      if os.path.exists(str(INSTANCE_DIR)):
        os.rmdir(INSTANCE_DIR)

    if Remove_existing_concept_images:
      if os.path.exists(str(CONCEPT_DIR)):
        os.rmdir(CONCEPT_DIR)

    if Concept_folder:
      Concept_folder = Images_folder

    if chek_format_flag: chek_format(Images_folder)

    INSTANCE_DIR = Images_folder
    CONCEPT_DIR = Concept_folder

    print('\n[1;32mDone, proceed to the training cell')

  def dump_only_textenc(train_only_text_encoder, pretrained_model_name_or_path, instance_data_dir, output_dir, instance_prompt, GC, precision, learning_rate, max_train_steps):
      cmd = f'''!accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
        {train_only_text_encoder} \
        --image_captions_filename \
        --train_text_encoder \
        --dump_only_text_encoder \
        --pretrained_model_name_or_path={pretrained_model_name_or_path} \
        --instance_data_dir={instance_data_dir} \
        --output_dir={output_dir} \
        --instance_prompt={instance_prompt} \
        --resolution=512 \
        --train_batch_size=1 \
        --mixed_precision={precision} \
        --gradient_accumulation_steps=1 {GC} \
        --use_8bit_adam \
        --learning_rate={learning_rate} \
        --lr_scheduler="polynomial" \
        --lr_warmup_steps=0 \
        --max_train_steps={max_train_steps}'''
      
      subprocess.call(cmd, shell=True)


  def train_only_unet(style, stpsv, stp, SESSION_DIR, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, precision, Training_Steps):
      if Resume_Training:
          print('Resuming Training...')
      print('Training the UNet...')

      cmd = f'''!accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
        {style} \
        --stop_text_encoder_training={Text_Encoder_Training_Steps} \
        --train_only_unet \
        --save_starting_step={stpsv} \
        --save_n_steps={stp} \
        --Session_dir={SESSION_DIR} \
        --pretrained_model_name_or_path="{MODELT_NAME}" \
        --instance_data_dir="{INSTANCE_DIR}" \
        --output_dir="{OUTPUT_DIR}" \
        --instance_prompt="{PT}" \
        --resolution=512 \
        --mixed_precision={precision} \
        --train_batch_size=1 \
        --gradient_accumulation_steps=1 {GC} \
        --use_8bit_adam \
        --learning_rate={UNet_Learning_Rate} \
        --lr_scheduler="polynomial" \
        --lr_warmup_steps=0 \
        --max_train_steps={Training_Steps}'''
      
      subprocess.call(cmd, shell=True)

  ############################################################################################################################################################

  DATASET = input_Dataset
  CONCEPT = input_Concept
  Session_Name = input_Session_Name
  Resume_Training = input_Resume_Training
  UNet_Training_Steps = input_UNet_Training_Steps
  UNet_Learning_Rate = input_UNet_Learning_Rate
  Text_Encoder_Training_Steps = input_Text_Encoder_Training_Steps
  Text_Encoder_Concept_Training_Steps = input_Text_Encoder_Concept_Training_Steps
  Text_Encoder_Learning_Rate = input_Text_Encoder_Learning_Rate
  Save_Checkpoint_Every = input_Save_Checkpoint_Every
  Start_saving_from_the_step = input_Start_saving_from_the_step

  ############################################################################################################################################################

  Session_Name=Session_Name.replace(" ","_")
  PT=Session_Name
  INSTANCE_NAME=Session_Name
  OUTPUT_DIR="/content/gdrive/Shareddrives/TFG-Oier-Mentxaka/models/"+Session_Name
  SESSION_DIR="/content/gdrive/Shareddrives/TFG-Oier-Mentxaka/models/"+Session_Name
  INSTANCE_DIR=""
  CONCEPT_DIR=""
  MODEL_NAME="stabilityai/stable-diffusion-2-base"
  MODELT_NAME=MODEL_NAME

  ############################################################################################################################################################

  # Codificador de texto
  trnonltxt=""
  if UNet_Training_Steps==0:
    trnonltxt="--train_only_text_encoder"

  # Entrenamiento de un estilo o no, activa un flag
  Style_Training = False 
  Style=""
  if Style_Training:
    Style="--Style"

  # La resolucion en este programa siempre va a ser 512
  Resolution = "512" 
  Res=int(Resolution)

  # TODO
  fp16 = True
  if fp16:
    prec="fp16"
  else:
    prec="no"
  precision=prec

  # Comprueba si tiene alcun tipo de GPU A100
  GC="--gradient_checkpointing"
  s = getoutput('nvidia-smi')
  if 'A100' in s:
    GC=""

  # Creacion o carga de sesion 
  if os.path.exists(str(SESSION_DIR)) and not os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
    print('[1;32mLoading session with no previous model, using the original model or the custom downloaded model')
    if MODEL_NAME!="":
      print('[1;32mSession Loaded, proceed to uploading instance images')

  elif os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
      resume=True
      clear_output()
      print('[1;32mSession loaded.')
    
  elif not os.path.exists(str(SESSION_DIR)):
      print('[1;32mCreating session...')
      if MODEL_NAME!="":
        print('[1;32mSession created, uploading instance images')
        upload_images(Images_folder = DATASET, Concept_folder = CONCEPT)

  # Borrado de Jupyter Notebooks caches
  if os.path.exists(INSTANCE_DIR+"/.ipynb_checkpoints"):
    os.rmdir(INSTANCE_DIR+"/.ipynb_checkpoints")

  if os.path.exists(CONCEPT_DIR+"/.ipynb_checkpoints"):
    os.rmdir(CONCEPT_DIR+"/.ipynb_checkpoints")

  # Parametros para seguir un entrenamiento preexistente
  if Resume_Training and os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
    MODELT_NAME=OUTPUT_DIR
    print('[1;32mResuming Training...[0m')
  elif Resume_Training and not os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
    print('[1;31mPrevious model not found, training a new model...[0m')
    MODELT_NAME=MODEL_NAME
    while MODEL_NAME=="":
      print('[1;31mNo model found, use the "Model Download" cell to download a model.')
      time.sleep(5)

  # Parametros del text encoder y concept text encoder
  Enable_text_encoder_training= True
  Enable_Text_Encoder_Concept_Training= True

  if Text_Encoder_Training_Steps==0:
    Enable_text_encoder_training= False
  else:
    stptxt=Text_Encoder_Training_Steps

  if Text_Encoder_Concept_Training_Steps==0:
    Enable_Text_Encoder_Concept_Training= False
  else:
    stptxtc=Text_Encoder_Concept_Training_Steps

  if Enable_text_encoder_training :
    print('[1;33mTraining the text encoder...[0m')
    if os.path.exists(OUTPUT_DIR+'/'+'text_encoder_trained'):
      shutil.rmtree(OUTPUT_DIR+"/text_encoder_trained")
    dump_only_textenc(train_only_text_encoder=trnonltxt, pretrained_model_name_or_path=MODELT_NAME, instance_data_dir=INSTANCE_DIR, output_dir=OUTPUT_DIR, instance_prompt=PT, GC=GC, precision=prec, learning_rate=UNet_Learning_Rate, max_train_steps=stptxt)

  if Enable_Text_Encoder_Concept_Training:
    if os.path.exists(CONCEPT_DIR):
      if os.listdir(CONCEPT_DIR)!=[]:
        clear_output()
        if Resume_Training:
          print('[1;32mResuming Training...[0m')
        print('[1;33mTraining the text encoder on the concept...[0m')
        dump_only_textenc(train_only_text_encoder=trnonltxt, pretrained_model_name_or_path=MODELT_NAME, instance_data_dir=CONCEPT_DIR, output_dir=OUTPUT_DIR, instance_prompt=PT, GC=GC, precision=prec, learning_rate=UNet_Learning_Rate, max_train_steps=stptxtc)
      else:
        clear_output()
        if Resume_Training:
          print('[1;32mResuming Training...[0m')
        print('[1;31mNo concept images found, skipping concept training...')
        Text_Encoder_Concept_Training_Steps=0
        time.sleep(8)
    else:
        clear_output()
        if Resume_Training:
          print('[1;32mResuming Training...[0m')
        print('[1;31mNo concept images found, skipping concept training...')
        Text_Encoder_Concept_Training_Steps=0
        time.sleep(8)

  if UNet_Training_Steps!=0:
    train_only_unet(style=Style, stpsv=Text_Encoder_Training_Steps, stp=Start_saving_from_the_step, SESSION_DIR=SESSION_DIR, MODELT_NAME=MODELT_NAME, INSTANCE_DIR=INSTANCE_DIR, OUTPUT_DIR=OUTPUT_DIR, PT=PT, precision=prec, Training_Steps=UNet_Training_Steps)

  if UNet_Training_Steps==0 and Text_Encoder_Concept_Training_Steps==0 :
    print('[1;32mNothing to do')
  else:
    if os.path.exists("/content/gdrive/Shareddrives/TFG-Oier-Mentxaka/models/"+INSTANCE_NAME):
      prc="--fp16" if precision=="fp16" else ""
      print('[1;31mCompressing...')
      shutil.make_archive("/content/gdrive/Shareddrives/TFG-Oier-Mentxaka/models/"+Session_Name, 'zip', "/content/gdrive/Shareddrives/TFG-Oier-Mentxaka/models/"+Session_Name)
      print('[1;32mTraining completed, model saved in /content/gdrive/Shareddrives/TFG-Oier-Mentxaka/models/'+Session_Name)
    else:
      print("[1;31mSomething went wrong")
