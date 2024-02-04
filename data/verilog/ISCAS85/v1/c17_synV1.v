/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : P-2019.03-SP1-1
// Date      : Tue Nov 17 22:19:56 2020
/////////////////////////////////////////////////////////////


module c17 ( N1, N2, N3, N6, N7, N22, N23 );
  input N1, N2, N3, N6, N7;
  output N22, N23;
  wire   n6, n7, n8, n9, n10;

  NOR2_X1 U8 ( .A1(n6), .A2(n7), .ZN(N23) );
  NOR2_X1 U9 ( .A1(N2), .A2(N7), .ZN(n7) );
  INV_X1 U10 ( .I(n8), .ZN(n6) );
  NAND2_X1 U11 ( .A1(n9), .A2(n10), .ZN(N22) );
  NAND2_X1 U12 ( .A1(N2), .A2(n8), .ZN(n10) );
  NAND2_X1 U13 ( .A1(N6), .A2(N3), .ZN(n8) );
  NAND2_X1 U14 ( .A1(N1), .A2(N3), .ZN(n9) );
endmodule

