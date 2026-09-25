"""Single stuck-at faults and lists of them."""
import random


class Fault:
    """A single stuck-at fault: the net of node ``node_num`` is stuck at ``stuck_val``.

    Both values are stored as strings, e.g. ``Fault(23, 1)`` is node ``"23"``
    stuck at ``"1"``, written ``23@1``.

    Attributes
    ----------
    D_count : int
        Number of test patterns that detected the fault in a fault simulation.
    D_count_list : list
        Per-run detection counts (used by the confidence interval PPSF runs).
    """

    def __init__(self, node_num, stuck_val):
        self.node_num = str(node_num)
        self.stuck_val = str(stuck_val)
        self.D_count = 0
        self.D_count_list = []

    @classmethod
    def from_str(cls, text):
        """Parse the ``<node-num>@<stuck value>`` format."""
        num, val = text.strip().split("@")
        return cls(num, val)

    def __str__(self):
        return self.node_num + "@" + self.stuck_val

    def __repr__(self):
        return self.__str__()


class FaultList:
    """An ordered list of faults.

    Parameters
    ----------
    circuit : Circuit, optional
        Needed for ``fault_count``. A list made from a circuit alone is empty.
    fname : str, optional
        Add the faults read from this file (see ``add_file``).
    fault_list : FaultList, optional
        Add the faults of this list. The Fault objects are shared, not copied.
    fault_count : int or 'all', optional
        With a ``circuit``: ``'all'`` adds both stuck-at faults of every node,
        an integer adds that many different random faults.
    nodes : list of Node, optional
        Add both stuck-at faults of each of these nodes.
    """

    def __init__(self, circuit=None, fname=None, fault_list=None, fault_count=None, nodes=None):
        self.faults = []
        self.circuit = circuit

        if fname:
            self.add_file(fname)
        if fault_list:
            for fault in fault_list.faults:
                self.add_fault(fault)
        if fault_count is not None:
            if circuit is None:
                raise ValueError("fault_count needs a circuit")
            if fault_count == 'all':
                self.add_all()
            elif isinstance(fault_count, int):
                self.add_n_random(fault_count)
            else:
                raise ValueError(f"fault_count must be an int or 'all', not {fault_count!r}")
        if nodes:
            self.add_nodes(nodes)

    def __len__(self):
        return len(self.faults)

    def __iter__(self):
        return iter(self.faults)

    def add(self, node_num, stuck_val):
        self.faults.append(Fault(node_num, stuck_val))

    def add_fault(self, fault: Fault):
        self.faults.append(fault)

    def copy_fault(self, fault: Fault):
        """Add a new fault with the same site and the same ``D_count_list``."""
        new_f = Fault(fault.node_num, fault.stuck_val)
        new_f.D_count_list = fault.D_count_list.copy()
        self.add_fault(new_f)

    def add_str(self, fault_str):
        """Add the fault written ``<node-num>@<stuck value>``."""
        self.faults.append(Fault.from_str(fault_str))

    def add_str_list(self, faults_str_list):
        for fault in faults_str_list:
            self.add_str(fault)

    def add_node(self, node):
        """Add both stuck-at-0 and stuck-at-1 of ``node``."""
        self.add(node.num, 0)
        self.add(node.num, 1)

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_all(self):
        """Add both stuck-at faults of every node of the circuit."""
        self.add_nodes(self.circuit.nodes_lev)

    def add_n_random(self, n=1, rng=random):
        """Add ``n`` different random faults of the circuit's nodes.

        Raises
        ------
        ValueError
            If the circuit has fewer than ``n`` possible faults (two per node).
        """
        sites = [(num, val) for num in self.circuit.nodes for val in (0, 1)]
        if n > len(sites):
            raise ValueError(
                f"Cannot add {n} different faults, the circuit has only {len(sites)}")
        for num, val in rng.sample(sites, n):
            self.add(num, val)

    def faults_excluding(self, faults):
        """Strings of the faults in this list that are not in ``faults``.

        ``faults`` is a collection of Fault objects or ``<node>@<value>``
        strings. This list is not changed; the order of this list is kept.
        """
        excluded = {str(fault) for fault in faults}
        return [str(fault) for fault in self.faults if str(fault) not in excluded]

    def add_file(self, fname):
        """Add the faults of a file with one ``<node-num>@<stuck value>`` per line."""
        with open(fname) as infile:
            for line in infile:
                if line.strip():
                    self.add_str(line)

    def write_file(self, fname):
        """Write the faults, one ``<node-num>@<stuck value>`` per line."""
        with open(fname, "w") as outfile:
            for fault in self.faults:
                outfile.write(str(fault) + "\n")

    def write_file_extra(self, fname):
        """Write each fault followed by the values of its ``D_count_list``, comma separated."""
        with open(fname, "w") as outfile:
            for fault in self.faults:
                outfile.write(",".join([str(fault)] + [str(x) for x in fault.D_count_list]) + "\n")

    def calc_fc(self):
        """Fault coverage: the fraction of faults with ``D_count > 0`` (0 for an empty list)."""
        if not self.faults:
            return 0.0
        return sum(fault.D_count > 0 for fault in self.faults) / len(self.faults)

    def get_D_count(self):
        """Dict from fault string to its ``D_count``."""
        return {str(fault): fault.D_count for fault in self.faults}
