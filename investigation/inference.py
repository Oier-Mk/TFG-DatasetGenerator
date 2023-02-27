from diffusers import StableDiffusionPipeline

model_id = "stabilityai/stable-diffusion-2-base"

pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to("mps")

pipe.enable_attention_slicing() # Recommended if your computer has < 64 GB of RAM

prompt = "a photo of an astronaut riding a horse on mars"

image = pipe(prompt).images[0]  
    
image.save("astronaut_rides_horse.png")