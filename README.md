# Yolov10uno
An Uno card recognition model based on the open-source Uno dataset from the Internet and the Yolov10s and Yolov10n models
The datasets comes from: https://public.roboflow.com/object-detection/uno-cards
This is just an attempt. Both models have only run for 50 epochs, so their accuracy isn't good enough. 
If you want, you can simply run them using my template. Before start, please download Anaconda and use Anaconda Prompt.
using Anaconda Prompt and create the new environment by input: conda create -n yolov10uno python=3.10 -y
Then download cfg, data, default.yaml and uno datasets in the folders of the new environment.
Use pip to download the requirements in Requirements.txt and change the pathway in data/uno.yaml and default.yaml
finally input the code of CMD code to run the train.

