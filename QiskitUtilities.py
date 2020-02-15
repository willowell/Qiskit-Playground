"""
Importing Qiskit
    Basic circuit elements.
    Imports QuantumCircuit, QuantumRegister, Classical Register, etc.
    Also imports Aer and IBMQ.
    Use Aer for local simulators, or use IBMQ for IBM's machines.
"""
from qiskit import *
from qiskit.providers.ibmq import least_busy
# Use this to monitor jobs, especially ones on IBM's machines.
from qiskit.providers.ibmq.accountprovider import AccountProvider
from qiskit.tools.monitor import job_monitor
# Adds circuit_drawer(), plot_histogram(), etc.
from qiskit.tools.visualization import *

""" Useful additional modules """
# For file system access.
import os
# For some explicit typing.
from typing import *

""" Matplotlib, Numpy, Scipy, etc. """
# For plotting and linear algebra utilities.
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

""" Utility Functions """

"""
Queries IBM Q for available quantum computers.

"""


def query_ibmq_backends_with_min_qubits(num_qubits: int):
    IBMQ.load_account()
    provider = IBMQ.get_provider()
    backends = provider.backends()

    print("Available IBMQ backends: ")
    for backend in backends:
        print(backend)
        print(backend.configuration())
        print(backend.status())
        print()

    if (num_qubits > 0):
        large_enough_devices = provider.backends(filters=lambda x: x.configuration().n_qubits > num_qubits and
                                                                   not x.configuration().simulator)
    elif (num_qubits == 0):
        large_enough_devices = provider.backends(filters=lambda x: not x.configuration().simulator)
    else:
        print("Invalid number of qubits. Defaulting to minimum qubits of 0.")
        large_enough_devices = provider.backends(filters=lambda x: not x.configuration().simulator)

    best_real_backend = least_busy(large_enough_devices)
    print("The best real backend at IBM is: ", best_real_backend.name())
    return best_real_backend


def write_qasm_to_file(circuit: QuantumCircuit, destination_dir: str, file_name: str):
    qasm_source = circuit.qasm()
    f: TextIO = open(os.path.join(destination_dir, file_name + ".qasm"), "w")
    f.write(qasm_source)
    f.close()


def measure_circuit(circuit: QuantumCircuit, qregs: QuantumRegister, cregs: ClassicalRegister):
    circuit.barrier()
    circuit.measure(qregs, cregs)


def prepare_ghz_state(qregs: QuantumRegister, cregs: ClassicalRegister) -> QuantumCircuit:
    quantum_circuit = QuantumCircuit(qregs, cregs)
    quantum_circuit.h(qregs[0])
    for i in range(quantum_circuit.size - 1):
        quantum_circuit.cx(qregs[i], qregs[i + 1])
    return quantum_circuit


def prepare_superposition_state(qregs: QuantumRegister, cregs: ClassicalRegister) -> QuantumCircuit:
    quantum_circuit = QuantumCircuit(qregs, cregs)
    quantum_circuit.h(qregs)
    return quantum_circuit


def yes_or_no(question):
    reply = str(input(question + ' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return 1
    elif reply[0] == 'n':
        return 0
    else:
        return yes_or_no("Please Enter (y/n) ")


def inputNumber(message):
    while True:
        try:
            userInput = int(input(message))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput
            break
