import xml.etree.ElementTree as ET
import argparse
import statistics
import pandas as pd
from scipy.stats import ttest_ind

parser = argparse.ArgumentParser(
        prog='tripinfo statistic calculator',
        description='tripinfo statistic calculator')
parser.add_argument('filename')

args = parser.parse_args()

tree = ET.parse(args.filename)
root = tree.getroot()

durationsNormal = []
durationsAV = []
for tripinfo in root.findall('tripinfo'):
    if int(tripinfo.get('id')) % 3 == 0:
        duration = float(tripinfo.get('duration'))
        durationsAV.append(duration)
    else:
        duration = float(tripinfo.get('duration'))
        durationsNormal.append(duration)
       



meanAV = statistics.mean(durationsAV)
meanNormal = statistics.mean(durationsNormal)



t_stat, p_value = ttest_ind(durationsAV,durationsNormal, equal_var=False)

print(f"Normal Mean: {meanNormal:.2f}, AV Mean: {meanAV:.2f}")
print(f"t-statistic: {t_stat:.2f}")
print(f"p-value: {p_value:.2e}")
