
####################################
########## NOT TESTED AT ALL 
####################################
import os
import time
import matplotlib.pyplot as plt

import config
import utils
from circuit.circuit import Circuit
from distributions import Distribution, Normal, SkewNormal, MaxOp, SumOp, NumDist


class Circuit_SSTA(Circuit):

    def __init__(self, netlist_fname):
        super().__init__(self, netlist_fname)

    def ssta_pmf(self):
        # all gate distributions are pmf and all process is numerical on pmfs 
        for node in self.nodes_lev:
            # if int(node.num) > 10:
            #     return 
            # print("-----------------------------------------------")
            # print(node)

            # Initiate the PIs first:
            if node.ntype == "PI":
                node.dd_node = Normal(0, 1)
            elif node.ntype == "FB":
                node.dd_node = node.unodes[0].dd_node
            elif node.ntype in ["GATE", "PO"]:
                opmax = MaxOp()
                dd_node_unodes = [unode.dd_node for unode in node.unodes]
                dd_node_max = dd_node_unodes[0]
                for n in range(1, len(dd_node_unodes)):
                    dd_node_max = opmax.max_num(dd_node_max, dd_node_unodes[n])

                opsum = SumOp()
                dd_cell = self.cell_ssta[node.gtype]
                node.dd_node = opsum.sum_num(dd_cell, dd_node_max)


    def ssta_plot(self, fname, select="gate"):
        """ Saves the plot of the delay distribution of the nodes 
        It can be modified to only plot the internal gates and outputs
        
        Parameters
        ---------
        fname : str 
            output file name 
        select : string
            what nodes should be plotted
            all plots all nodes
            gate plots only gates and POs, no PI, FB
            output plots only outputs
        """
        if select not in ["gate", "all", "output"]:
            raise NameError("Error (ssta_plot): select arg is not valid")
        
        cmap = utils.get_cmap(20)
        plt.figure(figsize=(20,10))
        cnt = 0
        lines = ["-","--","-.",":"]
        linecycler = cycle(lines)

        for idx, node in enumerate(self.nodes_lev):
            if select == "output" and node.ntype != "PO":
                continue
            elif select == "gate" and node.ntype not in ["GATE", "PO"]:
                continue

            if isinstance(node.dd_node, NumDist):
                T, f_T = node.dd_node.pmf()
            elif isinstance(node.dd_node, Distribution):
                T, f_T = node.dd_node.pmf(samples=config.SAMPLES)
            else:
                print("Warning: a tuple distribution is found in circuit!")
                T = node.dd_node[0]
                f_T = node.dd_node[1]
            plt.plot(T, f_T, linewidth=3, color=cmap(cnt), \
                    alpha=0.5, linestyle=next(linecycler), label=node.num)
            cnt += 1
        
        plt.grid()
        plt.legend(loc=1, prop={'size': 10})
        # plt.xlim([-5,25])
        plt.savefig("{}".format(fname))
        plt.close()
        print("Circuit SSTA plot saved in {}".format(fname))
    

    def set_cell_ssta_delay(self, src="mcraw", tech=config.TECH, pvs=config.PVS):
        """ Reads Monte Carlo simulation results and generates ssta delay for cells 
        
        Parameters
        ----------
        src : str
            mcraw > raw data of MC simulations results
            mchist > Monte Carlo histogram, it can be filtered or cut before
            text > not implemented yet, txt file with distribution info 
        tech : str 
            the name of the technology, e.g. MOSFET_45nm_HP
        pvs : str
            process variation specifier, refer to CSM package
            e.g. vth0-N0.05_lg-N0.05_w-N0.10_toxe-N0.10_MC1000
        """ 
        cell_ssta_delay = dict()
        for node in self.nodes_lev:
            if node.ntype in ["PI", "FB"]: #TODO: delay of inputs and FB?
                node.cell_name = node.ntype
                continue
            
            cell_name = utils.get_node_gtype_fin(node) # gate name with fin 
            node.cell_name = cell_name
            if cell_name in cell_ssta_delay:
                continue
            
            # Store the delay distribution for this cell in circuit
            if src == "mchist":
                fname = tech + "_" + cell_name + "_" + pvs + "." + src 
                fname = os.path.join(config.SSTA_DATA_DIR, src + "/" + fname)
                print("Loading mchist file for {}: {}".format(cell_name, fname))
                T, h_T = utils.load_mchist(fname)
                h_T = utils.smooth_hist(h_T, 11) #TODO: mchist smooth hard-coded
                T, f_T = utils.hist2pmf(T, h_T)
                print("\tArea: {}".format(Distribution.area_pmf(T, f_T)))
                utils.plot_pmf(NumDist(T,f_T), fname=cell_name+".pdf")
                cell_ssta_delay[cell_name] = NumDist(T, f_T)
            
            elif src == "default":
                cell_ssta_delay[cell_name] = self.get_cell_delay(node.gtype)
            
            elif src == "mcraw":
                fname = tech + "_" + cell_name + "_" + pvs + "." + src 
                fname = os.path.join(config.SSTA_DATA_DIR, src + "/" + fname)
                print("Loading mcraw file for {}: {}".format(cell_name, fname))
                delays = utils.load_mcraw(fname)
                T, f_T = utils.mcraw2mchist(delays, 200, pad=3)
                f_T = utils.smooth_hist(f_T, window=5) 
                print("\tArea: {}".format(Distribution.area_pmf(T, f_T)))
                # utils.plot_pmf(NumDist(T,f_T), fname=cell_name+".pdf")
                cell_ssta_delay[cell_name] = NumDist(T, f_T)

            else:
                raise NameError("WRONG VALUES -- still developing")
        self.cell_ssta_delay = cell_ssta_delay
        

    def ssta_sim(self, mode, src, samples):
        """ Runs SSTA on the circuit. Currently the cell distributions are hard-coded

        Parameters
        ----------
        mode : str
            SSTA mode for statistical operations
            alt, analytical
            num, numerical 
        samples : int
            number of samples used for the numerical statistical operations

        Note: the delay of PI and FB is considered as 0
        """

        # First, what is the delay distribution of each gate? (num/alt)
        self.set_cell_ssta_delay(src, tech=config.TECH, pvs=config.PVS)
        for node in self.nodes_lev:
            if node.ntype in ["PI", "FB"]:
                node.dd_cell = 0 
            elif node.ntype in ["GATE", "PO"]:
                node.dd_cell = self.cell_ssta_delay[node.cell_name] 

        # Second, go over each gate and run a MAX-SUM simulation
        print("Node\tLevel\tMean\tSTD")
        for node in self.nodes_lev:
            t_s = time.time()
            print("Node: {}\t".format(node.num))
            if node.ntype == "PI":
                node.dd_node = 0 
            elif node.ntype == "FB":
                node.dd_node = node.unodes[0].dd_node
            elif node.ntype in ["GATE", "PO"]:
                opmax = MaxOp()
                dd_unodes = [unode.dd_node for unode in node.unodes]
                dd_max = dd_unodes[0]
                for n in range(1, len(dd_unodes)):
                    if mode == "alt":
                        dd_max = opmax.max_alt(dd_max, dd_unodes[n])
                    elif mode == "num":
                        print("\t- unode: {}".format(node.unodes[n].num))
                        dd_max = opmax.max_num(dd_max, dd_unodes[n], samples=samples, 
                            eps_error_area=0.01)
                        if dd_max != 0:
                            print("\tArea: {:.5f}".format(dd_max.area()))
                
                print("\tMAX time: {:2.4f}".format(time.time() - t_s))
                if dd_max != 0:
                    print("\tMAX Area: {:.5f}".format(dd_max.area()))
                t_s = time.time()
                opsum = SumOp()
                if mode == "alt":
                    node.dd_node = opsum.sum_alt(node.dd_cell, dd_max)
                elif mode == "num":
                    node.dd_node = opsum.sum_num(node.dd_cell, dd_max, samples=samples)
                    print("\tSUM time: {:3.4f}".format(time.time() - t_s))

                print("\tSUM Area: {:.5f}".format(node.dd_node.area()))
                utils.plot_pmf(node.dd_node, fname=self.c_name + "-" + node.num + ".pdf")

    def get_cell_delay(self):
        """ This method assigns temporary distributions to cells """ 
        cell_dg = {}
        # cell_dg["NOT"] = Normal(1, 1)
        # cell_dg["NAND"] = Normal(3, 1)
        # cell_dg["AND"] = Normal(4.2, 1)
        # cell_dg["NOR"] = Normal(3, 1)
        # cell_dg["OR"] = Normal(4.2, 1)
        # cell_dg["XOR"] = Normal(8, 1)
        # cell_dg["XNOR"] = Normal(8, 1)
        # cell_dg["BUFF"] = Normal(2, 1)
        cell_dg["NOT"] =    SkewNormal(1,   1, 10)
        cell_dg["NAND"] =   SkewNormal(4,   1, 10)
        cell_dg["AND"] =    SkewNormal(4.2, 1, 10)
        cell_dg["NOR"] =    SkewNormal(3,   1, 10)
        cell_dg["OR"] =     SkewNormal(4.2, 1, 10)
        cell_dg["XOR"] =    SkewNormal(8,   1, 10)
        cell_dg["XNOR"] =   SkewNormal(8,   1, 10)
        cell_dg["BUFF"] =   SkewNormal(2,   1, 10)
        return cell_dg


 
