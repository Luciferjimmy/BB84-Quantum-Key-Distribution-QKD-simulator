# BB84 Quantum Key Distribution Simulator

*"Where quantum physics meets unbreakable encryption"*  

**A hands-on journey through quantum cryptography** - Experience the revolutionary BB84 protocol that uses the strange laws of quantum mechanics to create perfectly secure communication.

## Why This Matters

In a world of increasing cyber threats, quantum cryptography offers:
- **Provable security** backed by physics laws
- **Eavesdropper detection** - know immediately if someone's listening
- **Future-proof** protection against quantum computers

This simulator makes these complex concepts **visually intuitive** and interactive.

## How to Use

1. **Alice prepares** qubits in random states (|0⟩, |1⟩, |+⟩, |-⟩)
2. **Bob measures** them in random bases
3. **Compare bases** to distill a secret key
4. **Toggle Eve** to see how quantum mechanics exposes eavesdroppers


# Run locally
git clone https://github.com/Luciferjimmy/BB84-Quantum-Key-Distribution-QKD-simulator.git
cd BB84-Quantum-Key-Distribution-QKD-simulator
python bb84_simulation.py

## Key Features
Feature	Description
Realistic Qubit Visualization	See photons in different polarization states
Interactive Eve	Watch how eavesdropping introduces detectable errors
Error Rate Calculation	Automatic QBER (Quantum Bit Error Rate) analysis

## Simulation Output Example

Output- 
🔁 Attempt 3
Sifted Key Length: 9
QBER: 22.22%
Eve Detected: True
Sifted Key (Alice): [1, 0, 1, 1, 0, 0, 1, 0, 1]
Sifted Key (Bob):   [1, 0, 0, 1, 1, 0, 1, 0, 1]

✅ Secure key established after 3 attempts!

## The Science Behind It
The BB84 protocol leverages two quantum principles:

- Heisenberg Uncertainty Principle: Measuring quantum states disturbs them
- No-Cloning Theorem: Quantum states cannot be perfectly copied

When Eve intercepts:

- She guesses wrong basis 75% of the time
- Introduces ~25% error rate (detectable by Alice & Bob)
- Perfect security when QBER < 11%

## Dependencies
Python 3.8+
Qiskit
Matplotlib
NumPy

## Roadmap
- Add quantum channel noise simulation
- Implement error correction
- Add multi-qubit entanglement visualization

## How to Contribute
We welcome quantum enthusiasts! To contribute:

- Fork the repository
- Create a feature branch (git checkout -b feature/quantum-magic)
- Commit your changes (git commit -m 'Add Schrödinger mode')
- Push to the branch (git push origin feature/quantum-magic)
- Open a Pull Request

## License
MIT License - See LICENSE for details.

The quantum security revolution starts here. Clone the repo and experience the future of encryption today!

**"The universe is not only stranger than we imagine, it's stranger than we can imagine." - J.B.S. Haldane**
