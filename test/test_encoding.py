import chardet

with open(r"../post_route_revA_20260226_113801/03/Utilization.rpt", "rb") as f:
    rawdata = f.read(1000)
    print(chardet.detect(rawdata))
