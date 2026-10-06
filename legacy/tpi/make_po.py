"""Circuit.make_PO from the original code base, kept until observation point insertion
is ported (see ROADMAP). It was a method of Circuit; ``circuit`` replaces ``self``.

Known problems: the new output branch is not added to ``target.dnodes`` and the circuit is
not levelized afterwards, so it cannot be used as it is.
"""
from pycad.node.node import BRCH


def make_PO(circuit, target):
    """ connects this target node to a PO using a branch 
    """
    if target.ntype == "PO":
        return 
    # target becomes stem, create new branches:
    new_brch = BRCH("PO", "BRCH", target.num+"-IPO") 
    old_brch = BRCH("FB", "BRCH", target.num+"-OLD")

    # fixing unodes for new branches
    new_brch.unodes.append(target)
    old_brch.unodes.append(target)
    old_brch.dnodes = target.dnodes

    # fixing unodes for target.dnodes
    # if target was stem:
    if len(target.dnodes) > 1:
        for dnode in target.dnodes:
            dnode.unodes = [old_brch]
    # if target was a gate
    else:
        new_unodes = []
        for unode in target.dnodes[0].unodes:
            if unode.num != target.num:
                new_unodes.append(unode)
        new_unodes.append(old_brch)
        target.dnodes[0].unodes = new_unodes

    circuit.outputs.append(new_brch)    
    circuit.nodes[new_brch.num] = new_brch

