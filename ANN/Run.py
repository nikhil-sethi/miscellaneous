import mnist  # Mnist data set loader by Hyeonseok Jung (hsjeong5) https://github.com/hsjeong5/MNIST-for-Numpy
import ANN
import numpy as np
mnist.init()  # download data set and store as .pkl file

x_train, l_train, x_test, l_test = mnist.load()
n_train = 60000    # number of training examples (max: 60,000)
n_test = 10000      # number of testing examples (max: 10,000)

# Refine the data set
x_train = (x_train[:n_train] / (np.max(x_train)-np.min(x_train))).T  # Truncate to size and normalise
l_train = (l_train[:n_train]).T
x_test = (x_test[:n_test] / (np.max(x_test)-np.min(x_test))).T

layer_struct = [len(x_train), 30, 10]   # [input_size,..hidden_layers..., output_size]

net = ANN.create(layer_struct)  # net
ANN.train(net, x_train, l_train, epochs=30, learning_rate=3, batchsize=10)

# returns output_nodes x n_test size array with all predicted examples
guess = ANN.test(net, x_test)