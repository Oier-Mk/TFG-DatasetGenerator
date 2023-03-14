import os
import traceback
from inference import infere

print("block inference")

models_dir = "/Users/mentxaka/GitHub/TFG-DatasetGenerator/Research/Models/"
n_steps = 20
n_images = 5
# schedulers = ["DDIM", "DDIMinverse", "DDPM", "DEIS", "DPM", "DPMA", "EulerA", "Euler", "Heun", "PNDM",
#               "LinearMultistep", "MultistepDPM", "PNDM", "RePaint", "SinglestepDPM", "Kerras", "UniPC", "VE-SDE"
#               ]
schedulers = [
                "DPM",
                "PNDM",
                "SinglestepDPM",
                "UniPC",
                "MultistepDPM"
             ]

#800 900 1000 1100
#2 3 4 
folders = [ 
                "Biscuits3E-5Stp1100",
            ]

# Get all folder names in the models directory
folder_names = os.listdir(models_dir)

# Run the inference for each folder and each scheduler
for folder_name in folder_names:
    if folder_name in folders:
        try:
            model_path = os.path.join(models_dir, folder_name)
            prompt = "a " + folder_name
            element = folder_name
            print("MODELO: "+ model_path)
            for scheduler in schedulers:
                # Call the infere function for the current folder and scheduler
                process_time = infere(model_path, prompt, n_steps, element, n_images, scheduler)
            
                print("Inference completed for folder:", folder_name, "and scheduler:", scheduler)
                print("Process time:", process_time)
        except:
            print("Error in folder:", folder_name)
            traceback.print_exc()
