from spectrum import aryule
from scipy.stats import pearsonr
from scipy.stats import entropy
from math import sqrt
from numpy.fft import fft, fftfreq

import pandas as pd
import statistics
import numpy as np


def obtain_band_energy(data, start, end):
    energy = 0
    for i in range(start-1, end):
        energy += pow(data[i], 2)
    return energy


def obtain_min(data):
    return np.min(data)


def obtain_max(data):
    return np.max(data)


def fourier_transform(data):
    return np.fft.fft(data)


def obtain_mean(data):
    return statistics.mean(data)


def obtain_std(data):
    return statistics.stdev(data)


def obtain_ar_coefficients(data, burg_order):
    ar, _, _ = aryule(data, order=burg_order)
    return ar


def obtain_correlation_coefficient(data1, data2):
    corr, _ = pearsonr(data1, data2)
    return corr


# Signal magnitude area
def obtain_sma(data_x, data_y, data_z):
    sma = 0
    for i in range(len(data_x)):
        sma += abs(data_x[i]) + abs(data_y[i]) + abs(data_z[i])
    return sma


def obtain_entropy(data):
    data = pd.Series(data)
    p_data = data.value_counts()           # counts occurrence of each value
    entropy_value = entropy(p_data)  # get entropy from counts
    return entropy_value


def obtain_max_index(data):
    return np.argmax(data)


def obtain_skewness(data):
    data = pd.DataFrame(data)
    return float(data.skew())


def obtain_magnitude(data_x, data_y, data_z):
    data_magnitude = []
    for i in range(0, len(data_x)):
        magnitude = sqrt(pow(data_x[i], 2) + pow(data_y[i], 2) + pow(data_z[i], 2))
        data_magnitude.append(magnitude)
    return np.asarray(data_magnitude)


def extract_features_t_body_acc(acc_x, acc_y, acc_z):
    features = []
    features.append(obtain_mean(acc_x))
    features.append(obtain_mean(acc_y))
    features.append(obtain_mean(acc_z))
    features.append(obtain_std(acc_x))
    features.extend(obtain_ar_coefficients(acc_x, 4))
    features.extend(obtain_ar_coefficients(acc_y, 4))
    features.extend(obtain_ar_coefficients(acc_z, 4))
    features.append(obtain_correlation_coefficient(acc_x, acc_y))
    features.append(obtain_correlation_coefficient(acc_z, acc_y))
    features.append(obtain_correlation_coefficient(acc_x, acc_z))
    return features


def extract_features_t_body_acc_jerk(acc_x, acc_y, acc_z):
    features = []
    features.extend(obtain_ar_coefficients(acc_x, 4))
    features.extend(obtain_ar_coefficients(acc_y, 4))
    features.extend(obtain_ar_coefficients(acc_z, 4))
    features.append(obtain_correlation_coefficient(acc_x, acc_y))
    features.append(obtain_correlation_coefficient(acc_z, acc_y))
    features.append(obtain_correlation_coefficient(acc_x, acc_z))
    return features


def extract_features_t_body_acc_mag(acc_mag):
    features = []
    features.extend(obtain_ar_coefficients(acc_mag, 4))
    return features


def extract_features_t_body_acc_jerk_mag(acc_jerk_mag):
    features = []
    features.extend(obtain_ar_coefficients(acc_jerk_mag, 4))
    return features


def extract_features_t_gravity_acc(acc_g__x, acc_g__y, acc_g__z):
    features = []
    features.append(obtain_mean(acc_g__x))
    features.append(obtain_mean(acc_g__y))
    features.append(obtain_mean(acc_g__z))
    features.append(obtain_std(acc_g__x))
    features.append(obtain_std(acc_g__y))
    features.append(obtain_std(acc_g__z))
    features.append(obtain_sma(acc_g__x, acc_g__y, acc_g__z))
    features.append(obtain_entropy(acc_g__x))
    features.append(obtain_entropy(acc_g__y))
    features.append(obtain_entropy(acc_g__z))
    features.extend(obtain_ar_coefficients(acc_g__x, 4))
    features.extend(obtain_ar_coefficients(acc_g__y, 4))
    features.extend(obtain_ar_coefficients(acc_g__z, 4))
    features.append(obtain_correlation_coefficient(acc_g__x, acc_g__y))
    features.append(obtain_correlation_coefficient(acc_g__z, acc_g__y))
    features.append(obtain_correlation_coefficient(acc_g__x, acc_g__z))
    return features


