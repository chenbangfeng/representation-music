'''
Evaluate the multi-task model with low-level sharing.

Tasks:

-- Hotness
-- Duration
-- Year

Model:

-- Low Level Sharing Four Hidden Layers

'''
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from Experiments.evaluate_model import EvaluateModel
from Models.low_level_sharing_four_hidden import LowLevelSharingModel
from utils.data_utils.labels import Labels
from utils.network_utils.params import LossTypes

# Path of the checkpoint file.
# Should look like "./Experiments/expt-name/epoch-n"
MODEL_FILE = ""

if __name__ == '__main__':
    model_class = LowLevelSharingModel
    # Labels to be used in the experiment.
    task_ids = {Labels.hotness.value: LossTypes.mse,
                Labels.tempo.value: LossTypes.mse,
                Labels.loudness.value: LossTypes.mse}

    evaluation = EvaluateModel(task_ids)
    evaluation.load_data()
    evaluation.load_model(MODEL_FILE, model_class)
    errors = evaluation.evaluate_model()
    sys.stderr.write(str(errors) + "\n")
