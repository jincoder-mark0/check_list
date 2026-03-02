import re

line = "| DESIGN_001                                                                                |                                                                      (top) |      37174 |      34634 |    1784 |  756 | 37601 |     52 |    110 |          133 |"
pat_hier = re.compile(r'\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|')

match = pat_hier.search(line)
if match:
    print("Matched!")
    for i, g in enumerate(match.groups()):
        print(f"Group {i+1}: {g}")
else:
    print("Not matched!")
