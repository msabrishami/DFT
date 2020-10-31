# Circuit Test Package
This package is written to cover different methods used for circuit netlists (graphs). The package reads the standard format circuit netlists and can perfom different *design for test* (DFT) operations, including: 
- Gate level logical simulation
- Fault simulation (PFS, DFS)
- Dominancy and equivalency relations
- Systematic fault dropping (CPT)
- Fault based ATPG (different versions of D-Algorithm and PODEM)
- Full circuit ATPG 
- Different controllability and observability measurements (e.g. SCOAP)
- Translation between different formats of circuits (.bench, .verilog, .ckt)

The package is capable of producing test-related datasets later used in down stream machine learning applications. 

## Developers and Affiliation: <br />
The package was first developed by a group of University of Southern California (USC) computer engineering graduate students as a joint research project with <cite>[**The System Power Optimization and Regulation Technology (SPORT) Lab**][1]</cite>. <br />

**Repository manager:** <br />
<cite>[M. Saeed Abrishami][10]</cite>  <br />

**Main contributers:**  <br /> 
<cite>[Amir Erfan Eshratifar][19]</cite>  <br />


**Graduate students who worked with this platform during their EE658 course** *(equal contribution):* <br /> 
Jiayi Wang <cite>[Linkedin][13]</cite>  <br />
Yang Shen  <cite>[LinkedIn][14]</cite> <br />
Jiaming Li <cite>[LinkedIn][15]</cite> <br />
Han Zhang  <cite>[LinkedIn][16]</cite>  <br />
Shubo Li   <cite>[LinkedIn][17]</cite>  <br />
Yida Yan <cite>[LinkedIn][18]</cite>  <br />

**Advisors:** <br />
<cite>[Prof. Massoud Pedram][11]</cite>  <br />
<cite>[Prof. Shahin Nazarian][12]</cite>  <br />

[1]: http://sportlab.usc.edu/ 
[10]: http://sportlab.usc.edu/~msabrishami/
[11]: http://sportlab.usc.edu/~shahin/
[12]: http://www.mpedram.com/
[13]: https://www.linkedin.com/in/jiayi-wang-a40473101/
[14]: https://www.linkedin.com/in/yshen245/
[15]: https://www.linkedin.com/in/jiaming-li-73b873191/
[16]: https://www.linkedin.com/in/han-zhang-usc/
[17]: https://www.linkedin.com/in/shubo-li-760991193/
[18]: https://www.linkedin.com/in/yida-yan-489b06191/
[19]: http://amirerfan.com/

## Setup Environment
Python3

## Circuit Input Format
The initial implementation was based on a modified version of *.CKT*, referred as *CKT658* [reference]. A translator is availabel to convert standard *.bench* format to *CKT658* and implemented inside the platform. 
`translator.py`
<!--This part is written by Yida-->


## Run code

At the command line, type below commands:

`cd src/`

`python3 main.py`

To run ATPG, type command:

`python3 atpg_v0.py c17`

c17 can be replaced with other circuits' name such as c432, c880, c1355...
  
## source codes:  

`classdef.py` is the source code ***class node***, it specifies attributes and methods for a node.

<!--This part is written by Jiaming and Shubo -->

`translator.py` is the source code to translate `bench` file to `ckt`
<!--This part is written by Yida-->

`cread.py` is the source code to read input ckt file and instatiate ***class node***
<!--This part is written by Jiaming and Shubo-->

`lev.py` is the source code for levelization of nodes
<!--This part is written by Han and Yang-->

`logicsim.py` is the source code for logic simulation
<!--This part is written by Han and Yang-->

`flr.py` is the source code for fault list reduction. The function is tested with *c17* circuit
<!--This part is written by Jiaming-->

`dfs.py` is the source code for deductive fault simulation
<!--This part is written by Shubo-->

`pfs.py` is the source code for parallel fault simulation. The faults dectected by given input sequence is generated to an output file called `pfsoutput.txt`. The function is tested with *c17* circuit
<!--This part is written by Han and Yang-->

`faultdict_gen.py` is the source code for generating fault dictionary. Generate a `full_fault_list.txt` for `pfs.py` to get the fault dictioanry. Output result in `fault_dict.txt`. PS: Changed pfs parameter format to achieve this function. Return a dictionary for Equvilance checking. The function is tested with *c17* circuit -- Problem: different size of bianry????
<!--This part is written by Jiaming-->

`mini_faultlist_gen.py` is the source code for generating minimum size of fault list. Uitilize faut list from flr and fault dictionary to get minimum fault list. Output result of mini fault list is in `mini_faultlist.txt`.Output result of reduced fault list is in `reduce_faultlist_file` PS: The function is tested with *c17* circuit <!--This part is written by Han-->

`pattern_information.py` use greedy to find the reduced test pattern, always find the test pattern that can detect the most remaining fault, the program will end when all the faults are detected, time complexity O(V + E) <!--This part is written by Jiayi-->


`equv_domain.py` is the source code for generating all the equivalence and domainance by going through the fault dictionary. PS: The function is tested with *c17* circuit <!--This part is written by Shubo-->

`checker.py` is the script to check the fault coverage of D algrithm and Podem. For smaller circuits: If D / Podem algorithm succceeded, it checks if the test patterns D / Podem algorithm generated are valid (found in fault dictionary). If D / Podem algorithm failed, it checks if the fault is really undetectable by checking the fault dictionary. For bigger circuits, since creating a fault dictionary takes too long time, it simply performs checks on the detected faults and its corresponding patterns returned by D / Podem, using parallel fault simulation to check if those patterns are valid for its fault therefore proves the correctness of P / Podem.<!--This part is written by Yang-->

`d_alg.py` is the source code for d algorithm in recursive manner. <!--This part is written by Han (mainly) and Yang-->

`main.py` is the source code for main function for testing. `c17.ckt658` is used as testing input
<!--This part is written by all of us-->

`MT.cpp` is the source code for multithreading fault dictionary generation. Each thread calls `parallel_processing.py` and generate a partial fault dictionary. This could speed up the fault dictionary generation significantly.

To run this code, type command:

`g++ MT.cpp -o MT -pthread && ./MT [CIRCUIT_NAME]`

<!--Possible Update: makefile-->

`atpg_vo.py` is the source code for implementtation of ATPG. Given circuit, atpg will return fault coverage, timing and respondning the number of input pattern. The detail explanations have been written in atpg_v0_report.pdf in documents repo  <!--This part is written by Han-->   

## Repository Structures

source codes are included in `src/` folder

input & output files are included in `tests/` folder

circuit file. like `.ckt` and `.bench`, and description files of the circuits are included in `circuits/` folder

fault dictionaries are included in `fault_dic/` folder

documents includes some rerferences and reports
