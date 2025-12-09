# Simulation

This project details a basic road-simulation around the BGSU campus area in Bowling Green, OH (USA). The project uses SUMO with python control logic (via TraCI). The project is for a simulations course CS4420.

## Authors

- Vaughn Gugger
- Andrew Humphreys

# Dependencies

- SUMO 1.25.0
- pandas

# Installation / Setup

First, install SUMO. The easiest way to use SUMO is with a python virtual environment:

```console
$ git clone git@github.com:vjgtigers/traffic-sim.git
$ cd traffic-sim
$ python -m venv venv
$ source venv/bin/activate
# note: may be need to run $ ./venv/bin/activate.bat on windows
$ pip3 install eclipse-sumo
```

Next, prior to running you must set the `SUMO_BIN` enviorment variable to the location the SUMO executable file.
On linux, using a virtual environment this looks like

```console
export SUMO_BIN=$(pwd)/venv/bin/sumo-gui
# or, for no GUI...
export SUMO_BIN=$(pwd)/venv/bin/sumo
```

Note: If you are using sumo-gui binary, you should run the simulation with the `--gui` flag (see usage below).

Next you may run either of the scenarios using

```console
$ python3 sim.py
# or 
$ python3 sim.py --knowledge-sharing
```

The python script will prompt you to press enter to continue. This allows you to perform any custom configuration in SUMO if desired. If not, simply press enter. This can by bypassed by using the `--no-wait` flag.


## General Usage

```
usage: sim.py [-h] [--knowledge-sharing] [--gui] [--no-wait]

Simulate BGSU campus with a crash on wooster

options:
  -h, --help            show this help message and exit
  --knowledge-sharing, -k
                        Enable knowledge sharing scenario
  --gui, -g             enable for GUI updates if using sumo-gui
  --no-wait, -n         Automatically start without waiting on user
```

# Scenarios

Two scenarios are defined:

- Crash Scenarios:
    - Both of the following scenarios simulate a "crash" by setting the maximum speed on a thoroughfare edge to very low. This will naturally cause traffic to back up, as routes were not planned ahead of time with this information.
    - Default - This scenario defines driving where the route information is not known ahead of time. I.e., the AV routes through the crash and has to u-turn and reroute.
    - Knowledge sharing (with `--knowledge-sharing` flag) - This scenario reflects knowledge sharing that allows AVs to automatically reroute for the road-closure (crash, etc)
- Base simulation - Simply run the map.sumocfg without either python script to simulate the network under normal conditions as a baseline.
    - You may also simulate the road closure in SUMO by manually closing the roads and continueing w/o any rerouting script. This would simulate no intelligence.
# Basic Statistics

The simulation tool will output some useful data files, i.e., `edges.xml`, and `tripinfo.xml`. The `tripStatistics.py` script is useful in computing
some basic summary statistics.

```console
$ python tripStatistics.py data/tripinfo.xml 
Avg. Trip Time: 261.49 seconds
Std. Deviation: 252.59

10th percentile (lower tail): 413.00 seconds
90th percentile (upper tail): 270.10 seconds

Bottom 10% average: 181.42 seconds
Top 10% average: 456.97 seconds

```

Additionally, you may use the `avgSpeedCalculation.py` file to extract an CSV file of the average speed at each period in the simulation.
ex usage: `python avgSpeedCalculation.py <file name>.xml -o "<output file name>.csv"`

# Data Visualization

SUMO provides many tool for this in the source code. If you installed SUMO the tradition way or compiled from source they will be packaged with it.
If not, clone the SUMO github to access the scripts:

```console
git clone git@github.com:eclipse-sumo/sumo.git
cd sumo
export SUMO_HOME=$(pwd)
```

### Heatmap of average edge speeds 

- Useful for visulization congestion

```console
$ sumo/tools/visualization/plot_net_speeds.py -c data/edges.xml -n sumoFiles/map.net.xml 
$ sumo/tools/visualization/plot_net_dump.py -n sumoFiles/map.net.xml -i data/edges.xml --measures entered,entered --default-width 1 --colormap "#0:#0000c0,.25:#404080,.5:#808080,.75:#804040,1:#c00000"

```

