// Verilog
// c4
// Ninputs 4
// Noutput 1
// NtotalGates 8
// NAND2 7
// NAND4 1

module c4 (N1, N4, N8, N12, N34);

input N1,N4,N8,N12;

output N34;

wire N23,N24,N27,N30,N31,N32,N33;

nand NAND2_23 (N23, N1, N8);
nand NAND2_24 (N24, N4, N8);
nand NAND2_27 (N27, N4, N12);
nand NAND2_30 (N30, N4, N23);
nand NAND2_31 (N31, N1, N24);
nand NAND2_32 (N32, N24, N12);
nand NAND2_33 (N33, N27, N8);
nand NAND4_34 (N34, N30, N31, N32, N33);

endmodule
