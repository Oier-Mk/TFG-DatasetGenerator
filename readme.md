# Final Bachelor Thesis - Server to train and execute Stable Diffusion to generate datasets

This project aims to increase the number of images in a small dataset, making it more useful for other projects like object detection using Yolo. 

The server for training and executing Stable Diffusion will be built using FastAPI and will be designed to work remotely.

HOWTO execute server:
  1. `uvicorn DatasetGenerator:app --reload`

For receiving in a web:
  1. Go to http://127.0.0.1:8000/
  2. Select the functionality you want!

Use the .sh files to do it automatically
