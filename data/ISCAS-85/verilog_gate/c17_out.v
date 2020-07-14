// Benchmark "ISCAS-85/c17" written by ABC on Sun Jun 21 14:55:51 2020

module \ISCAS-85/c17  ( 
    G1gat, G2gat, G3gat, G6gat, G7gat,
    G22gat, G23gat  );
  input  G1gat, G2gat, G3gat, G6gat, G7gat;
  output G22gat, G23gat;
  wire new_n8_, new_n9_, new_n10_, new_n12_;
  nand2  g0(.a(G3gat), .b(G1gat), .O(new_n8_));
  nand2  g1(.a(G6gat), .b(G3gat), .O(new_n9_));
  nand2  g2(.a(new_n9_), .b(G2gat), .O(new_n10_));
  nand2  g3(.a(new_n10_), .b(new_n8_), .O(G22gat));
  nand2  g4(.a(new_n9_), .b(G7gat), .O(new_n12_));
  nand2  g5(.a(new_n12_), .b(new_n10_), .O(G23gat));
endmodule


