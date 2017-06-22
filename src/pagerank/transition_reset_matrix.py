import tensorflow as tf

from src.utils.tensorflow_object import TensorFlowObject
from src.utils.update_edge_notifier import UpdateEdgeNotifier


class TransitionResetMatrix(TensorFlowObject, UpdateEdgeNotifier):
    def __init__(self, sess, name, graph, beta):
        TensorFlowObject.__init__(self, sess, name)
        UpdateEdgeNotifier.__init__(self)

        self.G = graph
        self.G.attach(self)

        self.beta = beta
        self.transition = tf.Variable(
            tf.where(self.G.is_not_sink_tf,
                     tf.add(
                         tf.scalar_mul(beta, tf.div(self.G.A_tf,
                                                    self.G.out_degrees_tf)),
                         (1 - beta) / self.G.n_tf),
                     tf.fill([self.G.n, self.G.n], tf.pow(self.G.n_tf, -1))),
            name=self.name + "_T")
        self.run(tf.variables_initializer([self.transition]))

    @property
    def get_tf(self):
        return self.transition

    def update_edge(self, edge, change):

        # print("Edge: " + str(edge) + "\tChange: " + str(change))

        if change > 0.0:
            self.run(tf.scatter_nd_update(
                self.transition, [[edge[0]]],
                tf.add(
                    tf.scalar_mul(
                        self.beta,
                        tf.div(
                            self.G.A_tf_vertex(edge[0]),
                            self.G.out_degrees_tf_vertex(edge[0]))),
                    (1 - self.beta) / self.G.n_tf)))
        else:
            self.run(tf.scatter_nd_update(
                self.transition, [[edge[0]]],
                tf.where(self.G.is_not_sink_tf_vertex(edge[0]),
                         tf.add(
                             tf.scalar_mul(
                                 self.beta,
                                 tf.div(
                                     self.G.A_tf_vertex(edge[0]),
                                     self.G.out_degrees_tf_vertex(edge[0]))),
                             (
                                 1 - self.beta) / self.G.n_tf),
                         tf.fill([1, self.G.n], tf.pow(self.G.n_tf, -1)))))
        self._notify(edge, change)
