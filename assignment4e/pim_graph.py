import random
import os
import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use("Agg")

'''
python3 pim_graph.py 16 1
'''

class Packet:
  def __init__(self, input_port, output_port, arrival_tick):
    self.input_port  = input_port
    self.output_port = output_port
    self.arrival_tick= arrival_tick
  def __str__(self):
    return f'Packet received at @ {self.arrival_tick} from port {self.input_port} destined to port {self.output_port}'


#data collection
delay_y = []
ticks_x = []

# User-supplied parameters
NUM_PORTS    = int(sys.argv[1])
SEED         = int(sys.argv[2])


ARRIVAL_PROB_X = list(np.arange(0.2,1.05,0.05))
PIM_ITERS_TOTAL = [1,2,3]

PIM_AVERAGE_DELAY_Y = [[],[],[]]


# Total number of simulation ticks
NUM_TICKS    = 20000

# Seed random number generator
random.seed(SEED)
for PIM_ITERS in PIM_ITERS_TOTAL:
    for ap in ARRIVAL_PROB_X:
        print(f'Arrival Probability {ap} ; PIM ITER: {PIM_ITERS}')

        # variables to compute average delay of packets transmitted out of output ports
        delay_count = 0
        delay_sum   = 0.0

        # Virtual output queues at each input
        # Initialized to empty queue for each combination of input port and output port
        # These queues sit on the input side.
        voqs = []
        for input_port in range(NUM_PORTS):
            voqs += [[]]
            for output_port in range(NUM_PORTS):
                voqs[input_port] += [[]]

        # Main simulator loop: Loop over ticks
        for tick in range(NUM_TICKS):
            # Tick every input port
            for input_port in range(NUM_PORTS):
                # Is there a packet here?
                if (random.random() < ap):
                    # If so, pick output port uniformly at random
                    output_port = random.randint(0, NUM_PORTS - 1)
                    voqs[input_port][output_port] += [Packet(input_port, output_port, tick)]

            # TODO: Implement PIM algorithm with a single iteration.
            # You can use the random.choice() function to pick one item at random from a list of items.
            if PIM_ITERS ==1:
                d={}
                for input_port_queue in voqs:
                    if any(input_port_queue):
                        virtual_output_port_queue = random.choice([vopq for vopq in input_port_queue if len(vopq)>=1])
                        packet = virtual_output_port_queue[0]
                        try:
                            d[packet.output_port].append(packet)
                        except KeyError:
                            d[packet.output_port] =[packet]

                for o_index in d.keys():
                    if d[o_index]:
                        # accept phase: pick a random packet destined to the output port and deque it
                        chosen_packet_in_output_queue = random.choice(d[o_index])
                        # print(chosen_packet_in_output_queue)

                        # calculate stats
                        delay = tick - chosen_packet_in_output_queue.arrival_tick
                        delay_sum += delay
                        delay_count += 1

                        #collect data
                        # delay_y.append(delay)
                        # ticks_x.append(tick)


                        # debugging print statements
                        # for packet in voqs[chosen_packet_in_output_queue.input_port][chosen_packet_in_output_queue.output_port]:
                        #   print('hii')
                        #   print(packet)

                        # dequeue from voc
                        voqs[chosen_packet_in_output_queue.input_port][chosen_packet_in_output_queue.output_port].remove(chosen_packet_in_output_queue)

            # TODO: Generalize this to multiple iterations by simply running the same code in a loop a fixed number of times
            # Each iteration must only consider inputs+outputs that are still unmatched after the previous iterations.

            else:
                already_dequed_outputport = []
                already_dequed_inputport = []
                for iteration in range(PIM_ITERS):
                    # print(iteration)
                    # print(input_port_options)
                    # print(output_port_options)
                    d = {}
                    for index_i,input_port_queue in enumerate(voqs):

                        if any(input_port_queue) and index_i not in already_dequed_inputport:
                            virtual_output_port_queue = random.choice([vopq for vopq in input_port_queue if len(vopq)>=1])
                            packet = virtual_output_port_queue[0]
                            try:
                                d[packet.output_port].append(packet)
                            except KeyError:
                                d[packet.output_port] =[packet]


                    for o_index in d.keys():
                        if d[o_index] and o_index not in already_dequed_outputport:
                            # accept phase: pick a random packet destined to the output port and deque it
                            chosen_packet_in_output_queue = random.choice(d[o_index])

                            # calculate stats
                            delay = tick - chosen_packet_in_output_queue.arrival_tick
                            delay_sum += delay
                            delay_count += 1


                            voqs[chosen_packet_in_output_queue.input_port][chosen_packet_in_output_queue.output_port].remove(chosen_packet_in_output_queue)

                            # add to input and output ports to already matched lsts
                            already_dequed_outputport.append(chosen_packet_in_output_queue.output_port)
                            already_dequed_inputport.append(chosen_packet_in_output_queue.input_port)





            # For both variants of PIM, if input I is matched to output O, complete the matching by dequeueing from voqs[I][O].

            # TODO: Update the average delay every time a packet is dequeued from a VOQ as a result of the matching process.
            # Otherwise, your average delay will be 0/0 because no samples would have been accumulated.

            # Average delay printing
            # if (tick % 100 == 0):
            #     print ("Average delay after ", tick, " ticks = ", delay_sum / delay_count, " ticks")
            #     delay_y.append(delay_sum / delay_count)
            #     ticks_x.append(tick)
        PIM_AVERAGE_DELAY_Y[PIM_ITERS-1].append(delay_sum / delay_count)

        
print(len(PIM_AVERAGE_DELAY_Y[2]))
print(len(ARRIVAL_PROB_X))

dirname = os.path.dirname(__file__)
# print(self.window_sizes_ticks)
# print(self.window_sizes)
plt.figure(figsize=(20,20))

for PIM_Y_index in range(len(PIM_AVERAGE_DELAY_Y)):
    print(PIM_Y_index)
    plt.plot(ARRIVAL_PROB_X,PIM_AVERAGE_DELAY_Y[PIM_Y_index],label=f'PIM Iteration {PIM_Y_index+1}')

plt.title('PIM Simulation for 20000 ticks')
plt.xlabel('Arival Probability')
plt.ylabel('Average delay after simulation')
plt.legend()
# plt.xticks(np.arange(0,10000,step=100))

# plt.show()
plt.savefig(os.path.join(dirname, 'figures/pim.png'), format='png')
plt.close()
