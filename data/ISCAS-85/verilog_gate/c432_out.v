// Benchmark "ISCAS-85/c432" written by ABC on Sun Jun 21 14:56:59 2020

module \ISCAS-85/c432  ( 
    G1gat, G4gat, G8gat, G11gat, G14gat, G17gat, G21gat, G24gat, G27gat,
    G30gat, G34gat, G37gat, G40gat, G43gat, G47gat, G50gat, G53gat, G56gat,
    G60gat, G63gat, G66gat, G69gat, G73gat, G76gat, G79gat, G82gat, G86gat,
    G89gat, G92gat, G95gat, G99gat, G102gat, G105gat, G108gat, G112gat,
    G115gat,
    G223gat, G329gat, G370gat, G421gat, G430gat, G431gat, G432gat  );
  input  G1gat, G4gat, G8gat, G11gat, G14gat, G17gat, G21gat, G24gat,
    G27gat, G30gat, G34gat, G37gat, G40gat, G43gat, G47gat, G50gat, G53gat,
    G56gat, G60gat, G63gat, G66gat, G69gat, G73gat, G76gat, G79gat, G82gat,
    G86gat, G89gat, G92gat, G95gat, G99gat, G102gat, G105gat, G108gat,
    G112gat, G115gat;
  output G223gat, G329gat, G370gat, G421gat, G430gat, G431gat, G432gat;
  wire new_n44_, new_n45_, new_n46_, new_n47_, new_n48_, new_n49_, new_n50_,
    new_n51_, new_n52_, new_n53_, new_n54_, new_n55_, new_n56_, new_n57_,
    new_n58_, new_n59_, new_n60_, new_n61_, new_n62_, new_n63_, new_n64_,
    new_n66_, new_n67_, new_n68_, new_n69_, new_n70_, new_n71_, new_n72_,
    new_n73_, new_n74_, new_n75_, new_n76_, new_n77_, new_n78_, new_n79_,
    new_n80_, new_n81_, new_n82_, new_n83_, new_n84_, new_n85_, new_n86_,
    new_n87_, new_n88_, new_n89_, new_n90_, new_n91_, new_n92_, new_n93_,
    new_n94_, new_n95_, new_n96_, new_n97_, new_n98_, new_n99_, new_n100_,
    new_n101_, new_n102_, new_n103_, new_n105_, new_n106_, new_n107_,
    new_n108_, new_n109_, new_n110_, new_n111_, new_n112_, new_n113_,
    new_n114_, new_n115_, new_n116_, new_n117_, new_n118_, new_n119_,
    new_n120_, new_n121_, new_n122_, new_n123_, new_n124_, new_n125_,
    new_n126_, new_n127_, new_n128_, new_n129_, new_n130_, new_n131_,
    new_n132_, new_n133_, new_n134_, new_n135_, new_n136_, new_n137_,
    new_n138_, new_n139_, new_n140_, new_n141_, new_n142_, new_n143_,
    new_n144_, new_n145_, new_n146_, new_n147_, new_n148_, new_n149_,
    new_n150_, new_n151_, new_n152_, new_n153_, new_n154_, new_n155_,
    new_n156_, new_n157_, new_n158_, new_n159_, new_n160_, new_n161_,
    new_n162_, new_n164_, new_n165_, new_n166_, new_n167_, new_n168_,
    new_n169_, new_n170_, new_n171_, new_n172_, new_n173_, new_n174_,
    new_n175_, new_n176_, new_n177_, new_n178_, new_n179_, new_n180_,
    new_n181_, new_n183_, new_n184_, new_n185_, new_n186_, new_n187_,
    new_n188_, new_n189_, new_n190_, new_n191_, new_n192_, new_n193_,
    new_n194_, new_n195_, new_n196_, new_n197_, new_n198_, new_n199_,
    new_n201_, new_n202_, new_n203_, new_n204_, new_n206_, new_n207_,
    new_n208_, new_n209_, new_n210_;
  inv1   g000(.a(G76gat), .O(new_n44_));
  nand2  g001(.a(G82gat), .b(new_n44_), .O(new_n45_));
  inv1   g002(.a(G37gat), .O(new_n46_));
  nand2  g003(.a(G43gat), .b(new_n46_), .O(new_n47_));
  inv1   g004(.a(G63gat), .O(new_n48_));
  nand2  g005(.a(G69gat), .b(new_n48_), .O(new_n49_));
  nand3  g006(.a(new_n49_), .b(new_n47_), .c(new_n45_), .O(new_n50_));
  inv1   g007(.a(new_n50_), .O(new_n51_));
  inv1   g008(.a(G1gat), .O(new_n52_));
  inv1   g009(.a(G11gat), .O(new_n53_));
  aoi22  g010(.a(G17gat), .b(new_n53_), .c(G4gat), .d(new_n52_), .O(new_n54_));
  inv1   g011(.a(G24gat), .O(new_n55_));
  nand2  g012(.a(G30gat), .b(new_n55_), .O(new_n56_));
  inv1   g013(.a(G102gat), .O(new_n57_));
  nand2  g014(.a(G108gat), .b(new_n57_), .O(new_n58_));
  inv1   g015(.a(G89gat), .O(new_n59_));
  nand2  g016(.a(G95gat), .b(new_n59_), .O(new_n60_));
  inv1   g017(.a(G50gat), .O(new_n61_));
  nand2  g018(.a(G56gat), .b(new_n61_), .O(new_n62_));
  nand4  g019(.a(new_n62_), .b(new_n60_), .c(new_n58_), .d(new_n56_), .O(new_n63_));
  inv1   g020(.a(new_n63_), .O(new_n64_));
  nand3  g021(.a(new_n64_), .b(new_n54_), .c(new_n51_), .O(G223gat));
  inv1   g022(.a(G86gat), .O(new_n66_));
  aoi22  g023(.a(G108gat), .b(new_n57_), .c(G30gat), .d(new_n55_), .O(new_n67_));
  aoi22  g024(.a(G95gat), .b(new_n59_), .c(G56gat), .d(new_n61_), .O(new_n68_));
  nand3  g025(.a(new_n68_), .b(new_n67_), .c(new_n54_), .O(new_n69_));
  oai21  g026(.a(new_n69_), .b(new_n50_), .c(G76gat), .O(new_n70_));
  nand3  g027(.a(new_n70_), .b(new_n66_), .c(G82gat), .O(new_n71_));
  inv1   g028(.a(G47gat), .O(new_n72_));
  oai21  g029(.a(new_n69_), .b(new_n50_), .c(G37gat), .O(new_n73_));
  nand3  g030(.a(new_n73_), .b(new_n72_), .c(G43gat), .O(new_n74_));
  inv1   g031(.a(G73gat), .O(new_n75_));
  oai21  g032(.a(new_n69_), .b(new_n50_), .c(G63gat), .O(new_n76_));
  nand3  g033(.a(new_n76_), .b(new_n75_), .c(G69gat), .O(new_n77_));
  nand3  g034(.a(new_n77_), .b(new_n74_), .c(new_n71_), .O(new_n78_));
  inv1   g035(.a(new_n78_), .O(new_n79_));
  inv1   g036(.a(G8gat), .O(new_n80_));
  inv1   g037(.a(G34gat), .O(new_n81_));
  inv1   g038(.a(G4gat), .O(new_n82_));
  aoi21  g039(.a(G223gat), .b(G1gat), .c(new_n82_), .O(new_n83_));
  inv1   g040(.a(G30gat), .O(new_n84_));
  aoi21  g041(.a(G223gat), .b(G24gat), .c(new_n84_), .O(new_n85_));
  aoi22  g042(.a(new_n85_), .b(new_n81_), .c(new_n83_), .d(new_n80_), .O(new_n86_));
  inv1   g043(.a(G21gat), .O(new_n87_));
  inv1   g044(.a(G17gat), .O(new_n88_));
  aoi21  g045(.a(G223gat), .b(G11gat), .c(new_n88_), .O(new_n89_));
  nand4  g046(.a(new_n64_), .b(new_n62_), .c(new_n54_), .d(new_n51_), .O(new_n90_));
  inv1   g047(.a(new_n62_), .O(new_n91_));
  oai21  g048(.a(new_n69_), .b(new_n50_), .c(new_n91_), .O(new_n92_));
  inv1   g049(.a(G60gat), .O(new_n93_));
  nand2  g050(.a(new_n93_), .b(G56gat), .O(new_n94_));
  aoi21  g051(.a(new_n92_), .b(new_n90_), .c(new_n94_), .O(new_n95_));
  aoi21  g052(.a(new_n89_), .b(new_n87_), .c(new_n95_), .O(new_n96_));
  inv1   g053(.a(G99gat), .O(new_n97_));
  inv1   g054(.a(G112gat), .O(new_n98_));
  inv1   g055(.a(G108gat), .O(new_n99_));
  aoi21  g056(.a(G223gat), .b(G102gat), .c(new_n99_), .O(new_n100_));
  inv1   g057(.a(G95gat), .O(new_n101_));
  aoi21  g058(.a(G223gat), .b(G89gat), .c(new_n101_), .O(new_n102_));
  aoi22  g059(.a(new_n102_), .b(new_n97_), .c(new_n100_), .d(new_n98_), .O(new_n103_));
  nand4  g060(.a(new_n103_), .b(new_n96_), .c(new_n86_), .d(new_n79_), .O(G329gat));
  inv1   g061(.a(G27gat), .O(new_n105_));
  nand2  g062(.a(G329gat), .b(G21gat), .O(new_n106_));
  nand3  g063(.a(new_n106_), .b(new_n89_), .c(new_n105_), .O(new_n107_));
  inv1   g064(.a(G40gat), .O(new_n108_));
  nand2  g065(.a(G329gat), .b(G34gat), .O(new_n109_));
  nand3  g066(.a(new_n109_), .b(new_n85_), .c(new_n108_), .O(new_n110_));
  inv1   g067(.a(G14gat), .O(new_n111_));
  nand2  g068(.a(G329gat), .b(G8gat), .O(new_n112_));
  nand3  g069(.a(new_n112_), .b(new_n83_), .c(new_n111_), .O(new_n113_));
  nand3  g070(.a(new_n113_), .b(new_n110_), .c(new_n107_), .O(new_n114_));
  inv1   g071(.a(new_n114_), .O(new_n115_));
  inv1   g072(.a(G115gat), .O(new_n116_));
  inv1   g073(.a(new_n100_), .O(new_n117_));
  aoi21  g074(.a(G329gat), .b(G112gat), .c(new_n117_), .O(new_n118_));
  nand2  g075(.a(G223gat), .b(G89gat), .O(new_n119_));
  nand3  g076(.a(new_n119_), .b(new_n97_), .c(G95gat), .O(new_n120_));
  inv1   g077(.a(new_n120_), .O(new_n121_));
  inv1   g078(.a(G329gat), .O(new_n122_));
  nand2  g079(.a(new_n122_), .b(new_n121_), .O(new_n123_));
  inv1   g080(.a(G105gat), .O(new_n124_));
  nand2  g081(.a(new_n102_), .b(new_n124_), .O(new_n125_));
  aoi21  g082(.a(G329gat), .b(new_n120_), .c(new_n125_), .O(new_n126_));
  aoi22  g083(.a(new_n126_), .b(new_n123_), .c(new_n118_), .d(new_n116_), .O(new_n127_));
  inv1   g084(.a(G53gat), .O(new_n128_));
  nand2  g085(.a(new_n73_), .b(G43gat), .O(new_n129_));
  inv1   g086(.a(new_n129_), .O(new_n130_));
  nand2  g087(.a(G329gat), .b(G47gat), .O(new_n131_));
  inv1   g088(.a(new_n74_), .O(new_n132_));
  nand2  g089(.a(G223gat), .b(G11gat), .O(new_n133_));
  nand3  g090(.a(new_n133_), .b(new_n87_), .c(G17gat), .O(new_n134_));
  nand2  g091(.a(new_n92_), .b(new_n90_), .O(new_n135_));
  inv1   g092(.a(new_n94_), .O(new_n136_));
  nand2  g093(.a(new_n136_), .b(new_n135_), .O(new_n137_));
  nand2  g094(.a(G223gat), .b(G102gat), .O(new_n138_));
  nand3  g095(.a(new_n138_), .b(new_n98_), .c(G108gat), .O(new_n139_));
  nand4  g096(.a(new_n120_), .b(new_n139_), .c(new_n137_), .d(new_n134_), .O(new_n140_));
  inv1   g097(.a(new_n140_), .O(new_n141_));
  nand4  g098(.a(new_n141_), .b(new_n86_), .c(new_n79_), .d(new_n132_), .O(new_n142_));
  nand4  g099(.a(new_n142_), .b(new_n131_), .c(new_n130_), .d(new_n128_), .O(new_n143_));
  nand4  g100(.a(new_n141_), .b(new_n95_), .c(new_n86_), .d(new_n79_), .O(new_n144_));
  nand2  g101(.a(G329gat), .b(new_n137_), .O(new_n145_));
  inv1   g102(.a(G56gat), .O(new_n146_));
  nor2   g103(.a(G66gat), .b(new_n146_), .O(new_n147_));
  nand4  g104(.a(new_n147_), .b(new_n145_), .c(new_n144_), .d(new_n135_), .O(new_n148_));
  and2   g105(.a(new_n148_), .b(new_n143_), .O(new_n149_));
  inv1   g106(.a(G92gat), .O(new_n150_));
  nand2  g107(.a(new_n70_), .b(G82gat), .O(new_n151_));
  inv1   g108(.a(new_n151_), .O(new_n152_));
  nand2  g109(.a(G329gat), .b(G86gat), .O(new_n153_));
  nand3  g110(.a(new_n153_), .b(new_n152_), .c(new_n150_), .O(new_n154_));
  inv1   g111(.a(G79gat), .O(new_n155_));
  nand2  g112(.a(new_n76_), .b(G69gat), .O(new_n156_));
  inv1   g113(.a(new_n156_), .O(new_n157_));
  nand2  g114(.a(G329gat), .b(G73gat), .O(new_n158_));
  inv1   g115(.a(new_n77_), .O(new_n159_));
  nand4  g116(.a(new_n141_), .b(new_n86_), .c(new_n79_), .d(new_n159_), .O(new_n160_));
  nand4  g117(.a(new_n160_), .b(new_n158_), .c(new_n157_), .d(new_n155_), .O(new_n161_));
  and2   g118(.a(new_n161_), .b(new_n154_), .O(new_n162_));
  nand4  g119(.a(new_n162_), .b(new_n149_), .c(new_n127_), .d(new_n115_), .O(G370gat));
  nand2  g120(.a(new_n112_), .b(new_n83_), .O(new_n164_));
  aoi21  g121(.a(G370gat), .b(G14gat), .c(new_n164_), .O(new_n165_));
  nand2  g122(.a(G370gat), .b(G66gat), .O(new_n166_));
  nand2  g123(.a(G223gat), .b(G50gat), .O(new_n167_));
  nand2  g124(.a(new_n167_), .b(G56gat), .O(new_n168_));
  aoi21  g125(.a(G329gat), .b(G60gat), .c(new_n168_), .O(new_n169_));
  nand2  g126(.a(new_n169_), .b(new_n166_), .O(new_n170_));
  nand2  g127(.a(new_n131_), .b(new_n130_), .O(new_n171_));
  inv1   g128(.a(new_n171_), .O(new_n172_));
  nand2  g129(.a(G370gat), .b(G53gat), .O(new_n173_));
  nand2  g130(.a(new_n173_), .b(new_n172_), .O(new_n174_));
  nand2  g131(.a(new_n106_), .b(new_n89_), .O(new_n175_));
  inv1   g132(.a(new_n175_), .O(new_n176_));
  nand2  g133(.a(G370gat), .b(G27gat), .O(new_n177_));
  nand2  g134(.a(new_n177_), .b(new_n176_), .O(new_n178_));
  and2   g135(.a(new_n109_), .b(new_n85_), .O(new_n179_));
  nand2  g136(.a(G370gat), .b(G40gat), .O(new_n180_));
  nand2  g137(.a(new_n180_), .b(new_n179_), .O(new_n181_));
  nand4  g138(.a(new_n181_), .b(new_n178_), .c(new_n174_), .d(new_n170_), .O(G430gat));
  inv1   g139(.a(G430gat), .O(new_n183_));
  nand2  g140(.a(new_n153_), .b(new_n152_), .O(new_n184_));
  inv1   g141(.a(new_n184_), .O(new_n185_));
  nand2  g142(.a(G370gat), .b(G92gat), .O(new_n186_));
  nand2  g143(.a(new_n186_), .b(new_n185_), .O(new_n187_));
  nand2  g144(.a(G370gat), .b(G105gat), .O(new_n188_));
  oai21  g145(.a(new_n122_), .b(new_n97_), .c(new_n102_), .O(new_n189_));
  inv1   g146(.a(new_n189_), .O(new_n190_));
  nand2  g147(.a(new_n190_), .b(new_n188_), .O(new_n191_));
  nand2  g148(.a(new_n158_), .b(new_n157_), .O(new_n192_));
  inv1   g149(.a(new_n192_), .O(new_n193_));
  nand2  g150(.a(G370gat), .b(G79gat), .O(new_n194_));
  nand2  g151(.a(new_n194_), .b(new_n193_), .O(new_n195_));
  nand2  g152(.a(G370gat), .b(G115gat), .O(new_n196_));
  nand2  g153(.a(new_n196_), .b(new_n118_), .O(new_n197_));
  nand4  g154(.a(new_n197_), .b(new_n195_), .c(new_n191_), .d(new_n187_), .O(new_n198_));
  inv1   g155(.a(new_n198_), .O(new_n199_));
  aoi21  g156(.a(new_n199_), .b(new_n183_), .c(new_n165_), .O(G421gat));
  and2   g157(.a(new_n181_), .b(new_n178_), .O(new_n201_));
  aoi21  g158(.a(new_n169_), .b(new_n166_), .c(new_n195_), .O(new_n202_));
  nand3  g159(.a(new_n202_), .b(new_n181_), .c(new_n174_), .O(new_n203_));
  nand4  g160(.a(new_n186_), .b(new_n174_), .c(new_n170_), .d(new_n185_), .O(new_n204_));
  nand3  g161(.a(new_n204_), .b(new_n203_), .c(new_n201_), .O(G431gat));
  aoi21  g162(.a(new_n186_), .b(new_n185_), .c(new_n191_), .O(new_n206_));
  nand3  g163(.a(new_n206_), .b(new_n181_), .c(new_n174_), .O(new_n207_));
  inv1   g164(.a(new_n174_), .O(new_n208_));
  inv1   g165(.a(new_n178_), .O(new_n209_));
  aoi21  g166(.a(new_n181_), .b(new_n208_), .c(new_n209_), .O(new_n210_));
  nand3  g167(.a(new_n210_), .b(new_n207_), .c(new_n203_), .O(G432gat));
endmodule