def extract_features_t_body_gyro(gyro_x, gyro_y, gyro_z):
    features = []
    features.append(obtain_mean(gyro_x))
    features.append(obtain_mean(gyro_y))
    features.append(obtain_mean(gyro_z))
    features.append(obtain_entropy(gyro_x))
    features.append(obtain_entropy(gyro_y))
    features.append(obtain_entropy(gyro_z))
    features.extend(obtain_ar_coefficients(gyro_x, 4))
    features.extend(obtain_ar_coefficients(gyro_y, 4))
    features.extend(obtain_ar_coefficients(gyro_z, 4))
    features.append(obtain_correlation_coefficient(gyro_x, gyro_y))
    features.append(obtain_correlation_coefficient(gyro_z, gyro_y))
    features.append(obtain_correlation_coefficient(gyro_x, gyro_z))
    return features


def extract_features_t_body_gyro_jerk(gyro_jerk_x, gyro_jerk_y, gyro_jerk_z):
    features = []
    features.append(obtain_mean(gyro_jerk_x))
    features.append(obtain_mean(gyro_jerk_y))
    features.append(obtain_mean(gyro_jerk_z))
    features.extend(obtain_ar_coefficients(gyro_jerk_x, 4))
    features.extend(obtain_ar_coefficients(gyro_jerk_y, 4))
    features.extend(obtain_ar_coefficients(gyro_jerk_z, 4))
    features.append(obtain_correlation_coefficient(gyro_jerk_x, gyro_jerk_y))
    features.append(obtain_correlation_coefficient(gyro_jerk_z, gyro_jerk_y))
    features.append(obtain_correlation_coefficient(gyro_jerk_x, gyro_jerk_z))
    return features


def extract_features_t_body_gyro_mag(gyro_mag):
    features = []
    features.append(obtain_entropy(gyro_mag))
    features.extend(obtain_ar_coefficients(gyro_mag, 4))
    return features


def extract_features_t_body_gyro_jerk_mag(gyro_jerk_mag):
    features = []
    features.extend(obtain_ar_coefficients(gyro_jerk_mag, 4))
    return features


def extract_features_f_body_acc(f_body_acc_x, f_body_acc_y, f_body_acc_z):
    freqs = fftfreq(len(f_body_acc_x))
    mask = freqs >= 0
    f_body_acc_x = 2 * f_body_acc_x[mask]
    f_body_acc_y = 2 * f_body_acc_y[mask]
    f_body_acc_z = 2 * f_body_acc_z[mask]
    features = []
    features.append(obtain_min(f_body_acc_x))
    features.append(obtain_min(f_body_acc_y))
    features.append(obtain_min(f_body_acc_z))
    features.append(obtain_max_index(f_body_acc_x))
    features.append(obtain_max_index(f_body_acc_y))
    features.append(obtain_max_index(f_body_acc_z))
    features.append(obtain_mean(f_body_acc_x))
    features.append(obtain_mean(f_body_acc_y))
    features.append(obtain_mean(f_body_acc_z))
    features.append(obtain_skewness(f_body_acc_x))
    features.append(obtain_skewness(f_body_acc_y))
    features.append(obtain_skewness(f_body_acc_z))
    # features.append(obtain_band_energy(f_body_acc_x, 57, 64))
    # features.append(obtain_band_energy(f_body_acc_y, 57, 64))
    # features.append(obtain_band_energy(f_body_acc_z, 57, 64))
    return features


