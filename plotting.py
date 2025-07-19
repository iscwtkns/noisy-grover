import numpy as np
from grover import grover_search
import matplotlib.pyplot as plt
from noise import get_noise_model

def plot_accuracy(n, iterationsmax, targets, noise_model =None):
    if isinstance(targets, int):
        targets = [targets]
    
    iterations = range(iterationsmax)
    accuracy = [0]*len(iterations)
    theoreticalX = np.linspace(0,iterationsmax, 200)
    theoretical = [0]*len(theoreticalX)
    theta = np.arcsin(np.sqrt(len(targets)/2**n))

    for i in range(len(theoreticalX)):
        theoretical[i] = np.sin((2*theoreticalX[i]+1)*theta)**2 * 100

   
    for i in iterations:
        counts = grover_search(n, targets, i, shots=1024, noise_model=noise_model)
        for target in targets:
            target_bitstring = format(target, f"0{n}b")
            accuracy[i] += counts.get(target_bitstring,0)/1024 * 100
            

    


    plt.scatter(iterations, accuracy, label = 'Actual Data')
    plt.plot(theoreticalX, theoretical, label = 'Theoretical Curve', color='red')
    plt.legend(loc='upper left')
    if noise_model is None:
        plt.title(f"Accuracy of Grover's Search as a Function of Iterations for n = {n} Qubits and {len(targets)} Target(s)")
    else:
        plt.title(f"Accuracy of Grover's Search as a Function of Iterations for n = {n} Qubits and {len(targets)} Target(s) with FakeLimaV2 Noise Model")
    plt.xlabel("Iterations")
    plt.ylabel("Accuracy (%)")

    plt.show()

plot_accuracy(8, 50, [1,2,3,4,5,6])