
# These used to be in the main method of main_saeed.py 
# Originally from 2020


    elif args.func == "writeOB":
        # circuit.co_ob_info()
        path = "../data/ob_stat/{}_TP{}.obs".format(ckt_name, args.tpLoad)
        print("Saving ob info in {}".format(path))
        circuit.write_ob_info(path)

    elif args.func == "analysisOB":
        TPs = [50, 100, 200, 500, 1000, 2000,
               5000, 10000, 20000, 50000, 100000]
        report_path = "../data/ob_stat/{}_REPORT.obsr".format(ckt_name)
        report = open(report_path, "w")
        data = []
        real_TP = []
        for tp in TPs:
            ob_fname = "../data/ob_stat/{}_TP{}.obs".format(ckt_name, tp)
            print(ob_fname)
            if not os.path.exists(ob_fname):
                print("SKIPPED", ob_fname)
                continue
            real_TP.append(tp)
            infile = open(ob_fname)
            lines = infile.readlines()
            data.append([(x.split()[1]) for x in lines[1:]])

        for idx in range(len(data)):
            report.write(str(real_TP[idx]) + "," + ",".join(data[idx]) + "\n")

        print("Report file generated in {}".format(report_path))

    elif args.func == "histOB":
        """ histogram of OB, reading from .stafan files"""
        mybins = np.logspace(-6, 0, 13)
        arr = []
        for node in circuit.nodes_lev:
            arr.append(node.B)
        min_val = min(arr)
        print(min_val)
        if min_val < 0:
            raise ValueError("min value is zero")
        if min_val == 0:
            print("Min value 0 spotted")
            exit()
        mybins = np.logspace(np.log10(min_val), 0, 11)
        # res = np.histogram(arr, mybins)
        res = np.histogram(arr, bins=mybins, density=False)
        # print(np.sum(res[0]))
        temp = [str(np.round(x, 3)) for x in res[0]]
        log = "," + ",".join(["{:.1e}".format(x) for x in res[1]]) + "\n"
        log += ckt_name + "," + ",".join(temp)
        print(log)

    elif args.func in ["deltaP", "deltaHTO"]:
        conv = convert.Converter(ckt_name, "EPFL")
        # TODO: be cautious about passing args
        ops = OPI(circuit, args.func, count_op=args.opCount, args=args)
        fname = "../data/observations/" + ckt_name + \
            "_" + args.func + "_B-" + str(args.Bth)
        fname += "_Count-" + str(args.opCount) + ".op"

        conv.nodes2tmax_OP(ops, fname)
        print("Stored Synopsys readable results in {}".format(fname))
        print(ops)
        for op in ops:
            print(op + "\t" + conv.n2g(op))

    elif args.func == "gen_stil":
        # Does not generate the test patterns but reads them, and creates stil file
        # generate a test pattern file in 658 format and save it in ../data/patterns/

        # We read the ckt_name circuit, which is the synthesized version
        # But we read the golden TP from ckt circuit, because we don't have ckt.v and only
        # have ckt_synVX.v
        tp_fname = "../data/patterns/" + args.ckt + args.synv + "deltaP_TP" + \
            str(args.tpLoad) + ".tp"
        stil_fname = "../data/patterns/" + \
            args.ckt + "_" + str(args.tp) + ".raw-stil"
        # circuit.gen_tp_file(args.tp, fname=tp_fname)
        circuit.logic_sim_file(tp_fname, stil_fname,
                               out_format="STIL", tp_count=args.tp)
        print("Done stil gen, added in {}".format(stil_fname))

    elif args.func == "Single_OP_FS":
        """ For one circuit, generates OPs, based on args settings (B_th)
        For each OP, generate a new verilog file, with name as cname_OP_<OP-node>.v
        Use a predefined .tp file to simulate your new circuit 
        Store the results for this new verilog in the .STIL format
        """

        conv = convert.Converter(args.ckt, utils.ckt_type(args.ckt))
        ops = OPI(circuit, args.OPIalg, count_op=args.opCount, B_th=args.Bth)
        print("Observation points are: ")
        for op in ops:
            print(op + "\t" + conv.n2g(op))

        tp_fname = os.path.join(
            cfg.PATTERN_DIR, args.ckt + "_" + str(args.tp) + ".tp")
        print("Reading test patterns from \t\t\t{}".format(tp_fname))

        OPs_fname = "../data/observations/" + args.ckt + "_" + \
            args.OPIalg + "_B-" + str(args.Bth)
        OPs_fname += "_Count-" + str(args.opCount) + ".op"
        conv.nodes2tmax_OP(ops, OPs_fname)
        print("Stored Synopsys observation file in     \t{}".format(fname))

        for op in ops:

            print("".join(["-"]*100))
            # Step 1: Generate a new verilog file
            print("Generating modified verilog for op: \t\t{}".format(op))
            cname_mod = args.ckt + "_OP_" + op
            path_in = os.path.join(cfg.VERILOG_DIR, args.ckt + ".v")
            path_out = os.path.join(cfg.VERILOG_DIR, cname_mod + ".v")
            convert.add_OP_verilog(path_in=path_in,
                                   op=op, path_out=path_out, verilog_version=utils.ckt_type(args.ckt))

            print("New verilog file generated in \t\t\t{}".format(path_out))

            # Step 2: Logic sim and generate STIL file
            ckt_mod = Circuit(cname_mod)
            ckt_mod.lev()
            LoadCircuit(ckt_mod, "v")
            stil_fname = os.path.join(cfg.PATTERN_DIR,
                                      cname_mod + "_" + str(args.tp) + ".raw-stil")
            ckt_mod.logic_sim_file(tp_fname, stil_fname, "STIL")
            print("STIL format file  generated in \t\t\t{}".format(stil_fname))
            # convert.replace_primitive2cell(path_out)

        print("".join(["-"]*100))

    elif args.func == "Multi_OP_FS":
        """ For one circuit, generates OPs, based on args settings (B_th)
        TODO: complete me after testing
        """

        conv = convert.Converter(args.ckt, utils.ckt_type(args.ckt))
        ops = OPI(circuit, args.OPIalg, count_op=args.opCount, B_th=args.Bth)
        print("Observation points are: ")
        for op in ops:
            print(op + "\t" + conv.n2g(op))

        tp_fname = os.path.join(
            cfg.PATTERN_DIR, args.ckt + "_" + str(args.tp) + ".tp")
        print("Reading test patterns from \t\t\t{}".format(tp_fname))

        OPs_fname = "../data/observations/" + args.ckt + "_" + \
            args.OPIalg + "_B-" + str(args.Bth)
        OPs_fname += "_Count-" + str(args.opCount) + ".op"
        conv.nodes2tmax_OP(ops, OPs_fname)
        print("Stored Synopsys observation file in     \t{}".format(fname))

        # The path to verilog file changes cumulitavely
        path_in = os.path.join(cfg.VERILOG_DIR, args.ckt + ".v")
        for idx, op in enumerate(ops):

            print("".join(["-"]*100))

            print("Generating modified verilog for {} ops.".format(idx+1))
            print("Original verilog netlist is: \t\t\t {}".format(path_in))

            # Step 1: Continuously modifying a verilog file
            cname_mod = args.ckt + "_OP_" + args.OPIalg + "_B-" + \
                str(args.Bth) + "_Acc" + str(idx+1)
            path_out = os.path.join(cfg.VERILOG_DIR, cname_mod + ".v")
            convert.add_OP_verilog(
                path_in=path_in,
                op=op,
                path_out=path_out,
                verilog_version=utils.ckt_type(args.ckt),
                new_buff="MSABUFF" + str(idx),
                new_po="MSAPO" + str(idx))
            print("New verilog file generated in \t\t\t{}".format(path_out))

            # Step 2: Logic sim and generate STIL file
            ckt_mod = Circuit(cname_mod)
            ckt_mod.lev()
            LoadCircuit(ckt_mod, "v")
            stil_fname = os.path.join(cfg.PATTERN_DIR,
                                      cname_mod + "_" + str(args.tp) + ".raw-stil")
            ckt_mod.logic_sim_file(tp_fname, stil_fname, "STIL")
            print("STIL format file  generated in \t\t\t{}".format(stil_fname))
            path_in = path_out
            # convert.replace_primitive2cell(path_out)

        print("".join(["-"]*100))

    elif args.func == "genV_TMAXOP":
        """ input: the address to the TMAX op file 
        output: verilog file with ops as PO to be sent to fault simulation """
        # TODO: what should be the output file name?

        path_in = os.path.join(cfg.VERILOG_DIR, ckt_name + ".v")
        print("the original circuit is {}".format(path_in))
        v_orig = convert.read_verilog_lines(path_in)

        # op_fname = "../data/observations/{}_TMAX.op".format(ckt_name)
        op_fname = f"../data/observations/{args.op_fname}.op"
        print("reading op file from {}".format(op_fname))

        conv = convert.Converter(ckt_name, utils.ckt_type(args.ckt))
        ops_gate = conv.tmax2nodes_OP(op_fname)
        # ops_gate = []
        print("Observation points are: ")
        ops_node = []
        args.opCount = args.opCount if args.opCount else len(ops_gate)
        for op in ops_gate[:args.opCount]:
            op = op.split("/")[0]
            ops_node.append(conv.g2n(op))
            print(op + "\t" + conv.g2n(op))

        new_pos = ["MSAPO" + op for op in ops_node]

        temp = "," + ", ".join(new_pos) + ");"
        v_orig[0] = v_orig[0].replace(");", temp)

        temp = "," + ", ".join(new_pos) + ";"
        v_orig[2] = v_orig[2].replace(";", temp)

        cname_mod = "{}_deltaP_Bth_{}_OP{}".format(
            ckt_name, args.Bth, args.opCount)
        path_out = "../data/verilog/{}.v".format(cname_mod)
        outfile = open(path_out, "w")
        outfile.write(v_orig[0] + "\n")
        outfile.write(v_orig[1] + "\n")
        outfile.write(v_orig[2] + "\n")
        outfile.write(v_orig[3] + "\n")
        for line in v_orig[4:-1]:
            outfile.write(line + "\n")

        for idx, op in enumerate(ops_node):
            new_buff = "MSABUFF" + op
            new_po = "MSAPO" + op
            outfile.write("BUF_X1 {} ( .I({}) , .Z({}) );\n".format(
                new_buff, op, new_po))

        outfile.write("endmodule\n")
        outfile.close()
        print("New verilog file generated in \t\t\t{}".format(path_out))

        # Step 2: Logic sim and generate STIL file
        tp_fname = os.path.join(
            cfg.PATTERN_DIR, args.ckt + "_TP" + str(args.tpLoad) + ".tp")
        print("Reading test patterns from \t\t\t{}".format(tp_fname))

        ckt_mod = Circuit(cname_mod)
        LoadCircuit(ckt_mod, "v")
        ckt_mod.lev()
        stil_fname = os.path.join(cfg.PATTERN_DIR,
                                  cname_mod + "_" + str(args.tp) + ".raw-stil")
        ckt_mod.logic_sim_file(tp_fname, stil_fname, "STIL", args.tp)
        print("STIL format file  generated in \t\t\t{}".format(stil_fname))

        print("".join(["-"]*100))


