import xml.etree.ElementTree as ET
import argparse
import statistics
import pandas as pd
from scipy.stats import ttest_ind

parser = argparse.ArgumentParser(
        prog='tripinfo statistic calculator',
        description='tripinfo statistic calculator')
parser.add_argument('fileone')
parser.add_argument('filetwo')

args = parser.parse_args()

tree = ET.parse(args.fileone)
root = tree.getroot()

tree2 = ET.parse(args.filetwo)
root2 = tree2.getroot()

durations = []
durations2 = []
for tripinfo in root.findall('tripinfo'):
    duration = float(tripinfo.get('duration'))
    durations.append(duration)

for tripinfo in root2.findall('tripinfo'):
    duration = float(tripinfo.get('duration'))
    durations2.append(duration)


t_stat, p_value = ttest_ind(durations,durations2, equal_var=False)

print(f"t-statistic: {t_stat}")
print(f"p-value: {p_value}")
