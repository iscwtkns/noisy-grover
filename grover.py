from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from math import pi, sqrt, floor
import matplotlib.pyplot as plt
import numpy as np
from oracle import apply_oracle
from diffusion import apply_diffuser
from noise import define_noise_model
from qiskit_ibm_runtime.fake_provider import FakeLimaV2 


def grover_step(circuit, n, target):
    '''
    Apply a single iteration of Grover's Algorithm to a circuit
    '''
    apply_oracle(circuit, n, target)
    apply_diffuser(circuit, n)

def grover_search(n, targets, iterations, shots = 1024, noise_model = None):
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
    simulator = AerSimulator()
    if noise_model is not None:
        backend = FakeLimaV2()
        basis_gates = noise_model.basis_gates
        coupling_map = backend.configuration().coupling_map
        simulator = AerSimulator(noise_model=noise_model, basis_gates=basis_gates, coupling_map=coupling_map)
    job = simulator.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Print results
    print("\nMeasurement results:")
    for bitstring, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{bitstring}: {count}")

    # Report accuracy
    correct = 0
    for target in targets:
        print(target)
        target_bitstring = format(target, f"0{n}b")
        correct += counts.get(target_bitstring, 0)
        print(f"\nTarget bitstring: {target_bitstring}")
        print(f"Found {counts.get(target_bitstring, 0)}/{shots}")
    print(f"\nCorrect results: {correct}/{shots} ({100 * correct / shots:.2f}%)")

    # Optionally plot histogram (comment out if using non-GUI environment)
    #plot_histogram(counts)
    #plt.show()

    return counts

noise_model = define_noise_model(0.001,0.01, [[0.9,0.1],[0.1,0.9]])
grover_search(10,20,20, noise_model=None)

    
