# Bacon-Shor[[9,1,3]]

## Bacon-Shor code for 3x3 distance 1 

As this is a demonstration of the code, the explanation will be more general and the details can be found in the following papers,

1. https://arxiv.org/pdf/quant-ph/0506023

2. https://arxiv.org/pdf/2009.11482


The code works as follows:

* Prepares a GHZ state for simplicity of measurement, but the standard routine given in (2) is also available in the code, which embeds a 3 qubit bit-flip redundancy code into a 3 qubit phase-flip redundancy code
* Performs syndrome measurements in period-2 measurement cycle of non-commuting groups of weight-2 gauges, $$X_{i}X_[i+3]$$-type and $$Z_{i}Z_{i+1}$$-type. Since these are gauge measurements which do not disturb the encoded information, we can simply switch between both gauge fixings and extract all the same information as a full weight-6 stabilizer.
* Direct error correction using pauli gates may be applied using syndrome measurements from pairs of gauge group generators and the correspoding 
* Circuit is evaluated with an artificial noise model correponding to a .3% change of error at each gate, being either X or Z type errors.
* After curcuit results are taken, a majority voting is performed where, given we start with a GHZ state, we should get results like measuring a single qubit in superposition.


## Important Notes
* Direct error correction is performed here for the sake of demonstration. It is recognized that in practice, one only performs error correction modulo subsystem structure, meaning our correction may act nontrivially on the gauge space, so long as the logical encoded codespace is restored (1)
* It is also understood that a GHZ state is not a natural state to prepare for this system, however it makes for the most intuitive interpretation of results
* It should be noted, one can combine weight-2 gauge measurements to construct the weight-6 stabilizers, effectively making a stabilizer code which does not measure stabilizers directly. If one wants to go "all the way", simply replace the ancilla to correspond to a stabilizer each, instead of a gauge group generator.


## Required Libraries in requirements.txt
* numpy==2.2.5
* qiskit==2.0.0
* qiskit_aer==0.17.0


## How to run this project in your environment

1. clone this project:
    'git clone https://github.com/DOWingard/Bacon-Shor.git'
2. pip install -r requirements.txt
4. import bacon_shor to execute


