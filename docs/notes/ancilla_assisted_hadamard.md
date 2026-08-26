# Ancilla-Assisted Hadamard Transformation for Stabilizer Codes

Theoretical derivation for performing a logical Hadamard transformation $\bar{H}$ using an additional ancilla qubit and controlled logical $\bar{X}$ and $\bar{Z}$ gates.

## Derivation

The computational basis states transform under $\bar{H}$ as:

$$\bar{H} |\bar{0}\rangle = \frac{1}{\sqrt{2}} (|\bar{0}\rangle + |\bar{1}\rangle)$$

$$\bar{H} |\bar{1}\rangle = \frac{1}{\sqrt{2}} (|\bar{0}\rangle - |\bar{1}\rangle)$$

$$\bar{H} \frac{1}{\sqrt{2}} (|\bar{0}\rangle + |\bar{1}\rangle) = |\bar{0}\rangle$$

$$\bar{H} \frac{1}{\sqrt{2}} (|\bar{0}\rangle - |\bar{1}\rangle) = |\bar{1}\rangle$$

where $|\bar{0}\rangle$ and $|\bar{1}\rangle$ are the logical $|0\rangle$ and $|1\rangle$ states, respectively.

Consider a register with target logical qubit in state $|\bar{\psi}\rangle = \alpha |\bar{0}\rangle + \beta |\bar{1}\rangle$ plus an ancilla initialized to $|0\rangle$. In general:

$$\bar{H} |\bar{\psi}\rangle \otimes |0\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1 \\ 1 & -1\end{bmatrix} \begin{bmatrix}\alpha \\ \beta\end{bmatrix} \otimes |0\rangle = \frac{1}{\sqrt{2}}((\alpha + \beta)|\bar{0}\rangle + (\alpha - \beta)|\bar{1}\rangle)\otimes |0\rangle$$

We can perform controlled logical operations where the single-bit ancilla acts as the control. Consider the following sequence of gates, where $C\bar{X}_{2,1}$ performs $\bar{X}|\bar{\psi}\rangle$ controlled by the ancilla qubit, $C\bar{Z}_{2,1}$ acts similarly, $H_2$ performs the single-qubit Hadamard gate on the ancilla, and $X_2$ performs the single-qubit Pauli-X gate on the ancilla:

$$H_2 C\bar{Z}_{2,1} X_2 C\bar{X}_{2,1} H_2 C\bar{Z}_{2,1} C\bar{X}_{2,1} H_2 |\bar{\psi} 0\rangle$$

$$= H_2 C\bar{Z}_{2,1} X_2 C\bar{X}_{2,1} H_2 C\bar{Z}_{2,1} C\bar{X}_{2,1} |\bar{\psi} + \rangle$$

$$= H_2 C\bar{Z}_{2,1} X_2 C\bar{X}_{2,1} H_2 C\bar{Z}_{2,1} C\bar{X}_{2,1} ((\alpha |\bar{0}\rangle + \beta |\bar{1}\rangle) |+\rangle)$$

$$= \frac{1}{\sqrt{2}} H_2 C\bar{Z}_{2,1} X_2 C\bar{X}_{2,1} H_2 C\bar{Z}_{2,1} C\bar{X}_{2,1} (\alpha |\bar{0}0\rangle + \beta |\bar{1}0\rangle + \alpha |\bar{0}1\rangle + \beta |\bar{1}1\rangle)$$

$$= \frac{1}{\sqrt{2}} H_2 C\bar{Z}_{2,1} X_2 C\bar{X}_{2,1} H_2 C\bar{Z}_{2,1} (\alpha |\bar{0}0\rangle + \beta |\bar{1}0\rangle + \alpha |\bar{1}1\rangle + \beta |\bar{0}1\rangle)$$

$$= \frac{1}{\sqrt{2}} H_2 C\bar{Z}_{2,1} X_2 C\bar{X}_{2,1} H_2 (\alpha |\bar{0}0\rangle + \beta |\bar{1}0\rangle - \alpha |\bar{1}1\rangle + \beta |\bar{0}1\rangle)$$

$$= \frac{1}{\sqrt{2}} H_2 C\bar{Z}_{2,1} X_2 C\bar{X}_{2,1} (\alpha |\bar{0}+\rangle + \beta |\bar{1}+\rangle - \alpha |\bar{1}-\rangle + \beta |\bar{0}-\rangle)$$

$$= \frac{1}{2} H_2 C\bar{Z}_{2,1} X_2 C\bar{X}_{2,1} (\alpha (|\bar{0}0\rangle + |\bar{0}1\rangle) + \beta(|\bar{1}0\rangle + |\bar{1}1\rangle) - \alpha (|\bar{1}0\rangle - |\bar{1}1\rangle) + \beta (|\bar{0}0\rangle - |\bar{0}1\rangle))$$

*(Optionally, measure the ancilla here and apply $\bar{X}$ if 1 and $\bar{Z}$ if 0. Without measurement, the circuit continues:)*

$$= \frac{1}{2} H_2 C\bar{Z}_{2,1} X_2 (\alpha (|\bar{0}0\rangle + |\bar{1}1\rangle) + \beta(|\bar{1}0\rangle + |\bar{0}1\rangle) - \alpha (|\bar{1}0\rangle - |\bar{0}1\rangle) + \beta (|\bar{0}0\rangle - |\bar{1}1\rangle))$$

$$= \frac{1}{2} H_2 C\bar{Z}_{2,1} (\alpha (|\bar{0}1\rangle + |\bar{1}0\rangle) + \beta(|\bar{1}1\rangle + |\bar{0}0\rangle) - \alpha (|\bar{1}1\rangle - |\bar{0}0\rangle) + \beta (|\bar{0}1\rangle - |\bar{1}0\rangle))$$

$$= \frac{1}{2} H_2 (\alpha (|\bar{0}1\rangle + |\bar{1}0\rangle) + \beta(|\bar{0}0\rangle - |\bar{1}1\rangle) + \alpha (|\bar{0}0\rangle + |\bar{1}1\rangle) + \beta (|\bar{0}1\rangle - |\bar{1}0\rangle))$$

$$= \frac{1}{\sqrt{2}} H_2 (\alpha|\bar{0}+\rangle + \alpha|\bar{1}+\rangle + \beta|\bar{0}+\rangle - \beta|\bar{1}+\rangle)$$

$$= \frac{1}{\sqrt{2}} (\alpha|\bar{0}\rangle + \alpha|\bar{1}\rangle + \beta|\bar{0}\rangle - \beta|\bar{1}\rangle) \otimes |0\rangle$$

$$= \frac{1}{\sqrt{2}} ((\alpha + \beta)|\bar{0}\rangle + (\alpha - \beta)|\bar{1}\rangle) \otimes |0\rangle$$

This gate sequence uses the predetermined logical $\bar{X}$ and $\bar{Z}$ operations for any stabilizer code to implement a logical Hadamard gate with a single ancilla qubit.
