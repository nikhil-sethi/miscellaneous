import numpy as np


# np.random.seed(0)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


# Input datasets
inputs = np.array([[1, 1], [1, 0], [0, 1], [0, 0]])
expected_output = np.array([[0], [1], [1], [0]])

epochs = 2
lr = 0.1
inputLayerNeurons, hiddenLayerNeurons, outputLayerNeurons = 2, 2, 1

# Random weights and bias initialization
# hidden_weights = np.random.uniform(size=(inputLayerNeurons, hiddenLayerNeurons))
# hidden_bias = np.random.uniform(size=(1, hiddenLayerNeurons))
# output_weights = np.random.uniform(size=(hiddenLayerNeurons, outputLayerNeurons))
# output_bias = np.random.uniform(size=(1, outputLayerNeurons))
hidden_weights = np.array([[0.81473259, 0.53481059], [0.7360752, 0.2979663]])
hidden_bias = np.array([[0.1875952, 0.25312396]])
output_weights = np.array([[0.19452747], [0.21469617]])
output_bias = np.array([[0.30892656]])


print("Initial hidden weights: ", end='')
print(*hidden_weights)
print("Initial hidden biases: ", end='')
print(*hidden_bias)
print("Initial output weights: ", end='')
print(*output_weights)
print("Initial output biases: ", end='')
print(*output_bias)

# Training algorithm
for _ in range(epochs):
    # Forward Propagation
    hidden_layer_activation = np.dot(inputs, hidden_weights)   # (4x2).(2x2)= 4x2
    hidden_layer_activation += hidden_bias  # (4x2) + (1x2) element wise sum = 4x2
    hidden_layer_output = sigmoid(hidden_layer_activation)

    output_layer_activation = np.dot(hidden_layer_output, output_weights)
    output_layer_activation += output_bias
    predicted_output = sigmoid(output_layer_activation)

    # Backpropagation
    error = expected_output - predicted_output
    d_predicted_output = error * sigmoid_derivative(predicted_output)

    error_hidden_layer = d_predicted_output.dot(output_weights.T)
    d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output)

    # Updating Weights and Biases
    output_weights += hidden_layer_output.T.dot(d_predicted_output) * lr
    output_bias += np.sum(d_predicted_output, axis=0, keepdims=True) * lr
    hidden_weights += inputs.T.dot(d_hidden_layer) * lr
    hidden_bias += np.sum(d_hidden_layer, axis=0, keepdims=True) * lr

print("Final hidden weights: ", end='')
print(*hidden_weights)
print("Final hidden bias: ", end='')
print(*hidden_bias)
print("Final output weights: ", end='')
print(*output_weights)
print("Final output bias: ", end='')
print(*output_bias)

print("\nOutput from neural network after 10,000 epochs: ", end='')
print(*predicted_output)