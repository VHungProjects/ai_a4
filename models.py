import nn

class PerceptronModel(object):
    def __init__(self, dim):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dim` is the dimensionality of the data.
        For example, dim=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dim)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x_point):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x_point: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        #Compute the dot product of stored weight vector and given output
        #Returns nn.DotProduct object
        #Usage of DotProduct: nn.DotProduct(weights, features)
        return nn.DotProduct(self.get_weights(),x_point)


    def get_prediction(self, x_point):
        """
        Calculates the predicted class for a single data point `x_point`.

        Returns: -1 or 1
        """
        "*** YOUR CODE HERE ***"
        #Use nn.as_scalar to convert scalar node to python float
        #Check if dot product is positive
        if nn.as_scalar(self.run(x_point)) < 0:
            return -1
        else:
            return 1


    def train_model(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        #Same process as 271
        #x = xmat
        #y = label/answer
        missed = True
        while missed:
            missed = False
            for xmat,yvec in dataset.iterate_once(1):
                guess = self.get_prediction(xmat) #Make a guess based on data xmat*weights
                actual = nn.as_scalar(yvec)
                if guess != actual: #Check if guess is = actual
                    missed = True
                    #Multiplier, direction
                    self.get_weights().update(actual,xmat) #Try to correct weights

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        #Underfit = increase output size
        #Overfit = decrease output size
        self.learn = 0.001
        self.batch = 1
        #Hidden Layer 1
        self.W1 = nn.Parameter(1,32)
        self.B1 = nn.Parameter(1,32)
        #Hidden Layer 2
        self.W2 = nn.Parameter(32,16)
        self.B2 = nn.Parameter(1,16)
        #Output Layer
        self.W3 = nn.Parameter(16,1)
        self.B3 = nn.Parameter(1,1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        #f(x) = relu( relu(x * W1 + b1) * W2 + b2) * W3 + b3
        layer1output = nn.ReLU(nn.AddBias(nn.Linear(x, self.W1), self.B1)) # relu(x * W1 + b1)
        layer2output = nn.ReLU(nn.AddBias(nn.Linear(layer1output, self.W2), self.B2)) #relu( layer1 * W2 + b2)
        prediction = (nn.AddBias(nn.Linear(layer2output, self.W3), self.B3)) # layer2 * W3 + b3
        return prediction

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        prediciton = self.run(x)
        loss  = nn.SquareLoss(prediciton,y)
        return loss

    def train_model(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        
        while True:
            for xmat, yvec in dataset.iterate_once(self.batch):
                loss = self.get_loss(xmat,yvec)
                
                grad_wrt_W1, grad_wrt_B1,grad_wrt_W2, grad_wrt_B2,grad_wrt_W3, grad_wrt_B3 = nn.gradients([self.W1, self.B1,self.W2, self.B2,self.W3, self.B3], loss)
                self.W1.update(-self.learn,grad_wrt_W1)
                self.B1.update(-self.learn,grad_wrt_B1)
                self.W2.update(-self.learn,grad_wrt_W2)
                self.B2.update(-self.learn,grad_wrt_B2)
                self.W3.update(-self.learn,grad_wrt_W3)
                self.B3.update(-self.learn,grad_wrt_B3)

            if nn.as_scalar(loss) < self.learn:
                return

        


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        #Underfit = increase output size
        #Overfit = decrease output size
        self.learn = 0.5
        self.batch = 100
        #Hidden Layer 1
        self.W1 = nn.Parameter(784,261)
        self.B1 = nn.Parameter(1,261)
        #Hidden Layer 2
        self.W2 = nn.Parameter(261,88)
        self.B2 = nn.Parameter(1,88)
        #Hidden Layer 3
        self.W3 = nn.Parameter(88,30)
        self.B3 = nn.Parameter(1,30)
        #Output Layer
        self.W4 = nn.Parameter(30,10)
        self.B4 = nn.Parameter(1,10)#0-9 10 digits

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        layer1output = nn.ReLU(nn.AddBias(nn.Linear(x, self.W1), self.B1)) # relu(x * W1 + b1)
        layer2output = nn.ReLU(nn.AddBias(nn.Linear(layer1output, self.W2), self.B2)) #relu( layer1 * W2 + b2)
        layer3output = nn.ReLU(nn.AddBias(nn.Linear(layer2output, self.W3), self.B3)) #relu( layer2 * W3 + b3)
        prediction = nn.AddBias(nn.Linear(layer3output, self.W4), self.B4) # layer3 * W4 + b4
        return prediction

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        prediciton = self.run(x)
        loss  = nn.SoftmaxLoss(prediciton,y)
        return loss

    def train_model(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for xmat, yvec in dataset.iterate_once(self.batch):
                loss = self.get_loss(xmat,yvec)
                
                grad_wrt_W1, grad_wrt_B1,grad_wrt_W2, grad_wrt_B2,grad_wrt_W3, grad_wrt_B3,grad_wrt_W4, grad_wrt_B4 = nn.gradients([self.W1, self.B1,self.W2, self.B2,self.W3, self.B3,self.W4, self.B4], loss)
                self.W1.update(-self.learn,grad_wrt_W1)
                self.B1.update(-self.learn,grad_wrt_B1)
                self.W2.update(-self.learn,grad_wrt_W2)
                self.B2.update(-self.learn,grad_wrt_B2)
                self.W3.update(-self.learn,grad_wrt_W3)
                self.B3.update(-self.learn,grad_wrt_B3)

            if dataset.get_validation_accuracy() > 0.98:
                return

