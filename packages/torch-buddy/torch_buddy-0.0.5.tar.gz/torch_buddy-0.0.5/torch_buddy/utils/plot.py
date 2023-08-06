# @Author: yican.kz
# @Date: 2019-08-02 11:41:11
# @Last Modified by:   yican.kz
# @Last Modified time: 2019-08-02 11:41:11

import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def subplots(data_for_plots, figsize=[12, 4]):
    """
        data_for_plots = [[1,2,3], [4,5,6]]
    """
    f, axes = plt.subplots(np.int(np.ceil(len(data_for_plots) / 2)), 2, figsize=figsize)
    for ax, data_for_plot in zip(axes.flat, data_for_plots):
        ax.plot(data_for_plot)
