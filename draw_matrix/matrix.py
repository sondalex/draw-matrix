from typing import List, Union
from draw_matrix.templates import CELL_HTML, ROW_HTML, NODE_HTML, TABLE_HTML
import numpy as np


def _parse_params(
    width: Union[int, None],
    height: Union[int, None],
    cellborder: Union[int, None],
    cellspacing: Union[int, None],
    bgcolor: Union[str, None],
    port: Union[str, None],
    fixedsize: bool,
) -> str:
    template = '{varname}="{value}"'
    width_str = ""
    height_str = ""
    cellborder_str = ""
    cellspacing_str = ""
    bgcolor_str = ""
    port_str = ""
    if height is not None:
        height_str = template.format(varname="HEIGHT", value=height)
    if width is not None:
        width_str = template.format(varname="WIDTH", value=width)
    if cellborder is not None:
        cellborder_str = template.format(varname="cellborder".upper(), value=cellborder)
    if cellspacing is not None:
        cellspacing_str = template.format(
            varname="cellspacing".upper(), value=cellspacing
        )
    if bgcolor is not None:
        bgcolor_str = template.format(varname="bgcolor".upper(), value=bgcolor)
    if port is not None:
        port_str = template.format(varname="port".upper(), value=port)
    fixed_size_str = template.format(
        varname="FIXEDSIZE", value=str(bool(fixedsize)).upper()
    )
    return " ".join(
        [
            height_str,
            width_str,
            cellborder_str,
            cellspacing_str,
            bgcolor_str,
            port_str,
            fixed_size_str,
        ]
    )


class Cell:
    def __init__(
        self,
        value,
        port: Union[str, None] = None,
        width: Union[int, None] = None,
        height: Union[int, None] = None,
        cellborder: Union[int, None] = None,
        cellspacing: Union[int, None] = None,
        fixedsize: bool = True,
    ):
        self.value = value
        self.params = _parse_params(
            width,
            height,
            cellborder,
            cellspacing,
            bgcolor=None,
            port=port,
            fixedsize=fixedsize,
        )

    def __str__(self):
        return CELL_HTML.format(params=self.params, value=self.value)


class Row:
    def __init__(
        self,
        cells: np.array,
        port: str,
        width: Union[int, None] = None,
        height: Union[int, None] = None,
        rel_to_cell: bool = False,
        fixedsize: bool = True,
        p_cellspacing: Union[int, None] = None,
    ):
        ncol = cells.shape[0]
        cell_width = width

        if rel_to_cell is True:
            # priority
            cell_width = width * ncol
        if p_cellspacing is not None:
            cell_width = cell_width + p_cellspacing * ncol

        self.children = [
            Cell(value=value, port=port + str(i), width=width, height=height)
            for i, value in enumerate(cells)
        ]

        self.params = _parse_params(
            cell_width, height, None, None, bgcolor=None, port=None, fixedsize=fixedsize
        )

    def __str__(self):
        return ROW_HTML.format(
            params=self.params,
            children="".join(child.__str__() for child in self.children),
        )


class Table:
    def __init__(
        self,
        rows: np.matrix,
        width: Union[int, None] = None,
        rel_to_cell: bool = False,
        height: Union[int, None] = None,
        cellborder: Union[int, None] = None,
        cellspacing: Union[int, None] = None,
        bgcolor: Union[str, None] = None,
        port: Union[str, None] = None,
        fixedsize: bool = True,
    ):
        nrow, ncol = rows.shape
        cell_width = width
        cell_height = height
        if cellborder is None:
            cellborder = 0
        if rel_to_cell is True:
            # priority
            cell_width = width * ncol
            cell_height = height * nrow
        cell_width = cell_width + cellborder * ncol
        cell_height = cell_height + cellborder * ncol
        self.children = [
            Row(
                cells=row,
                width=width,
                height=height,
                port=port,
                rel_to_cell=rel_to_cell,
                p_cellspacing=cellborder,
            )
            for row in rows
        ]
        self.params = _parse_params(
            cell_width,
            cell_height,
            cellborder,
            cellspacing,
            bgcolor,
            port=None,
            fixedsize=fixedsize,
        )

    def __str__(self):
        return TABLE_HTML.format(
            params=self.params,
            children="".join([row.__str__() for row in self.children]),
        )


class Node:
    def __init__(
        self,
        nodename: str,
        child,
        width: Union[int, None] = None,
        height: Union[int, None] = None,
        cellborder: Union[int, None] = None,
        cellspacing: Union[int, None] = None,
        fontsize: Union[str, None] = None,
    ):
        self.nodename = nodename
        self.child = child
        params = ""
        if fontsize is not None:
            params = 'fontsize="{fontsize}"'.format(fontsize=fontsize)
        self.params = params

    def __str__(self):
        args = self.params
        if self.params != "":
            args = self.params + ", "

        return NODE_HTML.format(
            nodename=self.nodename, child=self.child.__str__(), args=args
        )


class Matrix:
    """_summary_
    Example
    -------
    >>> from draw_matrix.matrix import Matrix
    >>> import numpy as np
    >>> mat = Matrix()
    >>> m = np.array([[0,1], [2, 1]])
    >>> m
            array([[0, 1],
                   [2, 1]])
    >>> mat(m)
    """

    def __init__(
        self,
        width=20,
        height=20,
        cellborder=1,
        cellspacing=0,
        bgcolor="lightpink",
        port="c",
    ):

        self.width = width
        self.height = height
        self.cellborder = cellborder
        self.cellspacing = cellspacing
        self.bgcolor = bgcolor
        self.port = port

    def __call__(self, matrix) -> str:
        table = Table(
            rows=matrix,
            width=self.width,
            height=self.height,
            cellborder=self.cellborder,
            cellspacing=self.cellspacing,
            bgcolor=self.bgcolor,
            port=self.port,
            rel_to_cell=True,
        )
        return table


class NodeMatrix:
    """
    Example
    -------
    >>> from draw_matrix.matrix import Matrix, NodeMatrix
    >>> import numpy as np
    >>> mat = Matrix()
    >>> m = np.array([[0,1], [2, 1]])
    >>> m
            array([[0, 1],
                   [2, 1]])
    >>> nm = NodeMatrix(nodename="t1")
    >>> nm(dmatrix=mat, m=m)
    """

    def __init__(self, nodename="t1", fontsize=None):
        self.nodename = nodename
        self.fontsize = fontsize

    def __call__(self, dmatrix: Matrix, matrix) -> Node:
        return Node(
            nodename=self.nodename,
            child=dmatrix(matrix),
            width=dmatrix.width,
            height=dmatrix.height,
            cellborder=dmatrix.cellborder,
            cellspacing=dmatrix.cellspacing,
            fontsize=self.fontsize,
        )
