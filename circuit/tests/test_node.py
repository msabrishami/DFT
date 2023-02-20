import pytest
from ..node import node

#TODO: test with multiple unodes if applicable

@pytest.mark.IPT
def test_ipt_imply():
    ipt_node = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    
    ipt_node.imply(1)
    assert ipt_node.value == 1

    ipt_node.imply(0)
    assert ipt_node.value == 0

@pytest.mark.IPT
def test_ipt_imply_b():
    ipt_node = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    
    # ipt_node.imply_b([1])
    # assert ipt_node.value == [1]

    # ipt_node.imply_b([0])
    # assert ipt_node.value == [0]

    # ipt_node.imply_b([1,0,1,0])
    # assert ipt_node.value == [1,0,1,0]

@pytest.mark.BUFF
def test_buff_imply():
    ipt_node = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    buff_node = node.BUFF(node.ntype.GATE, node.gtype.BUFF, "2")
    
    buff_node.add_unode(ipt_node)
    ipt_node.add_dnode(buff_node)

    ipt_node.imply(1)
    buff_node.imply()
    assert buff_node.value == 1
    
    ipt_node.imply(0)
    buff_node.imply()
    assert buff_node.value == 0

@pytest.mark.BUFF
def test_buff_imply_b():
    ipt_node = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    buff_node = node.BUFF(node.ntype.GATE, node.gtype.BUFF, "2")
    
    buff_node.add_unode(ipt_node)
    ipt_node.add_dnode(buff_node)

@pytest.mark.NOT
def test_not_imply():
    ipt_node = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    not_node = node.NOT(node.ntype.GATE, node.gtype.NOT, "2")
    
    not_node.add_unode(ipt_node)
    ipt_node.add_dnode(not_node)

    ipt_node.imply(1)
    not_node.imply()
    assert not_node.value == 0
    
    ipt_node.imply(0)
    not_node.imply()
    assert not_node.value == 1

@pytest.mark.NOT
def test_not_imply_b():
    ipt_node = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    not_node = node.NOT(node.ntype.GATE, node.gtype.NOT, "2")
    
    not_node.add_unode(ipt_node)
    ipt_node.add_dnode(not_node)

    ipt_node.imply_b(1)
    not_node.imply_b()
    print(not_node.value)
    # assert not_node.value == 0
    
    # ipt_node.imply_b(0)
    # not_node.imply_b()
    # assert not_node.value == 1

    # ipt_node.imply_b(10101)
    # not_node.imply_b()
    # assert not_node.value == 1010

@pytest.mark.OR
def test_or_imply():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    or_node = node.OR(node.ntype.GATE, node.gtype.OR, "3")
    
    or_node.add_unode(ipt_node1)
    or_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(or_node)
    ipt_node2.add_dnode(or_node)

    ipt_node1.imply(1)
    ipt_node2.imply(1)
    or_node.imply()
    assert or_node.value == 1

    ipt_node1.imply(1)
    ipt_node2.imply(0)
    or_node.imply()
    assert or_node.value == 1

    ipt_node1.imply(0)
    ipt_node2.imply(1)
    or_node.imply()
    assert or_node.value == 1

    ipt_node1.imply(0)
    ipt_node2.imply(0)
    or_node.imply()
    assert or_node.value == 0

@pytest.mark.OR
def test_or_imply_b():
    pass

@pytest.mark.NOR
def test_nor_imply():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    nor_node = node.NOR(node.ntype.GATE, node.gtype.NOR, "3")
    
    nor_node.add_unode(ipt_node1)
    nor_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(nor_node)
    ipt_node2.add_dnode(nor_node)

    ipt_node1.imply(1)
    ipt_node2.imply(1)
    nor_node.imply()
    assert nor_node.value == 0

    ipt_node1.imply(1)
    ipt_node2.imply(0)
    nor_node.imply()
    assert nor_node.value == 0

    ipt_node1.imply(0)
    ipt_node2.imply(1)
    nor_node.imply()
    assert nor_node.value == 0

    ipt_node1.imply(0)
    ipt_node2.imply(0)
    nor_node.imply()
    assert nor_node.value == 1

@pytest.mark.NOR
def test_nor_imply_b():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    nor_node = node.NOR(node.ntype.GATE, node.gtype.NOR, "3")
    
    nor_node.add_unode(ipt_node1)
    nor_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(nor_node)
    ipt_node2.add_dnode(nor_node)

    # ipt_node1.imply(1)
    # ipt_node2.imply(1)
    # nor_node.imply()
    # assert nor_node.value == 0

    # ipt_node1.imply(1)
    # ipt_node2.imply(0)
    # nor_node.imply()
    # assert nor_node.value == 0

    # ipt_node1.imply(0)
    # ipt_node2.imply(1)
    # nor_node.imply()
    # assert nor_node.value == 0

    # ipt_node1.imply(0)
    # ipt_node2.imply(0)
    # nor_node.imply()
    # assert nor_node.value == 1

