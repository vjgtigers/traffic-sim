import os,sys, time, traceback, traci, random, argparse
from watchers import EdgeEntryWatcher
from utility import get_unique_filename

rerouteTimes = {}
def addToRerouteQueue(simStep, vehs):
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
    conn.vehicle.rerouteTraveltime(veh)
    print(f"rerouting {veh}")
            
            
def vehicleRerouter(conn, veh):
    for vid in veh:
        conn.vehicle.rerouteTraveltime(vid)
        print(f"rerouting {vid}")

def disallowEdges(conn):
    print("entering disallow edges function")
    edges = ["301325216#0", "-301325216#0"]
    for i in edges:
        conn.edge.setMaxSpeed(i,1)
    print("crash simulated")

hasBeenRerouted = {}
def rerouteEveryVehOnDepart(conn, simStep):
    departed = conn.simulation.getDepartedIDList()
    for vid in departed:
        isDeparted = hasBeenRerouted.get(vid)
        if isDeparted is None:
            hasBeenRerouted[vid] = "rerouted"
            conn.vehicle.rerouteTraveltime(vid)

            print(f"[step {simStep}] {vid} has entered sim, being rerouted")


def main(args):
    traci.start([os.environ["SUMO_BIN"],
             "-c", os.getcwd()+"/map.sumocfg",
             "--start",
             "--edgedata-output",get_unique_filename("data/edges.xml"),
             "--fcd-output", get_unique_filename("data/fcd.xml"),
             "--netstate-dump", get_unique_filename("data/dump.xml")
            ])
    print("Connected to SUMO")

    closedEdges = ["-301325216#1", "301327121#12", "19317061#16", "19318601#13", "19317061#17"]
    edgeWatchers = [EdgeEntryWatcher(edge, seed_from_simulation=True) for edge in closedEdges]

    traci.simulationStep()
    disallowEdges(traci)
    if not args.no_wait:
        x = input("Waiting for user, press enter to continue...")
    step = 1
    while step < 60000:
        traci.simulationStep()
        if(args.knowledge_sharing):
            rerouteEveryVehOnDepart(traci, step)
        else:
            for watcher in edgeWatchers:
                """
                Iterate through each of the edge watchers, and track vehicles that have entered
                the selected edges 
                """
                vehiclesOnEdge = watcher.check(traci)
                for vID in vehiclesOnEdge:
                    print(f'[step {step}] {vID} entered {watcher.edge_id}')
                addToRerouteQueue(step, vehiclesOnEdge)
            delayedReroute(traci,step)
        if(args.gui):
            time.sleep(0.01) # small delay for GUI updates
        step += 1

    traci.close()

parser = argparse.ArgumentParser(description="Simulate BGSU campus with a crash on wooster")
parser.add_argument("--knowledge-sharing", "-k", action="store_true", help="Enable knowledge sharing scenario")
parser.add_argument("--gui", "-g", action="store_true", help="enable for GUI updates if using sumo-gui")
parser.add_argument("--no-wait", "-n", action="store_true", help="Automatically start without waiting on user")
args = parser.parse_args()

if __name__ == "__main__":
    if os.getenv("SUMO_BIN")==None:
        raise Exception("SUMO_BIN environment variable must be set")
    main(args)
