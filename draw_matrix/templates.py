CELL_HTML = """
<TD {params}>{value}</TD>
"""

ROW_HTML = """
<TR {params}>
{children}
</TR>
"""

NODE_HTML = """
    {nodename} [{args}label=<
    {child}
  >]
"""


TABLE_HTML = """
<TABLE {params}>
  {children}
</TABLE>
"""
