#!/usr/bin/python3

import tensorflow as tf
import numpy as np
import timeit

import tf_G


def main():
  beta: float = 0.85
  convergence: float = 0.0001

  edges_np: np.ndarray = tf_G.DataSets.naive_6()

  with tf.Session() as sess:
    writer: tf.summary.FileWriter = tf.summary.FileWriter(
      'logs/tensorflow/.')

    graph: tf_G.Graph = tf_G.GraphConstructor.from_edges(
      sess, "G", edges_np, writer, is_sparse=False)

    pr_alge: tf_G.PageRank = tf_G.AlgebraicPageRank(sess, "PR1",
                                                    graph,
                                                    beta)

    pr_iter: tf_G.PageRank = tf_G.IterativePageRank(sess, "PR1", graph, beta)
    '''
    g_upgradeable: tf_G.Graph = tf_G.GraphConstructor.empty(sess,
                                                           "Gfollowers",
                                                           7, writer)
    pr_upgradeable: tf_G.PageRank = tf_G.IterativePageRank(sess,
                                                          "PRfollowers",
                                                          g_upgradeable,
                                                          beta)
    '''

    # a = pr_alge.ranks_np()
    start_time: float = timeit.default_timer()
    a: np.ndarray = pr_alge.ranks_np(convergence=convergence, topics=[5],
                                   topics_decrement=True)
    elapsed: float = timeit.default_timer() - start_time
    print(elapsed)

    start_time: float = timeit.default_timer()
    b: np.ndarray = pr_iter.ranks_np(convergence=convergence, topics=[5],
                                   topics_decrement=True)
    elapsed: float = timeit.default_timer() - start_time
    print(elapsed)

    print(a)
    print(b)
    # print(c)
    # print((pr_alge.error_vector_compare_np(pr_iter)))
    # print(pr_iter.ranks_np(convergence=convergence))
    # print(pr_alge.error_ranks_compare_np(pr_iter))
    '''
    g_sparse = tf_G.GraphConstructor.as_sparsifier(sess, graph, 0.75)

    pr_sparse = tf_G.IterativePageRank(sess, "PR_sparse", g_sparse, beta)

    start_time: float = timeit.default_timer()
    d: np.ndarray = pr_sparse.ranks_np(convergence=convergence)
    elapsed: float = timeit.default_timer() - start_time
    print(elapsed)

    print(pr_iter.error_ranks_compare_np(pr_sparse))
    print(graph.m)
    print(g_sparse.m)
    '''
    '''
    g_sparse_upgradeable = tf_G.GraphConstructor.empty_sparsifier(
        sess=sess, name="G_su", n=6301, p=0.5)
    pr_iter: tf_G.PageRank = tf_G.IterativePageRank(
        sess, "PR_su", g_sparse_upgradeable, beta)

    e = pr_iter.ranks_np(convergence=convergence)
    for r in edges_np:
        g_sparse_upgradeable.append(r[0], r[1])
        e = pr_iter.ranks_np(convergence=convergence)
        tf_G.Utils.save_ranks("logs/csv/sparse_update.csv", e)

    print(e)
    # tf_G.Utils.save_ranks("logs/csv/alge.csv",a)
    # tf_G.Utils.save_ranks("logs/csv/sparse.csv", d)
    tf_G.Utils.save_ranks("logs/csv/sparse_update.csv", e)
    '''
    '''
    print(GraphConstructor.unweighted_random(sess, "GRandom", 10 ** 2,
                                             10 ** 3, writer=writer))
    '''
    tf_G.Utils.save_ranks("logs/csv/iter.csv", b)

    writer.add_graph(sess.graph)


if __name__ == '__main__':
  main()
