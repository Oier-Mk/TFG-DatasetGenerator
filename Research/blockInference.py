import os
from inference import infere

print("block inference")

models_dir = "/Users/mentxaka/Downloads/"
n_steps = 20
n_images = 10
schedulers = ["DDIM", "DDIMinverse", "DDPM", "DEIS", "DPM", "DPMA", "EulerA", "Euler", "Heun", "PNDM",
              "LinearMultistep", "MultistepDPM", "PNDM", "RePaint", "SinglestepDPM", "Kerras", "UniPC", "VE-SDE", 
              "VP-SDE", "VODiffusionScheduler"]
scheduler = schedulers[12]

# Get all folder names in the models directory
folder_names = os.listdir(models_dir)

# Run the inference for each folder
for folder_name in folder_names:
    try:
        model_path = os.path.join(models_dir, folder_name)
        prompt = "a " + folder_name
        element = folder_name

        # Call the infere function for the current folder
        print("MODELO: "+ model_path)
        process_time = infere(model_path, prompt, n_steps, element, n_images, scheduler)
        
        print("Inference completed for folder:", folder_name)
        print("Process time:", process_time)
    except:
        print("Error in folder:", folder_name)
