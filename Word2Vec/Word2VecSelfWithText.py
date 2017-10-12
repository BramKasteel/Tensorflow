## Not working, copied from text from tensorflow website

import tensorflow as tf


#Embedding matrix; it is just a big random matrix to start with.
#Dimensions: #words, DimEmbedding, auto, 1
embeddings = tf.Variable(
    tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0)
)

#DO NOT KNOW HOW THIS NCE FUNCTION WORKS YET.
#it has something to do with initialising. we have #words * DimEmbedding Gaussian numbers
nce_weights = tf.Variable(
    tf.truncated_normal([vocabulary_size, embedding_size],
                        stddev=1.0 / math.sqrt(embedding_size)))
#something similar for biases
nce_biases = tf.Variable(tf.zeros([vocabulary_size]))

#We suppose that we have already integerized our text corpus. See tensorflow/examples/tutorials/word2vec/word2vec_basic
#Skip-Gram takes two inputs. One is a batch full of integers representing context words,
# the other is a batch of target words (?)
train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])

#Now we need to look up the vector for each of the source words in the batch (random at first)
embed = tf.nn.embedding_lookup(embeddings, train_inputs)

#Now that we have the embeddings for each word, we'd like to try to predict the target word using
#the noise-contrasting training objective
loss = tf.reduce_mean(
    tf.nn.nce_loss(weights=nce_weights,
                   biases=nce_biases,
                   labels=train_labels,
                   inputs=embed,
                   num_sampled=num_sampled,
                   num_classes=vocabulary_size))

#We want to perform stochastic gradient descent on this loss function (also called a 'node')
optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.0).minimize(loss)

