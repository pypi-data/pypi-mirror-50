import numpy as np
import pandas as pd
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def convert_out_of_range2min_or_max(min_value, max_value, target):
    """ 最小最大の範囲外を最小または最大に変換 """
    if target < min_value:
        return min_value
    elif max_value < target:
        return max_value
    else:
        return target


def convert_selection_range2scaling_from_to(start_point, end_point, size):
    """ 選択範囲を座標から画面全体のパーセントにスケーリングし、順序も直す """
    from_ = min([start_point, end_point]) / size
    to_   = max([start_point, end_point]) / size
    return from_, to_


def convert_drag_point2scaling_point(min_value, max_value, drag_point, drop_point):
    drag_in_range = convert_out_of_range2min_or_max(min_value, max_value, drag_point)
    drop_in_range = convert_out_of_range2min_or_max(min_value, max_value, drop_point)
    from_, to_ = convert_selection_range2scaling_from_to(drag_in_range, drop_in_range, max_value)
    return from_, to_


def convert_scaling_point2data_range(from_point, to_point, data_min, data_max):
    """ 画面全体のパーセンテージから、データの値に変換 """
    data_range_from = (data_max - data_min) * from_point + data_min
    data_range_to   = (data_max - data_min) * to_point   + data_min
    return data_range_from, data_range_to


def convert_scaling_point2index_range(from_point, to_point, data_num):
    """ 画面全体のパーセンテージから、選択されたカテゴリ値リストに変換 """
    unit_size = 1 / data_num
    data_index_from = max(int(from_point // unit_size), 0)
    data_index_to   = min(int(to_point   // unit_size), data_num-1)

    return data_index_from, data_index_to
