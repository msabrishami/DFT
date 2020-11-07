// 
// ******************************************************************************
// *                                                                            *
// *                   Copyright (C) 2004-2014, Nangate Inc.                    *
// *                           All rights reserved.                             *
// *                                                                            *
// * Nangate and the Nangate logo are trademarks of Nangate Inc.                *
// *                                                                            *
// * All trademarks, logos, software marks, and trade names (collectively the   *
// * "Marks") in this program are proprietary to Nangate or other respective    *
// * owners that have granted Nangate the right and license to use such Marks.  *
// * You are not permitted to use the Marks without the prior written consent   *
// * of Nangate or such third party that may own the Marks.                     *
// *                                                                            *
// * This file has been provided pursuant to a License Agreement containing     *
// * restrictions on its use. This file contains valuable trade secrets and     *
// * proprietary information of Nangate Inc., and is protected by U.S. and      *
// * international laws and/or treaties.                                        *
// *                                                                            *
// * The copyright notice(s) in this file does not indicate actual or intended  *
// * publication of this file.                                                  *
// *                                                                            *
// *    NGLibraryCharacterizer, Development_version_64 - build 201405281900     *
// *                                                                            *
// ******************************************************************************
// 
// * Default delays
//   * comb. path delay        : 0.1
//   * seq. path delay         : 0.1
//   * delay cells             : 0.1
//   * timing checks           : 0.1
// 
// * NTC Setup
//   * Export NTC sections     : true
//   * Combine setup / hold    : true
//   * Combine recovery/removal: true
// 
// * Extras
//   * Export `celldefine      : false
//   * Export `timescale       : -
// 
`timescale 1ns/1ns
module AND2_X1 (A1, A2, Z);
  input A1;
  input A2;
  output Z;

  and(Z, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
  endspecify

endmodule

module AND2_X2 (A1, A2, Z);
  input A1;
  input A2;
  output Z;

  and(Z, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
  endspecify

endmodule

module AND3_X1 (A1, A2, A3, Z);
  input A1;
  input A2;
  input A3;
  output Z;

  and(Z, i_16, A3);
  and(i_16, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
    (A3 => Z) = (0.1, 0.1);
  endspecify

endmodule

module AND3_X2 (A1, A2, A3, Z);
  input A1;
  input A2;
  input A3;
  output Z;

  and(Z, i_22, A3);
  and(i_22, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
    (A3 => Z) = (0.1, 0.1);
  endspecify

endmodule

module AND4_X1 (A1, A2, A3, A4, Z);
  input A1;
  input A2;
  input A3;
  input A4;
  output Z;

  and(Z, i_8, A4);
  and(i_8, i_9, A3);
  and(i_9, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
    (A3 => Z) = (0.1, 0.1);
    (A4 => Z) = (0.1, 0.1);
  endspecify

endmodule

module AND4_X2 (A1, A2, A3, A4, Z);
  input A1;
  input A2;
  input A3;
  input A4;
  output Z;

  and(Z, i_8, A4);
  and(i_8, i_9, A3);
  and(i_9, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
    (A3 => Z) = (0.1, 0.1);
    (A4 => Z) = (0.1, 0.1);
  endspecify

endmodule

module ANTENNA (I);
  input I;

endmodule

module AOI21_X1 (A1, A2, B, ZN);
  input A1;
  input A2;
  input B;
  output ZN;

  not(ZN, i_26);
  or(i_26, i_27, B);
  and(i_27, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b0)) (B => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1)) (B => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0)) (B => ZN) = (0.1, 0.1);
  endspecify

endmodule

module AOI21_X2 (A1, A2, B, ZN);
  input A1;
  input A2;
  input B;
  output ZN;

  not(ZN, i_20);
  or(i_20, i_21, B);
  and(i_21, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b0)) (B => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1)) (B => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0)) (B => ZN) = (0.1, 0.1);
  endspecify

endmodule

module AOI22_X1 (A1, A2, B1, B2, ZN);
  input A1;
  input A2;
  input B1;
  input B2;
  output ZN;

  not(ZN, i_12);
  or(i_12, i_13, i_14);
  and(i_13, A1, A2);
  and(i_14, B1, B2);

  specify
    if((A2 == 1'b1) && (B1 == 1'b0) && (B2 == 1'b0)) (A1 => ZN) = (0.1, 0.1);
    if((A2 == 1'b1) && (B1 == 1'b0) && (B2 == 1'b1)) (A1 => ZN) = (0.1, 0.1);
    if((A2 == 1'b1) && (B1 == 1'b1) && (B2 == 1'b0)) (A1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (B1 == 1'b0) && (B2 == 1'b0)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (B1 == 1'b0) && (B2 == 1'b1)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (B1 == 1'b1) && (B2 == 1'b0)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b0) && (B2 == 1'b1)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1) && (B2 == 1'b1)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0) && (B2 == 1'b1)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b0) && (B1 == 1'b1)) (B2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1) && (B1 == 1'b1)) (B2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0) && (B1 == 1'b1)) (B2 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module AOI22_X2 (A1, A2, B1, B2, ZN);
  input A1;
  input A2;
  input B1;
  input B2;
  output ZN;

  not(ZN, i_12);
  or(i_12, i_13, i_14);
  and(i_13, A1, A2);
  and(i_14, B1, B2);

  specify
    if((A2 == 1'b1) && (B1 == 1'b0) && (B2 == 1'b0)) (A1 => ZN) = (0.1, 0.1);
    if((A2 == 1'b1) && (B1 == 1'b0) && (B2 == 1'b1)) (A1 => ZN) = (0.1, 0.1);
    if((A2 == 1'b1) && (B1 == 1'b1) && (B2 == 1'b0)) (A1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (B1 == 1'b0) && (B2 == 1'b0)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (B1 == 1'b0) && (B2 == 1'b1)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (B1 == 1'b1) && (B2 == 1'b0)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b0) && (B2 == 1'b1)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1) && (B2 == 1'b1)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0) && (B2 == 1'b1)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b0) && (B1 == 1'b1)) (B2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1) && (B1 == 1'b1)) (B2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0) && (B1 == 1'b1)) (B2 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module BUF_X1 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module BUF_X2 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module BUF_X4 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module BUF_X8 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module BUF_X12 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module BUF_X16 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module CLKBUF_X1 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module CLKBUF_X2 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module CLKBUF_X4 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module CLKBUF_X8 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module CLKBUF_X12 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module CLKBUF_X16 (I, Z);
  input I;
  output Z;

  buf(Z, I);

  specify
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

primitive \seq_CLKGATETST_X1  (QD, CLK, nextstate, NOTIFIER);
  output QD;
  input CLK;
  input nextstate;
  input NOTIFIER;
  reg QD;

  table
      // CLK   nextstate    NOTIFIER     : @QD :          QD
           0           0           ?       : ? :           0;
           0           1           ?       : ? :           1;
           1           ?           ?       : ? :           -; // Ignore non-triggering clock edge
           ?           *           ?       : ? :           -; // Ignore all edges on nextstate
           ?           ?           *       : ? :           x; // Any NOTIFIER change
  endtable
endprimitive

module CLKGATETST_X1 (CLK, E, TE, Q);
  input CLK;
  input E;
  input TE;
  output Q;
  reg NOTIFIER;

  `ifdef NTC
    and(Q, CLK_d, QD);
    \seq_CLKGATETST_X1 (QD, CLK_d, nextstate, NOTIFIER);
    not(QDn, QD);
    or(nextstate, E_d, TE_d);

  `else
    and(Q, CLK, QD);
    \seq_CLKGATETST_X1 (QD, CLK, nextstate, NOTIFIER);
    not(QDn, QD);
    or(nextstate, E, TE);

  `endif

  specify
    if((E == 1'b0) && (TE == 1'b0)) (negedge CLK => (Q +: 1'b0)) = (0.1, 0.1);
    if((E == 1'b0) && (TE == 1'b1)) (CLK => Q) = (0.1, 0.1);
    if((E == 1'b1) && (TE == 1'b0)) (CLK => Q) = (0.1, 0.1);
    if((E == 1'b1) && (TE == 1'b1)) (CLK => Q) = (0.1, 0.1);
    `ifdef NTC
      $setuphold(posedge CLK, negedge E, 0.1, 0.1, NOTIFIER, , ,CLK_d, E_d);
      $setuphold(posedge CLK, negedge TE, 0.1, 0.1, NOTIFIER, , ,CLK_d, TE_d);
      $setuphold(posedge CLK, posedge E, 0.1, 0.1, NOTIFIER, , ,CLK_d, E_d);
      $setuphold(posedge CLK, posedge TE, 0.1, 0.1, NOTIFIER, , ,CLK_d, TE_d);
      $width(negedge CLK, 0.1, 0, NOTIFIER);
    `else
      $setuphold(posedge CLK, negedge E, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK, negedge TE, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK, posedge E, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK, posedge TE, 0.1, 0.1, NOTIFIER);
      $width(negedge CLK, 0.1, 0, NOTIFIER);
    `endif
  endspecify

endmodule

primitive \seq_DFFRNQ_X1  (IQ, RN, nextstate, CLK, NOTIFIER);
  output IQ;
  input RN;
  input nextstate;
  input CLK;
  input NOTIFIER;
  reg IQ;

  table
       // RN   nextstate         CLK    NOTIFIER     : @IQ :          IQ
           ?           0           r           ?       : ? :           0;
           1           1           r           ?       : ? :           1;
           ?           0           *           ?       : 0 :           0; // reduce pessimism
           1           1           *           ?       : 1 :           1; // reduce pessimism
           1           *           ?           ?       : ? :           -; // Ignore all edges on nextstate
           1           ?           n           ?       : ? :           -; // Ignore non-triggering clock edge
           0           ?           ?           ?       : ? :           0; // RN activated
           *           ?           ?           ?       : 0 :           0; // Cover all transitions on RN
           ?           ?           ?           *       : ? :           x; // Any NOTIFIER change
  endtable
endprimitive

module DFFRNQ_X1 (D, RN, CLK, Q);
  input D;
  input RN;
  input CLK;
  output Q;
  reg NOTIFIER;

  `ifdef NTC
    `ifdef RECREM
      buf (RN_d, RN_di);
    `else
      buf (RN_d, RN);
    `endif
    \seq_DFFRNQ_X1 (IQ, RN_d, nextstate, CLK_d, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    buf(nextstate, D_d);

    // Delayed data/reference logic
    buf(id_5, RN_d);

    `ifdef TETRAMAX
    `else
      ng_xbuf(xid_5, id_5, 1'b1);
    `endif
  `else
    \seq_DFFRNQ_X1 (IQ, RN, nextstate, CLK, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    buf(nextstate, D);

    // Delayed data/reference logic
    buf(id_4, RN);

    `ifdef TETRAMAX
    `else
      ng_xbuf(xid_4, id_4, 1'b1);
    `endif
  `endif

  specify
    (posedge CLK => (Q +: D)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    `ifdef NTC
      `ifdef RECREM
        $recrem(posedge RN, posedge CLK, 0.1, 0.1, NOTIFIER, , ,RN_di, CLK_d);
      `else
        $hold(posedge CLK, posedge RN, 0.1, NOTIFIER);
        $recovery(posedge RN, posedge CLK, 0.1, NOTIFIER);
      `endif
      $setuphold(posedge CLK &&& (xid_5), negedge D, 0.1, 0.1, NOTIFIER, , ,CLK_d, D_d);
      $setuphold(posedge CLK &&& (xid_5), posedge D, 0.1, 0.1, NOTIFIER, , ,CLK_d, D_d);
      $width(negedge CLK &&& (xid_5), 0.1, 0, NOTIFIER);
      $width(negedge RN, 0.1, 0, NOTIFIER);
      $width(posedge CLK &&& (xid_5), 0.1, 0, NOTIFIER);
    `else
      $hold(posedge CLK, posedge RN, 0.1, NOTIFIER);
      $recovery(posedge RN, posedge CLK, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_4), negedge D, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_4), posedge D, 0.1, 0.1, NOTIFIER);
      $width(negedge CLK &&& (xid_4), 0.1, 0, NOTIFIER);
      $width(negedge RN, 0.1, 0, NOTIFIER);
      $width(posedge CLK &&& (xid_4), 0.1, 0, NOTIFIER);
    `endif
  endspecify

endmodule

primitive \seq_DFFSNQ_X1  (IQ, SN, nextstate, CLK, NOTIFIER);
  output IQ;
  input SN;
  input nextstate;
  input CLK;
  input NOTIFIER;
  reg IQ;

  table
       // SN   nextstate         CLK    NOTIFIER     : @IQ :          IQ
           1           0           r           ?       : ? :           0;
           ?           1           r           ?       : ? :           1;
           1           0           *           ?       : 0 :           0; // reduce pessimism
           ?           1           *           ?       : 1 :           1; // reduce pessimism
           1           *           ?           ?       : ? :           -; // Ignore all edges on nextstate
           1           ?           n           ?       : ? :           -; // Ignore non-triggering clock edge
           0           ?           ?           ?       : ? :           1; // SN activated
           *           ?           ?           ?       : 1 :           1; // Cover all transitions on SN
           ?           ?           ?           *       : ? :           x; // Any NOTIFIER change
  endtable
endprimitive

module DFFSNQ_X1 (D, SN, CLK, Q);
  input D;
  input SN;
  input CLK;
  output Q;
  reg NOTIFIER;

  `ifdef NTC
    `ifdef RECREM
      buf (SN_d, SN_di);
    `else
      buf (SN_d, SN);
    `endif
    \seq_DFFSNQ_X1 (IQ, SN_d, nextstate, CLK_d, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    buf(nextstate, D_d);

    // Delayed data/reference logic
    buf(id_5, SN_d);

    `ifdef TETRAMAX
    `else
      ng_xbuf(xid_5, id_5, 1'b1);
    `endif
  `else
    \seq_DFFSNQ_X1 (IQ, SN, nextstate, CLK, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    buf(nextstate, D);

    // Delayed data/reference logic
    buf(id_4, SN);

    `ifdef TETRAMAX
    `else
      ng_xbuf(xid_4, id_4, 1'b1);
    `endif
  `endif

  specify
    (posedge CLK => (Q +: D)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    `ifdef NTC
      `ifdef RECREM
        $recrem(posedge SN, posedge CLK, 0.1, 0.1, NOTIFIER, , ,SN_di, CLK_d);
      `else
        $hold(posedge CLK, posedge SN, 0.1, NOTIFIER);
        $recovery(posedge SN, posedge CLK, 0.1, NOTIFIER);
      `endif
      $setuphold(posedge CLK &&& (xid_5), negedge D, 0.1, 0.1, NOTIFIER, , ,CLK_d, D_d);
      $setuphold(posedge CLK &&& (xid_5), posedge D, 0.1, 0.1, NOTIFIER, , ,CLK_d, D_d);
      $width(negedge CLK &&& (xid_5), 0.1, 0, NOTIFIER);
      $width(negedge SN, 0.1, 0, NOTIFIER);
      $width(posedge CLK &&& (xid_5), 0.1, 0, NOTIFIER);
    `else
      $hold(posedge CLK, posedge SN, 0.1, NOTIFIER);
      $recovery(posedge SN, posedge CLK, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_4), negedge D, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_4), posedge D, 0.1, 0.1, NOTIFIER);
      $width(negedge CLK &&& (xid_4), 0.1, 0, NOTIFIER);
      $width(negedge SN, 0.1, 0, NOTIFIER);
      $width(posedge CLK &&& (xid_4), 0.1, 0, NOTIFIER);
    `endif
  endspecify

endmodule

module FA_X1 (A, B, CI, CO, S);
  input A;
  input B;
  input CI;
  output CO;
  output S;

  or(CO, i_84, i_87);
  or(i_84, i_85, i_86);
  and(i_85, B, CI);
  and(i_86, B, A);
  and(i_87, CI, A);
  not(S, i_92);
  or(i_92, i_93, i_99);
  and(i_93, i_94, A);
  not(i_94, i_95);
  or(i_95, i_96, i_97);
  and(i_96, B, CI);
  not(i_97, i_98);
  or(i_98, B, CI);
  not(i_99, i_100);
  or(i_100, i_101, A);
  not(i_101, i_102);
  or(i_102, i_103, i_104);
  and(i_103, B, CI);
  not(i_104, i_105);
  or(i_105, B, CI);

  specify
    if((B == 1'b0) && (CI == 1'b1)) (A => CO) = (0.1, 0.1);
    if((B == 1'b1) && (CI == 1'b0)) (A => CO) = (0.1, 0.1);
    if((A == 1'b0) && (CI == 1'b1)) (B => CO) = (0.1, 0.1);
    if((A == 1'b1) && (CI == 1'b0)) (B => CO) = (0.1, 0.1);
    if((A == 1'b0) && (B == 1'b1)) (CI => CO) = (0.1, 0.1);
    if((A == 1'b1) && (B == 1'b0)) (CI => CO) = (0.1, 0.1);
    if((B == 1'b0) && (CI == 1'b0)) (A => S) = (0.1, 0.1);
    if((B == 1'b0) && (CI == 1'b1)) (A => S) = (0.1, 0.1);
    if((B == 1'b1) && (CI == 1'b0)) (A => S) = (0.1, 0.1);
    if((B == 1'b1) && (CI == 1'b1)) (A => S) = (0.1, 0.1);
    if((A == 1'b0) && (CI == 1'b0)) (B => S) = (0.1, 0.1);
    if((A == 1'b0) && (CI == 1'b1)) (B => S) = (0.1, 0.1);
    if((A == 1'b1) && (CI == 1'b0)) (B => S) = (0.1, 0.1);
    if((A == 1'b1) && (CI == 1'b1)) (B => S) = (0.1, 0.1);
    if((A == 1'b0) && (B == 1'b0)) (CI => S) = (0.1, 0.1);
    if((A == 1'b0) && (B == 1'b1)) (CI => S) = (0.1, 0.1);
    if((A == 1'b1) && (B == 1'b0)) (CI => S) = (0.1, 0.1);
    if((A == 1'b1) && (B == 1'b1)) (CI => S) = (0.1, 0.1);
  endspecify

endmodule

module FILLTIE ();

endmodule

module FILL_X1 ();

endmodule

module FILL_X2 ();

endmodule

module FILL_X4 ();

endmodule

module FILL_X8 ();

endmodule

module FILL_X16 ();

endmodule

module HA_X1 (A, B, CO, S);
  input A;
  input B;
  output CO;
  output S;

  and(CO, A, B);
  not(S, i_58);
  or(i_58, i_59, i_60);
  and(i_59, A, B);
  not(i_60, i_61);
  or(i_61, A, B);

  specify
    (A => CO) = (0.1, 0.1);
    (B => CO) = (0.1, 0.1);
    if((B == 1'b0)) (A => S) = (0.1, 0.1);
    if((B == 1'b1)) (A => S) = (0.1, 0.1);
    if((A == 1'b0)) (B => S) = (0.1, 0.1);
    if((A == 1'b1)) (B => S) = (0.1, 0.1);
  endspecify

endmodule

module INV_X1 (I, ZN);
  input I;
  output ZN;

  not(ZN, I);

  specify
    (I => ZN) = (0.1, 0.1);
  endspecify

endmodule

module INV_X2 (I, ZN);
  input I;
  output ZN;

  not(ZN, I);

  specify
    (I => ZN) = (0.1, 0.1);
  endspecify

endmodule

module INV_X4 (I, ZN);
  input I;
  output ZN;

  not(ZN, I);

  specify
    (I => ZN) = (0.1, 0.1);
  endspecify

endmodule

module INV_X8 (I, ZN);
  input I;
  output ZN;

  not(ZN, I);

  specify
    (I => ZN) = (0.1, 0.1);
  endspecify

endmodule

module INV_X12 (I, ZN);
  input I;
  output ZN;

  not(ZN, I);

  specify
    (I => ZN) = (0.1, 0.1);
  endspecify

endmodule

module INV_X16 (I, ZN);
  input I;
  output ZN;

  not(ZN, I);

  specify
    (I => ZN) = (0.1, 0.1);
  endspecify

endmodule

primitive \seq_LHQ_X1  (IQ, nextstate, E, NOTIFIER);
  output IQ;
  input nextstate;
  input E;
  input NOTIFIER;
  reg IQ;

  table
// nextstate           E    NOTIFIER     : @IQ :          IQ
           0           1           ?       : ? :           0;
           1           1           ?       : ? :           1;
           *           ?           ?       : ? :           -; // Ignore all edges on nextstate
           ?           0           ?       : ? :           -; // Ignore non-triggering clock edge
           ?           ?           *       : ? :           x; // Any NOTIFIER change
  endtable
endprimitive

module LHQ_X1 (D, E, Q);
  input D;
  input E;
  output Q;
  reg NOTIFIER;

  `ifdef NTC
    \seq_LHQ_X1 (IQ, nextstate, E_d, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    buf(nextstate, D_d);

  `else
    \seq_LHQ_X1 (IQ, nextstate, E, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    buf(nextstate, D);

  `endif

  specify
    (D => Q) = (0.1, 0.1);
    (posedge E => (Q +: D)) = (0.1, 0.1);
    `ifdef NTC
      $setuphold(negedge E, negedge D, 0.1, 0.1, NOTIFIER, , ,E_d, D_d);
      $setuphold(negedge E, posedge D, 0.1, 0.1, NOTIFIER, , ,E_d, D_d);
      $width(posedge E, 0.1, 0, NOTIFIER);
    `else
      $setuphold(negedge E, negedge D, 0.1, 0.1, NOTIFIER);
      $setuphold(negedge E, posedge D, 0.1, 0.1, NOTIFIER);
      $width(posedge E, 0.1, 0, NOTIFIER);
    `endif
  endspecify

endmodule

module MUX2_X1 (I0, I1, S, Z);
  input I0;
  input I1;
  input S;
  output Z;

  or(Z, i_24, i_25);
  and(i_24, S, I1);
  and(i_25, i_26, I0);
  not(i_26, S);

  specify
    if((I1 == 1'b0) && (S == 1'b0)) (I0 => Z) = (0.1, 0.1);
    if((I1 == 1'b1) && (S == 1'b0)) (I0 => Z) = (0.1, 0.1);
    if((I0 == 1'b0) && (S == 1'b1)) (I1 => Z) = (0.1, 0.1);
    if((I0 == 1'b1) && (S == 1'b1)) (I1 => Z) = (0.1, 0.1);
    if((I0 == 1'b0) && (I1 == 1'b1)) (S => Z) = (0.1, 0.1);
    if((I0 == 1'b1) && (I1 == 1'b0)) (S => Z) = (0.1, 0.1);
  endspecify

endmodule

module NAND2_X1 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;

  not(ZN, i_28);
  and(i_28, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NAND2_X2 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;

  not(ZN, i_22);
  and(i_22, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NAND3_X1 (A1, A2, A3, ZN);
  input A1;
  input A2;
  input A3;
  output ZN;

  not(ZN, i_14);
  and(i_14, i_15, A3);
  and(i_15, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    (A3 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NAND3_X2 (A1, A2, A3, ZN);
  input A1;
  input A2;
  input A3;
  output ZN;

  not(ZN, i_14);
  and(i_14, i_15, A3);
  and(i_15, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    (A3 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NAND4_X1 (A1, A2, A3, A4, ZN);
  input A1;
  input A2;
  input A3;
  input A4;
  output ZN;

  not(ZN, i_12);
  and(i_12, i_13, A4);
  and(i_13, i_14, A3);
  and(i_14, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    (A3 => ZN) = (0.1, 0.1);
    (A4 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NAND4_X2 (A1, A2, A3, A4, ZN);
  input A1;
  input A2;
  input A3;
  input A4;
  output ZN;

  not(ZN, i_12);
  and(i_12, i_13, A4);
  and(i_13, i_14, A3);
  and(i_14, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    (A3 => ZN) = (0.1, 0.1);
    (A4 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NOR2_X1 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;

  not(ZN, i_16);
  or(i_16, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NOR2_X2 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;

  not(ZN, i_16);
  or(i_16, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NOR3_X1 (A1, A2, A3, ZN);
  input A1;
  input A2;
  input A3;
  output ZN;

  not(ZN, i_8);
  or(i_8, i_9, A3);
  or(i_9, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    (A3 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NOR3_X2 (A1, A2, A3, ZN);
  input A1;
  input A2;
  input A3;
  output ZN;

  not(ZN, i_8);
  or(i_8, i_9, A3);
  or(i_9, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    (A3 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NOR4_X1 (A1, A2, A3, A4, ZN);
  input A1;
  input A2;
  input A3;
  input A4;
  output ZN;

  not(ZN, i_12);
  or(i_12, i_13, A4);
  or(i_13, i_14, A3);
  or(i_14, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    (A3 => ZN) = (0.1, 0.1);
    (A4 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module NOR4_X2 (A1, A2, A3, A4, ZN);
  input A1;
  input A2;
  input A3;
  input A4;
  output ZN;

  not(ZN, i_12);
  or(i_12, i_13, A4);
  or(i_13, i_14, A3);
  or(i_14, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    (A3 => ZN) = (0.1, 0.1);
    (A4 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module OAI21_X1 (A1, A2, B, ZN);
  input A1;
  input A2;
  input B;
  output ZN;

  not(ZN, i_8);
  and(i_8, i_9, B);
  or(i_9, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1)) (B => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0)) (B => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b1)) (B => ZN) = (0.1, 0.1);
  endspecify

endmodule

module OAI21_X2 (A1, A2, B, ZN);
  input A1;
  input A2;
  input B;
  output ZN;

  not(ZN, i_8);
  and(i_8, i_9, B);
  or(i_9, A1, A2);

  specify
    (A1 => ZN) = (0.1, 0.1);
    (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1)) (B => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0)) (B => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b1)) (B => ZN) = (0.1, 0.1);
  endspecify

endmodule

module OAI22_X1 (A1, A2, B1, B2, ZN);
  input A1;
  input A2;
  input B1;
  input B2;
  output ZN;

  not(ZN, i_12);
  and(i_12, i_13, i_14);
  or(i_13, A1, A2);
  or(i_14, B1, B2);

  specify
    if((A2 == 1'b0) && (B1 == 1'b0) && (B2 == 1'b1)) (A1 => ZN) = (0.1, 0.1);
    if((A2 == 1'b0) && (B1 == 1'b1) && (B2 == 1'b0)) (A1 => ZN) = (0.1, 0.1);
    if((A2 == 1'b0) && (B1 == 1'b1) && (B2 == 1'b1)) (A1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (B1 == 1'b0) && (B2 == 1'b1)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (B1 == 1'b1) && (B2 == 1'b0)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (B1 == 1'b1) && (B2 == 1'b1)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1) && (B2 == 1'b0)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0) && (B2 == 1'b0)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b1) && (B2 == 1'b0)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1) && (B1 == 1'b0)) (B2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0) && (B1 == 1'b0)) (B2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b1) && (B1 == 1'b0)) (B2 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module OAI22_X2 (A1, A2, B1, B2, ZN);
  input A1;
  input A2;
  input B1;
  input B2;
  output ZN;

  not(ZN, i_12);
  and(i_12, i_13, i_14);
  or(i_13, A1, A2);
  or(i_14, B1, B2);

  specify
    if((A2 == 1'b0) && (B1 == 1'b0) && (B2 == 1'b1)) (A1 => ZN) = (0.1, 0.1);
    if((A2 == 1'b0) && (B1 == 1'b1) && (B2 == 1'b0)) (A1 => ZN) = (0.1, 0.1);
    if((A2 == 1'b0) && (B1 == 1'b1) && (B2 == 1'b1)) (A1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (B1 == 1'b0) && (B2 == 1'b1)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (B1 == 1'b1) && (B2 == 1'b0)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (B1 == 1'b1) && (B2 == 1'b1)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1) && (B2 == 1'b0)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0) && (B2 == 1'b0)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b1) && (B2 == 1'b0)) (B1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0) && (A2 == 1'b1) && (B1 == 1'b0)) (B2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b0) && (B1 == 1'b0)) (B2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1) && (A2 == 1'b1) && (B1 == 1'b0)) (B2 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module OR2_X1 (A1, A2, Z);
  input A1;
  input A2;
  output Z;

  or(Z, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
  endspecify

endmodule

module OR2_X2 (A1, A2, Z);
  input A1;
  input A2;
  output Z;

  or(Z, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
  endspecify

endmodule

module OR3_X1 (A1, A2, A3, Z);
  input A1;
  input A2;
  input A3;
  output Z;

  or(Z, i_4, A3);
  or(i_4, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
    (A3 => Z) = (0.1, 0.1);
  endspecify

endmodule

module OR3_X2 (A1, A2, A3, Z);
  input A1;
  input A2;
  input A3;
  output Z;

  or(Z, i_4, A3);
  or(i_4, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
    (A3 => Z) = (0.1, 0.1);
  endspecify

endmodule

module OR4_X1 (A1, A2, A3, A4, Z);
  input A1;
  input A2;
  input A3;
  input A4;
  output Z;

  or(Z, i_8, A4);
  or(i_8, i_9, A3);
  or(i_9, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
    (A3 => Z) = (0.1, 0.1);
    (A4 => Z) = (0.1, 0.1);
  endspecify

endmodule

module OR4_X2 (A1, A2, A3, A4, Z);
  input A1;
  input A2;
  input A3;
  input A4;
  output Z;

  or(Z, i_8, A4);
  or(i_8, i_9, A3);
  or(i_9, A1, A2);

  specify
    (A1 => Z) = (0.1, 0.1);
    (A2 => Z) = (0.1, 0.1);
    (A3 => Z) = (0.1, 0.1);
    (A4 => Z) = (0.1, 0.1);
  endspecify

endmodule

primitive \seq_SDFFRNQ_X1  (IQ, RN, nextstate, CLK, NOTIFIER);
  output IQ;
  input RN;
  input nextstate;
  input CLK;
  input NOTIFIER;
  reg IQ;

  table
       // RN   nextstate         CLK    NOTIFIER     : @IQ :          IQ
           ?           0           r           ?       : ? :           0;
           1           1           r           ?       : ? :           1;
           ?           0           *           ?       : 0 :           0; // reduce pessimism
           1           1           *           ?       : 1 :           1; // reduce pessimism
           1           *           ?           ?       : ? :           -; // Ignore all edges on nextstate
           1           ?           n           ?       : ? :           -; // Ignore non-triggering clock edge
           0           ?           ?           ?       : ? :           0; // RN activated
           *           ?           ?           ?       : 0 :           0; // Cover all transitions on RN
           ?           ?           ?           *       : ? :           x; // Any NOTIFIER change
  endtable
endprimitive

module SDFFRNQ_X1 (D, RN, SE, SI, CLK, Q);
  input D;
  input RN;
  input SE;
  input SI;
  input CLK;
  output Q;
  reg NOTIFIER;

  `ifdef NTC
    `ifdef RECREM
      buf (RN_d, RN_di);
    `else
      buf (RN_d, RN);
    `endif
    \seq_SDFFRNQ_X1 (IQ, RN_d, nextstate, CLK_d, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    or(nextstate, i_16, i_17);
    and(i_16, SE_d, SI_d);
    and(i_17, i_18, D_d);
    not(i_18, SE_d);

    // Delayed data/reference logic
    buf(id_15, RN_d);
    and(id_16, id_15, i_23);
    not(i_23, SE_d);
    and(id_17, id_15, SE_d);

    `ifdef TETRAMAX
    `else
      ng_xbuf(xid_15, id_15, 1'b1);
      ng_xbuf(xid_16, id_16, 1'b1);
      ng_xbuf(xid_17, id_17, 1'b1);
    `endif
  `else
    \seq_SDFFRNQ_X1 (IQ, RN, nextstate, CLK, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    or(nextstate, i_16, i_17);
    and(i_16, SE, SI);
    and(i_17, i_18, D);
    not(i_18, SE);

    // Delayed data/reference logic
    buf(id_12, RN);
    and(id_13, id_12, i_22);
    not(i_22, SE);
    and(id_14, id_12, SE);

    `ifdef TETRAMAX
    `else
      ng_xbuf(xid_12, id_12, 1'b1);
      ng_xbuf(xid_13, id_13, 1'b1);
      ng_xbuf(xid_14, id_14, 1'b1);
    `endif
  `endif

  specify
    (posedge CLK => (Q +: D)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0) && (SE == 1'b0) && (SI == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0) && (SE == 1'b0) && (SI == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0) && (SE == 1'b1) && (SI == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0) && (SE == 1'b1) && (SI == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1) && (SE == 1'b0) && (SI == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1) && (SE == 1'b0) && (SI == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1) && (SE == 1'b1) && (SI == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1) && (SE == 1'b1) && (SI == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0) && (SE == 1'b0) && (SI == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0) && (SE == 1'b0) && (SI == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0) && (SE == 1'b1) && (SI == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0) && (SE == 1'b1) && (SI == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1) && (SE == 1'b0) && (SI == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1) && (SE == 1'b0) && (SI == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1) && (SE == 1'b1) && (SI == 1'b0)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1) && (SE == 1'b1) && (SI == 1'b1)) (negedge RN => (Q +: 1'b0)) = (0.1, 0.1);
    `ifdef NTC
      `ifdef RECREM
        $recrem(posedge RN, posedge CLK, 0.1, 0.1, NOTIFIER, , ,RN_di, CLK_d);
      `else
        $hold(posedge CLK, posedge RN, 0.1, NOTIFIER);
        $recovery(posedge RN, posedge CLK, 0.1, NOTIFIER);
      `endif
      $setuphold(posedge CLK &&& (xid_16), negedge D, 0.1, 0.1, NOTIFIER, , ,CLK_d, D_d);
      $setuphold(posedge CLK &&& (xid_16), posedge D, 0.1, 0.1, NOTIFIER, , ,CLK_d, D_d);
      $setuphold(posedge CLK &&& (xid_17), negedge SI, 0.1, 0.1, NOTIFIER, , ,CLK_d, SI_d);
      $setuphold(posedge CLK &&& (xid_17), posedge SI, 0.1, 0.1, NOTIFIER, , ,CLK_d, SI_d);
      $setuphold(posedge CLK, negedge SE, 0.1, 0.1, NOTIFIER, , ,CLK_d, SE_d);
      $setuphold(posedge CLK, posedge SE, 0.1, 0.1, NOTIFIER, , ,CLK_d, SE_d);
      $width(negedge CLK &&& (xid_15), 0.1, 0, NOTIFIER);
      $width(negedge RN, 0.1, 0, NOTIFIER);
      $width(posedge CLK &&& (xid_15), 0.1, 0, NOTIFIER);
    `else
      $hold(posedge CLK, posedge RN, 0.1, NOTIFIER);
      $recovery(posedge RN, posedge CLK, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_13), negedge D, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_13), posedge D, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_14), negedge SI, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_14), posedge SI, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK, negedge SE, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK, posedge SE, 0.1, 0.1, NOTIFIER);
      $width(negedge CLK &&& (xid_12), 0.1, 0, NOTIFIER);
      $width(negedge RN, 0.1, 0, NOTIFIER);
      $width(posedge CLK &&& (xid_12), 0.1, 0, NOTIFIER);
    `endif
  endspecify

endmodule

primitive \seq_SDFFSNQ_X1  (IQ, SN, nextstate, CLK, NOTIFIER);
  output IQ;
  input SN;
  input nextstate;
  input CLK;
  input NOTIFIER;
  reg IQ;

  table
       // SN   nextstate         CLK    NOTIFIER     : @IQ :          IQ
           1           0           r           ?       : ? :           0;
           ?           1           r           ?       : ? :           1;
           1           0           *           ?       : 0 :           0; // reduce pessimism
           ?           1           *           ?       : 1 :           1; // reduce pessimism
           1           *           ?           ?       : ? :           -; // Ignore all edges on nextstate
           1           ?           n           ?       : ? :           -; // Ignore non-triggering clock edge
           0           ?           ?           ?       : ? :           1; // SN activated
           *           ?           ?           ?       : 1 :           1; // Cover all transitions on SN
           ?           ?           ?           *       : ? :           x; // Any NOTIFIER change
  endtable
endprimitive

module SDFFSNQ_X1 (D, SE, SI, SN, CLK, Q);
  input D;
  input SE;
  input SI;
  input SN;
  input CLK;
  output Q;
  reg NOTIFIER;

  `ifdef NTC
    `ifdef RECREM
      buf (SN_d, SN_di);
    `else
      buf (SN_d, SN);
    `endif
    \seq_SDFFSNQ_X1 (IQ, SN_d, nextstate, CLK_d, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    or(nextstate, i_16, i_17);
    and(i_16, SE_d, SI_d);
    and(i_17, i_18, D_d);
    not(i_18, SE_d);

    // Delayed data/reference logic
    buf(id_15, SN_d);
    and(id_16, id_15, i_23);
    not(i_23, SE_d);
    and(id_17, id_15, SE_d);

    `ifdef TETRAMAX
    `else
      ng_xbuf(xid_15, id_15, 1'b1);
      ng_xbuf(xid_16, id_16, 1'b1);
      ng_xbuf(xid_17, id_17, 1'b1);
    `endif
  `else
    \seq_SDFFSNQ_X1 (IQ, SN, nextstate, CLK, NOTIFIER);
    not(IQN, IQ);
    buf(Q, IQ);
    or(nextstate, i_16, i_17);
    and(i_16, SE, SI);
    and(i_17, i_18, D);
    not(i_18, SE);

    // Delayed data/reference logic
    buf(id_12, SN);
    and(id_13, id_12, i_22);
    not(i_22, SE);
    and(id_14, id_12, SE);

    `ifdef TETRAMAX
    `else
      ng_xbuf(xid_12, id_12, 1'b1);
      ng_xbuf(xid_13, id_13, 1'b1);
      ng_xbuf(xid_14, id_14, 1'b1);
    `endif
  `endif

  specify
    (posedge CLK => (Q +: D)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0) && (SE == 1'b0) && (SI == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0) && (SE == 1'b0) && (SI == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0) && (SE == 1'b1) && (SI == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b0) && (SE == 1'b1) && (SI == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1) && (SE == 1'b0) && (SI == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1) && (SE == 1'b0) && (SI == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1) && (SE == 1'b1) && (SI == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b0) && (D == 1'b1) && (SE == 1'b1) && (SI == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0) && (SE == 1'b0) && (SI == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0) && (SE == 1'b0) && (SI == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0) && (SE == 1'b1) && (SI == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b0) && (SE == 1'b1) && (SI == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1) && (SE == 1'b0) && (SI == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1) && (SE == 1'b0) && (SI == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1) && (SE == 1'b1) && (SI == 1'b0)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    if((CLK == 1'b1) && (D == 1'b1) && (SE == 1'b1) && (SI == 1'b1)) (negedge SN => (Q +: 1'b1)) = (0.1, 0.1);
    `ifdef NTC
      `ifdef RECREM
        $recrem(posedge SN, posedge CLK, 0.1, 0.1, NOTIFIER, , ,SN_di, CLK_d);
      `else
        $hold(posedge CLK, posedge SN, 0.1, NOTIFIER);
        $recovery(posedge SN, posedge CLK, 0.1, NOTIFIER);
      `endif
      $setuphold(posedge CLK &&& (xid_16), negedge D, 0.1, 0.1, NOTIFIER, , ,CLK_d, D_d);
      $setuphold(posedge CLK &&& (xid_16), posedge D, 0.1, 0.1, NOTIFIER, , ,CLK_d, D_d);
      $setuphold(posedge CLK &&& (xid_17), negedge SI, 0.1, 0.1, NOTIFIER, , ,CLK_d, SI_d);
      $setuphold(posedge CLK &&& (xid_17), posedge SI, 0.1, 0.1, NOTIFIER, , ,CLK_d, SI_d);
      $setuphold(posedge CLK, negedge SE, 0.1, 0.1, NOTIFIER, , ,CLK_d, SE_d);
      $setuphold(posedge CLK, posedge SE, 0.1, 0.1, NOTIFIER, , ,CLK_d, SE_d);
      $width(negedge CLK &&& (xid_15), 0.1, 0, NOTIFIER);
      $width(negedge SN, 0.1, 0, NOTIFIER);
      $width(posedge CLK &&& (xid_15), 0.1, 0, NOTIFIER);
    `else
      $hold(posedge CLK, posedge SN, 0.1, NOTIFIER);
      $recovery(posedge SN, posedge CLK, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_13), negedge D, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_13), posedge D, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_14), negedge SI, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK &&& (xid_14), posedge SI, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK, negedge SE, 0.1, 0.1, NOTIFIER);
      $setuphold(posedge CLK, posedge SE, 0.1, 0.1, NOTIFIER);
      $width(negedge CLK &&& (xid_12), 0.1, 0, NOTIFIER);
      $width(negedge SN, 0.1, 0, NOTIFIER);
      $width(posedge CLK &&& (xid_12), 0.1, 0, NOTIFIER);
    `endif
  endspecify

endmodule

module TBUF_X1 (EN, I, Z);
  input EN;
  input I;
  output Z;

  bufif0(Z, Z_in, Z_enable);
  not(Z_enable, EN);
  buf(Z_in, I);

  specify
    (EN => Z) = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1);
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module TBUF_X2 (EN, I, Z);
  input EN;
  input I;
  output Z;

  bufif0(Z, Z_in, Z_enable);
  not(Z_enable, EN);
  buf(Z_in, I);

  specify
    (EN => Z) = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1);
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module TBUF_X4 (EN, I, Z);
  input EN;
  input I;
  output Z;

  bufif0(Z, Z_in, Z_enable);
  not(Z_enable, EN);
  buf(Z_in, I);

  specify
    (EN => Z) = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1);
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module TBUF_X8 (EN, I, Z);
  input EN;
  input I;
  output Z;

  bufif0(Z, Z_in, Z_enable);
  not(Z_enable, EN);
  buf(Z_in, I);

  specify
    (EN => Z) = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1);
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module TBUF_X12 (EN, I, Z);
  input EN;
  input I;
  output Z;

  bufif0(Z, Z_in, Z_enable);
  not(Z_enable, EN);
  buf(Z_in, I);

  specify
    (EN => Z) = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1);
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module TBUF_X16 (EN, I, Z);
  input EN;
  input I;
  output Z;

  bufif0(Z, Z_in, Z_enable);
  not(Z_enable, EN);
  buf(Z_in, I);

  specify
    (EN => Z) = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1);
    (I => Z) = (0.1, 0.1);
  endspecify

endmodule

module TIEH (Z);
  output Z;

  buf(Z, 1);
endmodule

module TIEL (ZN);
  output ZN;

  buf(ZN, 0);
endmodule

module XNOR2_X1 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;

  not(ZN, i_38);
  not(i_38, i_39);
  or(i_39, i_40, i_41);
  and(i_40, A1, A2);
  not(i_41, i_42);
  or(i_42, A1, A2);

  specify
    if((A2 == 1'b0)) (A1 => ZN) = (0.1, 0.1);
    if((A2 == 1'b1)) (A1 => ZN) = (0.1, 0.1);
    if((A1 == 1'b0)) (A2 => ZN) = (0.1, 0.1);
    if((A1 == 1'b1)) (A2 => ZN) = (0.1, 0.1);
  endspecify

endmodule

module XOR2_X1 (A1, A2, Z);
  input A1;
  input A2;
  output Z;

  not(Z, i_34);
  or(i_34, i_35, i_36);
  and(i_35, A1, A2);
  not(i_36, i_37);
  or(i_37, A1, A2);

  specify
    if((A2 == 1'b0)) (A1 => Z) = (0.1, 0.1);
    if((A2 == 1'b1)) (A1 => Z) = (0.1, 0.1);
    if((A1 == 1'b0)) (A2 => Z) = (0.1, 0.1);
    if((A1 == 1'b1)) (A2 => Z) = (0.1, 0.1);
  endspecify

endmodule

`ifdef TETRAMAX
`else
  primitive ng_xbuf (o, i, d);
	output o;
	input i, d;
	table
	// i   d   : o
	   0   1   : 0 ;
	   1   1   : 1 ;
	   x   1   : 1 ;
	endtable
  endprimitive
`endif
//
// End of file
//
