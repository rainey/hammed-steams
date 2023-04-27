# hammed-steams
Praise Artemis! Some quick tools to help label unlimited steam VODs

Run the 'ffmpeg_scene_change_crop.sh` - this short script takes two arguments: the name of the VOD file, and the folder to dump its output to.
Use it like so:

bash ffmpeg_scene_change_crop.sh unlimited_steams_v17776358049.mpg sceneinfo_v17763

This will create 

 - a series of png files
 - frame_sd.log - ffmpeg log
 - frame_source.log - Contains the name of the source file 
 - dat.csv - data extracted from the process. Includes:
     - pts: time in 90KHz ticks since start of file
     - pts_time: - row seconds since start of file
     - in_file: - the png file associated with this row
     - rightvalue_raw: Raw extracted string from tesseract
     - timestamp: the timestamp extracted from rightvalue_raw: This may be used as the episode ID.
     - mse_introscene: mean-squared error of the cropped frame vs a reference frame from the premiere episode 
     - mse_startingscene: mse of the cropped frame vs ref frame from starting scene outside the house
     - ep: The number to the left of the timestamp - zero if this is a premiere
     - premiere: set to true when ep is zero
     - newepisode_start: set to true when mse_introscene is below a threshold value. When true, it indicates that the frame at this time is the start of a premiere episode
     - opening_scene: set to true when mse_startingscene is below a threshold. When true, indicates that this is the start of the opening scene, outside of Seymour's house. 

Quick note on what's going on:

First, we use ffmpeg to detect scene changes and crop the video. We have enough info in the bottom right of the frame to identify the scene and episode info. ffmpeg dumps these cropped images into the specified folder

The python script then uses pytesseract OCR to attempt to extract episode info from the png files. A fairly basic regex is used to extract the "ep" and "timestamp" columns.

Finally, to check for start of premiere episodes and start of regular episodes, a basic mean squared error is checked for each png against reference frames. When the MSE is under a given value, it should tell us that the frame is a match. Note that this may result in some false negatives - The lighting in the opening scene wasn't super consistent - that is, this process may miss some opening scenes.

