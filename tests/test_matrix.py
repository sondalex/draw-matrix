from draw_matrix.matrix import Matrix, NodeMatrix, Cell, Row, Table, Node
from graphviz import Graph, Source


def test_cell(matrix):
    value = matrix[0, 0]
    
    cell = Cell(
        value,
        port="1",
        width="20",
        height="20",
        cellborder="1",
        cellspacing="0"
    )
    str(cell)


def test_row(matrix):
    cells = matrix[0]
    row = Row(cells=cells, width="20", height="20", port="c1")
    str(row)


def test_table(matrix):
    table = Table(rows=matrix, width="20", height="20", cellborder="1", cellspacing="0", bgcolor="lightpink", port="c")
    str(table)


def test_node(matrix):
    table = Table(rows=matrix, width="20", height="20", cellborder="1", cellspacing="0", bgcolor="lightpink", port="c")
    node = Node(
        nodename="t1",
        child=table, 
        width="20",
        height="20",
        cellborder="1",
        cellspacing="0"
    )
    str(node)


def test_matrix(matrix):
    mat = Matrix()
    table = mat(matrix)
    h = Graph("table")
    h.node('tab', label="<{table}>".format(table=table.__str__()))
    h.pipe(format="dot")


def test_nodematrix(matrix):
    mat = Matrix()
    nm = NodeMatrix(nodename="t2")
    node = nm(dmatrix=mat, matrix=matrix)
    # render raw
    
    src = Source(r"digraph nodematrix {" + str(node) + r"}")
    src.pipe(format="dot")
