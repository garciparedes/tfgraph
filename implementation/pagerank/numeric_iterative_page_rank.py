import tensorflow as tf

from pagerank.numeric_page_rank import NumericPageRank
from pagerank.transition_reset_matrix import TransitionResetMatrix


class NumericIterativePageRank(NumericPageRank):
    def __init__(self, sess, name, graph, beta=None):
        T = TransitionResetMatrix(sess, name,
                                  graph,
                                  beta)
        NumericPageRank.__init__(self, sess, name, graph, beta, T)

        self.v_last = tf.Variable(tf.fill([1, self.G.n], 0.0),
                                  name=self.name + "_Vi-1")

        self.iter = [self.v_last.assign(self.v),
                     self.v.assign(tf.matmul(self.v, self.T.get,
                                             b_is_sparse=True))]
        self.sess.run(tf.variables_initializer([self.v_last]))

    def _page_rank_until_convergence(self, convergence):
        diff = tf.reduce_max(tf.abs(tf.subtract(self.v_last, self.v)), 1)
        self.sess.run(self.iter)
        while self.sess.run(diff)[0] > convergence / self.sess.run(self.G.n_tf):
            self.sess.run(self.iter)
        return self.sess.run(self.v)

    def _page_rank_until_steps(self, steps):
        for step in range(steps):
            self.sess.run(self.iter)
        return self.sess.run(self.v)

    def _page_rank_exact(self):
        raise NotImplementedError(
            'NumericIterativePageRank not implements exact PageRank')