def extract_features_f_body_acc_jerk(f_body_acc_jerk_x, f_body_acc_jerk_y, f_body_acc_jerk_z):
    freqs = fftfreq(len(f_body_acc_jerk_x))
    mask = freqs >= 0
    f_body_acc_jerk_x = 2 * f_body_acc_jerk_x[mask]
    f_body_acc_jerk_y = 2 * f_body_acc_jerk_y[mask]
    f_body_acc_jerk_z = 2 * f_body_acc_jerk_z[mask]
    features = []
    features.append(obtain_min(f_body_acc_jerk_x))
    features.append(obtain_min(f_body_acc_jerk_y))
    features.append(obtain_min(f_body_acc_jerk_z))
    features.append(obtain_max_index(f_body_acc_jerk_x))
    features.append(obtain_max_index(f_body_acc_jerk_y))
    features.append(obtain_max_index(f_body_acc_jerk_z))
    features.append(obtain_skewness(f_body_acc_jerk_x))
    features.append(obtain_skewness(f_body_acc_jerk_y))
    features.append(obtain_skewness(f_body_acc_jerk_z))
    # features.append(obtain_band_energy(f_body_acc_jerk_x, 57, 64))
    # features.append(obtain_band_energy(f_body_acc_jerk_y, 57, 64))
    # features.append(obtain_band_energy(f_body_acc_jerk_z, 57, 64))
    return features


def extract_features_f_body_acc_mag(f_body_acc_mag):
    freqs = fftfreq(len(f_body_acc_mag))
    mask = freqs >= 0
    f_body_acc_mag = 2 * f_body_acc_mag[mask]
    features = []
    features.append(obtain_min(f_body_acc_mag))
    features.append(obtain_max_index(f_body_acc_mag))
    features.append(obtain_mean(f_body_acc_mag))
    features.append(obtain_skewness(f_body_acc_mag))
    return features


def extract_features_f_body_acc_jerk_mag(f_body_acc_jerk_mag):
    freqs = fftfreq(len(f_body_acc_jerk_mag))
    mask = freqs >= 0
    f_body_acc_jerk_mag = 2 * f_body_acc_jerk_mag[mask]
    features = []
    features.append(obtain_min(f_body_acc_jerk_mag))
    features.append(obtain_max_index(f_body_acc_jerk_mag))
    features.append(obtain_mean(f_body_acc_jerk_mag))
    features.append(obtain_skewness(f_body_acc_jerk_mag))
    return features


def extract_features_f_body_gyro(f_body_gyro_x, f_body_gyro_y, f_body_gyro_z):
    freqs = fftfreq(len(f_body_gyro_x))
    mask = freqs >= 0
    f_body_gyro_x = 2 * f_body_gyro_x[mask]
    f_body_gyro_y = 2 * f_body_gyro_y[mask]
    f_body_gyro_z = 2 * f_body_gyro_z[mask]
    features = []
    features.append(obtain_min(f_body_gyro_x))
    features.append(obtain_min(f_body_gyro_y))
    features.append(obtain_min(f_body_gyro_z))
    features.append(obtain_max_index(f_body_gyro_x))
    features.append(obtain_max_index(f_body_gyro_y))
    features.append(obtain_max_index(f_body_gyro_z))
    features.append(obtain_mean(f_body_gyro_x))
    features.append(obtain_mean(f_body_gyro_y))
    features.append(obtain_mean(f_body_gyro_z))
    features.append(obtain_skewness(f_body_gyro_x))
    features.append(obtain_skewness(f_body_gyro_y))
    features.append(obtain_skewness(f_body_gyro_z))
    # features.append(obtain_band_energy(f_body_gyro_x, 49, 56))
    # features.append(obtain_band_energy(f_body_gyro_y, 49, 56))
    # features.append(obtain_band_energy(f_body_gyro_z, 49, 56))
    return features


def extract_features_f_body_gyro_mag(f_body_gyro_mag):
    freqs = fftfreq(len(f_body_gyro_mag))
    mask = freqs >= 0
    f_body_gyro_mag = 2 * f_body_gyro_mag[mask]
    features = []
    features.append(obtain_min(f_body_gyro_mag))
    features.append(obtain_max(f_body_gyro_mag))
    features.append(obtain_max_index(f_body_gyro_mag))
    features.append(obtain_skewness(f_body_gyro_mag))
    return features


