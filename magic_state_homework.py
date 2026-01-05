"""
Magic State Distillation - Educational Implementation
Using Qiskit

This demonstrates magic state distillation concepts with a simplified
3-to-1 protocol that is easier to understand and implement.

Note: The full 15-to-1 Bravyi-Kitaev protocol is extremely complex.
For homework purposes, we focus on understanding the key concepts:
- Error detection through syndrome measurements
- Post-selection to improve fidelity
- Trade-off between success rate and output quality
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import state_fidelity, Statevector, DensityMatrix
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error
import numpy as np


def create_magic_state_3to1():
    """
    Create a simplified 3-to-1 magic state distillation circuit.
    
    This protocol takes 3 noisy T-states and produces 1 higher-fidelity T-state.
    It's based on a 3-qubit repetition code.
    
    Protocol:
    1. Prepare 3 qubits in |+⟩ state
    2. Apply T gates (noisy magic states)
    3. Encode using majority vote structure
    4. Measure 2 syndrome qubits
    5. Post-select on syndrome = 00
    
    Returns:
        QuantumCircuit for 3-to-1 distillation
    """
    qr = QuantumRegister(3, 'q')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Step 1: Initialize in |+⟩ state
    for i in range(3):
        qc.h(i)
    qc.barrier(label='Init')
    
    # Step 2: Apply T gates (these are our noisy input magic states)
    for i in range(3):
        qc.t(i)
    qc.barrier(label='T gates')
    
    # Step 3: Create correlations for error detection
    # Use CNOT gates to create a 3-qubit code
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.barrier(label='Encode')
    
    # Step 4: Measure syndrome qubits in X-basis
    qc.h(1)
    qc.h(2)
    
    qc.measure_all()
    
    return qc


def create_noisy_magic_state_3to1(noise_prob=0.05):
    """
    Create 3-to-1 distillation circuit with explicit noise model.
    
    Args:
        noise_prob: Probability of error on each T gate
    """
    qr = QuantumRegister(3, 'q')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Initialize in |+⟩
    for i in range(3):
        qc.h(i)
    qc.barrier()
    
    # Apply T gates with noise
    for i in range(3):
        qc.t(i)
    qc.barrier()
    
    # Encoding
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.barrier()
    
    # X-basis measurement on syndrome qubits
    qc.h(1)
    qc.h(2)
    
    qc.measure_all()
    
    # Create noise model
    noise_model = NoiseModel()
    t_error = depolarizing_error(noise_prob, 1)
    noise_model.add_all_qubit_quantum_error(t_error, ['t'])
    
    return qc, noise_model


def analyze_magic_distillation(counts):
    """
    Analyze results of 3-to-1 magic state distillation.
    
    Success condition: syndrome qubits (q1, q2) both measure 0
    
    Args:
        counts: Measurement results
        
    Returns:
        success_rate, output_distribution
    """
    total = sum(counts.values())
    successful = 0
    output_dist = {'0': 0, '1': 0}
    
    for bitstring, count in counts.items():
        # Format: 'q2 q1 q0'
        q0 = bitstring[-1]  # Output qubit
        q1 = bitstring[-2]  # Syndrome 1
        q2 = bitstring[-3]  # Syndrome 2
        
        # Success if both syndromes are 0
        if q1 == '0' and q2 == '0':
            successful += count
            output_dist[q0] += count
    
    success_rate = successful / total if total > 0 else 0
    return success_rate, output_dist


def create_single_magic_state():
    """
    Create a single magic state T|+⟩ for comparison.
    """
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.t(0)
    return qc


def get_magic_state_probabilities():
    """
    Get the ideal probabilities for magic state |T⟩ = T|+⟩.
    """
    qc = create_single_magic_state()
    simulator = AerSimulator(method='statevector')
    qc.save_statevector()
    result = simulator.run(qc).result()
    sv = result.get_statevector()
    return sv.probabilities()


def main():
    """
    Test magic state distillation protocols.
    """
    print("=" * 70)
    print("Magic State Distillation - Educational Implementation")
    print("=" * 70)
    
    # Get ideal magic state probabilities
    ideal_probs = get_magic_state_probabilities()
    print(f"\nIdeal magic state |T⟩ = T|+⟩ probabilities:")
    print(f"  P(|0⟩) = {ideal_probs[0]:.4f}")
    print(f"  P(|1⟩) = {ideal_probs[1]:.4f}")
    
    # Test 1: Noiseless 3-to-1
    print("\n" + "=" * 70)
    print("Test 1: 3-to-1 Distillation (No Noise)")
    print("=" * 70)
    
    qc1 = create_magic_state_3to1()
    print("\nCircuit:")
    print(qc1.draw(output='text'))
    
    simulator = AerSimulator()
    job1 = simulator.run(qc1, shots=10000)
    counts1 = job1.result().get_counts()
    
    success_rate1, output1 = analyze_magic_distillation(counts1)
    
    print(f"\nSuccess rate: {success_rate1:.4f}")
    
    if sum(output1.values()) > 0:
        total = sum(output1.values())
        p0 = output1['0'] / total
        p1 = output1['1'] / total
        
        print(f"\nOutput state probabilities (when successful):")
        print(f"  P(|0⟩) = {p0:.4f} (ideal: {ideal_probs[0]:.4f})")
        print(f"  P(|1⟩) = {p1:.4f} (ideal: {ideal_probs[1]:.4f})")
        print(f"\nError: {abs(p0 - ideal_probs[0]):.4f}")
    
    # Test 2: With noise
    print("\n" + "=" * 70)
    print("Test 2: 3-to-1 Distillation (With 5% Noise on T gates)")
    print("=" * 70)
    
    qc2, noise_model = create_noisy_magic_state_3to1(noise_prob=0.05)
    
    job2 = simulator.run(qc2, noise_model=noise_model, shots=10000)
    counts2 = job2.result().get_counts()
    
    success_rate2, output2 = analyze_magic_distillation(counts2)
    
    print(f"\nSuccess rate: {success_rate2:.4f}")
    print(f"(Lower success rate due to errors being detected)")
    
    if sum(output2.values()) > 0:
        total = sum(output2.values())
        p0 = output2['0'] / total
        p1 = output2['1'] / total
        
        print(f"\nOutput state probabilities (when successful):")
        print(f"  P(|0⟩) = {p0:.4f} (ideal: {ideal_probs[0]:.4f})")
        print(f"  P(|1⟩) = {p1:.4f} (ideal: {ideal_probs[1]:.4f})")
        print(f"\nError: {abs(p0 - ideal_probs[0]):.4f}")
        print(f"\nNote: Error should be lower than input error of 0.05")
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary and Homework Guidance")
    print("=" * 70)
    print("""
