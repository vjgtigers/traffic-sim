import xml.etree.ElementTree as ET
import argparse
import statistics

parser = argparse.ArgumentParser(
        prog='tripinfo statistic calculator',
        description='tripinfo statistic calculator')
parser.add_argument('filename')

args = parser.parse_args()

tree = ET.parse(args.filename)
root = tree.getroot()

durations= []
for tripinfo in root.findall('tripinfo'):
    duration = float(tripinfo.get('duration'))
    durations.append(duration)

average_trip_time = statistics.mean(durations)
std_dev = statistics.stdev(durations)
print(f'Avg. Trip Time: {average_trip_time:.2f} seconds')
print(f'Std. Deviation: {std_dev:.2f}')


# Calcualte what time represents the top/bottom 10% of trip times
n = len(durations)
lower_10_index = int(n * 0.10)
upper_10_index = int(n * 0.90)

lower_10_percentile = durations[lower_10_index]
upper_10_percentile = durations[upper_10_index]

# Get the actual tail values (bottom 10% and top 10%)
bottom_10_percent = durations[:lower_10_index]
top_10_percent = durations[upper_10_index:]

print(f"\n10th percentile (lower tail): {lower_10_percentile:.2f} seconds")
print(f"90th percentile (upper tail): {upper_10_percentile:.2f} seconds")

if bottom_10_percent:
    print(f"\nBottom 10% average: {statistics.mean(bottom_10_percent):.2f} seconds")
if top_10_percent:
    print(f"Top 10% average: {statistics.mean(top_10_percent):.2f} seconds")
