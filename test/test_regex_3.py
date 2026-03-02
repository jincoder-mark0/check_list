import re

line = "| top_with_ddr3                                                                                |                                                                      (top) |      37174 |      34634 |    1784 |  756 | 37601 |     52 |    110 |          133 |"
# Add re.IGNORECASE to match BaseParser behavior
pat_hier = re.compile(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|', re.IGNORECASE)

match = pat_hier.search(line)
if match:
    print("Matched!")
else:
    print("Not matched!")
