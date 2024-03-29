import tensorflow as tf
import pandas as pd
import math

# Parse through data
cols = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']
class_names = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
dataset = pd.read_csv('iris.data', names=cols)
dataset['class'] = [0] * 50 + [1] * 50 + [2] * 50

training_data = pd.concat([dataset[:40], dataset[50:90], dataset[100:140]]).sample(frac=1).reset_index(drop=True)
test_data = pd.concat([dataset[40:50], dataset[90:100], dataset[140:]]).sample(frac=1).reset_index(drop=True)

# Convert the training and test DataFrames to DatasetV1Adapters
training_dataset = tf.data.Dataset.from_tensor_slices((
    training_data[cols[:4]].values,
    training_data['class'].values
))


test_dataset = tf.data.Dataset.from_tensor_slices((
    tf.cast(test_data[cols[:4]].values, tf.float32),
    tf.cast(test_data['class'].values, tf.int32)
))

print(type(training_dataset))

# Build and compile the model with one hidden layer and one output layer
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(4, )),
    tf.keras.layers.Dense(3, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Test the model with the training dataset
BATCH_SIZE = 10
model.fit(training_dataset.shuffle(120).repeat().batch(BATCH_SIZE), epochs=120/BATCH_SIZE, steps_per_epoch=math.ceil(120))

# Test the model with the test dataset
test_loss, test_accuracy = model.evaluate(test_dataset.batch(10).repeat(), steps=math.ceil(30))
print('Test dataset accuracy:', test_accuracy)