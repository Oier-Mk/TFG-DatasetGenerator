import os
from IPython.utils import capture
from IPython.display import clear_output
from subprocess import getoutput
import time
import shutil
import wget
from os import system
def install_dependencies():
  print('[1;32mInstalling dependencies...')
  with capture.capture_output() as cap:
      system.exec("pip install -q --no-deps accelerate==0.12.0")
      system.exec("wget -q -i 'https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dependencies/dbdeps.txt'")
      for i in range(1,8):
          !mv "deps.{i}" "deps.7z.00{i}"
      !7z x -y -o/ deps.7z.001
      !rm *.00* *.txt
      !git clone --depth 1 --branch updt https://github.com/TheLastBen/diffusers
      s = getoutput('nvidia-smi')
      if "A100" in s:
          !wget -q https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/A100/A100
          !rm -r /usr/local/lib/python3.8/dist-packages/xformers
          !7z x -y -o/usr/local/lib/python3.8/dist-packages/ /content/A100
          !rm /content/A100
  
  if not os.path.exists('/content/stable-diffusion-v2-512'):
      clear_output()
      !mkdir /content/stable-diffusion-v2-512
      !git init
      !git lfs install --system --skip-repo
      !git remote add -f origin  "https://USER:{token}@huggingface.co/stabilityai/stable-diffusion-2-1-base"
      !git config core.sparsecheckout true
      !echo -e "scheduler\ntext_encoder\ntokenizer\nunet\nvae\nfeature_extractor\nmodel_index.json\n!*.safetensors" > .git/info/sparse-checkout
      !git pull origin main
      !rm -r /content/stable-diffusion-v2-512/.git
      clear_output()
      print('[1;32mDONE !')
      MODEL_NAME="/content/stable-diffusion-v2-512"
  else:
    MODEL_NAME="/content/stable-diffusion-v2-512"
    print("[1;32mThe v2-512px model already exists, using this model.")

 
