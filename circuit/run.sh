
####### Question 1: can we read circuits? 
##### CKT files these files pass the test 
# python main_saeed.py -ckt ../data/ckt/c17.ckt        -func test 
# python main_saeed.py -ckt ../data/ckt/c1.ckt         -func  test
# python main_saeed.py -ckt ../data/ckt/c2.ckt         -func  test
# python main_saeed.py -ckt ../data/ckt/c3.ckt         -func  test
# python main_saeed.py -ckt ../data/ckt/c4.ckt         -func  test
# python main_saeed.py -ckt ../data/ckt/FA_NAND.ckt    -func  test
# python main_saeed.py -ckt ../data/ckt/c1355.ckt        -func  test 
# python main_saeed.py -ckt ../data/ckt/c432.ckt         -func  test
# python main_saeed.py -ckt ../data/ckt/c499.ckt         -func  test
# python main_saeed.py -ckt ../data/ckt/c6288.ckt        -func  test  
# python main_saeed.py -ckt ../data/ckt/c880.ckt         -func  test 
# python main_saeed.py -ckt ../data/ckt/cmini.ckt         -func  test 
# python main_saeed.py -ckt ../data/ckt/x3mult.ckt         -func  test 

###### VERILOG FILES
## ISCAS85 -- all pass the test
# python3 main_saeed.py -ckt ../data/verilog/c1355.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c5315.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c1908.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c2670.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c880.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c7552.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c499.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c6288.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c17.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c3540.v -func test
# python3 main_saeed.py -ckt ../data/verilog/c432.v -func test

## EPFL -- simple synthesis
# # python3 main_saeed.py -ckt ../data/verilog/ctrl_syn.v -func test #----> bug here
# # python3 main_saeed.py -ckt ../data/verilog/router_syn.v -func test #----> bug here
# python3 main_saeed.py -ckt ../data/verilog/priority_syn.v -func test
# python3 main_saeed.py -ckt ../data/verilog/int2float_syn.v -func test
# python3 main_saeed.py -ckt ../data/verilog/dec_syn.v -func test
# python3 main_saeed.py -ckt ../data/verilog/cavlc_syn.v -func test
# python3 main_saeed.py -ckt ../data/verilog/adder_syn.v -func test
# # python3 main_saeed.py -ckt ../data/verilog/i2c_syn.v -func test # ----> bug here
# python3 main_saeed.py -ckt ../data/verilog/bar_syn.v -func test
# python3 main_saeed.py -ckt ../data/verilog/sin_syn.v -func test
# python3 main_saeed.py -ckt ../data/verilog/max_syn.v -func test
# python3 main_saeed.py -ckt ../data/verilog/arbiter_syn.v -func test
# python3 main_saeed.py -ckt ../data/verilog/voter_syn.v -func test
# # python3 main_saeed.py -ckt ../data/verilog/square_syn.v -func test # ---> bug here
# # python3 main_saeed.py -ckt ../data/verilog/sqrt_syn.v -func test # ---- > takes so much time  
# python3 main_saeed.py -ckt ../data/verilog/multiplier_syn.v -func test
# python3 main_saeed.py -ckt ../data/verilog/log2_syn.v -func test 
# # python3 main_saeed.py -ckt ../data/verilog/mem_ctrl_syn.v -func test # ----> bug here
# # python3 main_saeed.py -ckt ../data/verilog/div_syn.v -func test # ---> didn't test it 
# # python3 main_saeed.py -ckt ../data/verilog/hyp_syn.v -func test # ---> didn't test ut

## EPFL --- synV different synthesis versions for a sample of the EPFL circuits
## All below passed
# python3 main_saeed.py -ckt ../data/verilog/priority_synV0.v -func test
# python3 main_saeed.py -ckt ../data/verilog/int2float_synV0.v -func test
# python3 main_saeed.py -ckt ../data/verilog/dec_synV0.v -func test
# python3 main_saeed.py -ckt ../data/verilog/cavlc_synV0.v -func test
# python3 main_saeed.py -ckt ../data/verilog/adder_synV0.v -func test
# python3 main_saeed.py -ckt ../data/verilog/priority_synV1.v -func test
# python3 main_saeed.py -ckt ../data/verilog/int2float_synV1.v -func test
# python3 main_saeed.py -ckt ../data/verilog/dec_synV1.v -func test
# python3 main_saeed.py -ckt ../data/verilog/cavlc_synV1.v -func test
# python3 main_saeed.py -ckt ../data/verilog/adder_synV1.v -func test
# python3 main_saeed.py -ckt ../data/verilog/priority_synV2.v -func test
# python3 main_saeed.py -ckt ../data/verilog/int2float_synV2.v -func test
# python3 main_saeed.py -ckt ../data/verilog/dec_synV2.v -func test
# python3 main_saeed.py -ckt ../data/verilog/cavlc_synV2.v -func test
# python3 main_saeed.py -ckt ../data/verilog/adder_synV2.v -func test


# python3 main_saeed.py -ckt ../data/ckt/c2.ckt -func test1
# python3 main_saeed.py -ckt ../data/ckt/c2.ckt -func test2 -tp 3
# python3 main_saeed.py -ckt ../data/ckt/c2.ckt -func test3
# python3 main_saeed.py -ckt ../data/ckt/c17.ckt -func test4 -tp 2
# python3 main_saeed.py -v ../data/verilog/c4.v -func test1
# python3 main_saeed.py -ckt ../data/ckt/c1.ckt -func test0
# python3 main_saeed.py -ckt ../data/ckt/c1.ckt -func nei




