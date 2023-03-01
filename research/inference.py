# make sure you're logged in with `huggingface-cli login`
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("/Users/mentxaka/Github/TFG-DatasetGenerator/investigation/model")
# pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
# pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-base")

pipe = pipe.to("mps")

# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

prompt = "a WholeBiscuit27022023"

# # First-time "warmup" pass (see explanation above)
# _ = pipe(prompt, num_inference_steps=1)

# Results match those from the CPU device after the warmup pass.
image = pipe(prompt).images[0]

# Save the image
image.save("image.png")