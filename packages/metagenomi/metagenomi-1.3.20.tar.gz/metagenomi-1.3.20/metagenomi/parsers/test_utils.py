from utils import *


def test_repeat_bitcodes():
    # Starts with GTT
    r = 'GTTCACTGCCGTACAGGCAGCTTAGAAA'
    r_dir = orient_repeat(r)
    assert r_dir[0] == '+'
    assert r_dir[1] == 3
    assert r_dir[2] == [1, 0, 1, 0, 1, 0, 0, 0]
    bitstring = ''.join([str(i) for i in r_dir[2]])
    assert int(bitstring, 2) == 168

    # Starts and ends with GTT
    r = 'GTTCACTGCCGTACAGGCAGCTTAGAAC'
    r_dir = orient_repeat(r)
    assert r_dir[0] is None
    assert r_dir[1] == 0
    assert r_dir[2] == [1, 1, 1, 1, 1, 1, 0, 0]
    bitstring = ''.join([str(i) for i in r_dir[2]])
    assert int(bitstring, 2) == 252

    # End with GTT, starts with GYY
    r = 'GCTCACTGCCGTACAGGCAGCTTAGAAC'
    r_dir = orient_repeat(r)
    assert r_dir[0] == '-'
    assert r_dir[1] == 3
    assert r_dir[2] == [1, 1, 1, 1, 0, 1, 0, 0]
    bitstring = ''.join([str(i) for i in r_dir[2]])
    assert int(bitstring, 2) == 244

    # No direction
    r = 'CCTCACTGCCGTACAGGCAGCTTAGAAA'
    r_dir = orient_repeat(r)
    assert r_dir[0] is None
    assert r_dir[1] == 0
    assert r_dir[2] == [0, 0, 0, 0, 0, 0, 0, 0]
    bitstring = ''.join([str(i) for i in r_dir[2]])
    assert int(bitstring, 2) == 0

    # Begins and ends with motif
    r = 'CTTTCAATTGCCGTACAGGCAATTGAAAA'
    r_dir = orient_repeat(r)
    assert r_dir[0] is None
    assert r_dir[1] == 0
    assert r_dir[2] == [0, 0, 0, 0, 0, 0, 1, 1]
    bitstring = ''.join([str(i) for i in r_dir[2]])
    assert int(bitstring, 2) == 3

    # Ends with G
    r = 'CTTGCAATTGCCGTACAGGCAATTGATAC'
    r_dir = orient_repeat(r)
    assert r_dir[0] == '-'
    assert r_dir[1] == 1
    assert r_dir[2] == [0, 1, 0, 0, 0, 0, 0, 0]
    bitstring = ''.join([str(i) for i in r_dir[2]])
    assert int(bitstring, 2) == 64

    # Starts and ends with G
    r = 'GAAGCAATTGCCGTACAGGCAATTGACAC'
    r_dir = orient_repeat(r)
    assert r_dir[0] is None
    assert r_dir[1] == 0
    assert r_dir[2] == [1, 1, 0, 0, 0, 0, 0, 0]
    bitstring = ''.join([str(i) for i in r_dir[2]])
    assert int(bitstring, 2) == 192

    # Starts and ends with GYY
    r = 'GCCGCAATTGCCGTACAGGCAATTGAGGC'
    r_dir = orient_repeat(r)
    assert r_dir[0] is None
    assert r_dir[1] == 0
    assert r_dir[2] == [1, 1, 1, 1, 0, 0, 0, 0]
    bitstring = ''.join([str(i) for i in r_dir[2]])
    assert int(bitstring, 2) == 240
