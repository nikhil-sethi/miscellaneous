import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def dsigmoid(x):
    return x * (1 - x)


class Network:
    """ Creates network between two layers
    - Takes the overall layer structure and the current input layer as the inputs
    """

    def __init__(self, node_list, layerNum):
        self.l = layerNum
        self.z = None
        self.weights = np.random.uniform(size=(node_list[self.l + 1], node_list[self.l]))
        self.biases = np.random.uniform(size=(node_list[self.l + 1], 1))  # ,  n_train, axis=1)
        # print(self.biases, self.weights, '\n')

    def feedforward(self, _input, batchsize=1):
        self.z = np.dot(self.weights, _input) / batchsize + self.biases
        return sigmoid(self.z)

    def backpropagate(self, layers, cost, lr, batchsize):
        prev_cost = np.dot(self.weights.T, cost) * dsigmoid(
            layers[self.l])  # (input x output).(output x n_train) = (input x n_train)
        self.db = np.sum(cost, axis=1, keepdims=True)  # 2*(output x n_train)*(output x n_train) = output x n_train
        self.dw = np.dot(cost, layers[
            self.l].T)  # / len(x_batch.T)  # (output x n_train).(n_train x input) = (output x input)
        self.weights += lr * self.dw / batchsize  # divided by batchsize to take average
        self.biases += lr * self.db / batchsize
        return prev_cost


def create(layer_structure):
    """
    :param layer_structure: list of number of nodes in each layer
    :return: list of network objects containing weights and biases for all layers
    """
    network = [0] * (len(layer_structure) - 1)
    for l in range(len(network)):
        network[l] = Network(layer_structure, l)
    return network


# Train
def train(network, x_train, l_train, epochs, learning_rate, batchsize):
    """
    :param network: list of networks between layers to train
    :param x_train: Training data; numpy array; Shape= (input_size x number of training_examples)
    :param l_train: Training data labels; Shape= (1 x number of training_examples)
    :param epochs: Number of training epochs
    :param learning_rate: Learning rate (Default 0.3)
    :param batchsize: Size of SGD batches
    :return: -Nan-
    """
    n_train = len(x_train.T)
    x_batchlist = [x_train[:, n:n + batchsize] for n in np.arange(n_train // batchsize) * batchsize]

    targets = np.zeros((len(network[-1].biases), n_train))
    targets[l_train, np.arange(n_train)] = 1
    targetlist = [targets[:, n:n + batchsize] for n in np.arange(n_train // batchsize) * batchsize]
    e = 0
    while e < epochs:
        for x_batch, target in zip(x_batchlist, targetlist):
            layers = [np.random.shuffle(x_batch.T), 0, 0]
            for l in range(len(network)):
                layers[l + 1] = network[l].feedforward(layers[l], batchsize)
            cost = target - layers[-1]
            d_cost = cost * dsigmoid(layers[-1])
            for l in np.flip(np.arange(len(network))):
                d_cost = network[l].backpropagate(layers, d_cost, learning_rate, batchsize)
        e += 1


# test
def test(network, x_test):
    # x_test = (x_test[:n_train] / 255).T
    # l_test = (l_test[:n_train]).T
    n_test = len(x_test.T)
    layers = [x_test, 0, 0]
    for l in range(len(network)):
        layers[l + 1] = network[l].feedforward(layers[l])
    # targets_test = np.zeros((output_nodes, n_test))
    # targets_test[l_test, np.arange(n_test)] = 1
    # a=abs(targets_test-layers[-1])
    return layers[-1]


'''
Pseudocode

load training +test data set
train network

number of layers
number of nodes in hidden layers


def activation function
    bla bla

feed forward part:
create input vector matrix
randomly initialize weight matrix
repeat for number of layers:
    calculate neuron values for next layer with activation function

calculate loss function for output layer




weight matrix at layer L= random matrix, dims= neurons(L-1) x neurons(L)
input layer= flattened image with pixel values as neurons
out

class network
    init
        input layer 
        output layer
        weight matrix
        bias matrix
    
    activation function
        
    feedforward
        calculate values for output layer
    
#main
x= input layer
node-list = [len(input layer, hidden layers, len(output layer)]
y_t= target output layer
for _ in node-list
    create network objects in networks array (_,_+1)
    feedforward

calculate loss of last layer 
    backpropagation
    
'''
