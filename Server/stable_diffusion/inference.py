# https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/text2img
# https://huggingface.co/docs/diffusers/api/schedulers/overview

from diffusers import DiffusionPipeline, DDIMScheduler, DDIMInverseScheduler, DDPMScheduler, DEISMultistepScheduler, KDPM2DiscreteScheduler, \
KDPM2AncestralDiscreteScheduler, EulerAncestralDiscreteScheduler, EulerDiscreteScheduler, HeunDiscreteScheduler, \
IPNDMScheduler, LMSDiscreteScheduler, DPMSolverMultistepScheduler, PNDMScheduler, RePaintScheduler, DPMSolverSinglestepScheduler, \
KarrasVeScheduler, UniPCMultistepScheduler, ScoreSdeVeScheduler, VQDiffusionScheduler
import os
import time

def infere(model, prompt = "a car", nSteps = 20, element = "car", nImages = 1, scheduler = "PNDM", test = False):

    schedulerStr= scheduler
    print(schedulerStr)

    if scheduler == "DDIM":
        scheduler = DDIMScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "DDIMinverse":
        scheduler = DDIMInverseScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "DDPM":
        scheduler = DDPMScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "DEIS":
        scheduler = DEISMultistepScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "DPM":
        scheduler = KDPM2DiscreteScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "DPMA":
        scheduler = KDPM2AncestralDiscreteScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "EulerA":
        scheduler = EulerAncestralDiscreteScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "Euler":
        scheduler = EulerDiscreteScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "Heun":
        scheduler = HeunDiscreteScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "PNDM":
        scheduler = IPNDMScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "LinearMultistep":
        scheduler = LMSDiscreteScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "MultistepDPM":
        scheduler = DPMSolverMultistepScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "PNDM":
        scheduler = PNDMScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "RePaint":
        scheduler = RePaintScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "SinglestepDPM":
        scheduler = DPMSolverSinglestepScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "Kerras":
        scheduler = KarrasVeScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "UniPC":
        scheduler = UniPCMultistepScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "VE-SDE":
        scheduler = ScoreSdeVeScheduler.from_pretrained(model, subfolder="scheduler")
    elif scheduler == "VP-SDE":
        scheduler = VQDiffusionScheduler.from_pretrained(model, subfolder="scheduler")
    else:
        print("Scheduler not found, using PNDM")
        scheduler = PNDMScheduler.from_pretrained(model, subfolder="scheduler")
    scheduler = PNDMScheduler.from_pretrained(model, subfolder="scheduler")

    pipe = DiffusionPipeline.from_pretrained(pretrained_model_name_or_path = model, scheduler = scheduler)

    pipe.enable_attention_slicing()

    if test:
        image = pipe(prompt, num_inference_steps = nSteps).images[0] #batch_size = num_images_per_prompt 
        image_path = element+"-"+str(nSteps)+"/"+element+" "+str(nSteps)+" "+str(0)+".png"
        image.save(image_path)   
        return image_path
    else:
        try: os.mkdir(element+"-"+str(nSteps)+"/")
        except: pass

        # start the timer
        start_time = time.perf_counter()

        for i in range(nImages):
            image = pipe(prompt, num_inference_steps = nSteps).images[0] #batch_size = num_images_per_prompt 
            image.save(element+"-"+str(nSteps)+"/"+element+" "+str(nSteps)+" "+str(i)+".png")


        # end the timer
        end_time = time.perf_counter()

        # calculate the time taken
        time_taken = end_time - start_time - 0.07931395899504423*nImages

        return time_taken
