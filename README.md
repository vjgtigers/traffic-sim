# Dependencies

SUMO 1.25.0


# Installation / Setup

First, install SUMO. The easiest way to use SUMO is with a python virtual environment:

```
$ git clone git@github.com:vjgtigers/traffic-sim.git
$ cd traffic-sim
$ python -m venv venv
$ source venv/bin/activate
# note: may be need to run $ ./venv/bin/activate.bat on windows
$ pip3 install eclipse-sumo
```

Next, prior to running you must set the `SUMO_BIN` enviorment variable to the location the SUMO executable file.
On linux, using a virtual environment this looks like

```
export SUMO_BIN=$(pwd)/venv/bin/sumo-gui
# or, for no GUI...
export SUMO_BIN=$(pwd)/venv/bin/sumo
```

Next you may run either of the scenarios using

```
$ python3 closeReroute.py
# or 
$ python3 rerouteImmediately.py
```

The python script will prompt you to close the roads. Close the roads in the SUMO-GUI, then
continue in the script by pressing enter

# Scenariso

Two scenarios are defined:

- `closeReroute.py` - This scenario defines driving where the route information is not known ahead of time. I.e., the AV routes through the crash and has to u-turn and reroute.
- `rerouteImmediately.py` - This scenario reflects knowledge sharing that allows AVs to automatically reroute for the road-closure (crash, etc)
- Base simulation - Simply run the map.sumocfg without either python script to simulate the network under normal conditions as a baseline.
    - You may also simulate the road closure in SUMO by manually closing the roads and continueing w/o any rerouting script. This would simulate no intelligence.

----

if you run sumo with the command sumo-gui -c map.sumocfg --remote-port 13333 --start --fcd-output <file name>.xml --device.fcd.period 1.0

this will provide a file of data from the simulation, the avgSpeedCalculation.py can be used to extract a .csv file of the avg speed at each period
ex usage: python avgSpeedCalculation.py <file name>.xml -o "<output file name>.csv"

i havent experimented with collecting other data other than what that program gets.
the avg speed with just the rerouting when getting close basically brings it back up to almost the regular speed without any accident, so thats why i want to 
implement some sort of slowing down the cars when they get close to make it a bit more noticable

but we should try to find some other data we can also get that will show more
