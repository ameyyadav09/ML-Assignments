import numpy as np
import random

def sigmoid(z):
	"""
	Regular sigmoid function
	"""
	return 1.0/(1.0+(np.exp(-z)))

def sigmoid_prime(z):
	"""
	returns the derivative of the sigmoid function
	"""
	sig = sigmoid(z)
	return sig*(1-sig)

class NetworkDriver:
	def __init__(self, sizes):
		"""
		sizes = list of size of each layer in the neural network
		here bias value is assumed to be per layer but not per neuron
		"""
		self.num_layers = len(sizes)
		self.sizes = sizes
		# since first layer is input layer a neural net doesn't require bias for that since biases are only used in computing the outputs from later layers
		self.biases = [np.random.randn(x, 1) for x in sizes[1:]]
		self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

	def feedforward(self, a):
		"""
		a is input for layer 1
		we overwrite its values with output of layer 1, and then use them as input to layer 2,
		and continue to do so until we have the output of final layer

		"""
		for b, w in zip(self.biases, self.weights):
			a = sigmoid(np.dot(w, a)+b)
		return a

	def sgd(self, train_data, epochs, mini_batch_size, eta, test_data = None):
		n_train = len(train_data)
		if test_data:
			n_test = len(test_data)

		#for each epoch
		for i in xrange(epochs):
			#optional to shuffle training data
			random.shuffle(train_data)
			mini_batches = [train_data[j:j+mini_batch_size] for j in xrange(0, n_train, mini_batch_size)]

			for mini_batch in mini_batches:
				self.update_mini_batch(mini_batch, eta)
			if test_data:
				print "{}".format(self.evaluate(test_data)/(n_test*1.0))

	def update_mini_batch(self, mini_batch, eta):
		"""
		applies a single step of gradient descent for given data and updates the biases and weights
		"""
		nabla_b = [np.zeros(i.shape) for i in self.biases]
		nabla_w = [np.zeros(i.shape) for i in self.weights]

		for x, y in mini_batch:
			delta_nabla_b, delta_nabla_w = self.backprop(x, y)
			nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
			nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
			print nabla_b

		self.weights = [w-(eta/len(mini_batch))*nw for w, nw in zip(self.weights, nabla_w)]
		self.biases = [b-(eta/len(mini_batch))*nb for b, nb in zip(self.biases, nabla_b)]

	def evaluate(self, test_data):
		test_results = [(np.argmax(self.feedforward(x)), y) for (x, y) in test_data]
		return sum(int(x == y) for x, y in test_results)

	def cost_derivative(self, output_activations, y):
		return output_activations-y

	def backprop(self, x, y):
		"""Return a tuple ``(nabla_b, nabla_w)`` representing the
		gradient for the cost function C_x.  ``nabla_b`` and
		``nabla_w`` are layer-by-layer lists of numpy arrays, similar
		to ``self.biases`` and ``self.weights``
		"""
		nabla_b = [np.zeros(b.shape) for b in self.biases]
		nabla_w = [np.zeros(w.shape) for w in self.weights]
		# feedforward
		activation = x
		activations = [x] # list to store all the activations, layer by layer
		zs = [] # list to store all the z vectors, layer by layer
		for b, w in zip(self.biases, self.weights):
		    z = np.dot(w, activation)+b
		    zs.append(z)
		    activation = sigmoid(z)
		    activations.append(activation)
		# backward pass
		delta = self.cost_derivative(activations[-1], y) * \
		    sigmoid_prime(zs[-1])
		nabla_b[-1] = delta
		nabla_w[-1] = np.dot(delta, activations[-2].transpose())
		# Note that the variable l in the loop below is used a little
		# differently to the notation in Chapter 2 of the book.  Here,
		# l = 1 means the last layer of neurons, l = 2 is the
		# second-last layer, and so on.  It's a renumbering of the
		# scheme in the book, used here to take advantage of the fact
		# that Python can use negative indices in lists.
		for l in xrange(2, self.num_layers):
		    z = zs[-l]
		    sp = sigmoid_prime(z)
		    delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
		    nabla_b[-l] = delta
		    nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
		return (nabla_b, nabla_w)