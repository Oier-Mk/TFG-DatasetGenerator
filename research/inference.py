# https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/text2img

from diffusers import StableDiffusionPipeline, LMSDiscreteScheduler

def infere(model, prompt = "a car", nSteps = 20, element = "car", nImages = 1):
    pipe = StableDiffusionPipeline.from_pretrained(pretrained_model_name_or_path = model)

    pipe = pipe.to("mps")

    pipe.enable_attention_slicing()

    _ = pipe(prompt, num_inference_steps=1)

    for i in range(nImages):
        image = pipe(prompt, num_inference_steps = nSteps).images[0] #batch size num_images_per_prompt 
        image.save(element+" "+str(i)+".png")

    return True

infere(model = "/Users/mentxaka/GitHub/TFG-DatasetGenerator/Research/Models/WholeBiscuit022032023", nSteps = 30, prompt = "a WholeBiscuit27022023", element = "WholeBiscuit27022023")
