/****************************************************************************
 *                                                                          *
 *  VERILOG BEHAVIORAL DESCRIPTION OF THE ISCAS-85 BENCHMARK CIRCUIT c432   *
 *                                                                          *
 *  Function: 27-channel interrupt controller                               *
 *                                                                          *
 *  Written by: Mark C. Hansen                                              *
 *                                                                          *
 *  Last modified: Oct 17, 1997                                             *
 *                                                                          *
 ****************************************************************************/

module Circuit432 (in4, in17, in30, in43, in56, in69, in82, in95, in108,
                  in1, in11, in24, in37, in50, in63, in76, in89, in102,
                  in8, in21, in34, in47, in60, in73, in86, in99, in112,
                  in14, in27, in40, in53, in66, in79, in92, in105, in115,
                  out223, out329, out370,
                  out421, out430, out431, out432);

  input         in4, in17, in30, in43, in56, in69, in82, in95, in108,
                in1, in11, in24, in37, in50, in63, in76, in89, in102,
                in8, in21, in34, in47, in60, in73, in86, in99, in112,
                in14, in27, in40, in53, in66, in79, in92, in105, in115;
  output        out223, out329, out370,
                out421, out430, out431, out432;

  wire [8:0]    A, B, C, E;
  wire          PA, PB, PC;
  wire [3:0]    Chan;

  assign
      E[8:0] = { in4, in17, in30, in43, in56, in69, in82, in95, in108 },
      A[8:0] = { in1, in11, in24, in37, in50, in63, in76, in89, in102 },
      B[8:0] = { in8, in21, in34, in47, in60, in73, in86, in99, in112 },
      C[8:0] = { in14, in27, in40, in53, in66, in79, in92, in105, in115 },
	  
// There is an error!!! 
// The original lines: 
//     PA = out223,
//     PB = out329,
//	   PC = out370,
// ------------------
// The new lines: 
      out223 = PA,
	     out329 = PB,
	     out370 = PC,
// ------------------
       
      Chan[3:0] = { out421, out430, out431, out432 };
	
  TopLevel432b Ckt432 (E, A, B, C, PA, PB, PC, Chan);

endmodule /* Circuit432 */

/*************************************************************************/

module TopLevel432b (E, A, B, C, PA, PB, PC, Chan);

  input[8:0]	E, A, B, C;
  output     	PA, PB, PC;
  output[3:0] Chan;
  wire[8:0] X1, X2, I;

  PriorityA M1(E, A, PA, X1);
  PriorityB M2(E, X1, B, PB, X2);
  PriorityC M3(E, X1, X2, C, PC);
  EncodeChan M4(E, A, B, C, PA, PB, PC, I);
  DecodeChan M5(I, Chan);

endmodule /* TopLevel432b */

/*************************************************************************/

module PriorityA(E, A, PA, X1);

  input[8:0] E, A;
  output     PA;
  output[8:0] X1;
  
  wire [8:0] Ab, EAb;

  assign Ab = ~A;
  assign EAb = ~(Ab & E);
  assign PA = ~&EAb;
  assign X1 = EAb ^ {9{PA}};

endmodule /* PriorityA */

/*************************************************************************/

module PriorityB(E, X1, B, PB, X2);

  input[8:0] E, X1, B;
  output     PB;
  output[8:0] X2;
  
  wire [8:0] Eb, EbB, XEB;

  assign Eb = ~E;
  assign EbB = ~(Eb | B);
  assign XEB = ~(X1 & EbB);
  assign PB = ~&XEB;
  assign X2 = XEB ^ {9{PB}};

endmodule /* PriorityB */

/*************************************************************************/

module PriorityC(E, X1, X2, C, PC);

  input[8:0] E, X1, X2, C;
  output     PC;
  
  wire [8:0] Eb, EbC, XEC;

  assign Eb = ~E;
  assign EbC = ~(Eb | C);
  assign XEC = ~(X1 & X2 & EbC);
  assign PC = ~&XEC;

endmodule /*PriorityC */

/*************************************************************************/

module EncodeChan(E, A, B, C, PA, PB, PC, I);

  input[8:0] E, A, B, C; 
  input PA, PB, PC;
  output[8:0] I;

  wire [8:0] APA, BPB, CPC;

  assign APA = ~(A & {9{PA}});
  assign BPB = ~(B & {9{PB}});
  assign CPC = ~(C & {9{PC}});
  assign I = ~(E & APA & BPB & CPC);

endmodule /* EncodeChan */

/*************************************************************************/

module DecodeChan(I, Chan);
 
  input[8:0] I;
  output[3:0] Chan;

  wire Iand, I8b, I1b, I2b, I3b, I5b, I56, I245, I3456, I1256;

  assign I8b = ~I[8];
  assign Iand = &I[7:0];
  assign Chan[3] = ~(I8b | Iand);

  assign I1b = ~I[1];
  assign I2b = ~I[2];
  assign I3b = ~I[3];
  assign I5b = ~I[5];

  assign I56 = ~(I5b & I[6]);
  assign I245 = ~(I2b & I[4] & I[5]);
  assign I3456 = ~(I3b & I[4] & I[5] & I[6]);
  assign I1256 = ~(I1b & I[2] & I[5] & I[6]);

  assign Chan[2] = ~(I[4] & I[6] & I[7] & I56);
  assign Chan[1] = ~(I[6] & I[7] & I245 & I3456);
  assign Chan[0] = ~(I[7] & I56 & I1256 & I3456);

endmodule /* DecodeChan */