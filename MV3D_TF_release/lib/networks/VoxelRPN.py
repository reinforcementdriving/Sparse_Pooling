#!/usr/bin/env python
# -*- coding:UTF-8 -*-

# File Name : rpn.py
# Purpose :
# Creation Date : 10-12-2017
# Last Modified : Thu 21 Dec 2017 09:03:36 PM CST
# Created By : Jialin Zhao

import tensorflow as tf
import numpy as np

from utils.config_voxels import cfg


small_addon_for_BCE = 1e-6


class MiddleAndRPN:
    def __init__(self, input, training=True, name='',output_score=True):
        # scale = [batchsize, 10, 400/200, 352/240, 128] should be the output of feature learning network
        self.input = input
        self.training = training

        with tf.variable_scope('MiddleAndRPN_' + name):
            # convolutinal middle layers
            '''
            temp_conv = ConvMD(3, 4, 4, 3, (2, 1, 1),
                               (1, 1, 1), self.input, name='conv1')
            temp_conv = ConvMD(3, 4, 4, 3, (1, 1, 1),
                               (0, 1, 1), temp_conv, name='conv2')
            temp_conv = ConvMD(3, 4, 4, 3, (2, 1, 1),
                               (1, 1, 1), temp_conv, name='conv3')
            temp_conv = tf.transpose(temp_conv, perm=[0, 2, 3, 4, 1])
            temp_conv = tf.reshape(
                temp_conv, [-1, cfg.INPUT_HEIGHT, cfg.INPUT_WIDTH, 8])

            # rpn
            # block1:
            temp_conv = ConvMD(2, 8, 2, 3, (2, 2), (1, 1),
                               temp_conv, training=self.training, name='conv4')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv5')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv6')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv7')
            deconv1 = Deconv2D(2, 2, 3, (1, 1), (0, 0),
                               temp_conv, training=self.training, name='deconv1')

            # block2:
            temp_conv = ConvMD(2, 2, 2, 3, (2, 2), (1, 1),
                               temp_conv, training=self.training, name='conv8')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv9')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv10')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv11')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv12')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv13')
            deconv2 = Deconv2D(2, 2, 2, (2, 2), (0, 0),
                               temp_conv, training=self.training, name='deconv2')

            # block3:
            temp_conv = ConvMD(2, 2, 2, 3, (2, 2), (1, 1),
                               temp_conv, training=self.training, name='conv14')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv15')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv16')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv17')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv18')
            temp_conv = ConvMD(2, 2, 2, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv19')
            deconv3 = Deconv2D(2, 2, 4, (4, 4), (0, 0),
                               temp_conv, training=self.training, name='deconv3')
            '''
            
            temp_conv = ConvMD(3, 128, 64, 3, (2, 1, 1),
                               (1, 1, 1), self.input, name='conv1')
            temp_conv = ConvMD(3, 64, 64, 3, (1, 1, 1),
                               (0, 1, 1), temp_conv, name='conv2')
            temp_conv = ConvMD(3, 64, 64, 3, (2, 1, 1),
                               (1, 1, 1), temp_conv, name='conv3')
            temp_conv = tf.transpose(temp_conv, perm=[0, 2, 3, 4, 1])
            temp_conv = tf.reshape(
                temp_conv, [-1, cfg.INPUT_HEIGHT, cfg.INPUT_WIDTH, 128])

            # rpn
            # block1:
            temp_conv = ConvMD(2, 128, 128, 3, (2, 2), (1, 1),
                               temp_conv, training=self.training, name='conv4')
            temp_conv = ConvMD(2, 128, 128, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv5')
            temp_conv = ConvMD(2, 128, 128, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv6')
            temp_conv = ConvMD(2, 128, 128, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv7')
            deconv1 = Deconv2D(128, 256, 3, (1, 1), (0, 0),
                               temp_conv, training=self.training, name='deconv1')

            # block2:
            temp_conv = ConvMD(2, 128, 128, 3, (2, 2), (1, 1),
                               temp_conv, training=self.training, name='conv8')
            temp_conv = ConvMD(2, 128, 128, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv9')
            temp_conv = ConvMD(2, 128, 128, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv10')
            temp_conv = ConvMD(2, 128, 128, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv11')
            temp_conv = ConvMD(2, 128, 128, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv12')
            temp_conv = ConvMD(2, 128, 128, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv13')
            deconv2 = Deconv2D(128, 256, 2, (2, 2), (0, 0),
                               temp_conv, training=self.training, name='deconv2')

            # block3:
            temp_conv = ConvMD(2, 128, 256, 3, (2, 2), (1, 1),
                               temp_conv, training=self.training, name='conv14')
            temp_conv = ConvMD(2, 256, 256, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv15')
            temp_conv = ConvMD(2, 256, 256, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv16')
            temp_conv = ConvMD(2, 256, 256, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv17')
            temp_conv = ConvMD(2, 256, 256, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv18')
            temp_conv = ConvMD(2, 256, 256, 3, (1, 1), (1, 1),
                               temp_conv, training=self.training, name='conv19')
            deconv3 = Deconv2D(256, 256, 4, (4, 4), (0, 0),
                               temp_conv, training=self.training, name='deconv3')
            
            # final:
            temp_conv = tf.concat([deconv3, deconv2, deconv1], -1)
            # Probability score map, scale = [None, 200/100, 176/120, 4]
            p_map = ConvMD(2, 768, 4, 1, (1, 1), (0, 0), temp_conv,
                           training=self.training, name='conv20', last_layer=True)
            # Regression(residual) map, scale = [None, 200/100, 176/120, 14]
            r_map = ConvMD(2, 768, 14, 1, (1, 1), (0, 0),
                           temp_conv, training=self.training, name='conv21', last_layer=True)
            # softmax output for positive anchor and negative anchor, scale = [None, 200/100, 176/120, 1]
            self.conv_feature = temp_conv
            if output_score:
              self.p_map = p_map
              self.r_map = r_map 
              self.p_pos = tf.sigmoid(p_map)
            self.output_shape = [cfg.FEATURE_HEIGHT, cfg.FEATURE_WIDTH]



def smooth_l1(deltas, targets, sigma=3.0):
    sigma2 = sigma * sigma
    diffs = tf.subtract(deltas, targets)
    smooth_l1_signs = tf.cast(tf.less(tf.abs(diffs), 1.0 / sigma2), tf.float32)

    smooth_l1_option1 = tf.multiply(diffs, diffs) * 0.5 * sigma2
    smooth_l1_option2 = tf.abs(diffs) - 0.5 / sigma2
    smooth_l1_add = tf.multiply(smooth_l1_option1, smooth_l1_signs) + \
        tf.multiply(smooth_l1_option2, 1 - smooth_l1_signs)
    smooth_l1 = smooth_l1_add

    return smooth_l1


def ConvMD(M, Cin, Cout, k, s, p, input, training=True, name='conv', last_layer=False):
    temp_p = np.array(p)
    temp_p = np.lib.pad(temp_p, (1, 1), 'constant', constant_values=(0, 0))
    with tf.variable_scope(name) as scope:
        if(M == 2):
            paddings = (np.array(temp_p)).repeat(2).reshape(4, 2)
            pad = tf.pad(input, paddings, "CONSTANT")
            temp_conv = tf.layers.conv2d(
                pad, Cout, k, strides=s, padding="valid", reuse=tf.AUTO_REUSE, name=scope)
        if(M == 3):
            paddings = (np.array(temp_p)).repeat(2).reshape(5, 2)
            pad = tf.pad(input, paddings, "CONSTANT")
            temp_conv = tf.layers.conv3d(
                pad, Cout, k, strides=s, padding="valid", reuse=tf.AUTO_REUSE, name=scope)
        if not(last_layer):
            temp_conv = tf.layers.batch_normalization(
                temp_conv, axis=-1, fused=True, training=training, reuse=tf.AUTO_REUSE, name=scope)
            temp_conv = tf.nn.relu(temp_conv)
        return temp_conv


def Deconv2D(Cin, Cout, k, s, p, input, training=True, name='deconv'):
    temp_p = np.array(p)
    temp_p = np.lib.pad(temp_p, (1, 1), 'constant', constant_values=(0, 0))
    paddings = (np.array(temp_p)).repeat(2).reshape(4, 2)
    pad = tf.pad(input, paddings, "CONSTANT")
    with tf.variable_scope(name) as scope:
        temp_conv = tf.layers.conv2d_transpose(
            pad, Cout, k, strides=s, padding="SAME", reuse=tf.AUTO_REUSE, name=scope)
        temp_conv = tf.layers.batch_normalization(
            temp_conv, axis=-1, fused=True, training=training, reuse=tf.AUTO_REUSE, name=scope)
        return tf.nn.relu(temp_conv)


if(__name__ == "__main__"):
    m = MiddleAndRPN(tf.placeholder(
        tf.float32, [None, 10, cfg.INPUT_HEIGHT, cfg.INPUT_WIDTH, 128]))
