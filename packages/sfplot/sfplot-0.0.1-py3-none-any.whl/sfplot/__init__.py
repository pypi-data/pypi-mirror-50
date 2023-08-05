# -*- coding:utf-8 -*-
__version__ = '0.0.1'

from sfplot.search_from_boxplot import SearchFromBoxplot
from sfplot.search_from_scatter import SearchFromScatter

CANVAS_SIZE_X = 600
CANVAS_SIZE_Y = 600
DPI = 100

scatter = SearchFromScatter(CANVAS_SIZE_X, CANVAS_SIZE_Y, DPI)
boxplot = SearchFromBoxplot(CANVAS_SIZE_X, CANVAS_SIZE_Y, DPI)
