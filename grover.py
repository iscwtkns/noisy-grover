from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from math import pi, sqrt, floor
import matplotlib.pyplot as plt
import numpy as np

def apply_oracle(circuit, n_qubits, target):
    '''
    Flips the sign of the amplitude corresponding to the target bitstring
    '''
    #Encode target number in binary
    binary = format(target, f'0{n_qubits}b')[::-1]

    #Loop through bits in the target and perform an X gate on qubits corresponding to 0 bits
    #This results in the target state to be measured now being all 1s.
    for i, bit in enumerate(binary):
        if bit == '0':
            circuit.x(i)
    
    #Apply multi-controlled x on all gates targeting ancilla qubit (set to - state)
    circuit.mcx(list(range(n_qubits)), n_qubits)

    #Undo the X gates
    for i, bit in enumerate(binary):
        if bit == '0':
            circuit.x(i)

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

def grover_search(n, target, iterations, shots = 1024):
    #check if valid test call
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
        grover_step(qc, n, target)
    
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
    target_bitstring = format(target, f"0{n}b")
    correct = counts.get(target_bitstring, 0)
    print(f"\nTarget bitstring: {target_bitstring}")
    print(f"Correct results: {correct}/{shots} ({100 * correct / shots:.2f}%)")

    # Optionally plot histogram (comment out if using non-GUI environment)
    #plot_histogram(counts)
    #plt.show()

    return counts

def plot_accuracy(n, iterationsmax, target):

    target_bitstring = format(target, f"0{n}b")
    iterations = range(iterationsmax)
    accuracy = [0]*len(iterations)
    theoretical = [0]*len(iterations)
    theta = np.arcsin(1/np.sqrt(2**n))

    for i in iterations:
        counts = grover_search(n, target, i, shots=1024)
        accuracy[i] = counts.get(target_bitstring,0)/1024 * 100
        theoretical[i] = np.sin((2*i+1)*theta) * 100

    


    plt.scatter(iterations, accuracy, label = 'Actual Data')
    plt.plot(iterations, theoretical, label = 'Theoretical Accuracy Curve')
    plt.legend(loc='upper left')
    plt.title(f"Accuracy of Grover's Search as a Function of Iterations for n = {n} qubits")
    plt.xlabel("Iterations")
    plt.ylabel("Accuracy (%)")

    plt.show()

plot_accuracy(10, 50, 397)

    
