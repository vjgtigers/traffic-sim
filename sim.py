import os,sys, time, traceback, traci, random, argparse
from watchers import EdgeEntryWatcher
from utility import get_unique_filename

rerouteTimes = {}
def addToRerouteQueue(simStep, vehs):
    """
    Asks vehicles to reroute after 50 simulation steps.
    This delay in time simulates real-world behavior where
    knowledge about the crash ahead is unkown.
    """
    for i in vehs:
        rerouteTimes[i] = simStep+50
        print(f"[step {simStep}] {i} added to reroute queue")

def delayedReroute(conn, simStep):
    for vid in rerouteTimes:
        if rerouteTimes[vid] == simStep:
            try:
                individualRerouter(conn, vid)
                print(f"[step {simStep}] {vid} delayReroute")
            except:
                print(f"[step {simStep}] {vid} doesnt exist, cant reroute")

def individualRerouter(conn, veh):
    """
    This function tells a specificed vehicle to re-perform it's routing algorithm
    """
    conn.vehicle.rerouteTraveltime(veh)
    print(f"rerouting {veh}")
            
            
def vehicleRerouter(conn, veh):
    for vid in veh:
        conn.vehicle.rerouteTraveltime(vid)
        print(f"rerouting {vid}")

def disallowEdges(conn):
    """
    This function "disallows" two edges to simulate a crash.
    It does this by setting the max speed to a low value, simulating
    the real life behavior of a crash. Upon re-route, most vehicles will
    determine that it is faster to find a route around the crash
    than go through it.
    """
    print("entering disallow edges function")
    edges = ["301325216#0", "-301325216#0"]
    for i in edges:
        conn.edge.setMaxSpeed(i,1)
    print("crash simulated")

hasBeenRerouted = {}
def rerouteEveryVehOnDepart(conn, simStep):
    """
    This function is called every simulation step, and if a vehicle
    is departing on this step it will immediately perform the
    rerouting algorithm to avoid the crash.
    """
    departed = conn.simulation.getDepartedIDList()
    for vid in departed:
        isDeparted = hasBeenRerouted.get(vid)
        if isDeparted is None:
            hasBeenRerouted[vid] = "rerouted"
            conn.vehicle.rerouteTraveltime(vid)

            print(f"[step {simStep}] {vid} has entered sim, being rerouted")

def rerouteSomeVehOnDepart(conn, simStep):
    """
    This function is called every simulation step, and if a vehicle
    is departing on this step it will immediately perform the
    rerouting algorithm to avoid the crash.
    """
    departed = conn.simulation.getDepartedIDList()
    for vid in departed:
        if(int(vid) % 3 == 0):
            isDeparted = hasBeenRerouted.get(vid)
            if isDeparted is None:
                hasBeenRerouted[vid] = "rerouted"
                conn.vehicle.rerouteTraveltime(vid)

                print(f"[step {simStep}] {vid} has entered sim, being rerouted")


def main(args):
    """
    main(args)
        args - argparse args variable

    This method contains the main logic of the script.
    """


    # Start SUMO with a TraCI connection,
    # and some command line arguments:
    traci.start([os.environ["SUMO_BIN"],
             "-c", os.getcwd()+"/map.sumocfg",
             "--start", # auto-start w/o user
                 # log output datae
             "--edgedata-output",get_unique_filename("data/edges.xml"),
             "--fcd-output", get_unique_filename("data/fcd.xml"),
             "--netstate-dump", get_unique_filename("data/dump.xml"),
             "--tripinfo-output", get_unique_filename("data/tripinfo.xml")
            ])
    print("Connected to SUMO")

    # The following edges are connected to the closed edge:
    approachEdges = ["-301325216#1", "301327121#12", "19317061#16", "19318601#13", "19317061#17"]
    # The "EdgeEntryWatcher" class lets us watch these edges, and if needed reroute cars:
    edgeWatchers = [EdgeEntryWatcher(edge, seed_from_simulation=True) for edge in approachEdges]

    # Simulate the crash via disallowEdges function:
    traci.simulationStep()
    disallowEdges(traci)

    # Wait on user (if desired)
    if not args.no_wait:
        x = input("Waiting for user, press enter to continue...")

    # Move through the simulation:
    step = 1
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        if(args.no_intelligence):
            pass
        elif(args.knowledge_sharing):
            # if the knowledge sharing scenario is enabled
            # immediately reroute every vehicle as soon as it
            # johns the simulation
            rerouteEveryVehOnDepart(traci, step)
        else:
            if(args.mixed_intelligence):
                rerouteSomeVehOnDepart(traci,step)
            # For the normal simulation scenario, each of the edge
            # watchers will look for vehicles approaching the crash.
            for watcher in edgeWatchers:
                # Iterate through each of the edge watchers, and track vehicles that have entered
                # the selected edges 
                vehiclesOnEdge = watcher.check(traci)
                for vID in vehiclesOnEdge:
                    print(f'[step {step}] {vID} entered {watcher.edge_id}')
                addToRerouteQueue(step, vehiclesOnEdge)
            delayedReroute(traci,step)

        if(args.gui):
            time.sleep(0.01) # small delay for GUI updates
        step += 1

    traci.close()

"""
argparse

Our command line arguments are defined here:
"""

parser = argparse.ArgumentParser(description="Simulate BGSU campus with a crash on wooster")
parser.add_argument("--knowledge-sharing", "-k", action="store_true", help="Enable knowledge sharing scenario")
parser.add_argument("--mixed-intelligence", "-m", action="store_true")
parser.add_argument("--no-intelligence", "-d", action="store_true", help="Disable crash-rerouting")
parser.add_argument("--gui", "-g", action="store_true", help="enable for GUI updates if using sumo-gui")
parser.add_argument("--no-wait", "-n", action="store_true", help="Automatically start without waiting on user")
args = parser.parse_args()

if __name__ == "__main__":
    if os.getenv("SUMO_BIN")==None:
        raise Exception("SUMO_BIN environment variable must be set")
    main(args)
