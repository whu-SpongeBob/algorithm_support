# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: model.py
@time: 2020/4/23 0:24

这一行开始写关于本文件的说明与解释


"""
import os
import tensorflow as tf
import matplotlib.pyplot as plt

from dataset_reader import x_train, x_test, y_train, y_test


class Model:
    def __init__(self, hidden_layers=10):
        self.hidden_layers = hidden_layers

    def create_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(20, activation='relu', input_shape=(15,)))
        model.add(tf.keras.layers.Dense(self.hidden_layers, activation='relu'))
        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
        return model

    def train(self, output_dir):
        model = self.create_model()
        model.summary()
        model.compile(optimizer='adam',
                      loss='binary_crossentropy',  # 二分类问题选择二元交叉熵损失函数
                      metrics=['AUC'])

        history = model.fit(x_train, y_train,
                            batch_size=64,
                            epochs=30,
                            validation_split=0.2  # 分割一部分训练数据用于验证
                            )
        os.mkdir(output_dir)
        model.save(output_dir + '/keras_model.h5')
        self.plot_metric(history, "loss")
        self.plot_metric(history, "AUC")

    @classmethod
    def plot_metric(cls, history, metric):
        train_metrics = history.history[metric]
        val_metrics = history.history['val_' + metric]
        epochs = range(1, len(train_metrics) + 1)
        plt.plot(epochs, train_metrics, 'bo--')
        plt.plot(epochs, val_metrics, 'ro-')
        plt.title('Training and validation ' + metric)
        plt.xlabel("Epochs")
        plt.ylabel(metric)
        plt.legend(["train_" + metric, 'val_' + metric])
        plt.show()


if __name__ == '__main__':
    my_model = Model()
    my_model.train(output_dir="./data/output")
