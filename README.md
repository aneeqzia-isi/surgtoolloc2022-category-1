# surgtoolloc2022-category-1

# Docker image & algorithm submission for the SurgToolLoc Challenge 2022

This repository has everything you and your team need to make an algorithm submission for the [SurgToolLoc Challenge](https://surgtoolloc.grand-challenge.org/). This algorithm will be used for the inference and evaluation of your model.

Be sure that you have a verified account on Grand Challenge and are accepted as a participant in the SurgToolLoc challenge.
You should be able to submit your Docker container/algorithm [here](https://grand-challenge.org/algorithms/create/).

Here are some useful documentation links for your submission process:
- [Tutorial on how to make an algorithm container on Grand Challenge](https://grand-challenge.org/blogs/create-an-algorithm/)
- [Docker documentation](https://docs.docker.com/)
- [Evalutils documentation](https://evalutils.readthedocs.io/)
- [Grand Challenge documentation](https://comic.github.io/grand-challenge.org/algorithms.html)

## Prerequisites

You will need to have [Docker](https://docs.docker.com/) installed on your system. We recommend using Linux with a Docker installation. If you are on Windows, please use [WSL 2.0](https://docs.microsoft.com/en-us/windows/wsl/install).

## Our two modalities

You can choose to participate in one or both of our modalities: surgical tool classification and/or surgical tool detection, following the guidelines for the [SurgToolLoc Challenge](https://surgtoolloc.grand-challenge.org/). The instructions below are valid to generate both Docker containers.

### Category #1 – Surgical tool classification:  

The output json file needs to be a list of dictionaries, containing information of tools present (from the total of 14 possible tools) in each frame of the input video. An example is given below: 
```
[ 
  { 
    "slice_nr": 0, 
    "needle_driver": true, 
    "monopolar_curved_scissor": true, 
    "force_bipolar": false, 
    "clip_applier": false, 
    "tip_up_fenestrated_grasper": false, 
    "cadiere_forceps": false, 
    "bipolar_forceps": false, 
    "vessel_sealer": false, 
    "suction_irrigator": false, 
    "bipolar_dissector": false, 
    "prograsp_forceps": false, 
    "stapler": false, 
    "permanent_cautery_hook_spatula": false, 
    "grasping_retractor": false 
  }, 
  { 
    "slice_nr": 1, 
    "needle_driver": true, 
    "monopolar_curved_scissor": true, 
    "force_bipolar": false, 
    "clip_applier": false, 
    "tip_up_fenestrated_grasper": false, 
    "cadiere_forceps": false, 
    "bipolar_forceps": false, 
    "vessel_sealer": false, 
    "suction_irrigator": false, 
    "bipolar_dissector": false, 
    "prograsp_forceps": false, 
    "stapler": false, 
    "permanent_cautery_hook_spatula": false, 
    "grasping_retractor": false 
  } 
] 
```
 where slice_nr is the frame number. 

### Category #2 – Surgical tool classification and localization:  

The output json file needs to be a dictionary containing the set of tools detected in each frame with its correspondent bounding box corners (x, y), again generating a single json file for each video like given below:  
```
{ 
    "type": "Multiple 2D bounding boxes", 
    "boxes": [ 
        { 
        "corners": [ 
            [ 92.66666412353516, 136.06668090820312, 0.50], 
            [ 54.79999923706055, 136.06668090820312, 0.5], 
            [ 54.79999923706055, 95.53333282470703, 0.5], 
            [ 92.66666412353516, 95.53333282470703, 0.5] 
        ], 
        "name": "slice_nr_1_needle_driver" 
        }, 
        { 
        "corners": [ 
            [ 92.66666412353516, 136.06668090820312, 0.5], 
            [ 54.79999923706055, 136.06668090820312, 0.5], 
            [ 54.79999923706055, 95.53333282470703, 0.5], 
            [ 92.66666412353516, 95.53333282470703, 0.5] 
        ], 
        "name": "slice_nr_2_monopolar_curved_scissor" 
        } 
    ], 
    "version": { "major": 1, "minor": 0 } 
} 
```
 Please note that the third value of each corner coordinate is not necessary for predictions but must be kept 0.5 always to comply with the Grand Challenge automated evaluation system (which was built to also consider datasets of 3D images). To standardize the submissions, the first corner is intended to be the top left corner of the bounding box, with the subsequent corners following the clockwise direction. The “type” and “version” entries are to comply with grand-challenge automated evaluation system. 

## Adapting the container to your algorithm

1. First, clone this repository:

```
git clone https://github.com/DeepPathology/MIDOG_reference_docker
```

2. Our `Dockerfile` should have everything you need, but you may change it to another base image/add your algorithm requirements if your algorithm requires it:

![Alt text](README_files/dockerfile_instructions.png?raw=true "Flow")

3. Edit `process.py`, which contains both functions for classification and prediction.

    a. The class Surgtoolloc_det contains the predict function. You should replace the dummy code in this function with the code for your inference algorihm. Use `__init__` to load your weights and/or perform any needed operation.

4. Run `test.sh`  to build the container. You should see an output of this kind at the end of its execution:
    ```
      Video file to be loaded: /input/video_1.mp4
      *** output of the generated json printed here ***
    ```
    
5. Run `export.sh`. This script will will produce `surgtoolloc_trial.tar.gz`. This is the file to be used when uploading the algorithm to Grand Challenge.

## Uploading your container to the MICCAI platform

1. Create a new algorithm [here](https://grand-challenge.org/algorithms/create/). Fill in the fields as specified on the form.

2. On the page of your new algorithm, go to `Containers` on the left menu and click `Upload a Container`. Now upload your `.tar.gz` file produced in step 5. **We will not accept submissions of containers linked to a GitHub repo.**

3. After the Docker container is marked as `Ready`, you can try out your own algorithm when clicking `Try-out Algorithm` on the page of your algorithm, again in the left menu.

4. Now, we will make a submission to one of the test phases. Go to the [SurgToolLoc Challenge](https://surgtoolloc.grand-challenge.org/) and click `Submit`. Choose which method you want to submit (classification and/or detection) and fill out the form. Under `Algorithm`, choose the algorithm that you just created. Then hit `Save`. After the processing in the backend is done, your submission should show up on the leaderboard.

The figure below indicates the step-by-step of how to upload a container:

![Alt text](README_files/MICCAI_surgtoolloc_fig.png?raw=true "Flow")

If something does not work for you, please do not hesitate to [contact us](mailto:isi.challenges@intusurg.com) or [add a post in the forum](https://grand-challenge.org/forums/forum/endoscopic-surgical-tool-localization-using-tool-presence-labels-663/). If the problem is related to the code of this repository, please create a new issue on GitHub.