def extract_features_f_body_gyro_jerk_mag(f_body_gyro_jerk_mag):
    freqs = fftfreq(len(f_body_gyro_jerk_mag))
    mask = freqs >= 0
    f_body_gyro_jerk_mag = 2 * f_body_gyro_jerk_mag[mask]
    features = []
    features.append(obtain_max_index(f_body_gyro_jerk_mag))
    features.append(obtain_mean(f_body_gyro_jerk_mag))
    features.append(obtain_skewness(f_body_gyro_jerk_mag))
    return features


# This function takes in a 2D list of data points from one window slice
# and returns a list of the features extracted from the data points
def extract_features(two_d_data):
    # Each two_d_data gives us a ?*6 matrix
    num_points = len(two_d_data)
    two_d_data = np.asarray(two_d_data)
    two_d_data_transpose = two_d_data.T
    features = []
    # Add Acc magnitude
    acc_data_magnitude = obtain_magnitude(two_d_data_transpose[0], two_d_data_transpose[1],
                                          two_d_data_transpose[2])
    two_d_data_transpose = np.append(two_d_data_transpose, acc_data_magnitude.reshape(1, len(acc_data_magnitude)),
                                     axis=0)
    # Add Gyro magnitude
    gyro_data_magnitude = obtain_magnitude(two_d_data_transpose[3], two_d_data_transpose[4],
                                           two_d_data_transpose[5])
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     gyro_data_magnitude.reshape(1, len(gyro_data_magnitude)), axis=0)
    # Add Frequency body Acceleration
    f_body_acc_x = np.abs(fft(np.asanyarray(two_d_data_transpose[0])) / num_points)
    f_body_acc_y = np.abs(fft(np.asanyarray(two_d_data_transpose[1])) / num_points)
    f_body_acc_z = np.abs(fft(np.asanyarray(two_d_data_transpose[2])) / num_points)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_acc_x.reshape(1, len(f_body_acc_x)), axis=0)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_acc_y.reshape(1, len(f_body_acc_y)), axis=0)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_acc_z.reshape(1, len(f_body_acc_z)), axis=0)
    # Add Frequency body acceleration magnitude
    f_body_acc_magnitude = np.abs(fft(np.asanyarray(two_d_data_transpose[6])) / num_points)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_acc_magnitude.reshape(1, len(f_body_acc_magnitude)), axis=0)

    # Add Frequency body gyro
    f_body_gyro_x = np.abs(fft(np.asanyarray(two_d_data_transpose[3])) / num_points)
    f_body_gyro_y = np.abs(fft(np.asanyarray(two_d_data_transpose[4])) / num_points)
    f_body_gyro_z = np.abs(fft(np.asanyarray(two_d_data_transpose[5])) / num_points)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_gyro_x.reshape(1, len(f_body_gyro_x)), axis=0)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_gyro_y.reshape(1, len(f_body_gyro_y)), axis=0)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_gyro_z.reshape(1, len(f_body_gyro_z)), axis=0)
    # Add Frequency body gyro mag
    f_body_gyro_mag = np.abs(fft(np.asanyarray(two_d_data_transpose[7])) / num_points)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_gyro_mag.reshape(1, len(f_body_gyro_mag)), axis=0)

    # Start extracting time features
    features.extend(extract_features_t_body_acc(two_d_data_transpose[0], two_d_data_transpose[1],
                                                two_d_data_transpose[2]))
    features.extend(extract_features_t_body_acc_mag(two_d_data_transpose[6]))
    features.extend(extract_features_t_body_gyro(two_d_data_transpose[3], two_d_data_transpose[4],
                                                 two_d_data_transpose[5]))
    features.extend(extract_features_t_body_gyro_mag(two_d_data_transpose[7]))

    # Start extracting frequency features
    features.extend(extract_features_f_body_acc(two_d_data_transpose[8], two_d_data_transpose[9],
                                                two_d_data_transpose[10]))
    features.extend(extract_features_f_body_acc_mag(two_d_data_transpose[11]))

    features.extend(extract_features_f_body_gyro(two_d_data_transpose[12], two_d_data_transpose[13],
                                                 two_d_data_transpose[14]))
    features.extend(extract_features_f_body_gyro_mag(two_d_data_transpose[15]))
    return features
