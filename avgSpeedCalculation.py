#!/usr/bin/env python3
"""
sumo_avg_speed.py

Read a SUMO FCD output XML file and compute the average speed per timestep.

Usage:
    python sumo_avg_speed.py input_fcd.xml
    python sumo_avg_speed.py input_fcd.xml -o avg_speeds.csv
"""

import argparse
import csv
import math
import sys
import xml.etree.ElementTree as ET

def tag_name(tag):
    """Strip namespace if present"""
    if tag is None:
        return None
    return tag.rsplit('}', 1)[-1]  # handles {ns}tag or tag

def process_fcd(input_path, output_path):
    """
    Stream-parse input_path and write average speeds per timestep to output_path.
    """
    csvfile = open(output_path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(['time', 'avg_speed_m_s', 'avg_speed_km_h', 'vehicle_count', 'total_speed_sum'])

    # Use iterparse and get the root element
    context = ET.iterparse(input_path, events=('start', 'end'))
    _, root = next(context)  # get root element

    timesteps_processed = 0
    overall_sum_speed = 0.0
    overall_count = 0
    min_avg = None
    max_avg = None

    for event, elem in context:
        name = tag_name(elem.tag)
        if event == 'end' and name == 'timestep':
            # timestep element finished; compute stats
            t = elem.attrib.get('time') or elem.attrib.get('begin') or elem.attrib.get('value')
            try:
                time_val = float(t) if t is not None else None
            except ValueError:
                time_val = t

            sum_speed = 0.0
            count = 0
            # Iterate child vehicle elements
            for child in list(elem):
                child_name = tag_name(child.tag)
                if child_name.lower() in ('vehicle', 'veh', 'car'):
                    sp = child.attrib.get('speed') or child.attrib.get('spd')
                    if sp is None:
                        continue
                    try:
                        s = float(sp)
                    except ValueError:
                        continue
                    sum_speed += s
                    count += 1

            if count > 0:
                avg_m_s = sum_speed / count
                avg_km_h = avg_m_s * 3.6
            else:
                avg_m_s = float('nan')
                avg_km_h = float('nan')

            writer.writerow([
                time_val if time_val is not None else '',
                f"{avg_m_s:.6f}" if not math.isnan(avg_m_s) else '',
                f"{avg_km_h:.6f}" if not math.isnan(avg_km_h) else '',
                count,
                f"{sum_speed:.6f}"
            ])

            # Update summary stats
            if count > 0:
                overall_sum_speed += sum_speed
                overall_count += count
                if min_avg is None or avg_m_s < min_avg:
                    min_avg = avg_m_s
                if max_avg is None or avg_m_s > max_avg:
                    max_avg = avg_m_s
            timesteps_processed += 1

            # --- MEMORY CLEANUP (fixed) ---
            # clear the element's contents
            elem.clear()
            # remove the element from the root to free memory (works if timestep is a direct child)
            try:
                root.remove(elem)
            except ValueError:
                # if it's not a direct child for some reason, ignore (elem.clear() already helps)
                pass

    csvfile.close()

    # Print a short summary
    print(f"Processed {timesteps_processed} timesteps.")
    if overall_count > 0:
        overall_avg = overall_sum_speed / overall_count
        print(f"Overall average speed (over all vehicles & timesteps): {overall_avg:.6f} m/s ({overall_avg*3.6:.6f} km/h)")
        print(f"Timestep average range (m/s): min={min_avg:.6f}, max={max_avg:.6f}")
    else:
        print("No vehicle speed data found in file.")

def main():
    parser = argparse.ArgumentParser(description="Compute average speed per timestep from SUMO FCD XML.")
    parser.add_argument('input', help='Path to SUMO FCD XML file')
    parser.add_argument('-o', '--output', help='Output CSV file (default: <input>_avg_speeds.csv)')
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output or (input_path.rsplit('.', 1)[0] + '_avg_speeds.csv')

    try:
        process_fcd(input_path, output_path)
    except FileNotFoundError:
        print(f"File not found: {input_path}", file=sys.stderr)
        sys.exit(2)
    except ET.ParseError as e:
        print(f"XML parse error: {e}", file=sys.stderr)
        sys.exit(3)

if __name__ == '__main__':
    main()
