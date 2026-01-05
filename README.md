# Bell-State and Magic State Distillation: Educational Materials

This package contains educational materials for teaching quantum state distillation protocols, including theoretical explanations, implementation examples, and a comprehensive homework assignment.

## Contents

### 1. Educational Documents

**`distillation_explanation.md`**
- Comprehensive explanation of Bell-state and magic state distillation
- Covers the BBPSSW protocol for entanglement distillation
- Explains the 15-to-1 protocol for magic state distillation
- Introduces quantum state tomography for verification
- Written in an accessible style suitable for advanced undergraduate or graduate students

### 2. Implementation Examples

**`bbpssw_homework.py`**
- Implementation of the BBPSSW Bell-state distillation protocol
- Uses Qiskit dynamic circuits with mid-circuit measurements
- Includes simulation and analysis functions
- Students will complete and extend this for the homework

**`magic_state_homework.py`**
- Implementation of the 15-to-1 magic state distillation protocol
- Demonstrates the specific pattern of 15 T-gates across 5 qubits
- Includes syndrome measurement and post-selection logic
- Students will complete and test this on real hardware

**`tomography_homework.py`**
- Quantum state tomography implementation
- Shows how to measure states in different bases
- Demonstrates fidelity calculation
- Includes examples for both Bell states and magic states

### 3. Homework Assignment

**`distillation_homework.md`**
- Complete homework assignment for students
- Two main problems: Bell-state distillation and magic state distillation
- Requires implementation, simulation, and real hardware testing
- Central question: "Is the quantum computer below the threshold for distillation to work?"
- Includes state tomography verification requirements

## Key Concepts Covered

### Why These Protocols Matter

Both protocols address the fundamental challenge of noise in quantum computing:

1. **Bell-State Distillation (BBPSSW)**
   - Purifies noisy entangled pairs
   - Essential for quantum communication and distributed quantum computing
   - Uses local operations and classical communication (LOCC)
   - Demonstrates error filtering through measurement post-selection

2. **Magic State Distillation (15-to-1)**
   - Produces high-fidelity non-Clifford states
   - Enables universal fault-tolerant quantum computation
   - Based on quantum error-correcting codes
   - Shows cubic error suppression (p_out ≈ 35p_in³)

### The Core Question

The homework is designed around a critical experimental question:

> **Is the current quantum hardware below the noise threshold such that distillation actually improves state fidelity?**

Students will:
1. Measure input state fidelity using quantum state tomography
2. Run the distillation protocol on real IBM Quantum hardware
3. Measure output state fidelity
4. Compare input vs. output to determine if distillation worked
5. Analyze whether the device noise is low enough for the protocol to be beneficial

## Using These Materials

### For Instructors

1. **Lecture Preparation:**
   - Use `distillation_explanation.md` as a basis for lectures
   - The document explains both "what" and "why" for each protocol
   - Includes mathematical details and intuitive explanations

2. **Lab Session:**
   - Walk students through the Python examples
   - Demonstrate how to use Qiskit dynamic circuits
   - Show how to connect to IBM Quantum hardware
   - Explain state tomography procedures

3. **Assignment:**
   - Distribute `distillation_homework.md` and the three Python templates
   - Ensure students have IBM Quantum access
   - Recommend devices with dynamic circuit support and lowest noise
   - Set deadline allowing time for hardware queue

### For Students

1. **Read the Theory:**
   - Start with `distillation_explanation.md`
   - Understand the circuit structure and why it works
   - Pay attention to the error detection mechanisms

2. **Study the Code:**
   - Review all three Python files
   - Understand the circuit construction
   - Learn how dynamic circuits work in Qiskit

3. **Complete the Homework:**
   - Follow the tasks in `distillation_homework.md`
   - Test your code in simulation first
   - Run on real hardware and collect data
   - Perform state tomography to verify results
   - Write a comprehensive report with analysis

## Technical Requirements

### Software
- Python 3.8 or higher
- Qiskit >= 1.0
- Qiskit Aer (for simulation)
- Qiskit IBM Runtime (for hardware access)
- Qiskit Experiments (for state tomography)
- NumPy, Matplotlib

### Hardware Access
- IBM Quantum account (free tier available)
- Access to devices supporting dynamic circuits
- Recommended: devices with < 1% gate error rates

### Installation

```bash
pip install qiskit qiskit-aer qiskit-ibm-runtime qiskit-experiments numpy matplotlib
```

## Important Notes

### Dynamic Circuits

Both protocols require **dynamic circuits** - the ability to:
- Perform mid-circuit measurements
- Use measurement outcomes for classical control flow
- Conditionally apply gates based on measurement results

Not all IBM Quantum devices support dynamic circuits. Check the device specifications before selecting a backend.

### State Tomography Overhead

Quantum state tomography requires many measurements:
- 1 qubit: 3 measurement settings (X, Y, Z)
- 2 qubits: 9 measurement settings (XX, XY, XZ, YX, YY, YZ, ZX, ZY, ZZ)
- N qubits: 3^N measurement settings

For the homework, students will perform tomography on 1-2 qubit systems, which is manageable. Emphasize that tomography becomes exponentially expensive for larger systems.

### Expected Outcomes

**Bell-State Distillation:**
- Success probability: ~50% in ideal case
- Fidelity improvement: depends on input noise
- On current hardware: may or may not show improvement

**Magic State Distillation:**
- Success probability: depends on input error rate
- Requires very low input errors to be beneficial
- On current hardware: likely will NOT show improvement
- This is expected and is part of the learning experience!

The goal is for students to understand that we are still in the NISQ era, and many fault-tolerance protocols require better hardware than we currently have.

## Additional Resources

### Papers
- Bennett et al., "Purification of Noisy Entanglement" (1996)
- Bravyi & Kitaev, "Universal quantum computation with ideal Clifford gates" (2005)
- Litinski, "Magic State Distillation: Not as Costly as You Think" (2019)

### Documentation
- Qiskit Dynamic Circuits: https://qiskit.org/documentation/
- IBM Quantum Experience: https://quantum.ibm.com/
- Qiskit Experiments: https://qiskit-community.github.io/qiskit-experiments/

## Contact

For questions about these materials, please contact your course instructor.

---

**Created by:** Manus AI  
**Date:** January 04, 2026  
**Version:** 1.0

## 🌐 Interactive Website

**NEW:** An interactive web application for visualizing the distillation protocols!

**Live Demo:** https://3000-isjg55ap8jksw7e9otzci-fda10d60.us2.manus.computer

### Features
- **Holographic UI Design** with glassmorphism effects and purple gradient theme
- **Step-by-step Circuit Animations** for both BBPSSW and 15-to-1 protocols
- **Real-time Parameter Controls** to adjust noise levels and see effects
- **Theoretical Calculations** showing error suppression formulas
- **Educational Explanations** integrated with interactive visualizations

### Running Locally

```bash
cd quantum-distillation-viz
pnpm install
pnpm dev
```

The website provides an engaging way to understand the protocols before implementing them in code!

