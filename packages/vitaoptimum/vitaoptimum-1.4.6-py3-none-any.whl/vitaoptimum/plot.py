import os
import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

from operator import sub
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
from matplotlib._png import read_png
from matplotlib.cbook import get_sample_data


class Logotype:
    ''' Class that keeps parameters of a logotype that
        should be added to different graphs.
    '''

    def __init__(self, file_path, x=0, y=0, alpha=0.5):
        my_dir = os.path.dirname(os.path.realpath(__file__))
        path = Path(os.path.join(my_dir, file_path)).resolve()
        if not path.is_file():
            raise FileNotFoundError("logo file is not found: " + file_path)
        self._file_path = path
        if x >= 0:
            self._x = x
        else:
            raise ValueError("Logo position coordinate x must be positive")

        if y >= 0:
            self._y = y
        else:
            raise ValueError("Logo position coordinate y must be positive")

        if alpha > 0 and alpha <= 1:
            self._alpha = alpha
        else:
            raise ValueError("Logo alpha value must be in (0, 1]")

    @property
    def file_path(self):
        return self._file_path

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def alpha(self):
        return self._alpha

    def add_to_3d_graph(self, range_x, range_y, ax):
        # TODO: implement 2d logo on 3d graphs
        with cbook.get_sample_data(self._file_path) as file:
            img = image.imread(file)
            xrng = plt.xlim(range_x[0], range_x[1])
            yrng = plt.ylim(range_y[0], range_y[1])
            ax.imshow(img,
                      extent=[1, 0.1, 10, 0.1],
                      origin='upper',
                      alpha=self._alpha,
                      aspect='auto')

    def add_to_2d_graph(self, fig):
        with cbook.get_sample_data(self._file_path) as file:
            img = image.imread(file)
            fig.figimage(img,
                         self._x,
                         self._y,
                         zorder=1,
                         alpha=self._alpha)


def _add_logo_2d(logo, fig):
    if logo:
        if isinstance(logo, bool):
            logo = Logotype("logo64.png", x=400, y=300, alpha=0.4)
        if isinstance(logo, Logotype):
            logo.add_to_2d_graph(fig)


def _add_logo_3d(logo, ax):
    if logo:
        raise AttributeError("Logotypes are not supported for d>1")
        logo.add_to_3d_graph(range_x, range_y, ax)


def convergence(convergence, title, logo=True, save_to=None):
    '''Plot convergence to a solution (result: 2d graph)
    '''
    fig, ax = plt.subplots()
    _add_logo_2d(logo, fig)

    ax.set_xlabel('number of function evaluations')
    ax.set_ylabel('value of function')
    ax.set_title(title)
    ax.plot(convergence, 'b', label='line')
    ax.grid()

    if save_to:
        plt.savefig(save_to, bbox_inches='tight')
    else:
        plt.show()


def fobj_2d(fobj, range_x, range_y, title, logo=True, save_to=None):
    '''Plot 2d objective function (result: 3d graph)
    '''
    step_x = abs(range_x[0] - range_x[1]) / 200
    step_y = abs(range_y[0] - range_y[1]) / 200
    x = np.arange(range_x[0], range_x[1], step_x)
    y = np.arange(range_y[0], range_y[1], step_y)
    X, Y = np.meshgrid(x, y)
    zs = np.array([fobj([x, y]) for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.grid(b=False, which='major', color='#D3D3D3', linestyle='-')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('objective function')
    ax.set_title(title)
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', antialiased=False, )
    plt.show()
    # _add_logo_3d(logo, ax)

    if save_to:
        plt.savefig(save_to, bbox_inches='tight')
    else:
        plt.show()


def fobj_1d(fobj, range_x, title, logo=True, save_to=None):
    '''Plot 1d objective function (result: 2d graph)
    '''
    fig, ax = plt.subplots()
    _add_logo_2d(logo, fig)

    ax.set_xlabel('x')
    ax.set_ylabel('objective function')
    ax.set_title(title)

    x = np.arange(range_x[0], range_x[1], 0.01)
    y = fobj(x)

    ax.plot(x, y, label='line')
    ax.grid()

    if save_to:
        plt.savefig(save_to, bbox_inches='tight')
    else:
        plt.show()


def optimum_1d(title, fobj, solution, eps, logo, save_to=None):
    '''Plot optimum area for 1d objective function (result: 2d graph)
    '''
    fig, ax = plt.subplots()
    _add_logo_2d(logo, fig)

    ax.set_xlabel('x')
    ax.set_ylabel('fobj')
    ax.set_title(title)

    x = np.arange(solution - eps, solution + eps, eps / 100)
    y = fobj(x)

    ax.grid()
    for i in range(9):
        ax.plot(solution, fobj(solution), 'ro', fillstyle='none', markersize=i)
    ax.plot(x, y, label='line')

    if save_to:
        plt.savefig(save_to, bbox_inches='tight')
    else:
        plt.show()


def optimum_2d(title, fobj, solution, eps, logo, save_to=None):
    '''Plot optimum area for 1d objective function (result: 2d graph)
    '''
    x = np.arange(solution[0] - eps, solution[0] + eps, eps / 100)
    y = np.arange(solution[1] - eps, solution[1] + eps, eps / 100)
    X, Y = np.meshgrid(x, y)
    zs = np.array([fobj([x, y]) for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.grid(b=False, which='major', color='#D3D3D3', linestyle='-')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('fobj')
    ax.set_title(title)
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', antialiased=False, )

    ax.plot([solution[0]], [solution[1]], [fobj(solution)], 'ro', markersize=7)

    plt.show()
    # _add_logo_3d(logo, ax)

    if save_to:
        plt.savefig(save_to, bbox_inches='tight')
    else:
        plt.show()
