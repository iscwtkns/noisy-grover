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