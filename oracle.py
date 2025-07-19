def apply_oracle(circuit, n_qubits, targets):
    '''
    Flips the sign of the amplitude corresponding to the target bitstring (or bitstrings)
    '''
    #Ensure targets is a list not an int
    if isinstance(targets, int):
        targets = [targets]

    for target in targets:
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