# Dependencies

SUMO 1.25.0


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


# Data Collection




----

if you run sumo with the command sumo-gui -c map.sumocfg --remote-port 13333 --start --fcd-output <file name>.xml --device.fcd.period 1.0

this will provide a file of data from the simulation, the avgSpeedCalculation.py can be used to extract a .csv file of the avg speed at each period
ex usage: python avgSpeedCalculation.py <file name>.xml -o "<output file name>.csv"

i havent experimented with collecting other data other than what that program gets.
the avg speed with just the rerouting when getting close basically brings it back up to almost the regular speed without any accident, so thats why i want to 
implement some sort of slowing down the cars when they get close to make it a bit more noticable

but we should try to find some other data we can also get that will show more
