"""
Quantum State Tomography Example
For verifying Bell states and Magic states

This example shows how to perform quantum state tomography
to measure the fidelity of distilled states.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import state_fidelity, Statevector, DensityMatrix
from qiskit_experiments.library import StateTomography
from qiskit_experiments.framework import ParallelExperiment
import numpy as np


def create_bell_state_circuit():
    """
    Create a circuit that prepares a Bell state |Φ+⟩.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def create_magic_state_circuit():
    """
    Create a circuit that prepares a T-type magic state |T0⟩.
    
    |T0⟩ = cos(β)|0⟩ + e^(iπ/4)sin(β)|1⟩
    where β = (1/2)arccos(1/√3)
    """
    beta = 0.5 * np.arccos(1 / np.sqrt(3))
    
    qc = QuantumCircuit(1)
    qc.ry(2 * beta, 0)
    qc.p(np.pi / 4, 0)  # Phase shift
    
    return qc


def perform_state_tomography_manual(circuit, num_qubits, shots=10000):
    """
    Perform manual state tomography by measuring in different bases.
    
    For N qubits, we need to measure in 3^N different basis combinations:
    - Each qubit can be measured in X, Y, or Z basis
    
    Args:
        circuit: QuantumCircuit preparing the state
        num_qubits: Number of qubits in the state
        shots: Number of measurement shots per basis
        
    Returns:
        reconstructed_density_matrix: DensityMatrix object
    """
    simulator = AerSimulator()
    
    # Generate all measurement bases
    bases = ['X', 'Y', 'Z']
    
    if num_qubits == 1:
        basis_combinations = [['X'], ['Y'], ['Z']]
    elif num_qubits == 2:
        basis_combinations = [
            ['X', 'X'], ['X', 'Y'], ['X', 'Z'],
            ['Y', 'X'], ['Y', 'Y'], ['Y', 'Z'],
            ['Z', 'X'], ['Z', 'Y'], ['Z', 'Z']
        ]
    else:
        raise NotImplementedError("Only 1 and 2 qubit tomography implemented")
    
    measurement_results = {}
    
    # Measure in each basis combination
    for basis_combo in basis_combinations:
        # Create measurement circuit
        meas_circuit = circuit.copy()
        
        # Apply basis rotation gates before measurement
        for qubit_idx, basis in enumerate(basis_combo):
            if basis == 'X':
                meas_circuit.h(qubit_idx)
            elif basis == 'Y':
                meas_circuit.sdg(qubit_idx)
                meas_circuit.h(qubit_idx)
            # Z basis: no rotation needed
        
        meas_circuit.measure_all()
        
        # Run simulation
        job = simulator.run(meas_circuit, shots=shots)
        counts = job.result().get_counts()
        
        basis_key = ''.join(basis_combo)
        measurement_results[basis_key] = counts
    
    # Reconstruct density matrix from measurements
    # This is a simplified version - in practice, use maximum likelihood estimation
    print(f"\nMeasurement results for {num_qubits}-qubit state:")
    for basis, counts in measurement_results.items():
        print(f"  Basis {basis}: {counts}")
    
    return measurement_results


def calculate_bell_state_fidelity(measurement_results):
    """
    Calculate fidelity to ideal Bell state |Φ+⟩ from tomography results.
    
    For a Bell state, we can estimate fidelity from specific measurements:
    - ZZ measurement: should give 00 or 11 with equal probability
    - XX measurement: should give 00 or 11 with equal probability
    """
    # Ideal Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
    ideal_bell = Statevector.from_label('00')
    ideal_bell = (Statevector.from_label('00') + Statevector.from_label('11')) / np.sqrt(2)
    
    # Extract ZZ measurement
    zz_counts = measurement_results.get('ZZ', {})
    total = sum(zz_counts.values())
    
    # Calculate probabilities
    p_00 = zz_counts.get('00', 0) / total
    p_11 = zz_counts.get('11', 0) / total
    p_01 = zz_counts.get('01', 0) / total
    p_10 = zz_counts.get('10', 0) / total
    
    print(f"\nZZ measurement probabilities:")
    print(f"  P(00) = {p_00:.4f} (ideal: 0.5000)")
    print(f"  P(11) = {p_11:.4f} (ideal: 0.5000)")
    print(f"  P(01) = {p_01:.4f} (ideal: 0.0000)")
    print(f"  P(10) = {p_10:.4f} (ideal: 0.0000)")
    
    # Simple fidelity estimate: F ≈ P(00) + P(11) for Bell state
    estimated_fidelity = p_00 + p_11
    
    return estimated_fidelity


