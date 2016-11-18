import tensorflow as tf
from parameters import weight_variable, bias_variable
from regularization import dropout_layer, batch_norm_layer
from activation import relu, leaky_relu


class Layers(object):
    def __init__(self):
        """
        self.layers = a dictionary of all the layers keyed by the layer_id. Each layer_id should be unique
        """
        self.layers = dict()

    def _add_input_layer(self, width, layer_id='input'):
        """
        Adds input layer to the model
        :param width: The width of the input = dimension of the input
        :param layer_id: The unique id of the layer. Type=string
        :return: None
        """
        assert self.__layer_verifier(layer_id), 'Invalid: This layer is already present.'
        self.layers[layer_id] = tf.placeholder("float", [None, width])

    def _add_hidden_layer(self, input_layer_id, input_width, output_width, layer_id, scope_id, duplicate=False):
        """
        Adds the hidden layer to the model
        :param input_layer_id: The input layer identifier
        :param input_width: The width of the input for this layer
        :param output_width: The width of the output for this layer
        :param layer_id: The unique id of the layer. Type=string
        :param scope_id: The scope id same as the layer with which we want to share the weights
        :param duplicate: True if this layer is to have shared weights with a layer already present in the self.layers,
                            else False
        :return: None
        """
        assert self.__layer_verifier(layer_id), 'Invalid: This layer is already present.'
        with tf.variable_scope(scope_id) as scope:
            weights = weight_variable([input_width, output_width])
            biases = bias_variable([output_width])
            if duplicate:
                scope.reuse_variables()
            self.layers[layer_id] = tf.matmul(self.layers[input_layer_id], weights) + biases

    def _add_regularization_layer(self, input_layer_id, layer_id, regularization_type='dropout',
                                  weights=None, epsilon=None, dropout_ratio=None):
        """
        Adds the regularization layer to the model
        :param input_layer_id: The input layer identifier
        :param layer_id: The unique id of the layer. Type=string
        :param regularization_type: 'dropout' for Dropout and 'batch_norm' for Batch Normalization. Default = 'dropout'
        :param weights: The weights of the current layer
        :param epsilon: The batch_norm parameter to ensure that division is not by zero when variance of batch = 0
        :param dropout_ratio: The fraction of the layers to be masked.
        :return: None
        """
        assert self.__layer_verifier(layer_id), 'Invalid: This layer is already present.'
        if regularization_type == 'dropout':
            if dropout_ratio:
                self.layers[layer_id] = dropout_layer(self.layers[input_layer_id], dropout_ratio)
            else:
                self.layers[layer_id] = dropout_layer(self.layers[input_layer_id])
        elif regularization_type == 'batch_norm':
            assert weights is not None, 'Weights must be provided..'
            if epsilon:
                self.layers[layer_id] = batch_norm_layer(self.layers[input_layer_id], weights, epsilon)
            else:
                self.layers[layer_id] = batch_norm_layer(self.layers[input_layer_id], weights)
        else:
            raise ValueError('The type of regularization can only be one of ["dropout", "batch_norm"]')

    def _add_output_layer(self, input_layer_id, input_width, output_width, layer_id='output'):
        """
        Adds the output layer to the model
        :param input_layer_id: The input layer identifier
        :param input_width: The width of the input for this layer
        :param output_width: The width of the output for this layer
        :param layer_id: The unique id of the layer. Type=string
        :return: None
        """
        assert self.__layer_verifier(layer_id), 'Invalid: This layer is already present.'
        weights = weight_variable([input_width, output_width])
        biases = bias_variable([output_width])
        self.layers[layer_id] = tf.matmul(self.layers[input_layer_id], weights) + biases

    def _add_activation_layer(self, input_layer_id, layer_id):
        """
        Adds the activation layer
        :param input_layer_id: The input layer identifier
        :param layer_id: The unique id of the layer. Type=string
        :return: None
        """
        assert self.__layer_verifier(layer_id), 'Invalid: This layer is already present.'
        self.layers[layer_id] = relu(self.layers[input_layer_id])

    def __layer_verifier(self, layer_id):
        """
        Verifies if the layer asked to be formed is a valid layer and is not already formed before
        :param layer_id: The unique id of the layer. Type=string
        :return: True, if the layer is valid, else False
        """
        return layer_id not in self.layers
