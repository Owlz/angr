#!/usr/bin/env python

import nose
import angr
import os

test_location = str(os.path.dirname(os.path.realpath(__file__)))
bina = os.path.join(test_location, "blob/x86_64/test_project_resolve_simproc")

"""
We voluntarily don't use SimProcedures for 'rand' and 'sleep' because we want
to step into their lib code.
"""

def test_bina():
    p = angr.Project(bina, exclude_sim_procedures=['rand', 'sleep'], load_options={"auto_load_libs":True})

    # Make sure external functions are not replaced with a SimProcedure
    sleep_jmpslot = p.main_binary.jmprel['sleep']
    rand_jmpslot = p.main_binary.jmprel['rand']
    read_jmpslot = p.main_binary.jmprel['read']

    sleep_addr = p.ld.memory.read_addr_at(sleep_jmpslot.addr)
    rand_addr = p.ld.memory.read_addr_at(rand_jmpslot.addr)
    read_addr = p.ld.memory.read_addr_at(read_jmpslot.addr)

    nose.tools.assert_equal(sleep_addr, 0x40011904c0)
    nose.tools.assert_equal(rand_addr, 0x4001111b40)
    nose.tools.assert_equal(read_addr, 0x6e928307afd6984)

    nose.tools.assert_true("libc___so___6.read.read" in
                           p.sim_procedures[0x6e928307afd6984].__str__())

if __name__ == '__main__':
    test_bina()
