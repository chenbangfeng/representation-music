'''
A single-task baseline experiment.

Task

-- Hotness

Models

-- Low Level Sharing Four Hidden Model
'''
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from Experiments.experiment import Experiment
from Models.single_task_four_hidden import SingleTaskFourHiddenModel
from utils.argument_parser import parse_arguments
from utils.data_utils.data_handler import fetch_data
from utils.data_utils.labels import Labels
from utils.network_utils.params import LossTypes

EXPERIMENT_NAME = "single-task-baseline"

if __name__ == '__main__':
    args = parse_arguments()

    # We will predict a single label for this experiment.
    task_ids = [Labels.hotness.value: LossTypes.mse]

    # Produce the training, validation, and testing set.
    x_train, x_validate, x_test, y_train, y_validate, y_test = fetch_data(task_ids)

    e = Experiment(expt_name=EXPERIMENT_NAME,
                   task_ids=task_ids,
                   x_train=x_train, x_validate=x_validate, x_test=x_test,
                   y_train=y_train, y_validate=y_validate, y_test=y_test,
                   model_class=SingleTaskFourHiddenModel,
                   learning_rate=args.learning_rate,
                   batch_size=args.batch_size,
                   num_epochs=args.num_epochs)

    e.initialize_network()
    e.train()
