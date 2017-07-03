import tensorflow as tf
import numpy as np

from tf_G.pagerank.transition.transition_reset_matrix import \
  TransitionResetMatrix
from tf_G.graph.graph import Graph


class TransitionRandom(TransitionResetMatrix):
  def __init__(self, sess: tf.Session, name: str, graph: Graph,
               beta: float) -> None:
    TransitionResetMatrix.__init__(self, sess, name + "_log", graph, beta)

    self.run_tf(self.transition.assign(tf.log(self.transition)))

  def get_tf(self, *args, **kwargs):
    t = args[0]
    return (tf.scatter_nd(
      tf.reshape(tf.multinomial(self.transition, num_samples=1),
                 [self.G.n, 1]),
      tf.fill([self.G.n], 1 / (self.G.n + t)), [self.G.n]))
