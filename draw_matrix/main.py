import argparse
from draw_matrix.matrix import NodeMatrix, Matrix
import numpy as np


def gen_dot_matrix(matrix, matrix_name, width, height, embed, fontsize):
    mat = Matrix(width=width, height=height)
    node = NodeMatrix(nodename=matrix_name, fontsize=fontsize)

    text = str(node(dmatrix=mat, matrix=matrix))
    if embed is True:
        text = r" digraph matrix {" + "\n  node[shape=plaintext]" + text + r"}"

    return text


# I need matrix multiplication for proper matrix
# Which is not the case for the moment.


def cli():
    parser = argparse.ArgumentParser(
        description="Generate Two D Array dot representation - random array - The output should be embed in graph"
    )
    parser.add_argument("size", nargs=2, type=int, help="Size of random matrix")
    parser.add_argument(
        "--name",
        dest="name",
        default="t1",
        type=str,
        action="store",
        required=False,
        help="Name of matrix",
    )
    parser.add_argument(
        "--bgcolor",
        dest="bgcolor",
        default="lightpink",
        type=str,
        action="store",
        required=False,
        help="Background color",
    )
    parser.add_argument(
        "--width",
        dest="width",
        default=35,
        type=int,
        action="store",
        required=False,
        help="Width",
    )
    parser.add_argument(
        "--height",
        dest="height",
        default=35,
        type=int,
        action="store",
        required=False,
        help="Height",
    )
    parser.add_argument(
        "--embed",
        dest="embed",
        default=0,
        type=int,
        action="store",
        required=False,
        help="Whether to include the output in digraph. Practical for Unix pipe",
    )
    parser.add_argument(
        "--fontsize",
        dest="fontsize",
        default=None,
        type=str,
        action="store",
        required=False,
        help="Fontsize",
    )
    parser.add_argument(
        "--random",
        dest="random",
        default=1,
        type=int,
        action="store",
        required=False,
        help="Whether to compute random values. If set to 0 and empty array is returned",
    )
    return parser


def main():
    parser = cli()
    args = parser.parse_args()
    if bool(args.random) is True:
        matrix = np.around(np.random.uniform(0, 1, args.size), decimals=2)
    else:
        matrix = np.repeat([["" for i in range(args.size[1])]], args.size[0], 0)
    str_ = gen_dot_matrix(
        matrix=matrix,
        matrix_name=args.name,
        width=args.width,
        height=args.height,
        embed=bool(args.embed),
        fontsize=args.fontsize,
    )
    print(str_)


if __name__ == "__main__":
    main()
