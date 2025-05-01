from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.circuit import IfElseOp
from qiskit_aer import AerSimulator as Aer
from qiskit_aer.noise import NoiseModel, pauli_error
import numpy as np
'''
Derek Wingard, 04/2025

Evaluates a Bacon-Shor[[9,1,3]] subsystem code and performs majority vote decoding in post processing.

import whole file to run

'''
def bacon_shor():


    data = QuantumRegister(9, 'data')
    ancillax = QuantumRegister(6, 'ancillax')
    ancillaz = QuantumRegister(6, 'ancillaz')
    measure_all = ClassicalRegister(9, 'test')
    syndromex = ClassicalRegister(6, 'syndromex')
    syndromez = ClassicalRegister(6, 'syndromez')
    #qc = QuantumCircuit(data,syndromex, syndromez, ancillax, ancillaz, measure_all)
    qc = QuantumCircuit(data,syndromex, syndromez, ancillax, ancillaz, measure_all)

    def double_encoding():
        

        qc.cx(data[0],data[3])
        qc.cx(data[0],data[6])

        for i in [0,3,6]:
            qc.h(data[i])
            qc.cx(data[i],data[i+1])
            qc.cx(data[i],data[i+2])

        for i in range(9):
            qc.h(data[i])

    def prepare_GHZ():

        qc.h(data[0])
        
        for i in range(8):
            qc.cx(data[0],data[i+1])

    def correct_bit_flip():



        with qc.if_test((syndromez[0], 1)) as else_:
            with qc.if_test((syndromez[1], 0)):
                qc.x(data[0])

        with qc.if_test((syndromez[0], 0)) as else_:
            with qc.if_test((syndromez[1], 1)):
                qc.x(data[2])

        with qc.if_test((syndromez[0], 1)) as else_:
            with qc.if_test((syndromez[1], 1)):
                pass


        with qc.if_test((syndromez[2], 1)) as else_:
            with qc.if_test((syndromez[3], 0)):
                qc.x(data[3])

        with qc.if_test((syndromez[2], 0)) as else_:
            with qc.if_test((syndromez[3], 1)):
                qc.x(data[5])

        with qc.if_test((syndromez[2], 1)) as else_:
            with qc.if_test((syndromez[3], 1)):
                pass


        with qc.if_test((syndromez[4], 1)) as else_:
            with qc.if_test((syndromez[5], 0)):
                qc.x(data[6])

        with qc.if_test((syndromez[4], 0)) as else_:
            with qc.if_test((syndromez[5], 1)):
                qc.x(data[8])

        with qc.if_test((syndromez[4], 1)) as else_:
            with qc.if_test((syndromez[5], 1)):
                pass


    def correct_phase_flip():   



        with qc.if_test((syndromex[0], 1)) as else_:
            with qc.if_test((syndromex[3], 0)):
                qc.z(data[0])

        with qc.if_test((syndromex[0], 0)) as else_:
            with qc.if_test((syndromex[3], 1)):
                qc.z(data[6])

        with qc.if_test((syndromex[0], 1)) as else_:
            with qc.if_test((syndromex[3], 1)):
                pass



        with qc.if_test((syndromex[1], 1)) as else_:
            with qc.if_test((syndromex[4], 0)):
                qc.z(data[1])

        with qc.if_test((syndromex[1], 0)) as else_:
            with qc.if_test((syndromex[4], 1)):
                qc.z(data[7])

        with qc.if_test((syndromex[1], 1)) as else_:
            with qc.if_test((syndromex[4], 1)):
                pass



        with qc.if_test((syndromex[2], 1)) as else_:
            with qc.if_test((syndromex[5], 0)):
                qc.z(data[2])

        with qc.if_test((syndromex[2], 0)) as else_:
            with qc.if_test((syndromex[5], 1)):
                qc.z(data[8])

        with qc.if_test((syndromex[2], 1)) as else_:
            with qc.if_test((syndromex[5], 1)):
                pass



    def decoder():

        correct_bit_flip()
        correct_phase_flip()



    def majority_vote_decoder(counts):
        one_count = []
        zero_count = []
        for bitstring, count in counts.items():
            measured = bitstring.split()[0]
            measured_as_int = np.int64(measured)
            if np.sum(measured_as_int) > 4:
                measured = '1'
                one_count.append(count)
            else: 
                measured = '0'
                zero_count.append(count)
            
        one_counts = np.sum(one_count)
        zero_counts = np.sum(zero_count)   
        
        final_m = ['0','1']
        final_c = [zero_counts, one_counts]    
        final_results = dict(zip(final_m, final_c))
        print(  final_results)

        
        


    def build():

        #double_encoding()
        prepare_GHZ()

        count = 0
        for n in range(0,9,3):
            for j in range(3):
                if n == 6:
                    break
                idx1,idx2 = n+j, n+j+3
                qc.h(ancillax[count])
                qc.cx(data[idx1], ancillax[count])
                qc.cx(data[idx2], ancillax[count])
                qc.h(ancillax[count])
                qc.measure(ancillax[count], syndromex[count])
                count+=1
                


        count = 0
        for n in range(0,9,3):
            for j in range(2):
                idx1,idx2 = n+j, n+j+1
                qc.cx(data[idx1], ancillaz[count])
                qc.cx(data[idx2], ancillaz[count])
                qc.measure(ancillaz[count], syndromez[count])
                count+=1

        
        qc.measure(data,measure_all)

    def evaluate(error_prob=0.003):


        sim = Aer()
        noise_model =  NoiseModel()
        split = error_prob/2
        rest = 1-error_prob
        simulated_error_operator_1d = pauli_error([('X', split), ('Z', split), ('I', rest)])
        simulated_error_operator_2d = pauli_error([
            ('II', rest), ('IX', 0.5*split), ('XI', 0.5*split) , ('IZ', 0.5*split), ('ZI', 0.5*split)])
        noise_model.add_all_qubit_quantum_error(simulated_error_operator_1d, ['x','z', 'h'])
        noise_model.add_all_qubit_quantum_error(simulated_error_operator_2d, ['cx'])


        transpiled_circuit = transpile(qc , backend=sim)
        results = sim.run(transpiled_circuit,noise_model=noise_model, shots=1023).result()
        #results = sim.run(transpiled_circuit, shots=1023).result()
        counts= results.get_counts()
        #print(counts)
        majority_vote_decoder(counts)






    build()
    decoder()
    evaluate()



bacon_shor()




