run sumo from the command line with: sumo-gui -c map.sumocfg --remote-port 13333 --start
this is using sumo 1.25.0

then run the pythonConnect.py file

the simulation will not start until it connects

once it connects, it will freeze the simulation for you to close the roads.
the video i sent in the discord is the edges/roads you need to close from the sumo-gui

then go back to the python script command line and hit enter and the simulation will start running

this simulation simulates cars only turning around once they get close to the crash
depending on how much time i have to work on this, i might have the cars slow down around the area too to make the impact more noticable 

i dont have the cars rerouting from a farther distance yet 

the two other "simulations" would just be running the map.sumocfg, without connecting to the python file, just remove the --remote-port 13333
this would simulate the general enviroment without any accidents/road closures

the other "simulation" would be to close those edges right when the simulation starts and let the traffic back up
simulating no rerouting at all and letting traffic just continue to back up


----

if you run sumo with the command sumo-gui -c map.sumocfg --remote-port 13333 --start --fcd-output <file name>.xml --device.fcd.period 1.0

this will provide a file of data from the simulation, the avgSpeedCalculation.py can be used to extract a .csv file of the avg speed at each period
ex usage: python avgSpeedCalculation.py <file name>.xml -o "<output file name>.csv"

i havent experimented with collecting other data other than what that program gets.
the avg speed with just the rerouting when getting close basically brings it back up to almost the regular speed without any accident, so thats why i want to 
implement some sort of slowing down the cars when they get close to make it a bit more noticable

but we should try to find some other data we can also get that will show more