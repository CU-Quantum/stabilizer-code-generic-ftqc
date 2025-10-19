# Implementing 1-Qubit Simon's Algorithm with Surface Codes

This README provides a clear, example-driven walkthrough of how to implement Simon's Algorithm (1-qubit case) fault-tolerantly using surface code logical qubits. We’ll also compare two fault-tolerant methods for implementing logical CNOT: Transversal CNOT and Lattice Surgery.

---

## What is Simon’s Algorithm (1-qubit case)?

Simon's Algorithm solves the problem: given a function $( f: \{0,1\}^n \to \{0,1\}^n )$ that is either:
- 1-to-1, or
- 2-to-1 with a hidden period $( s \ne 0 )$

The algorithm finds $( s )$ efficiently. For $( n = 1 )$:

- $( f(0) = 0, f(1) = 0 )$ → periodic $( s = 1 )$
- $( f(0) = 0, f(1) = 1 )$ → 1-to-1 $( s = 0 )$

We’ll focus on the 2-to-1 case.

---

## Basic Simon Circuit for 1-Qubit

```
|0> ---H---●---H---M---  (result = s)
           |   
|0> -------Uf--------M---
```

Where:
- The top wire is the input register
- The bottom is the output register (for $( f(x) )$)
- The oracle $( U_f )$ is usually a CNOT gate

---

## Surface Code: Overview

Surface codes encode logical qubits across a 2D grid of physical qubits. They provide extremely high fault tolerance and are the backbone of most real quantum error correction.

- Each logical qubit is encoded using a $( d \times d )$ patch (e.g., $( 3 \times 3 )$)
- Logical operations are implemented via:
  - Transversal gates (if possible)
  - Lattice surgery (measurement-based entanglement)

---

## Step-by-step: Simon's Algorithm with Surface Code Logical Qubits

### Step 1: Encode two logical qubits
- Patch A = logical $( |x\rangle )$
- Patch B = logical $( |f(x)\rangle )$

### Step 2: Apply H to Patch A
- This creates a superposition over $( x )$

### Step 3: Apply logical CNOT (Patch A → Patch B)
- This implements the oracle $( U_f )$

### Step 4: Apply H to Patch A again and measure
- We recover the hidden string $( s )$

---

## Option 1: Transversal CNOT

### What it is
Apply physical CNOTs between corresponding qubits of two patches:

```python
for i in range(d**2):
    circuit.append(CNOT(control[i], target[i]))
```

### Pros
- Simple circuit
- Fast gate (one timestep)
- Matches textbook logical CNOT operator definition

### Cons
- Only works if patches are perfectly aligned
- Not flexible in layout
- Rarely used in hardware due to routing/layout constraints

---

## Option 2: Lattice Surgery

### What it is
A measurement-based method to entangle two logical qubits via their shared boundary:

1. Merge patches: measure Z⊗Z stabilizer across boundary
2. Measure ancilla qubit to extract parity
3. Split patches

This creates a logical CNOT indirectly.

### Pros
- Works between arbitrary logical qubits (not just aligned patches)
- Fault-tolerant
- Used by Google, IBM, and most surface code experiments

### Cons
- Involves 2–3 rounds of stabilizer measurements
- More complex circuit and scheduling

---

## Which One Should We Use?

| Feature              | Transversal CNOT | Lattice Surgery |
|---------------------|------------------|-----------------|
| Patch alignment      | Required         | Not required    |
| Qubit layout flexibility | Low          | High            |
| Fault-tolerance      | Yes (ideal)      | Yes (practical) |
| Real hardware usage  | Rare             | Common          |
| Latency              | Low              | Moderate        |

Use transversal CNOT in simulation/toy models where patches are aligned.  
Use lattice surgery in realistic or layout-flexible architectures.


---


## Understanding Aligned Patches in Surface Codes

### What Does “Aligned Patches” Mean?

In the context of **surface codes**, “aligned patches” refers to two **logical qubit patches** (each a block of physical qubits) being laid out on the 2D lattice in a way that:

1. They are the **same size** (e.g., both are $d \times d$ patches).
2. Each physical qubit in the first patch has a **corresponding physical qubit** in the second patch, at the **same relative position**.

This alignment allows operations like **transversal CNOT** to be performed cleanly and fault-tolerantly.

---

### Why Alignment Matters

For some quantum error-correcting codes (like Steane or color codes), **transversal gates** allow fault-tolerant logical operations by applying **identical physical gates** between corresponding qubits across logical blocks.

In surface codes, this only works **if the patches are perfectly aligned**. If they're not, transversal logic fails to preserve the stabilizer structure or logical operator transformations.

---

### Visual Example

Assume both Patch A and Patch B are $3 \times 3$ surface code patches:

```
Patch A (Control)        Patch B (Target)
+---+---+---+            +---+---+---+
| A | B | C |            | A'| B'| C'|
+---+---+---+            +---+---+---+
| D | E | F |            | D'| E'| F'|
+---+---+---+            +---+---+---+
| G | H | I |            | G'| H'| I'|
+---+---+---+            +---+---+---+
```

These are **aligned** if:

- A ↔ A’, B ↔ B’, ..., I ↔ I’

Then a transversal logical CNOT is implemented as:

```text
CNOT(A, A’)
CNOT(B, B’)
...
CNOT(I, I’)
```

---

### What If They’re Not Aligned?

If the patches:
- Are **different sizes**
- Are **misaligned** or **rotated**
- Are **separated on the chip**

Then applying transversal gates will not:
- Map logical operators correctly (e.g., $X_L \to X_L \otimes X_L$)
- Preserve stabilizer commutation
- Be fault-tolerant

In these cases, transversal CNOT is invalid.

---

### Alternative: Lattice Surgery

When patches aren't aligned or when the architecture restricts qubit placement, you can still perform logical entanglement using **lattice surgery**. This method:

- Measures **joint stabilizers** across patch boundaries
- Doesn't require qubit alignment
- Is widely used in real hardware systems like Google’s and IBM’s surface code chips

---

### Summary Table

| Condition                  | Transversal CNOT | Lattice Surgery |
|---------------------------|------------------|-----------------|
| Requires aligned patches  | Yes              | No              |
| Requires equal patch size | Yes              | No              |
| Used in practice          | Rarely           | Frequently      |
| Layout flexible           | No               | Yes             |

---

# TL;DR

To implement Simon’s algorithm fault-tolerantly using surface codes:
- You’ll need to apply a logical CNOT between two logical qubits.
- Surface codes can support transversal CNOT only in ideal, aligned cases.
- Lattice surgery is the industry-standard way to implement this reliably.

For most scalable designs, lattice surgery is the preferred method.
