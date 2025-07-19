from qiskit_aer.noise import depolarizing_error, NoiseModel, ReadoutError
from qiskit_ibm_runtime.fake_provider import FakeLimaV2

def define_noise_model(p1, p2, readoutErrorMatrix):
    '''
    Defines a noise model with single-qubit-gate probability of depolarisation p1 and two-qubit-gate probability p2,
    as well as readoutErrorMatrix of the form [[P(0|0), P(0|1)], [P(1|0), P(1|1)]]

    '''
    noise_model = NoiseModel()
    error_1 = depolarizing_error(p1, 1)
    error_2 = depolarizing_error(p2, 2)
    readout_error = ReadoutError(readoutErrorMatrix)

    noise_model.add_all_qubit_quantum_error(error_1, ['u3', 'x'])
    noise_model.add_all_qubit_quantum_error(error_2, ['cx'])
    noise_model.add_all_qubit_readout_error(readout_error)

    return noise_model

def get_noise_model():
    '''
    Gets a realistic noise model from qiskit 
    '''
    backend = FakeLimaV2()
    noise_model = NoiseModel.from_backend(backend)
    return noise_model
    

