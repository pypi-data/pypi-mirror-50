import importlib
from keras.models import Model
from keras.layers import Dropout, Dense
from keras.optimizers import Adam
from aisthetics.utils.losses import earth_movers_distance


class Nima:
    """
    This class implements the architecture of the NIMA neural network
    """

    def __init__(self, base_model_name, n_classes=10, learning_rate=0.001, dropout_rate=0, loss=earth_movers_distance,
                 decay=0, weights='imagenet'):
        """
        Constructor of the class

        :param base_model_name: indicates which model to use as a base for NIMA
        :param n_classes: indicates the number of possible classes (scores) to classify
        :param learning_rate: learning rate for the NN
        :param dropout_rate: dropout rate for the NN
        :param loss: which loss function to use (has to be a callable(tensor,tensor)->tensor)
        :param weights: weights to use for the model
        """
        self.n_classes = n_classes
        self.base_model_name = base_model_name
        self.learning_rate = learning_rate
        self.dropout_rate = dropout_rate
        self.loss = loss
        self.decay = decay
        self.weights = weights
        self._get_base_module()

    def _get_base_module(self):
        """ Helper function to select the base model using the input string base_model_name """
        # import Keras base model module
        if self.base_model_name == 'InceptionV3':
            self.base_module = importlib.import_module('keras.applications.inception_v3')
        elif self.base_model_name == 'InceptionResNetV2':
            self.base_module = importlib.import_module('keras.applications.inception_resnet_v2')
        else:
            self.base_module = importlib.import_module('keras.applications.'+self.base_model_name.lower())

    def build(self):
        """ Model builder method: gets the base CNN and adds a dropout layer and a base layer on top """
        # get base model class
        BaseCnn = getattr(self.base_module, self.base_model_name)

        # load pre-trained model
        self.base_model = BaseCnn(input_shape=(224, 224, 3), weights=self.weights, include_top=False, pooling='avg')

        # add dropout and dense layer
        x = Dropout(self.dropout_rate)(self.base_model.output)
        x = Dense(units=self.n_classes, activation='softmax')(x)

        self.nima_model = Model(self.base_model.inputs, x)

    def compile(self):
        """ Tensorflow compile model """
        self.nima_model.compile(optimizer=Adam(lr=self.learning_rate, decay=self.decay), loss=self.loss)

    def preprocessing_function(self):
        """ Returns the specific model pre-processing function """
        return self.base_module.preprocess_input
