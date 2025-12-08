class EdgeEntryWatcher:
    """
    Watch a SUMO edge and report vehicles that *entered* since the last check.
    Usage: create one watcher per watched edge and call .check() after each traci.simulationStep().
    """
    def __init__(self, edge_id: str, seed_from_simulation: bool=False):
        """
        edge_id: SUMO edge id to watch
        seed_from_simulation: if True, initializes the internal 'previous' set to the current vehicles
                              on the edge so vehicles already on the edge are NOT reported as 'new'
                              on the first check. If False, the first check will report all present vehicles.
        """
        self.edge_id = edge_id
        self.prev_on_edge = set()
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