def check_images(Remove_existing_instance_images = False):

  from tqdm import tqdm
  import cv2
  import os

  if Remove_existing_instance_images:
    if os.path.exists(str(INSTANCE_DIR)):
      !rm -r "$INSTANCE_DIR"
    if os.path.exists(str(CAPTIONS_DIR)):
      !rm -r "$CAPTIONS_DIR"

  IMAGES_FOLDER="/content/gdrive/Shareddrives/TFG-Oier-Mentxaka/Datasets/WholeBiscuits24012023" #@param{type: 'string'}

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
    with capture.capture_output() as cap:
      !cp $IMAGES_FOLDER/*.txt $CAPTIONS_DIR

    for filename in tqdm(os.listdir(IMAGES_FOLDER), bar_format='  |{bar:15}| {n_fmt}/{total_fmt} Uploaded'):
      %cp -r "$IMAGES_FOLDER/$filename" "$INSTANCE_DIR"

  Same_concept_images = True #@param{type: 'boolean'}

  if Same_concept_images:
    CONCEPT_IMAGES = IMAGES_FOLDER

  Remove_existing_concept_images= False #@param{type: 'boolean'}

  if Remove_existing_concept_images:
    if os.path.exists(str(CONCEPT_DIR)):
      !rm -r "$CONCEPT_DIR"

  if not os.path.exists(str(CONCEPT_DIR)):
    %mkdir -p "$CONCEPT_DIR"

  CONCEPT_IMAGES="" #@param{type: 'string'}

  while CONCEPT_IMAGES !="" and not os.path.exists(str(CONCEPT_IMAGES)):
    print('[1;31mThe image folder specified does not exist, use the colab file explorer to copy the path :')
    CONCEPT_IMAGES=input('')

  if CONCEPT_IMAGES!="":
    for filename in tqdm(os.listdir(CONCEPT_IMAGES), bar_format='  |{bar:15}| {n_fmt}/{total_fmt} Uploaded'):
      %cp -r "$CONCEPT_IMAGES/$filename" "$CONCEPT_DIR"



  print('\n[1;32mDone, proceed to the training cell')


def train_model(session, attributes):

  import os
  from subprocess import getoutput
  from IPython.display import clear_output
  from google.colab import runtime
  import time
  import random

  if os.path.exists(INSTANCE_DIR+"/.ipynb_checkpoints"):
  #   %rm -r $INSTANCE_DIR"/.ipynb_checkpoints"

  if os.path.exists(CONCEPT_DIR+"/.ipynb_checkpoints"):
  #   %rm -r $CONCEPT_DIR"/.ipynb_checkpoints"

  if os.path.exists(CAPTIONS_DIR+"/.ipynb_checkpoints"):
  #   %rm -r $CAPTIONS_DIR"/.ipynb_checkpoints"

  if os.path.exists(CAPTIONS_DIR+"off"):
    !mv $CAPTIONS_DIR"off" $CAPTIONS_DIR

  Resume_Training = False #@param {type:"boolean"}

  if resume and not Resume_Training:
    print('[1;31mOverwrite your previously trained model ?, answering "yes" will train a new model, answering "no" will resume the training of the previous model?  yes or no ?[0m')
    while True:
      ansres=input('')
      if ansres=='no':
        Resume_Training = True
        break
      elif ansres=='yes':
        Resume_Training = False
        resume= False
        break

  while not Resume_Training and MODEL_NAME=="":
    print('[1;31mNo model found, use the "Model Download" cell to download a model.')
    time.sleep(5)

  #@markdown  - If you're not satisfied with the result, check this box, run again the cell and it will continue training the current model.

  MODELT_NAME=MODEL_NAME

  UNet_Training_Steps=650 #@param{type: 'number'}
  UNet_Learning_Rate = 1e-5 #@param ["2e-5","1e-5","9e-6","8e-6","7e-6","6e-6","5e-6", "4e-6", "3e-6", "2e-6"] {type:"raw"}
  untlr=UNet_Learning_Rate

  #@markdown - These default settings are for a dataset of 10 pictures which is enough for training a face, start with 650 or lower, test the model, if not enough, resume training for 150 steps, keep testing until you get the desired output, `set it to 0 to train only the text_encoder`.

  Text_Encoder_Training_Steps=250 #@param{type: 'number'}

  #@markdown - 200-450 steps is enough for a small dataset, keep this number small to avoid overfitting, set to 0 to disable, `set it to 0 before resuming training if it is already trained`.

  Text_Encoder_Concept_Training_Steps=0 #@param{type: 'number'}

  #@markdown - Suitable for training a style/concept as it acts as heavy regularization, set it to 1500 steps for 200 concept images (you can go higher), set to 0 to disable, set both the settings above to 0 to fintune only the text_encoder on the concept, `set it to 0 before resuming training if it is already trained`.

  Text_Encoder_Learning_Rate = 1e-6 #@param ["2e-6", "1e-6","8e-7","6e-7","5e-7","4e-7"] {type:"raw"}
  txlr=Text_Encoder_Learning_Rate

  #@markdown - Learning rate for both text_encoder and concept_text_encoder, keep it low to avoid overfitting (1e-6 is higher than 4e-7)

  trnonltxt=""
  if UNet_Training_Steps==0:
    trnonltxt="--train_only_text_encoder"

  Seed=''

  External_Captions = False #@param {type:"boolean"}
  #@markdown - Get the captions from a text file for each instance image.
  extrnlcptn=""
  if External_Captions:
    extrnlcptn="--external_captions"


  Style_Training = False #@param {type:"boolean"}

  #@markdown - Further reduce overfitting, suitable when training a style or a general theme, don't check the box at the beginning, check it after training for at least 1000 steps. (Has no effect when using External Captions)

  Style=""
  if Style_Training:
    Style="--Style"

  Resolution = "512" #@param ["512", "576", "640", "704", "768", "832", "896", "960", "1024"]
  Res=int(Resolution)

  #@markdown - Higher resolution = Higher quality, make sure the instance images are cropped to this selected size (or larger).

  fp16 = True

  if Seed =='' or Seed=='0':
    Seed=random.randint(1, 999999)
  else:
    Seed=int(Seed)

  GC="--gradient_checkpointing"

  if fp16:
    prec="fp16"
  else:
    prec="no"

  s = getoutput('nvidia-smi')
  if 'A100' in s:
    GC=""

  precision=prec

  resuming=""
  if Resume_Training and os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
    MODELT_NAME=OUTPUT_DIR
    print('[1;32mResuming Training...[0m')
    resuming="Yes"
  elif Resume_Training and not os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
    print('[1;31mPrevious model not found, training a new model...[0m')
    MODELT_NAME=MODEL_NAME
    while MODEL_NAME=="":
      print('[1;31mNo model found, use the "Model Download" cell to download a model.')
      time.sleep(5)

  Enable_text_encoder_training= True
  Enable_Text_Encoder_Concept_Training= True

  if Text_Encoder_Training_Steps==0 or External_Captions:
    Enable_text_encoder_training= False
  else:
    stptxt=Text_Encoder_Training_Steps

  if Text_Encoder_Concept_Training_Steps==0:
    Enable_Text_Encoder_Concept_Training= False
  else:
    stptxtc=Text_Encoder_Concept_Training_Steps

  #@markdown ---------------------------
  Save_Checkpoint_Every_n_Steps = False #@param {type:"boolean"}
  Save_Checkpoint_Every=500 #@param{type: 'number'}
  if Save_Checkpoint_Every==None:
    Save_Checkpoint_Every=1
  #@markdown - Minimum 200 steps between each save.
  stp=0
  Start_saving_from_the_step=500 #@param{type: 'number'}
  if Start_saving_from_the_step==None:
    Start_saving_from_the_step=0
  if (Start_saving_from_the_step < 200):
    Start_saving_from_the_step=Save_Checkpoint_Every
  stpsv=Start_saving_from_the_step
  if Save_Checkpoint_Every_n_Steps:
    stp=Save_Checkpoint_Every
  #@markdown - Start saving intermediary checkpoints from this step.

  Disconnect_after_training=False #@param {type:"boolean"}

  #@markdown - Auto-disconnect from google colab after the training to avoid wasting compute units.

  def dump_only_textenc(trnonltxt, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps):
      
      !accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
      $trnonltxt \
      --image_captions_filename \
      --train_text_encoder \
      --dump_only_text_encoder \
      --pretrained_model_name_or_path="$MODELT_NAME" \
      --instance_data_dir="$INSTANCE_DIR" \
      --output_dir="$OUTPUT_DIR" \
      --instance_prompt="$PT" \
      --seed=$Seed \
      --resolution=512 \
      --mixed_precision=$precision \
      --train_batch_size=1 \
      --gradient_accumulation_steps=1 $GC \
      --use_8bit_adam \
      --learning_rate=$txlr \
      --lr_scheduler="polynomial" \
      --lr_warmup_steps=0 \
      --max_train_steps=$Training_Steps

  def train_only_unet(stpsv, stp, SESSION_DIR, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, Res, precision, Training_Steps):
      clear_output()
      if resuming=="Yes":
        print('[1;32mResuming Training...[0m')
      print('[1;33mTraining the UNet...[0m')
      !accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
      $Style \
      $extrnlcptn \
      --stop_text_encoder_training=$Text_Encoder_Training_Steps \
      --image_captions_filename \
      --train_only_unet \
      --save_starting_step=$stpsv \
      --save_n_steps=$stp \
      --Session_dir=$SESSION_DIR \
      --pretrained_model_name_or_path="$MODELT_NAME" \
      --instance_data_dir="$INSTANCE_DIR" \
      --output_dir="$OUTPUT_DIR" \
      --captions_dir="$CAPTIONS_DIR" \
      --instance_prompt="$PT" \
      --seed=$Seed \
      --resolution=$Res \
      --mixed_precision=$precision \
      --train_batch_size=1 \
      --gradient_accumulation_steps=1 $GC \
      --use_8bit_adam \
      --learning_rate=$untlr \
      --lr_scheduler="polynomial" \
      --lr_warmup_steps=0 \
      --max_train_steps=$Training_Steps


  if Enable_text_encoder_training :
    print('[1;33mTraining the text encoder...[0m')
    if os.path.exists(OUTPUT_DIR+'/'+'text_encoder_trained'):
  #     %rm -r $OUTPUT_DIR"/text_encoder_trained"
    dump_only_textenc(trnonltxt, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps=stptxt)

  if Enable_Text_Encoder_Concept_Training:
    if os.path.exists(CONCEPT_DIR):
      if os.listdir(CONCEPT_DIR)!=[]:
        clear_output()
        if resuming=="Yes":
          print('[1;32mResuming Training...[0m')
        print('[1;33mTraining the text encoder on the concept...[0m')
        dump_only_textenc(trnonltxt, MODELT_NAME, CONCEPT_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps=stptxtc)
      else:
        clear_output()
        if resuming=="Yes":
          print('[1;32mResuming Training...[0m')
        print('[1;31mNo concept images found, skipping concept training...')
        Text_Encoder_Concept_Training_Steps=0
        time.sleep(8)
    else:
        clear_output()
        if resuming=="Yes":
          print('[1;32mResuming Training...[0m')
        print('[1;31mNo concept images found, skipping concept training...')
        Text_Encoder_Concept_Training_Steps=0
        time.sleep(8)

  if UNet_Training_Steps!=0:
    train_only_unet(stpsv, stp, SESSION_DIR, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, Res, precision, Training_Steps=UNet_Training_Steps)

  if UNet_Training_Steps==0 and Text_Encoder_Concept_Training_Steps==0 and External_Captions :
    print('[1;32mNothing to do')
  else:
    if os.path.exists('/content/models/'+INSTANCE_NAME+'/unet/diffusion_pytorch_model.bin'):
      prc="--fp16" if precision=="fp16" else ""
      !python /content/diffusers/scripts/convertosdv2.py $prc $OUTPUT_DIR $SESSION_DIR/$Session_Name".ckpt"
      clear_output()
      if os.path.exists(SESSION_DIR+"/"+INSTANCE_NAME+'.ckpt'):
        clear_output()
        print("[1;32mDONE, the CKPT model is in your Gdrive in the sessions folder")
        if Disconnect_after_training :
          time.sleep(20)
          runtime.unassign()
      else:
        print("[1;31mSomething went wrong")
    else:
      print("[1;31mSomething went wrong")

  #@markdown ---
  #@markdown #Mis notas
  #@markdown * UNet_Training_Steps: Training epochs cuantos mas, mas accurate pero mas tiempo, son unos 1200 de media
  #@markdown * UNet_Learning_Rate: Frecuencia de update del modelo mientras se entrena, cuando mas, mas facil es sacar mejores resultados. 2e-6
  #@markdown * Text_Encoder_Training_Steps:
  #@markdown * Text_Encoder_Concept_Training_Steps:
  #@markdown * Text_Encoder_Learning_Rate:

def train(Session_Name):

  PT=""
  WORKSPACE='/content/gdrive/Shareddrives/TFG-Oier-Mentxaka/Fast-Dreambooth'
  INSTANCE_NAME=None
  OUTPUT_DIR=None
  SESSION_DIR=None
  MDLPTH=None
  INSTANCE_DIR=None
  CONCEPT_DIR=None
  CAPTIONS_DIR=None

 
  def load_session(Session_Name):
    try:
      MODEL_NAME
      pass
    except:
      MODEL_NAME=""
      
    Session_Name=Session_Name.replace(" ","_")

    nonlocal INSTANCE_NAME
    nonlocal OUTPUT_DIR
    nonlocal SESSION_DIR
    nonlocal MDLPTH
    nonlocal INSTANCE_DIR
    nonlocal CONCEPT_DIR
    nonlocal CAPTIONS_DIR

    INSTANCE_NAME=Session_Name
    OUTPUT_DIR="/content/models/"+Session_Name
    SESSION_DIR=WORKSPACE+'/Sessions/'+Session_Name
    MDLPTH=str(SESSION_DIR+"/"+Session_Name+'.ckpt')
    INSTANCE_DIR=SESSION_DIR+'/instance_images'
    CONCEPT_DIR=SESSION_DIR+'/concept_images'
    CAPTIONS_DIR=SESSION_DIR+'/captions'

    if os.path.exists(str(SESSION_DIR)):
      mdls=[ckpt for ckpt in os.listdir(SESSION_DIR) if ckpt.split(".")[-1]=="ckpt"]
      if not os.path.exists(MDLPTH) and '.ckpt' in str(mdls):  
        k=0
        print('[1;33mNo final checkpoint model found, select which intermediary checkpoint to use, enter only the number, (000 to skip):\n[1;34m')

        for i in mdls:
          print(str(k)+'- '+i)
          k=k+1
        n=input()
        while int(n)>k-1:
          n=input()
        if n!="000":
          k=0
          for i in mdls:
            if k==n:
              shutil.move(str(SESSION_DIR+"/"+i),str(MDLPTH))
            k=k+1
          print('[1;32mUsing the model '+ mdls[int(n)]+" ...")
          time.sleep(2)
        else:
          print('[1;32mSkipping the intermediary checkpoints.')
        del n

    if os.path.exists(str(SESSION_DIR)) and not os.path.exists(MDLPTH):
      print('[1;32mLoading session with no previous model, using the original model or the custom downloaded model')
      if MODEL_NAME=="":
        print('[1;31mNo model found, use the "Model Download" cell to download a model.')
      else:
        print('[1;32mSession Loaded, proceed to uploading instance images')

    elif os.path.exists(MDLPTH):
      print('[1;32mSession found, loading the trained model ...')
      wget.download('https://raw.githubusercontent.com/TheLastBen/fast-stable-diffusion/main/Dreambooth/convertodiffv2.py', '/content/convertodiff.py')
      clear_output()
      print('[1;32mSession found, loading the trained model ...')
      os.system("python /content/convertodiff.py "+MDLPTH+" "+OUTPUT_DIR+" --v2 --reference_model stabilityai/stable-diffusion-2-1-base")
      
    elif not os.path.exists(str(SESSION_DIR)):
        print('[1;32mCreating session...')
        if MODEL_NAME=="":
          print('[1;31mNo model found, use the "Model Download" cell to download a model.')
        else:
          print('[1;32mSession created, proceed to uploading instance images')

  load_session( "WholeBiscuit24012023" )
