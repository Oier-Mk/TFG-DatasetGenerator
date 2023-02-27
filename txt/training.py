from subprocess import run
from datetime import datetime

MODEL_NAME="runwayml/stable-diffusion-v2"
DATA_DIR="path-to-dir-containing-images"
OUTPUT_DIR="textual_inversion_cat"

statment = [
    "python",
	"launch",
	"textual_inversion.py",
  	"--pretrained_model_name_or_path="+MODEL_NAME,
  	"--train_data_dir="+DATA_DIR,
  	"--output_dir="+OUTPUT_DIR,
  	"--learnable_property="+"object",
  	"--placeholder_token="+"<cat-toy>", #exactamente el nombre de lo que estamos entrenando
	"--resolution=512",
  	"--train_batch_size="+str(1),
 	"--gradient_accumulation_steps="+str(4),
  	"--max_train_steps="+str(3000)
  	"--learning_rate="+"5.0e-04" 
  	"--scale_lr"
  	"--lr_scheduler="+"constant",
  	"--lr_warmup_steps="str(0),
]

output = run(statment, text=True, capture_output=True)

current_time = datetime.now().strftime("%H:%M:%S")

print(f'Runtime {current_time}:  {output.stdout.strip()}')

