import os,sys, time, traceback, traci, random
from watchers import EdgeEntryWatcher

rerouteTimes = {}
def addToRerouteQueue(simStep, vehs):
    for i in vehs:
        rerouteTimes[i] = simStep+200
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

hasBeenRerouted = {}
def rerouteEveryVehOnDepart(conn, simStep):
    departed = conn.simulation.getDepartedIDList()
    for vid in departed:
        isDeparted = hasBeenRerouted.get(vid)
        if isDeparted is None:
            hasBeenRerouted[vid] = "rerouted"
            conn.vehicle.rerouteTraveltime(vid)

            print(f"[step {simStep}] {vid} has entered sim, being rerouted")

def disallowEdges(conn):
    print("entering disallow edges function")
    edges = ["301325216#0", "-301325216#0"]
    for i in edges:
        conn.edge.setMaxSpeed(i,1)
    print("crash simulated")


def main():
    traci.start([os.environ["SUMO_BIN"], "-c", "/home/andrew/Documents/School/FA25/CS4420/traffic-sim/map.sumocfg","--start"])
    print("Connected to SUMO")

    closedEdges = ["-301325216#1", "301327121#12", "19317061#16", "19318601#13", "19317061#17"]
    edgeWatchers = [EdgeEntryWatcher(edge, seed_from_simulation=True) for edge in closedEdges]

    traci.simulationStep()
    disallowEdges(traci)
    x = input("Waiting for user, press enter to continue...")
    step = 1
    while step < 6000:
        traci.simulationStep()
        rerouteEveryVehOnDepart(traci, step)
        time.sleep(0.01) # small delay for GUI updates
        step += 1

    traci.close()

if __name__ == "__main__":
    main()
