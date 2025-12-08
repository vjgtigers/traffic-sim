# connect_diagnostic.py
import os, sys, time, traceback

# Set this to the port you started SUMO-GUI with
PORT = 13333

if "SUMO_HOME" not in os.environ:
    raise RuntimeError("Please set SUMO_HOME to your SUMO installation directory")

sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
import traci


import random


import traceback
import traci


import sumolib
import networkx as nx

net = sumolib.net.readNet("./sumoFiles/map.net.xml")
G_base = nx.DiGraph()

for edge in net.getEdges():
    u = edge.getFromNode().getID()
    v = edge.getToNode().getID()
    base_cost = edge.getLength() / max(edge.getSpeed(), 0.1)
    G_base.add_edge(u, v,
                    base_cost=base_cost,
                    edge_id=edge.getID())
















class EdgeEntryWatcher:
    """
    Watch a SUMO edge and report vehicles that *entered* since the last check.
    Usage: create one watcher per watched edge and call .check() after each traci.simulationStep().
    """
    def __init__(self, edge_id: str, seed_from_simulation: bool = False):
        """
        edge_id: SUMO edge id to watch
        seed_from_simulation: if True, initializes the internal 'previous' set to the current vehicles
                              on the edge so vehicles already on the edge are NOT reported as 'new'
                              on the first check. If False, the first check will report all present vehicles.
        """
        self.edge_id = edge_id
        if seed_from_simulation:
            try:
                self.prev_on_edge = set(traci.edge.getLastStepVehicleIDs(self.edge_id))
            except Exception:
                # if traci not connected yet or edge unknown, start empty
                self.prev_on_edge = set()
        else:
            self.prev_on_edge = set()

    def check(self, conn):
        """
        Call this once per simulation step (after traci.simulationStep()).
        Returns a list of vehicle ids that entered the edge since the last check.
        """
        current_on_edge = set(conn.edge.getLastStepVehicleIDs(self.edge_id))
        newly_entered = list(current_on_edge - self.prev_on_edge)
        self.prev_on_edge = current_on_edge
        return newly_entered

    def check_and_notify(self, callback):
        """
        Same as check(), but calls callback(veh_id) for each newly-entered vehicle.
        Returns the list of newly-entered vehicle ids.
        """
        newly = self.check()
        for vid in newly:
            callback(vid)
        return newly








def disallowEdges(conn):
    print("entering disallow edges function")

    types = conn.vehicletype.getIDList()  # list of vehicle type ids in the simulation
    disallowed = list(types)
    ALL_CLASSES = ["passenger", "truck", "bus", "motorcycle", "bicycle", "coach"]

    edges = ["301325216#0", "-301325216#0"]
    for i in edges:
        conn.edge.setDisallowed(i,ALL_CLASSES)
    print("edges blocked")


rerouteTimes = {}

def addToRerouteQueue(simStep, vehs):
    for i in vehs:
        rerouteTimes[i] = simStep+200
        print(f"[step {simStep}] {i} added to reroute queue")

def delayedReroute(conn, simStep):
    for vid in rerouteTimes:
        if rerouteTimes[vid] == simStep:
            try:
                indivehRerouter(conn, vid)
                print(f"[step {simStep}] {vid} delayReroute")
            except:
                print(f"[step {simStep}] {vid} doesnt exist, cant reroute")
def indivehRerouter(conn, veh):
    conn.vehicle.rerouteTraveltime(veh)
    print(f"rerouting {veh}")


def vehicleRerouter(conn, veh):
    for vid in veh:
        conn.vehicle.rerouteTraveltime(vid)
        print(f"rerouting {vid}")

def deleteDifficultVehicles(conn):
    vids = ["338"]

    departed = conn.simulation.getDepartedIDList()
    for vid in departed:
        if vid in vids:
            print(f"FOUND ROAD IDDDDDDDDDDDDDDDDDDDDD {conn.vehicle.getRoadID(vid)}")
            conn.vehicle.remove(vid)


hasBeenRerouted = {}

def rerouteEveryVehOnDepart(conn, simStep):
    departed = conn.simulation.getDepartedIDList()
    for vid in departed:
        isDeparted = hasBeenRerouted.get(vid)
        if isDeparted is None:
            hasBeenRerouted[vid] = "rerouted"
            conn.vehicle.rerouteTraveltime(vid)

            print(f"[step {simStep}] {vid} has entered sim, being rerouted")



def main():
    print("Attempting traci.connect(port={}) ...".format(PORT))
    try:
        # Some versions of traci return a connection object from connect(), some don't.
        conn = traci.connect(port=PORT)
    except Exception as e:
        print("traci.connect() raised:", repr(e))
        traceback.print_exc()
        return

    # If connect() returned None, fetch the active connection object explicitly.
    try:
        if conn is None:
            conn = traci.getConnection()
    except Exception as e:
        print("Could not get connection object with traci.getConnection():", repr(e))
        traceback.print_exc()
        return

    print("Connected — connection object:", conn)
    #manager = SpawnManager(conn, spawn_per_step=4, max_total=None, route_len=6, depart_pos="base")
    #watcher = EdgeEntryWatcher("301325216#0", seed_from_simulation=True)
    #watcher = EdgeEntryWatcher("-301325216#1", seed_from_simulation=True)
    #watcher2 = EdgeEntryWatcher("-301325216#0", seed_from_simulation=True)
    #watcher2 = EdgeEntryWatcher("301327121#12", seed_from_simulation=True)

    approachClose_ids = ["-301325216#1", "301327121#12", "19317061#16", "19318601#13", "19317061#17"]
    watchers = [EdgeEntryWatcher(edges, seed_from_simulation=True) for edges in approachClose_ids]
    checkWatchers = False
    # Do a small, safe probe before stepping
    try:
        # Try a lightweight query that verifies the server is responsive.
        # Use traci API via the connection object where possible.
        # The following call may raise FatalTraCIError if the connection dies.
        print("Querying simulation min expected vehicle count ...")
        n = conn.simulation.getMinExpectedNumber()
        print("Min expected vehicles:", n)
    except Exception as e:
        print("Lightweight probe failed:", type(e), e)
        traceback.print_exc()
        try:
            conn.close()
        except Exception:
            pass
        return
    conn.simulation.writeMessage("Python connected to SUMO, beginning simulation")


    # Now try stepping repeatedly and report exactly when/why it fails.
    try:
        for step in range(6000):
            try:
                if step == 0:

                    x = input("please continue")
                    #disallowEdges(conn)
                conn.simulationStep()
                if checkWatchers:
                    for w in watchers:
                        entries = w.check(conn)
                        for vid in entries:
                            print(f"[step {step}] {vid} entered {w.edge_id}")
                        ##vehicleRerouter(conn, entries)
                        addToRerouteQueue(step, entries)
                    #deleteDifficultVehicles(conn)
                    delayedReroute(conn, step)

                rerouteEveryVehOnDepart(conn, step)


            except Exception as e:
                print("simulationStep() failed at step", step, "->", type(e), e)
                raise
            # small sleep so GUI updates visibly
            time.sleep(0.01)
    except Exception:
        print("Exiting after simulationStep failure.")
    finally:
        try:
            conn.close()
            print("Closed connection cleanly.")
        except Exception:
            pass

if __name__ == "__main__":
    main()