def perform_tomography_with_qiskit_experiments(circuit):
    """
    Perform state tomography using Qiskit Experiments library.
    
    This is the recommended way to do tomography in practice.
    """
    # Create state tomography experiment
    qstexp = StateTomography(circuit)
    
    # Run on simulator
    backend = AerSimulator()
    qstdata = qstexp.run(backend, shots=10000).block_for_results()
    
    # Get reconstructed state
    state_result = qstdata.analysis_results("state")
    reconstructed_state = state_result.value
    
    return reconstructed_state, qstdata


def main():
    """
    Demonstrate state tomography for Bell state and magic state.
    """
    print("=" * 70)
    print("Quantum State Tomography Example")
    print("=" * 70)
    
    # Example 1: Bell State Tomography
    print("\n" + "=" * 70)
    print("Example 1: Bell State |Φ+⟩ Tomography")
    print("=" * 70)
    
    bell_circuit = create_bell_state_circuit()
    print("\nBell state circuit:")
    print(bell_circuit.draw(output='text'))
    
    # Perform manual tomography
    bell_measurements = perform_state_tomography_manual(bell_circuit, num_qubits=2)
    
    # Calculate fidelity
    bell_fidelity = calculate_bell_state_fidelity(bell_measurements)
    print(f"\nEstimated fidelity to |Φ+⟩: {bell_fidelity:.4f}")
    
    # Example 2: Magic State Tomography
    print("\n" + "=" * 70)
    print("Example 2: Magic State |T0⟩ Tomography")
    print("=" * 70)
    
    magic_circuit = create_magic_state_circuit()
    print("\nMagic state circuit:")
    print(magic_circuit.draw(output='text'))
    
    # Perform manual tomography
    magic_measurements = perform_state_tomography_manual(magic_circuit, num_qubits=1)
    
    # For magic state, calculate expected probabilities
    beta = 0.5 * np.arccos(1 / np.sqrt(3))
    ideal_p0_z = np.cos(beta)**2
    ideal_p1_z = np.sin(beta)**2
    
    z_counts = magic_measurements.get('Z', {})
    total_z = sum(z_counts.values())
    p0_z = z_counts.get('0', 0) / total_z
    p1_z = z_counts.get('1', 0) / total_z
    
    print(f"\nZ-basis measurement:")
    print(f"  P(0) = {p0_z:.4f} (ideal: {ideal_p0_z:.4f})")
    print(f"  P(1) = {p1_z:.4f} (ideal: {ideal_p1_z:.4f})")
    
    print("\n" + "=" * 70)
    print("Using Qiskit Experiments (Recommended Method)")
    print("=" * 70)
    print("\nTo use Qiskit Experiments for tomography:")
    print("```python")
    print("from qiskit_experiments.library import StateTomography")
    print("")
    print("qstexp = StateTomography(circuit)")
    print("qstdata = qstexp.run(backend, shots=10000).block_for_results()")
    print("reconstructed_state = qstdata.analysis_results('state').value")
    print("")
    print("# Calculate fidelity")
    print("fidelity = state_fidelity(reconstructed_state, ideal_state)")
    print("```")
    print("=" * 70)


if __name__ == "__main__":
    main()
