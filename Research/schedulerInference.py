import os
import traceback
from inference import infere

print("block inference")

models_dir = "/Users/mentxaka/GitHub/TFG-DatasetGenerator/Research/Models/"
n_steps = 20
n_images = 5
schedulers = [
            "UniPC"
              ]
# schedulers = [
#               "DPM", "DPMA", "EulerA", "Euler", "Heun",
#               "LinearMultistep", "MultistepDPM", "SinglestepDPM"
#              ]
# schedulers = [
#               "DDIM", "DDPM", "DEIS", "DPM", "DPMA", "EulerA", "Euler", "Heun", "PNDM",
#               "LinearMultistep", "MultistepDPM", "PNDM", "SinglestepDPM", "Kerras", "UniPC", "VE-SDE"
#              ]


folders = [ 
                # "Biscuits2E-5Stp200",
                # "Biscuits2E-5Stp300",
                # "Biscuits2E-5Stp400",
                # "Biscuits2E-5Stp500",
                "Biscuits2E-5Stp600",
                # "Biscuits2E-5Stp700",
                # "Biscuits2E-5Stp800",
                # "Biscuits2E-5Stp900",
                # "Biscuits2E-5Stp1000",
                # "Biscuits2E-5Stp1100",
                # "Biscuits2E-5Stp1200",

                # "Biscuits3E-5Stp800",
                # "Biscuits3E-5Stp900",
                # "Biscuits3E-5Stp1000",
                # "Biscuits3E-5Stp1100",

                # "Biscuits4E-5Stp800",
                # "Biscuits4E-5Stp900",
                # "Biscuits4E-5Stp1000",
                # "Biscuits4E-5Stp1100",
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
