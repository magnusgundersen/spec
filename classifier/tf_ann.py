import tensorflow as tf

class ANN:
    def __init__(self, number_of_input_nodes, number_of_output_nodes):
        self.number_of_input_nodes = number_of_input_nodes
        self.number_of_output_nodes = number_of_output_nodes

        self.setup()

    def setup(self):

        x = []
        y = []
        # Weights and biases between input layer and hidden layer
        # Weights are uniformly chosen in the range [-0.1, 0.1)
        # Biases are uniformly chosen in the range [0.0, 0.01)
        W = tf.Variable(tf.random_uniform([self.number_of_input_nodes, self.number_of_output_nodes], -0.1, 0.1))
        b = tf.Variable(tf.random_uniform([self.number_of_output_nodes], 0.0, 0.01))

        # Output layer
        # Multiplying input values with weights, before adding biases
        # Activating nodes using rectifier (rectified linear unit)
        output_layer = tf.nn.tanh(tf.add(tf.matmul(x, W), b))



    x = [[float(x) for x in range(100000000000)] for x in range(100)] # Input layer
    y = [[float(y)] for y in range(100)]

    #x = [[1.0,1.0],[1.0,1.0],[1.0,1.0],[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0]]
    #y = [1.0,1.0,1.0,0.0,0.0,0.0,0.0]
    number_of_input_values = len(x[0])
    number_of_output_values = len(y)





    # Calculating mean square error (MSE) between excpected output and actual output
    mse = tf.reduce_mean(tf.square(tf.sub(y, output_layer)))

    # Training network minimizing MSE
    train_step = tf.train.GradientDescentOptimizer(0.25).minimize(mse)


    # Setting up Tensorflow and initializing variables
    sess = tf.Session()
    sess.run(tf.initialize_all_variables())


    # Running max 5000 iterations
    # If no solution is found after 5000 iterations,
    # the network will probably oscillate forever
    for i in range(5000):
        # Calculate error
        error, _ = sess.run([mse, train_step])

        # If error is sufficiently low, exit loop
        if error < 0.01:
            break
    else:
        # Print warning if no solution found in 5000 steps
        print('No solution found')

    # Print number of steps, final MSE, and final solution
    print('Steps %d: MSE: %f' % (i, error))
    print(sess.run(output_layer))


ann = ANN()