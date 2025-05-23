import random
import numpy as np
from dataclasses import dataclass, field
from typing import Callable
from activation import Activation
from activation import ActivationFunction

# Default instance for sigmoid
SIGMOID = ActivationFunction(func=Activation.sigmoid, derivative=Activation.sigmoid_derivative)
RELU = ActivationFunction(func=Activation.relu, derivative=Activation.relu_derivative)
TANH = ActivationFunction(func=Activation.tanh, derivative=Activation.tanh_derivative)

@dataclass
class Node:
    """
    This class represents a Neural Network Node
    """
    value: float = 0.0
    weights: list = field(default_factory=list)
    bias: float = 0.0
    debug: bool = False
    activation: ActivationFunction = SIGMOID

    def __post_init__(self):
        if self.debug: print("Initialized Node")

    def __str__(self):
        return f"Node(value={self.value:.4f}, bias={self.bias:.4f}, weights={len(self.weights)})"

    def initialize_weights(self, x):
        """
        Argument: x is an example list
        """
        self.weights = [random.uniform(0, 1) for _ in range(len(x))]

    def initialize_bias(self):
        """
        Argument: x is an example list
        """
        self.bias = random.uniform(0, 1)

    def forward_prop(self, x):
        """
        One step of forward propagation.
        """
        if len(self.weights) == 0:
            self.initialize_weights(x)

        if self.bias == 0:
            self.initialize_bias()

        z = np.dot(self.weights, x) + self.bias
        self.z = z
        self.value = self.activation.func(z)
        return self.value

    def backward_prop(self, learning_rate, prev_activations, y_true=None, next_layer=None):
        """
        One step of backward propagation.
        """
        if y_true:
            self.delta = (self.value - y_true) * self.activation.func(self.z)
        else:
            delta_sum = sum(w * node.delta for w, node in zip(self.weights, next_layer))
            self.delta = delta_sum * self.activation.derivative(self.z)

        for i in range(len(self.weights)):
            self.weights[i] -= learning_rate * self.delta * prev_activations[i]

        self.bias -= learning_rate * self.delta

    def print_weights(self):
        print(self.weights)


