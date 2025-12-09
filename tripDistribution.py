import xml.etree.ElementTree as ET
import argparse
import statistics
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
        prog='tripinfo histogram',
        description='tripinfo historgram')
parser.add_argument('filename')

args = parser.parse_args()

tree = ET.parse(args.filename)
root = tree.getroot()

durations= []
for tripinfo in root.findall('tripinfo'):
    duration = float(tripinfo.get('duration'))
    durations.append(duration)

plt.figure(figsize=(10,6))
plt.hist(durations, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
plt.xlabel("Trip Duration (s)", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.title("Trip Time Distribution", fontsize=14)
plt.grid(axis='y', alpha=0.5)
plt.show()
