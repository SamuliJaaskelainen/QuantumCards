from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, IBMQ, execute
from qiskit.providers.aer import noise
from qiskit.providers.aer.noise import NoiseModel
from random import shuffle

def get_scores(game, s, simulate = True, noisy = False):

	#Initialisation
	q = QuantumRegister(s)
	c = ClassicalRegister(s)
	qc = QuantumCircuit(q, c)

	#Shuffle players' qubits
	qbts = [i for i in range(0, s)]
	shuffle(qbts)
	pq = {}
	for p in range(0, s):
		pq[p] = qbts[p]

	#Parse game string and construct quantum circuit
	i = 0
	while i < len(game):
		g = game[i].upper()
		if g == "H":
			p = pq[int(game[i+1])-1]
			qc.h(q[p])
			i += 2
		elif g == "I":
			p = pq[int(game[i+1])-1]
			qc.iden(q[p])
			i += 2
		elif g == "X":
			p = pq[int(game[i+1])-1]
			qc.x(q[p])
			i += 2
		elif g == "Y":
			p = pq[int(game[i+1])-1]
			qc.y(q[p])
			i += 2
		elif g == "Z":
			p = pq[int(game[i+1])-1]
			qc.z(q[p])
			i += 2
		elif g == "C":
			p1 = pq[int(game[i+1])-1]
			p2 = pq[int(game[i+2])-1]
			qc.cx(q[p1], q[p2])
			i += 3
		elif g == "S":
			p1 = pq[int(game[i+1])-1]
			p2 = pq[int(game[i+2])-1]
			qc.swap(q[p1], q[p2])
			i += 3
		else:
			print("Error",g)
	
	#Measurement
	qc.measure(q, c)
	if simulate:
		if noisy:
			#Load IBMQ credentials
			IBMQ.load_accounts()
			device = IBMQ.get_backend('ibmqx4') #4-qubit IBMQ
			noise_model = noise.device.basic_device_noise_model(device.properties())
			backend = Aer.get_backend('qasm_simulator')
			job_sim = execute(qc, backend, noise_model = noise_model)
		else:
			backend = Aer.get_backend('qasm_simulator')
			job_sim = execute(qc, backend, noise_model = None)
	else:
			#Load IBMQ credentials
			IBMQ.load_accounts()
			backend = IBMQ.get_backend('ibmqx4') #4-qubit IBMQ
			job_sim = execute(qc, backend)
	
	sim_result = job_sim.result()
	counts = sim_result.get_counts(qc)

	#Compute players' scores
	score = [0]*s
	for result in counts:
		c = counts[result]
		for p in range(0, s):
			if result[s-1-pq[p]] == "1":
				score[p] += c
	
	return score;

def check_game(game, s):
	gates = {"H": 1, "I": 1, "X": 1, "Y": 1, "Z": 1, "C": 2, "S": 2}	
	valid = True
	i = 0
	while i < len(game):
		g = game[i].upper()
		if g not in gates:
			valid = False
			break
		else:
			if i + gates[g] >= len(game):
				valid = False
				break
			for j in range(0, gates[g]):
				n = game[i+j+1]
				if ord(n) not in range(ord("1"), ord("1")+s):
					valid = False
					break
			if gates[g] > 1 and game[i+1] == game[i+2]:
				valid = False
				break
		i += gates[g] + 1
	
	return valid;
	
