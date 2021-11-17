
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

# read -p 'Test counts? ' TEST_COUNT
# python3 main_saeed.py -ckt  ../data/ckt/c1.ckt -func pfsp -tp $TEST_COUNT
# python3 main_saeed.py -ckt  ../data/ckt/c1.ckt -func ppsf -tp $TEST_COUNT
# python3 main_saeed.py -ckt  ../data/ckt/c3.ckt -func pfs-vs-ppsf -tp $TEST_COUNT
# python3 main_saeed.py -ckt ../data/ckt/c3.ckt -func pfs -tp $TEST_COUNT

# python3 FC_test.py -ckt ../data/ckt/c432.ckt -func fctp
# python3 FC_test.py -ckt ../data/ckt/c1.ckt -func fcfs

# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "002"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "003"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "004"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "005"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "006"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "007"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "008"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "009"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "010"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "011"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "012"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "013"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "014"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "015"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "016"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "017"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "018"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "019"  -code 'g'

# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc -tp 500 -op_fname "001"  -code 'g'
# python3 main_saeed.py -ckt ../data/verilog/c432_synV0.v -func tpfc-fig -tp 500 -op_fname "001" -code 'g'

python3 main_saeed.py -v ../data/verilog/c432_synV0.v -func fc-es-fig -tpLoad 1000 -tp 100 -times 15 -code 'fig'