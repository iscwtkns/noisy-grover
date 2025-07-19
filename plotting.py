import numpy as np
from grover import grover_search
import matplotlib.pyplot as plt

def plot_accuracy(n, iterationsmax, targets):
    if isinstance(targets, int):
        targets = [targets]
    
    iterations = range(iterationsmax)
    accuracy = [0]*len(iterations)
    theoretical = [0]*len(iterations)
    theta = np.arcsin(np.sqrt(len(targets)/2**n))

    for i in iterations:
        theoretical[i] = np.sin((2*i+1)*theta)**2 * 100
        counts = grover_search(n, targets, i, shots=1024)
        for target in targets:
            target_bitstring = format(target, f"0{n}b")
            accuracy[i] += counts.get(target_bitstring,0)/1024 * 100
            

    


    plt.scatter(iterations, accuracy, label = 'Actual Data')
    plt.plot(iterations, theoretical, label = 'Theoretical Accuracy Curve', color='red')
    plt.legend(loc='upper left')
    plt.title(f"Accuracy of Grover's Search as a Function of Iterations for n = {n} qubits")
    plt.xlabel("Iterations")
    plt.ylabel("Accuracy (%)")

    plt.show()
