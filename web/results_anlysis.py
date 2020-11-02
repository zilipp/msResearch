from datetime import datetime
import numpy
import pandas as pd
import os
from pathlib import Path

from core_alg.base import Bone


# default directory path
_out_root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
_user_result_dir = os.path.join(_out_root_dir, 'out', 'core_alg', 'results')

# user assign a file name in output
# type of bone
# true value of bone
name = '2020-10-13-15-37-12-femur.csv'
bone_type = Bone.Type.FEMUR


fbml = 439.2
feb = 81.2
fhd = 46.8
fml = 442.0
fmld = 26.8
femur_true_values = [fbml, feb, fhd, fml, fmld]

heb = 63.8
hhd = 46.5
hml = 304.0
humerus_true_values = [heb, hhd, hml]

rml = 237.5
rmld = 16.1
radius_true_values = [rml, rmld]

tml = 352.0
tpb = 77.0
tibia_true_values = [tml, tpb]


def read_file(name):
    file_name = os.path.join(_user_result_dir, name)
    df = pd.read_csv(file_name, index_col=None)
    return df


def analysis_femur(input_array, number_bone, number_measurements):
    # abs: |measure - true|
    # scale: |measure - true| / true
    abs_avg_res = []
    abs_std_res = []
    scale_avg_res = []
    scale_std_res = []
    for i in range(number_measurements):
        abs_errors = []
        scale_errors = []

        for j in range(number_bone):
            abs_errors.append(abs(input_array[j][i] - femur_true_values[i]))
            scale_errors.append(abs(input_array[j][i] - femur_true_values[i]) / femur_true_values[i])

        abs_errors_mean = sum(abs_errors) / len(abs_errors)
        abs_variance = sum([((x - abs_errors_mean) ** 2) for x in abs_errors]) / len(abs_errors)
        abs_stdev = abs_variance ** 0.5
        abs_avg_res.append(abs_errors_mean)
        abs_std_res.append(abs_stdev)

        sca_errors_mean = sum(scale_errors) / len(scale_errors)
        sca_variance = sum([((x - sca_errors_mean) ** 2) for x in scale_errors]) / len(scale_errors)
        sca_stdev = sca_variance ** 0.5
        scale_avg_res.append(sca_errors_mean)
        scale_std_res.append(sca_stdev)

    return abs_avg_res, abs_std_res, scale_avg_res, scale_std_res


def analysis_tibia(input_array, number_bone, number_measurements):
    # |measure - true|
    res = []
    for i in range(number_measurements):
        sum = 0
        for j in range(number_bone):
            sum += abs(input_array[j][i] - tibia_true_values[i])

        avg = sum / number_bone
        res.append(avg)
    return res


def analysis_humerus(input_array, number_bone, number_measurements):
    # |measure - true|
    res = []
    for i in range(number_measurements):
        sum = 0
        for j in range(number_bone):
            sum += abs(input_array[j][i] - humerus_true_values[i])

        avg = sum / number_bone
        res.append(avg)
    return res


def analysis_radius(input_array, number_bone, number_measurements):
    # |measure - true|
    res = []
    for i in range(number_measurements):
        sum = 0
        for j in range(number_bone):
            sum += abs(input_array[j][i] - radius_true_values[i])

        avg = sum / number_bone
        res.append(avg)
    return res


if __name__ == "__main__":
    df = read_file(name)
    print(df)
    two_d_array = df.to_numpy()

    # rows
    number_bone = two_d_array.shape[0]
    # columns
    number_measurements = two_d_array.shape[1]

    abs_res = []
    scale_res = []
    if bone_type == Bone.Type.FEMUR:
        abs_avg_res, abs_std_res, scale_avg_res, scale_std_res = analysis_femur(two_d_array, number_bone, number_measurements)
    elif bone_type == Bone.Type.HUMERUS:
        res = analysis_humerus(two_d_array, number_bone, number_measurements)
    elif bone_type == Bone.Type.RADIUS:
        res = analysis_radius(two_d_array, number_bone, number_measurements)
    elif bone_type == Bone.Type.TIBIA:
        res = analysis_tibia(two_d_array, number_bone, number_measurements)

    to_append = abs_avg_res
    df_length = len(df)
    df.loc[df_length] = to_append

    to_append = abs_std_res
    df_length = len(df)
    df.loc[df_length] = to_append

    to_append = scale_avg_res
    df_length = len(df)
    df.loc[df_length] = to_append

    to_append = scale_std_res
    df_length = len(df)
    df.loc[df_length] = to_append

    print(df)
