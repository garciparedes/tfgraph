import tensorflow as tf
import warnings

from src.utils.tensorflow_object import TensorFlowObject


class TransitionMatrix(TensorFlowObject):
    def __init__(self, sess, name, graph):
        TensorFlowObject.__init__(self, sess, name)
        self.G = graph
        self.G.attach(self)
        self.transition = tf.Variable(
            tf.where(self.G.is_not_sink_tf,
                     tf.div(self.G.A_tf, self.G.out_degrees_tf),
                     tf.fill([self.G.n, self.G.n], 1 / self.G.n)),
            name=self.name + "_T")
        self.run(tf.variables_initializer([self.transition]))

    @property
    def get_tf(self):
        return self.transition

    def update(self, edge, change):
        warnings.warn('TransitionResetMatrix auto-update not implemented yet!')

        print("Edge: " + str(edge) + "\tChange: " + str(change))

        self.run(tf.scatter_nd_update(
            self.transition, [[edge[0]]],
            tf.gather(
                tf.where(self.G.is_not_sink_tf,
                         tf.div(self.G.A_tf, self.G.out_degrees_tf),
                         tf.fill([self.G.n, self.G.n], 1 / self.G.n)),
                [edge[0]])))

