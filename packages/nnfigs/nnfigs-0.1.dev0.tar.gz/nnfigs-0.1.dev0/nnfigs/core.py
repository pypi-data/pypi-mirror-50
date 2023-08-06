#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Neural Network Figures

# The MIT License
#
# Copyright (c) 2017 Jeremie DECOCK (http://www.jdhp.org)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
import matplotlib.lines as mlines


def init_figure(size_x=10, size_y=5):
    fig, ax = plt.subplots(figsize=(size_x, size_y))
    ax.set_axis_off()
    ax.axis('equal')
    ax.set_xlim(-10, 20)   # TODO
    return fig, ax

def draw_neuron(axis,
                center,
                radius,
                fill_color='w',
                line_color='k',
                line_width=1,
                empty=False,
                ag_func=None,
                tr_func=None):

    #circle = plt.Circle(center, radius, fill=True, color=fill_color, alpha=0)
    #axis.add_artist(circle)

    circle = mpatches.Circle(center,
                            radius=radius,
                            fill=True,
                            edgecolor=line_color,
                            facecolor=fill_color)
    circle.set_zorder(20)  # put the circle on top
    axis.add_patch(circle)

    #circle = plt.Circle(center, radius, fill=False, color=line_color)
    #ax.add_artist(circle)

    x = center[0]
    y = center[1]

    if not empty:
        line = mlines.Line2D([x, x],
                             [y - radius + 0.05, y + radius - 0.05],
                             lw=line_width,
                             color=line_color)
        line.set_zorder(21)
        axis.add_line(line)

    # Agregation function ######################

    if not empty and ag_func == "sum":
        line = mlines.Line2D([x - radius/4., x - 3 * radius/4., x - radius/2., x - 3. * radius/4., x - radius/4.],
                             [y + radius/4., y + radius/4., y, y - radius/4., y - radius/4.],
                             lw=line_width,
                             color=line_color)
        line.set_zorder(21)
        axis.add_line(line)

    # Transition function ######################

    if not empty and tr_func == "linear":
        line = mlines.Line2D([x + radius/4., x + 3. * radius/4.],
                             [y - radius/4., y + radius/4.],
                             lw=line_width,
                             color=line_color)
        line.set_zorder(21)
        axis.add_line(line)
    elif not empty and tr_func == "logistic":
        line = mlines.Line2D([x + radius/4., x + radius/2., x + radius/2., x + 3. * radius/4.],
                             [y - radius/4., y - radius/4., y + radius/4., y + radius/4.],
                             lw=line_width,
                             color=line_color)
        line.set_zorder(21)
        axis.add_line(line)
    elif not empty and tr_func == "sigmoid":
        arc1 = mpatches.Arc((x + 1. * radius/4., y),
                               radius/2.,
                               radius/2.,
                               0,
                               -90,
                               0,
                               ec=line_color,
                               lw=line_width,
                               fill=False)
        arc2 = mpatches.Arc((x + 3. * radius/4., y),
                               radius/2.,
                               radius/2.,
                               0,
                               90,
                               180,
                               ec=line_color,
                               lw=line_width,
                               fill=False)

        arc1.set_zorder(21)
        arc2.set_zorder(21)

        axis.add_patch(arc1)
        axis.add_patch(arc2)


def draw_synapse(axis, p1, p2, color='k', line_width=1, label="", label_position=0.25, label_offset_y=0.3, fontsize=12):
    line = mlines.Line2D([p1[0], p2[0]],
                         [p1[1], p2[1]],
                         lw=line_width,
                         color=color)
    line.set_zorder(10)
    axis.add_line(line)

    plt.text(x=p1[0] + label_position * (p2[0]-p1[0]),
             y=p1[1] + label_position * (p2[1]-p1[1]) + label_offset_y,
             s=label,
             fontsize=fontsize)


def draw_neural_network():
    # Example
    fig, ax = init_figure()

    draw_synapse(ax, (-2, -6), (0, -6), label=r"$x_4$", label_position=0)
    draw_synapse(ax, (-2, -2), (0, -2), label=r"$x_3$", label_position=0)
    draw_synapse(ax, (-2,  2), (0,  2), label=r"$x_2$", label_position=0)
    draw_synapse(ax, (-2,  6), (0,  6), label=r"$x_1$", label_position=0)

    draw_synapse(ax, (0, -6), (10, 0), label=r"$w_4$", label_offset_y=-0.7)
    draw_synapse(ax, (0, -2), (10, 0), label=r"$w_3$", label_offset_y=-0.7)
    draw_synapse(ax, (0, 2),  (10, 0), label=r"$w_2$")
    draw_synapse(ax, (0, 6),  (10, 0), label=r"$w_1$")

    draw_synapse(ax, (10, 0), (12, 0), label_position=0.8, label=r"$y$")

    draw_neuron(ax, (0, -6), 1, tr_func="logistic")
    draw_neuron(ax, (0, -2), 1, tr_func="logistic")
    draw_neuron(ax, (0, 2),  1, tr_func="logistic")
    draw_neuron(ax, (0, 6),  1, tr_func="logistic")

    draw_neuron(ax, (10, 0), 1, ag_func="sum", tr_func="logistic")

    return fig, ax


def main():
    # Example
    fig, ax = init_figure()

    draw_synapse(ax, (-2, -6), (0, -6), label=r"$x_4$", label_position=0)
    draw_synapse(ax, (-2, -2), (0, -2), label=r"$x_3$", label_position=0)
    draw_synapse(ax, (-2,  2), (0,  2), label=r"$x_2$", label_position=0)
    draw_synapse(ax, (-2,  6), (0,  6), label=r"$x_1$", label_position=0)

    draw_synapse(ax, (0, -6), (10, 0), label=r"$w_4$", label_offset_y=-0.7)
    draw_synapse(ax, (0, -2), (10, 0), label=r"$w_3$", label_offset_y=-0.7)
    draw_synapse(ax, (0, 2),  (10, 0), label=r"$w_2$")
    draw_synapse(ax, (0, 6),  (10, 0), label=r"$w_1$")

    draw_synapse(ax, (10, 0), (12, 0), label_position=0.8, label=r"$y$")

    draw_neuron(ax, (0, -6), 1, tr_func="logistic")
    draw_neuron(ax, (0, -2), 1, tr_func="logistic")
    draw_neuron(ax, (0, 2),  1, tr_func="logistic")
    draw_neuron(ax, (0, 6),  1, tr_func="logistic")

    draw_neuron(ax, (10, 0), 1, ag_func="sum", tr_func="logistic")

    plt.show()

if __name__ == '__main__':
    main()

