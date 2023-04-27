#!/usr/bin/env python
# coding: utf-8

# In[6]:


from PIL import Image
import pytesseract
import glob
import pandas as pd
import numpy as np
import re
import sys
import random


# In[110]:


def get_steamed_scenes(folder_path):

    scene_data = pd.DataFrame(columns=["n", "pts", "pts_time", "start_ep", "rightvalue_raw", "timestamp"])
    scene_data.set_index("n")
    scene_data = {}
    with open(f"{folder_path}/frame_sd.log", "r") as scene_log:
        framedata_re = re.compile("n:\s*(\d+)\s*pts:(\d+)\s*pts_time:(\d+\.?\d*)")
        for line in scene_log:
            f_match = framedata_re.search(line)
            if f_match:
#                 print(f"n: {f_match.group(1)}, pts: {f_match.group(2)}")
#                 scene_data[f_match.group(1)] = [f_match.group(2), f_match.group(3)]
                scene_data[f_match.group(1)] = [ f_match.group(2), f_match.group(3), f"{folder_path}/{int(f_match.group(1))+1:05d}.png"]
#             scene_data[f_match.group(1)]["pts_time"] = f_match.group(3)
    return scene_data

def get_rvalue_raw(folder_path, df):
        deities = ["Artemis", "Gods", "Lord Bumbo", "Devil", "Jesus", "God", "Buddha", "Gods of Olde"]
        exclaim = ["Damn you", "Thank you", "Please", "Dammit", "Oouououuuouoh"]
        counter = 0 

        for i, f in df.iterrows():
            df.loc[i, "rightvalue_raw"] = pytesseract.image_to_string(Image.open(f["in_file"]))
            counter +=1
            if counter % 200 == 0:
                print(f"{random.choice(exclaim)} {random.choice(deities)}!  {counter}/{df.shape[0]}")
#             print(i, df.loc[i, "rightvalue_raw"],strip())

def get_ts(ts_value):
    matchv = re.search("(\d.*\d?)\.(2023\d{10})\.0", ts_value)
    if matchv:
        return matchv.group(2)
    else:
        return 0

def get_ep(ts_value):
    matchv = re.match("(\d.*\d?)\.(2023\d{10})\.0", ts_value)
    if matchv:
        return matchv.group(1)
    else:
        return -1

#From https://pyimagesearch.com/2014/09/15/python-compare-two-images/
def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err
    
image_intro = np.asarray(Image.open("ref/new_episode_start.png"))
image_episodestart = np.asarray(Image.open("ref/episode_start.png"))


# In[102]:

for folder in sys.argv[1:]:
    # folder = f
    print(folder)

    x = get_steamed_scenes(folder)
    data = pd.DataFrame(data=x).transpose()
    # data["start_ep"] = False
    # data["premiere"] = False
    data["rightvalue_raw"] = ""
    data["timestamp"] = 0
    data.rename(columns={0: "pts", 1: "pts_time", 2: "in_file"}, inplace=True)
    get_rvalue_raw(folder, data)


    # In[114]:





    # In[124]:


    data["mse_startingscene"] = data["in_file"].apply(lambda x: mse(image_episodestart, np.asarray(Image.open(x))))
    data["mse_introscene"] = data["in_file"].apply(lambda x: mse(image_intro, np.asarray(Image.open(x))))
    data["timestamp"] = data["rightvalue_raw"].apply(get_ts)
    data["ep"] = data["rightvalue_raw"].apply(get_ep)
    data["premiere"] = (data.ep == "0")
    data["newepisode_start"] = data["mse_introscene"] < 1000
    data["opening_scene"] = data["mse_startingscene"] < 600
    data[data.premiere == 1]
    data.to_csv(f"{folder}/dat.csv", index=False)


    # In[125]:


    # data[data["newepisode_start"]]

