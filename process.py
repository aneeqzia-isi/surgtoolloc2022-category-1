import SimpleITK
import numpy as np
import cv2
from pandas import DataFrame
from pathlib import Path
from scipy.ndimage import center_of_mass, label
from pathlib import Path
from evalutils import DetectionAlgorithm
from evalutils.validators import (
    UniquePathIndicesValidator,
    DataFrameValidator,
)
from typing import (Tuple)
from evalutils.exceptions import ValidationError
import random
from typing import Dict
import json

####
# Toggle the variable below to debug locally. The final container would need to have execute_in_docker=True
####
execute_in_docker = True

class VideoLoader():
    def load(self, *, fname):
        path = Path(fname)
        print(path)
        if not path.is_file():
            raise IOError(
                f"Could not load {fname} using {self.__class__.__qualname__}."
            )
            #cap = cv2.VideoCapture(str(fname))
        #return [{"video": cap, "path": fname}]
        return [{"path": fname}]

# only path valid
    def hash_video(self, input_video):
        pass


class UniqueVideoValidator(DataFrameValidator):
    """
    Validates that each video in the set is unique
    """

    def validate(self, *, df: DataFrame):
        try:
            hashes = df["video"]
        except KeyError:
            raise ValidationError("Column `video` not found in DataFrame.")

        if len(set(hashes)) != len(hashes):
            raise ValidationError(
                "The videos are not unique, please submit a unique video for "
                "each case."
            )


class Surgtoolloc_det(DetectionAlgorithm):
    def __init__(self):
        super().__init__(
            index_key='input_video',
            file_loaders={'input_video': VideoLoader()},
            input_path=Path("/input/") if execute_in_docker else Path("./test/"),
            output_file=Path("/output/surgical-tool-presence.json") if execute_in_docker else Path(
                "./output/surgical-tool-presence.json"),
            validators=dict(
                input_video=(
                    #UniqueVideoValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
        )
        
        ###                                                                                                     ###
        ###  TODO: adapt the following part for creating your model and loading weights
        ###                                                                                                     ###
        
        self.tool_list = ["needle_driver",
                          "monopolar_curved_scissor",
                          "force_bipolar",
                          "clip_applier",
                          "tip_up_fenestrated_grasper",
                          "cadiere_forceps",
                          "bipolar_forceps",
                          "vessel_sealer",
                          "suction_irrigator",
                          "bipolar_dissector",
                          "prograsp_forceps",
                          "stapler",
                          "permanent_cautery_hook_spatula",
                          "grasping_retractor"]

    def dummy_tool_detection_model_output(self):
        random_tool_predictions = [random.randint(0, len(self.tool_list) - 1), random.randint(0, len(self.tool_list) - 1)]

        return [self.tool_list[random_tool_predictions[0]], self.tool_list[random_tool_predictions[1]]]

    def tool_detect_json_sample(self):
        # single output dict
        slice_dict = {"slice_nr": 1}
        tool_boolean_dict = {i: False for i in self.tool_list}

        single_output_dict = {**slice_dict, **tool_boolean_dict}

        return single_output_dict

    def process_case(self, *, idx, case):

        # Input video would return the collection of all frames (cap object)
        input_video_file_path = case #VideoLoader.load(case)
        # Detect and score candidates
        scored_candidates = self.predict(case.path) #video file > load evalutils.py

        # return
        # Write resulting candidates to result.json for this case
        return scored_candidates

    def save(self):
        with open(str(self._output_file), "w") as f:
            json.dump(self._case_results[0], f)


    def predict(self, fname) -> Dict:
        """
        Inputs:
        fname -> video file path
        
        Output:
        tools -> list of prediction dictionaries (per frame) in the correct format as described in documentation 
        """
        
        print('Video file to be loaded: ' + str(fname))
        cap = cv2.VideoCapture(str(fname))
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        
        ###                                                                     ###
        ###  TODO: adapt the following part for YOUR submission: make prediction
        ###                                                                     ###
        
        print(num_frames)

        # generate output json
        all_frames_predicted_outputs = []
        for i in range(num_frames):
            frame_dict = self.tool_detect_json_sample()
            tool_detections = self.dummy_tool_detection_model_output()

            frame_dict['slice_nr'] = i
            
            # predict same two tools everytime
            frame_dict["grasping_retractor"] = True
            frame_dict["vessel_sealer"] = True

            all_frames_predicted_outputs.append(frame_dict)


        tools = all_frames_predicted_outputs

        return tools



if __name__ == "__main__":
    Surgtoolloc_det().process()