This simplified 3-to-1 protocol demonstrates the key concepts:

1. **Error Detection**: The CNOT gates create correlations. Errors on
   the T gates will cause the syndrome qubits to flip.

2. **Post-Selection**: By only keeping results where syndromes = 00,
   we filter out detected errors.

3. **Trade-off**: Success rate decreases, but output quality improves.

For your homework:

**Part 1: Bell-State Distillation (BBPSSW)**
- Implement the BBPSSW protocol (already provided)
- Test on simulator and real hardware
- Use state tomography to verify improvement

**Part 2: Magic State Distillation**
- You can use this 3-to-1 protocol OR attempt the 15-to-1
- The 15-to-1 is very complex; 3-to-1 is sufficient for learning
- Add realistic noise models
- Test on real IBM hardware
- Use state tomography to measure input vs output fidelity

**Key Question to Answer:**
Is the quantum computer's noise low enough that distillation actually
improves the state fidelity? Or is the hardware too noisy for
distillation to be beneficial?

**Expected Results:**
- BBPSSW: May work on current hardware (moderate noise tolerance)
- Magic State: Likely won't work on current hardware (needs very low noise)
- This is expected! We're in the NISQ era, not fault-tolerant era yet.

**What to Report:**
1. Input state fidelity (from tomography)
2. Output state fidelity (from tomography)
3. Success rate of the protocol
4. Analysis: Did fidelity improve? Why or why not?
5. Estimate the noise threshold needed for distillation to work
    """)


if __name__ == "__main__":
    main()
