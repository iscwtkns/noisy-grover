from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from math import pi, sqrt, floor
import matplotlib.pyplot as plt
import numpy as np
from oracle import apply_oracle


def apply_diffuser(circuit, n):
    '''
    Inverts the working qubits around the mean
    '''
    circuit.h(range(n))
    circuit.x(range(n))
    circuit.h(n-1)
    circuit.mcx(list(range(n-1)), n-1)
    circuit.h(n-1)
    circuit.x(range(n))
    circuit.h(range(n))

def grover_step(circuit, n, target):
    '''
    Apply a single iteration of Grover's Algorithm to a circuit
    '''
    apply_oracle(circuit, n, target)
    apply_diffuser(circuit, n)

def grover_search(n, targets, iterations, shots = 1024):
    #check if valid test call
    if isinstance(targets, int):
        targets = [targets]
    for target in targets:
        if target > 2**n-1:
            Exception("Invalid input")
    
    #Initialise quantum circuit, with additional qubit for ancilla
    qc = QuantumCircuit(n+1, n)

    #Set ancilla qubit to -
    qc.x(n)
    qc.h(n)

    #Put into equal superposition
    qc.h(list(range(n)))
    
    #Perform Grover's Algorithm steps
    for i in range(iterations):
        grover_step(qc, n, targets)
    
    # Measure only the main qubits (not the ancilla)
    qc.measure(range(n), range(n))

    # Run the circuit on the simulator
    backend = Aer.get_backend("qasm_simulator")
    job = backend.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Print results
    print("\nMeasurement results:")
    for bitstring, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{bitstring}: {count}")

    # Report accuracy
    correct = 0
    for target in targets:

        target_bitstring = format(target, f"0{n}b")
        correct += counts.get(target_bitstring, 0)
        print(f"\nTarget bitstring: {target_bitstring}")
        print(f"Found {counts.get(target_bitstring, 0)}/{shots}")
    print(f"\nCorrect results: {correct}/{shots} ({100 * correct / shots:.2f}%)")

    # Optionally plot histogram (comment out if using non-GUI environment)
    #plot_histogram(counts)
    #plt.show()

    return counts


grover_search(3, [4,6], 2)
    
