# -*- coding: utf-8 -*-
"""
Spyder Editor

First steps in Tensorflow
"""

import tensorflow as tf

#We can create floating point Tensors as follows:
node1 = tf.constant(3.0, tf.float32)
node2 = tf.constant(4.0) #also tf.float32 implicitly
print(node1,node2) #Does not evaluate the nodes

#To evaluate nodes, we must run the 'computational graph' within a 'Session'
sess = tf.Session()
print(sess.run([node1,node2]))

#You can create computations by combining Tensor nodes
node3 = tf.add(node1, node2)
print("node3: ", node3)
print("sess.run(node3): ", sess.run(node3))

#We can also make this computation a function of unknown input,
#by using placeholders: (we 'promise' to give the value of this node later on)
a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)
adder_node = a + b #shortcut for tf.add(a,b)
print(sess.run(adder_node, {a:3,b:4.5}))
print(sess.run(adder_node, {a:[1,3],b:[2,4]}))

#We can also introduce variables. (Bram: doe not know a real difference between them and placeholders yet)
W = tf.Variable([.3], tf.float32)
b = tf.Variable([-.3], tf.float32)
x = tf.placeholder(tf.float32)
linear_model = W * x + b
#Variables have to be run to get initialised
init = tf.global_variables_initializer()
sess.run(init)
print(sess.run(linear_model, {x:[1,2,3,4]}))

#Compare the linear model with some target vector  y
y = tf.placeholder(tf.float32)
squared_deltas = tf.square(linear_model - y)
loss = tf.reduce_sum(squared_deltas)
print(sess.run(loss, {x:[1,2,3,4], y:[0,-1,-2,-3]}))

#Assign the perfect model variables.
fixW = tf.assign(W, [-1.])
fixb = tf.assign(b, [1.])
sess.run([fixW, fixb])
print(sess.run(loss, {x:[1,2,3,4], y:[0,-1,-2,-3]})) #Error is zero now

#We can also train the parameters