@pytest.mark.AND
def test_and_imply():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    and_node = node.AND(node.ntype.GATE, node.gtype.AND, "3")
    
    and_node.add_unode(ipt_node1)
    and_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(and_node)
    ipt_node2.add_dnode(and_node)

    ipt_node1.imply(1)
    ipt_node2.imply(1)
    and_node.imply()
    assert and_node.value == 1

    ipt_node1.imply(1)
    ipt_node2.imply(0)
    and_node.imply()
    assert and_node.value == 0

    ipt_node1.imply(0)
    ipt_node2.imply(1)
    and_node.imply()
    assert and_node.value == 0

    ipt_node1.imply(0)
    ipt_node2.imply(0)
    and_node.imply()
    assert and_node.value == 0

@pytest.mark.AND
def test_and_imply_b():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    and_node = node.AND(node.ntype.GATE, node.gtype.AND, "3")
    
    and_node.add_unode(ipt_node1)
    and_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(and_node)
    ipt_node2.add_dnode(and_node)
    pass

@pytest.mark.NAND
def test_nand_imply():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    nand_node = node.NAND(node.ntype.GATE, node.gtype.NAND, "3")
    
    nand_node.add_unode(ipt_node1)
    nand_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(nand_node)
    ipt_node2.add_dnode(nand_node)

    ipt_node1.imply(1)
    ipt_node2.imply(1)
    nand_node.imply()
    assert nand_node.value == 0

    ipt_node1.imply(1)
    ipt_node2.imply(0)
    nand_node.imply()
    assert nand_node.value == 1

    ipt_node1.imply(0)
    ipt_node2.imply(1)
    nand_node.imply()
    assert nand_node.value == 1

    ipt_node1.imply(0)
    ipt_node2.imply(0)
    nand_node.imply()
    assert nand_node.value == 1

@pytest.mark.NAND
def test_nand_imply_b():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    nand_node = node.AND(node.ntype.GATE, node.gtype.NAND, "3")
    
    nand_node.add_unode(ipt_node1)
    nand_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(nand_node)
    ipt_node2.add_dnode(nand_node)
    pass

@pytest.mark.XOR
def test_xor_imply():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    xor_node = node.XOR(node.ntype.GATE, node.gtype.XOR, "3")
    
    xor_node.add_unode(ipt_node1)
    xor_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(xor_node)
    ipt_node2.add_dnode(xor_node)

    ipt_node1.imply(1)
    ipt_node2.imply(1)
    xor_node.imply()
    assert xor_node.value == 0

    ipt_node1.imply(1)
    ipt_node2.imply(0)
    xor_node.imply()
    assert xor_node.value == 1

    ipt_node1.imply(0)
    ipt_node2.imply(1)
    xor_node.imply()
    assert xor_node.value == 1

    ipt_node1.imply(0)
    ipt_node2.imply(0)
    xor_node.imply()
    assert xor_node.value == 0

@pytest.mark.XOR
def test_xor_imply_b():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    xor_node = node.XOR(node.ntype.GATE, node.gtype.XOR, "3")
    
    xor_node.add_unode(ipt_node1)
    xor_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(xor_node)
    ipt_node2.add_dnode(xor_node)
    pass

@pytest.mark.XNOR
def test_xnor_imply():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    xnor_node = node.XNOR(node.ntype.GATE, node.gtype.XNOR, "3")
    
    xnor_node.add_unode(ipt_node1)
    xnor_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(xnor_node)
    ipt_node2.add_dnode(xnor_node)

    ipt_node1.imply(1)
    ipt_node2.imply(1)
    xnor_node.imply()
    assert xnor_node.value ==  1

    ipt_node1.imply(1)
    ipt_node2.imply(0)
    xnor_node.imply()
    assert xnor_node.value == 0

    ipt_node1.imply(0)
    ipt_node2.imply(1)
    xnor_node.imply()
    assert xnor_node.value == 0

    ipt_node1.imply(0)
    ipt_node2.imply(0)
    xnor_node.imply()
    assert xnor_node.value == 1

@pytest.mark.XNOR
def test_xnor_imply_b():
    ipt_node1 = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    ipt_node2 = node.IPT(node.ntype.PI, node.gtype.IPT, "2")
    xnor_node = node.XNOR(node.ntype.GATE, node.gtype.XNOR, "3")
    
    xnor_node.add_unode(ipt_node1)
    xnor_node.add_unode(ipt_node2)
    ipt_node1.add_dnode(xnor_node)
    ipt_node2.add_dnode(xnor_node)
    pass

@pytest.mark.BRCH
def test_brch_imply():
    ipt_node = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    brch_node = node.BRCH(node.ntype.GATE, node.gtype.BRCH, "2")

    brch_node.add_unode(ipt_node)
    ipt_node.add_dnode(brch_node)

    ipt_node.imply(1)
    brch_node.imply()
    assert brch_node.value == 1
    
    ipt_node.imply(0)
    brch_node.imply()
    assert brch_node.value == 0

@pytest.mark.BRCH
def test_brch_imply_b():
    ipt_node = node.IPT(node.ntype.PI, node.gtype.IPT, "1")
    brch_node = node.BRCH(node.ntype.FB, node.gtype.BRCH, "2")
    
    brch_node.add_unode(ipt_node)
    ipt_node.add_dnode(brch_node)