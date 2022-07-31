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
        # return dict(type="Anything", tools=scored_candidates, version={"major": 1, "minor": 0})

    def save(self):
        with open(str(self._output_file), "w") as f:
            json.dump(self._case_results[0], f)

    # def _load_input_image(self, *, case) -> Tuple[SimpleITK.Image, Path]:
    #     input_image_file_path = case["path"]
    #
    #     input_image_file_loader = self._file_loaders["input_image"]
    #     if not isinstance(input_image_file_loader, ImageLoader):
    #         raise RuntimeError(
    #             "The used FileLoader was not of subclass ImageLoader"
    #         )
    #
    #     # Load the image for this case
    #     input_image = input_image_file_loader.load_image(input_image_file_path)
    #
    #     # Check that it is the expected image
    #     if input_image_file_loader.hash_image(input_image) != case["hash"]:
    #         raise RuntimeError("Image hashes do not match")
    #
    #     return input_image, input_image_file_path

    def predict(self, fname) -> Dict:
        print('Video file to be loaded: ' + str(fname))
        cap = cv2.VideoCapture(str(fname))
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(num_frames)

        # num_frames = 50
        # generate output json
        all_frames_predicted_outputs = []
        for i in range(num_frames):
            frame_dict = self.tool_detect_json_sample()
            tool_detections = self.dummy_tool_detection_model_output()

            frame_dict['slice_nr'] = i
            # "needle driver",
            # "monopolar curved scissor",
            frame_dict["needle_driver"] = True
            frame_dict["monopolar_curved_scissor"] = True
            # frame_dict[tool_detections[0]] = True
            # frame_dict[tool_detections[1]] = True

            all_frames_predicted_outputs.append(frame_dict)

        # type = {'type': 'Anything'}
        # version = {"version": {"major": 1, "minor": 0}}
        # tools = {'tools': all_frames_predicted_outputs}
        tools = all_frames_predicted_outputs


        # output_dict = {**type, **tools, **version}

        # print(output_dict)

        return tools



        # for i in range(num_frames):
        #     _, image_data = cap.read()
        #     # Detection: Compute connected components of the maximum values
        #     # in the input image and compute their center of mass
        #     sample_mask = image_data >= np.max(image_data)
        #     labels, num_labels = label(sample_mask)
        #     candidates = center_of_mass(
        #         input=sample_mask, labels=labels, index=np.arange(num_labels) + 1
        #     )
        #
        #     # Scoring: Score each candidate cluster with the value at its center
        #     candidate_scores = [
        #         image_data[tuple(coord)]
        #         for coord in np.array(candidates).astype(np.uint16)
        #     ]
        #
        #     # Serialize candidates and scores as a list of dictionary entries
        #     data = self._serialize_candidates(
        #         candidates=candidates,
        #         candidate_scores=candidate_scores,
        #         ref_image=fname,
        #     )
        #
        # # Convert serialized candidates to a pandas.DataFrame
        # return DataFrame(data)


if __name__ == "__main__":
    Surgtoolloc_det().process()
