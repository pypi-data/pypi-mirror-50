"""
Tests that Asap works in parallel simulations even if a process has no atoms.

Name: emptyNode.py

Description: Part of the Asap test suite.  Tests parallelization robustness.

Usage: mpirun -np 4 asap-python emptyNode.py

Expected result: The output should end with 'ALL TESTS SUCCEEDED'.
"""
from __future__ import print_function

from ase.build import bulk
from ase.lattice.cubic import FaceCenteredCubic
from asap3.testtools import ReportTest
from asap3 import MakeParallelAtoms, EMT
from asap3.mpi import world
import numpy as np
from ase.visualize import view

if world.size == 1:
    cpulayout = None
elif world.size == 2:
    cpulayout = [2,1,1]
elif world.size == 3:
    cpulayout = [1,3,1]
elif world.size == 4:
    cpulayout = [2,2,1]

def makesystem(delta):
    atoms = FaceCenteredCubic("Cu", size=(15,15,15), pbc=False)
    x = atoms.cell[0,0] / 2
    y = atoms.cell[1,1] / 2
    pos = atoms.get_positions()
    keep = np.logical_or(pos[:,0] > x + delta, pos[:,1] > y + delta)
    return atoms[keep]

def distribute(atoms):
    if world.rank != 0:
        atoms = None
    return MakeParallelAtoms(atoms, cpulayout)


def testsystem(origatoms, label):
    atoms = distribute(origatoms)
    atoms.suppress_warning_noatoms = True   # Kill a warning on stderr
    print("Number of atoms on process {}: {}".format(world.rank, len(atoms)))
    atoms.set_calculator(EMT())
    energy_par = atoms.get_potential_energy()

    origatoms.set_calculator(EMT())
    energy_ser = origatoms.get_potential_energy()

    ReportTest(label+": Energy match", energy_par, energy_ser, 1e-6)

a = makesystem(10.0)
testsystem(a, "Large missing part on master")

a.rotate(90, 'z', center='COU')
testsystem(a, "Large missing part on slave")

a = makesystem(1.0)
testsystem(a, "Small missing part on master")

a.rotate(90, 'z', center='COU')
testsystem(a, "Small missing part on slave")
