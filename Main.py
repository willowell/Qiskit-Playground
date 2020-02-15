from QiskitUtilities import *


backend = Aer.get_backend("qasm_simulator")
shots = 1024           # Number of shots to run the program (experiment); maximum is 8192 shots.
max_credits = 3        # Maximum number of credits to spend on executions.
num_quantum_regs = 5
num_classic_regs = 5

# Matplotlib Utilities
fig = plt.figure()
fig.set_size_inches(6, 6)
fig.set_dpi(100)


style = {
    "figwidth": 12,
    "fold": 30
}

def main():
##################################### INITIALIZATION ###################################################################

    if yes_or_no("Do you want to use a real backend?"):
        global backend
        backend = query_ibmq_backends_with_min_qubits(num_quantum_regs)
    else:
        # do nothing, the backend is automatically set to the local simulator
        pass
    print()

    print("The backend is set to: ", backend)
    print()

    will_measure = False
    if yes_or_no("Do you want to measure this circuit? WARNING: results will be invalid otherwise!"):
        will_measure = True
    else:
        pass
    print()

    q_reg = QuantumRegister(num_classic_regs, 'q')
    c_reg = ClassicalRegister(num_classic_regs, 'c')
    circ = QuantumCircuit(q_reg, c_reg)


##################################### CIRCUIT GOES HERE ################################################################

    circ.h(q_reg[3])
    circ.h(q_reg[4])

    circ.s(q_reg[3])
    circ.s(q_reg[4])

    circ.barrier()

    circ.h(q_reg[4])
    circ.cx(q_reg[3], q_reg[4])
    circ.h(q_reg[4])

    circ.barrier()

    circ.s(q_reg[3])
    circ.s(q_reg[4])

    circ.h(q_reg[3])
    circ.h(q_reg[4])

    circ.x(q_reg[3])
    circ.x(q_reg[4])

    circ.barrier()

    circ.h(q_reg[4])
    circ.cx(q_reg[3], q_reg[4])
    circ.h(q_reg[4])

    circ.barrier()

    circ.x(q_reg[3])
    circ.x(q_reg[4])

    circ.h(q_reg[3])
    circ.h(q_reg[4])


##################################### MEASURE AND EXECUTE ##############################################################

    if will_measure:
        measure_circuit(circ, q_reg, c_reg)

    print("Executing the circuit!")
    job_exp = execute(circ, backend=backend, shots=shots)

    job_monitor(job_exp)

    result_exp = job_exp.result()
    counts_exp = result_exp.get_counts(circ)
    print("Here are the number of times a particular state was measured: ")
    print(counts_exp)

    if backend == "statevector_simulator":
        psi = result_exp.get_statevector(circ)
        plot_bloch_multivector(psi).savefig("qsphere.png")

    print("Writing QASM to file...")
    write_qasm_to_file(circ, os.getcwd(), "circ")

    print("Making a pretty histogram :-) ...")
    plot_histogram(counts_exp).savefig("histogram.png")

    print("Making a drawing of the circuit...")
    circuit_drawer(circuit=circ, output="mpl", interactive=True, filename="circ.png", style=style)

    print("All done!")

if __name__ == "__main__":
    main()










