from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import random
import matplotlib.pyplot as plt
import numpy as np

# Safe display for environments without IPython
try:
    from IPython.display import display
except ImportError:
    def display(x):
        print(x)

def bb84_protocol(num_qubits=100, eve_present=True, eve_intercept_prob=1.0, noise_prob=0.05):
    alice_bits = [random.randint(0, 1) for _ in range(num_qubits)]
    alice_bases = [random.randint(0, 1) for _ in range(num_qubits)]  # 0 = Z, 1 = X
    bob_bases = [random.randint(0, 1) for _ in range(num_qubits)]
    eve_bases = [random.randint(0, 1) for _ in range(num_qubits)]
    eve_attacks = [False] * num_qubits

    qc = QuantumCircuit(num_qubits, num_qubits)

    # Step 1: Alice prepares qubits
    for i in range(num_qubits):
        if alice_bits[i]:
            qc.x(i)
        if alice_bases[i]:
            qc.h(i)

    # Step 2: Eve intercepts (REALISTICALLY)
    if eve_present:
        for i in range(num_qubits):
            if random.random() < eve_intercept_prob:
                eve_attacks[i] = True

                if eve_bases[i]:
                    qc.h(i)  # Rotate to X basis
                qc.measure(i, i)
                qc.barrier(i)
                qc.reset(i)
                if random.randint(0, 1):
                    qc.x(i)
                if eve_bases[i]:
                    qc.h(i)
                qc.barrier(i)

    # Add channel noise
    for i in range(num_qubits):
        if random.random() < noise_prob:
            qc.x(i)  # Flip the qubit (simulates channel noise)

    # Step 3: Bob measures
    for i in range(num_qubits):
        if bob_bases[i]:  # Fixed typo from bob_bases to bob_bases
            qc.h(i)
        qc.measure(i, i)

    # Step 4: Simulate circuit
    backend = AerSimulator()
    compiled_circuit = transpile(qc, backend)
    result = backend.run(compiled_circuit, shots=1).result()
    counts = list(result.get_counts().keys())[0]
    bob_results = [int(bit) for bit in reversed(counts)]

    # Step 5: Sifting
    sifted_indices = [i for i in range(num_qubits) if alice_bases[i] == bob_bases[i]]
    sifted_key = [alice_bits[i] for i in sifted_indices]
    bob_sifted = [bob_results[i] for i in sifted_indices]

    error_count = sum(1 for i in range(len(sifted_key)) if sifted_key[i] != bob_sifted[i])
    qber = error_count / len(sifted_key) if sifted_key else 0

    return {
        'alice_bits': alice_bits,
        'alice_bases': alice_bases,
        'bob_bases': bob_bases,
        'bob_results': bob_results,
        'sifted_key': sifted_key,
        'bob_sifted': bob_sifted,
        'qber': qber,
        'eve_detected': qber > 0.11,
        'eve_attacks': eve_attacks,
        'circuit': qc
    }

# Simple XOR encryption using the shared key
def xor_encrypt(message, key):
    message_bits = [ord(char) for char in message]
    key_repeated = key * (len(message_bits) // len(key)) + key[:len(message_bits) % len(key)]
    encrypted = [m ^ int(k) for m, k in zip(message_bits, key_repeated)]
    return encrypted

def xor_decrypt(encrypted, key):
    key_repeated = key * (len(encrypted) // len(key)) + key[:len(encrypted) % len(key)]
    decrypted = ''.join(chr(c ^ int(k)) for c, k in zip(encrypted, key_repeated))
    return decrypted

# 🚀 Retry Loop Until Eve is Not Detected
max_attempts = 10
mismatch_log = []
results = None

for attempt in range(1, max_attempts + 1):
    print(f"\n🔁 Attempt {attempt}")
    results = bb84_protocol(num_qubits=20, eve_present=True, eve_intercept_prob=0.3)

    print(f"Sifted Key Length: {len(results['sifted_key'])}")
    print(f"QBER: {results['qber']:.2%}")
    print(f"Eve Detected: {results['eve_detected']}")
    print("Sifted Key (Alice):", results['sifted_key'])
    print("Sifted Key (Bob):  ", results['bob_sifted'])

    # Log mismatches for histogram
    errors = [i for i in range(len(results['sifted_key'])) if results['sifted_key'][i] != results['bob_sifted'][i]]
    mismatch_log.extend(errors)

    if not results['eve_detected']:
        print(f"\n✅ Secure key established after {attempt} attempt(s)!\n")
        break
    else:
        print("⚠️ Eve was detected, retrying...")

# Save the final sifted key
if results and not results['eve_detected']:
    with open("key.txt", "w") as f:
        key_string = ''.join(map(str, results['sifted_key']))
        f.write(key_string)
    print("🔐 Final key saved to key.txt!")

    # Encrypting a message
    message = "hello world"
    encrypted_msg = xor_encrypt(message, results['sifted_key'])
    decrypted_msg = xor_decrypt(encrypted_msg, results['sifted_key'])

    print("🔒 Encrypted:", encrypted_msg)
    print("🔓 Decrypted:", decrypted_msg)

# 🎯 Visualizations
plt.figure(figsize=(14, 6))

# Alice vs Bob Bases
plt.subplot(1, 2, 1)
plt.title("Alice vs Bob Bases")
plt.plot(results['alice_bases'], 'bo', label='Alice Bases')
plt.plot(results['bob_bases'], 'rx', label='Bob Bases')
plt.ylabel("Basis (0 = Z, 1 = X)")
plt.xlabel("Qubit Index")
plt.legend()

# Errors + Eve Interference
plt.subplot(1, 2, 2)
plt.title(f"Errors and Eve Attacks (QBER: {results['qber']:.2%})")
plt.plot(results['sifted_key'], 'bo-', label="Alice's Key")
plt.plot(results['bob_sifted'], 'rx', label="Bob's Results")

error_pos = [i for i in range(len(results['sifted_key'])) if results['sifted_key'][i] != results['bob_sifted'][i]]
plt.plot(error_pos, [results['sifted_key'][i] for i in error_pos], 'gs', label='Errors', markersize=10)

eve_indices = [i for i, attacked in enumerate(results['eve_attacks']) if attacked]
plt.vlines(eve_indices, ymin=-0.2, ymax=1.2, colors='gray', linestyles='dotted', label='Eve Interference')

plt.xlabel("Qubit Index")
plt.ylabel("Bit Value")
plt.legend()
plt.tight_layout()
plt.show()

# Mismatch histogram
plt.figure(figsize=(10, 4))
plt.hist(mismatch_log, bins=range(128), color='red', alpha=0.7)
plt.title("🔁 Histogram of Mismatch Positions Across Retries")
plt.xlabel("Qubit Index")
plt.ylabel("Frequency of Mismatch")
plt.tight_layout()
plt.show()

# 🧠 Display Final Circuit
display(results['circuit'].draw(output='mpl', fold=-1, scale=0.6))