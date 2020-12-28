
'''
Usage:
python3 fifo_graph.py 16 1
'''
import random
import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

class Packet:
  def __init__(self, input_port, output_port, arrival_tick):
    self.input_port  = input_port
    self.output_port = output_port
    self.arrival_tick= arrival_tick
  def __str__(self):
    return f'Packet received at @ {self.arrival_tick} from port {self.input_port} destined to port {self.output_port}'

# User-supplied parameters
NUM_PORTS    = int(sys.argv[1])
SEED         = int(sys.argv[2])

ARRIVAL_PROB_X = list(np.arange(0.1,1.05,0.05))
AVERAGE_DELAY_Y = []
print(f'Arrival probabilities{ARRIVAL_PROB_X}')
# Total number of simulation ticks
NUM_TICKS    = 20000

# Seed random number generator
random.seed(SEED)


for ap in ARRIVAL_PROB_X:
    print(f'Arrival Probability : {ap}')
    # variables to compute average delay of packets transmitted out of output ports
    delay_count = 0
    delay_sum   = 0.0

    # One input queue for each input port
    # Initialized to empty queue for each input port
    input_queues = []
    for input_port in range(NUM_PORTS):
        input_queues += [[]]
    # Main simulator loop: Loop over ticks
    for tick in range(NUM_TICKS):
        # Tick every input port
        for input_port in range(NUM_PORTS):
            # Is there a packet here?
            if (random.random() < ap):
                # If so, pick output port uniformly at random
                output_port = random.randint(0, NUM_PORTS - 1)
                input_queues[input_port] += [Packet(input_port, output_port, tick)]
        d = {}
        for queue in input_queues:
            if queue:
                # only grab the first one 
                packet = queue[0]
                try:
                    d[packet.output_port].append(packet)
                except KeyError:
                    d[packet.output_port] = [packet]

        # print('NOW DEQUEING AND ENQUEIONG accordingly')
        for o_index in d.keys():
            # print(f'DEQUEUE {o_index}')
            if d[o_index]:
                # chose a random packet from output queue
                chosen_packet = random.choice(d[o_index])

                # calulate stats
                delay = tick - chosen_packet.arrival_tick
                delay_sum += delay
                delay_count += 1

                #dequeue from input queue
                input_queues[chosen_packet.input_port].remove(chosen_packet)




        # TODO: Update the average delay based on the packets that were just dequeued.
        # Otherwise, your average delay will be 0/0 because no samples would have been accumulated.

        # Average delay printing
        if (tick % 100 == 0):
            print ("Average delay after ", tick, " ticks = ", delay_sum / delay_count, " ticks")
    AVERAGE_DELAY_Y.append(delay_sum / delay_count)
    print()
dirname = os.path.dirname(__file__)
plt.figure(figsize=(20,20))
plt.plot(ARRIVAL_PROB_X,AVERAGE_DELAY_Y)
plt.xlabel('Arrival Probability')
# Set the y axis label of the current axis.
plt.ylabel('Average delay after simulation')
# Set a title of the current axes.
plt.title('Fifo Simulation for 20000 ticks')

# plt.show()
plt.savefig(os.path.join(dirname, 'figures/fifo.png'), format='png')
plt.close()
