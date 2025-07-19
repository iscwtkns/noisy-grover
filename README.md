# Grover's Algorithm with Qiskit

## 📚 Summary: Grover's Search Algorithm

Grover's algorithm is a quantum search algorithm that provides a quadratic speedup for unstructured search problems. Given a search space of size \( N = 2^n \), and \( M \) marked "solutions", Grover’s algorithm finds a solution in roughly:

\[
O\left(\sqrt{\frac{N}{M}}\right)
\]

iterations, compared to \( O(N/M) \) classically.

The algorithm consists of the following key steps:

1. **Initialization**: Create an equal superposition of all \( 2^n \) states.
2. **Grover Iteration**: Repeatedly apply:
   - The **oracle**, which flips the sign of the amplitude of the target states.
   - The **diffusion operator** (also called the Grover diffuser), which inverts the state amplitudes about the average.
3. **Measurement**: Measure the quantum state. With high probability, the result is one of the target solutions.

---

## 🧠 Oracle & Diffusion Operator

### 🔍 Oracle

The oracle is a quantum operation that marks the correct state(s) by flipping their phase. For a target state \(|x\rangle\), the oracle \( O \) acts as:

\[
O|x\rangle = 
\begin{cases}
-|x\rangle & \text{if } x \text{ is a solution} \\
|x\rangle & \text{otherwise}
\end{cases}
\]

In implementation, the oracle checks whether the current basis state matches any in the list of solution indices and applies a Z-gate (phase flip) if it does.

### 🔄 Diffusion Operator

The diffuser amplifies the amplitude of the marked states. It performs the transformation:

\[
D = 2|\psi\rangle\langle\psi| - I
\]

where \(|\psi\rangle\) is the uniform superposition state. It reflects the state vector about the average amplitude. In Qiskit, this is implemented as:

1. Apply Hadamard to all qubits
2. Apply X to all qubits
3. Apply a multi-controlled-Z gate
4. Apply X again
5. Apply Hadamard again

---

## 📊 Accuracy Graphs & Analysis

Below are plots showing the **probability of success** vs **number of Grover iterations** for various configurations.

Theoretical probability is given by:

\[
P_{\text{success}}(k) = \sin^2\left((2k + 1)\frac{\theta}{2}\right), \quad \theta = 2\sin^{-1}\left(\sqrt{\frac{M}{N}}\right)
\]

### ✅ Example Plot (10 Qubits, 1 Target)

> _(Insert your matplotlib/seaborn graph here)_

[Insert plot showing accuracy vs iteration count]

yaml
Copy
Edit

Note how the probability initially increases and peaks around the optimal number of iterations, then decreases in a sinusoidal fashion. Over-rotating (too many iterations) leads to a drop in success rate—this is intrinsic to the algorithm and is why knowing the number of solutions is important.

---

## 🔬 Noisy Simulation (coming soon...)

This implementation is currently **noiseless**. A future update will simulate realistic quantum noise using Qiskit’s `Aer` noise models, including:

- Bit-flip and phase-flip errors
- Depolarizing noise
- Readout errors

---

## 📁 Files

- `grover.py` — main implementation
- `oracle.py` — oracle builder
- `diffusion.py` — diffuser implementation
- `plots.py` — plotting utilities
- `README.md` — this file

---

## 📦 Requirements

- Python 3.8+
- Qiskit
- Matplotlib
- NumPy

---

## 🧪 Run the Code

```bash
python grover.py