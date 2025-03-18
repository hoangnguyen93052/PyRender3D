import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import inv

class QuantumGate:
    def __init__(self, matrix):
        self.matrix = np.array(matrix)

    def apply(self, state):
        return np.dot(self.matrix, state)

class QuantumCircuit:
    def __init__(self):
        self.gates = []
        self.initial_state = np.array([1, 0])  # Default to |0>

    def add_gate(self, gate):
        self.gates.append(gate)

    def run(self):
        state = self.initial_state
        for gate in self.gates:
            state = gate.apply(state)
        return state

class Qubit:
    def __init__(self, alpha=1, beta=0):
        norm = np.sqrt(alpha**2 + beta**2)
        self.alpha = alpha / norm
        self.beta = beta / norm
        self.state_vector = np.array([self.alpha, self.beta])

    def measure(self):
        probabilities = np.abs(self.state_vector)**2
        return np.random.choice([0, 1], p=probabilities)

class Hadamard(QuantumGate):
    def __init__(self):
        super().__init__([[1, 1], [1, -1]] / np.sqrt(2))

class PauliX(QuantumGate):
    def __init__(self):
        super().__init__([[0, 1], [1, 0]])

class PauliY(QuantumGate):
    def __init__(self):
        super().__init__([[0, -1j], [1j, 0]])

class PauliZ(QuantumGate):
    def __init__(self):
        super().__init__([[1, 0], [0, -1]])

class Simulator:
    def __init__(self):
        self.circuit = QuantumCircuit()

    def add_hadamard(self):
        self.circuit.add_gate(Hadamard())

    def add_pauli_x(self):
        self.circuit.add_gate(PauliX())

    def add_pauli_y(self):
        self.circuit.add_gate(PauliY())

    def add_pauli_z(self):
        self.circuit.add_gate(PauliZ())

    def run_simulation(self):
        final_state = self.circuit.run()
        return final_state

def main():
    print("Quantum Circuit Simulation")
    
    sim = Simulator()
    sim.add_hadamard()
    sim.add_pauli_x()

    final_state = sim.run_simulation()
    print("Final State:", final_state)

    qubit = Qubit(alpha=1, beta=0)
    measurement_result = qubit.measure()
    print("Measurement Result:", measurement_result)

if __name__ == "__main__":
    main()

def plot_state_vector(state_vector):
    plt.figure(figsize=(8, 4))
    plt.bar(['|0>', '|1>'], np.abs(state_vector)**2, color=['blue', 'red'])
    plt.ylabel('Probability')
    plt.title('Qubit State Probabilities')
    plt.ylim(0, 1)
    plt.show()

def plot_circuit(circuit):
    plt.figure(figsize=(10, len(circuit.gates) * 2))
    for i, gate in enumerate(circuit.gates):
        plt.text(0.5, i + 0.5, str(gate.__class__.__name__), fontsize=14,
                 ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
    plt.xlim(0, 1)
    plt.ylim(0, len(circuit.gates) + 1)
    plt.axis('off')
    plt.title('Quantum Circuit')
    plt.show()

class QuantumMeasurement:
    def __init__(self, state):
        self.state = state

    def perform_measurement(self):
        probabilities = np.abs(self.state)**2
        return np.random.choice([0, 1], p=probabilities)

def run_multiple_measurements(circuit, shots=100):
    results = []
    for _ in range(shots):
        final_state = circuit.run()
        measurement = QuantumMeasurement(final_state)
        result = measurement.perform_measurement()
        results.append(result)
    return results

def calculate_statistics(results):
    counts = np.bincount(results)
    return counts / len(results)

def main_simulation():
    sim = Simulator()
    sim.add_hadamard()
    sim.add_pauli_x()

    results = run_multiple_measurements(sim.circuit, shots=1000)
    counts = calculate_statistics(results)
    print("Measurement Results:", counts)

    plot_state_vector(sim.circuit.run())
    plot_circuit(sim.circuit)

if __name__ == "__main__":
    main_simulation()

def entanglement_state():
    return np.array([1, 0, 0, 1]) / np.sqrt(2)

def create_entangled_qubits():
    entangled = entanglement_state()
    return entangled.reshape(4, 1)

def apply_entanglement(circuit, entangled_state):
    circuit.initial_state = entangled_state

def run_entangled_simulation():
    sim = Simulator()
    entangled_state = create_entangled_qubits()
    apply_entanglement(sim.circuit, entangled_state)

    results = run_multiple_measurements(sim.circuit, shots=1000)
    counts = calculate_statistics(results)
    print("Entangled Measurement Results:", counts)

if __name__ == "__main__":
    run_entangled_simulation()

# Additional features could include error handling, more advanced quantum gates, and different quantum algorithms.
# This is a basic framework designed for educational purposes on quantum computing simulations.