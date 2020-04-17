from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.regularizers import l1

from keras import initializers
from keras import regularizers

#from MachineLearning.main_code.feature_extraction_final import extract_features
from feature_extraction_final import extract_features

import os
import numpy as np


# This function takes in a array of size 3, and normalizes the data
def normalize(data_points):
    data_points[0] = (data_points[0] - (-19.61)) / (19.61 - (-19.61))
    data_points[1] = (data_points[1] - (-19.61)) / (19.61 - (-19.61))
    data_points[2] = (data_points[2] - (-19.61)) / (19.61 - (-19.61))
    return data_points


# This function takes in the input dimension of the features
# and outputs the fully connected neural network model
def create_neural_network_model(input_dimension, output_dimension):
    opt = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)

    model = Sequential()
    model.add(Dense(256, input_dim=input_dimension, activation='relu', kernel_initializer='random_uniform',
                    bias_initializer=initializers.Constant(0.1)))
    model.add(Dense(256, activation='relu', kernel_initializer='random_uniform',
                    bias_initializer=initializers.Constant(0.1)))
    # model.add(Dense(256, activation='relu', kernel_initializer='random_uniform',
    #                 bias_initializer=initializers.Constant(0.1)))
    model.add(Dense(128, activation='relu', kernel_initializer='random_uniform',
                    bias_initializer=initializers.Constant(0.1)))
    model.add(Dense(output_dimension, activation='sigmoid', kernel_initializer='random_uniform',
                    bias_initializer='zeros'))
    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
    return model


# This function takes in the trained model, and the test data
# and prints out the classification report (recall, precision, f-measure
# and returns the confusion matrix and the accuracy
def test_model_nn(model_to_test, x_test, y_test):
    predictions = model_to_test.predict(x_test)
    predictions_boolean = np.argmax(predictions, axis=1)
    # Count start from 1
    predictions_boolean += 1
    y_test = y_test.astype(int)
    print(classification_report(y_test, predictions_boolean))
    return confusion_matrix(y_test, predictions_boolean), accuracy_score(y_test, predictions_boolean)


# This function takes in the trained model, and the name of the model
# and saves it as a .json and .h5 file
def save_model(model_to_save, name):
    model_json = model_to_save.to_json()
    save_path = os.path.join("Trained_models", name)
    with open(save_path + ".json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    save_path = os.path.join("Trained_models", name)
    model_to_save.save_weights(save_path + ".h5")
    print("Saved model to disk")


# This function takes in the model name
# and returns the trained model
def load_model(model_name):
    json_file = open(model_name + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_name + ".h5")
    print("Loaded model from disk")
    return loaded_model


# This function takes in the labels, which is represented by a number
# and returns the one hot encoded labels
def one_hot_encode_labels(labels):
    one_hot_encoder = OneHotEncoder(sparse=False)
    one_hot_encoded = one_hot_encoder.fit_transform(labels)
    return one_hot_encoded


# Returns a rows * window_size * num_features array
def continuous_to_time_step(x, window_size, num_features):
    x.drop(x.iloc[:, 0:1], inplace=True, axis=1)
    first = True
    for i in range(0, num_features):
        column = x.iloc[:, i:i+1]
        column = column.head(len(column) - len(column)%window_size)
        column = column.to_numpy()
        column = column.reshape((int(column.shape[0] / window_size), window_size))
        if first:
            data_reshaped = column
            first = False
        else:
            data_reshaped = np.dstack((data_reshaped, column))
    return data_reshaped


# This function takes in the path of the data set and the sampling rate
# and returns the x and y data such that each data point is 2.56s worth of data
def load_dance_dance_data_set(folder_path, sampling_rate, window_length):
    x_data = []
    y_data = []
    for text_file in os.listdir(folder_path):
        print("Processing:", text_file)
        full_path = os.path.join(folder_path, text_file)
        x_partial_data, y_partial_data = load_dance_dance_action(full_path, text_file, sampling_rate, window_length)
        x_data.extend(x_partial_data)
        y_data.extend(y_partial_data)
        print(np.asarray(x_partial_data).shape)
    y_data = np.asarray(y_data).reshape(-1, 1)
    return np.asarray(x_data), y_data


# This function takes in the path to a text file
# and returns the x and y data, with the features extracted
def load_dance_dance_action(text_file_path, text_file_partial_path, sampling_rate, window_length):
    lookup = {"dumbbells.txt": 1, "face_wipe.txt": 2, "muscle.txt": 3, "pac_man.txt": 4,
              "shooting_star.txt": 5, "shout_out.txt": 6, "tornado.txt": 7, "weight_lifting.txt": 8,
              "right.txt": 9, "left.txt": 10, "nothing.txt": 11}

    num_data_points = int(sampling_rate * window_length)
    x_partial_data_raw = []
    x_partial_data = []
    with open(text_file_path, "r") as data_file:
        for row in data_file:
            string_split = row.split()
            string_split = list(map(float, string_split))
            assert len(string_split) == 3
            assert type(isinstance(string_split[0], float))
            assert type(isinstance(string_split[1], float))
            assert type(isinstance(string_split[2], float))
            # string_split = normalize(string_split)
            x_partial_data_raw.append(string_split)
    # Extract features
    # Calculate the number of data points in one window
    num_data_points_per_window = int(sampling_rate * window_length)
    # Calculate the number of windows. It is multiplied by 2 beacuse of the 50% overlap
    number_of_windows = len(x_partial_data_raw)//num_data_points*2-1
    for i in range(number_of_windows):
        window_slice_raw = []
        for ii in range(num_data_points_per_window):
            # Add num_data_points_per_window data points to window_slice_raw
            window_slice_raw.append(x_partial_data_raw[i*num_data_points_per_window//2 + ii])
        # Format window_slice_raw and extract the features
        window_slice_raw = np.asarray(window_slice_raw)[:, 0:3].tolist()
        window_slice_features = extract_features(window_slice_raw)
        x_partial_data.append(window_slice_features)
    y_partial_data = np.full(len(x_partial_data), lookup[text_file_partial_path])
    return x_partial_data, y_partial_data
