import logging
import os
import pathlib
import warnings

import absl
import boto3
import botocore
import numpy as np

# Suppress warnigns from tensorflow about deprecations (common issue because tf2.0 is coming)
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=FutureWarning)
    import tensorflow as tf

log = logging.getLogger(__name__)

# Further suppress logging from tensorflow
absl.logging._warn_preinit_stderr = 0
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf_log = logging.getLogger('tensorflow')
tf_log.setLevel('ERROR')


class Nima(object):
    """
    This class loads a NIMA CNN from a model file in .pb format
    """

    def __init__(self, model_filepath: str):
        """
        Class constructor

        :param model_filepath: file containing model (both structure and weights) in ProtocolBuffers format
        """
        self.model_filepath = model_filepath
        self.input_height = 224
        self.input_width = 224
        self._load_graph(model_filepath=self.model_filepath)

    def _load_graph(self, model_filepath: str):
        """
        Load trained model from ProtocolBuffers file

        :param model_filepath: path to the model file
        """
        log.debug('Loading model...')
        self.graph = tf.Graph()
        self.sess = tf.compat.v1.InteractiveSession(graph=self.graph)

        with tf.io.gfile.GFile(model_filepath, 'rb') as fd:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(fd.read())

        log.debug('Check out the input placeholders:')
        nodes = [n.name + ' => ' + n.op for n in graph_def.node if n.op in ('Placeholder')]
        for node in nodes:
            log.debug(node)

        # Define input tensor
        self.input = tf.compat.v1.placeholder(np.float32,
                                              shape=[None, self.input_height, self.input_width, 3],
                                              name='input_1')

        tf.import_graph_def(graph_def, {'input_1': self.input})

        '''
        # Get layer names
        layers = [op.name for op in self.graph.get_operations()]
        for layer in layers:
            print(layer)
        '''
        '''
        # Check out the weights of the nodes
        weight_nodes = [n for n in graph_def.node if n.op == 'Const']
        for n in weight_nodes:
            print("Name of the node - %s" % n.name)
            print("Value - ")
            print(tf.make_ndarray(n.attr['value'].tensor))
        '''

        log.debug('Model loading complete.')

    def _get_file_from_s3(self, bucket_name: str, key: str, output_name: str):
        """
        Get file from s3

        :param bucket_name: name of the bucket
        :param key: name of the file in the bucket
        :param output_name: name of the file in the local filesystem
        """
        s3 = boto3.resource('s3')
        try:
            s3.Bucket(bucket_name).download_file(key, output_name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                log.error('The object does not exist.')
            else:
                raise

    def _process_file_path_string(self, file_path: str) -> str:
        """
        Process a file path to determine if it is local or S3.
        If it's an S3 path, download the image and return the name of the output local file.
        If it's a local path, expand the user tilde if necessary.

        :param file_path: string with either a local path or an s3 path
        """
        fullpath = pathlib.PurePosixPath(file_path)
        if fullpath.parts[0] == 's3:':
            bucket = str(fullpath.parts[1])
            key = str(pathlib.PurePosixPath(*fullpath.parts[2:]))
            outfile = '/tmp/img.jpg'
            self._get_file_from_s3(bucket_name=bucket, key=key, output_name=outfile)
            return outfile
        else:
            return str(pathlib.Path(file_path).expanduser())

    def _load_image(self, image_path: str) -> np.array:
        """
        From a local image path, preprocess it using the MobileNet preprocess_input function
        to match our target input size of (self.input_height, self.input_width)

        :param image_path: path to local image file
        """
        X = np.empty((1, self.input_height, self.input_width, 3))
        X[0, ] = np.asarray(tf.keras.preprocessing.image.load_img(image_path,
                                                                  target_size=(self.input_height, self.input_width)))
        X = tf.keras.applications.mobilenet.preprocess_input(X)
        return X

    def score_image(self, img_path: str):
        """
        Get an image path (either local or S3) and score it using NIMA.

        :param img_path: path to file (either local or S3)
        """
        # Process given path
        local_img = self._process_file_path_string(img_path)
        img_array = self._load_image(local_img)

        # Score image
        output_tensor = self.graph.get_tensor_by_name('import/dense_1/Softmax:0')
        scores_histogram = self.sess.run(output_tensor, feed_dict={self.input: img_array})[0]
        return np.sum(scores_histogram * np.arange(1, 11))


def aisthetics_scorer():
    path_to_current_file = pathlib.Path(__file__)
    relative_path_to_model = pathlib.Path('model/model.pb')
    absolute_path_to_model = pathlib.Path(*path_to_current_file.parts[:-1]) / relative_path_to_model
    log.debug('Loaded model from {}'.format(absolute_path_to_model))
    return Nima(str(absolute_path_to_model))
