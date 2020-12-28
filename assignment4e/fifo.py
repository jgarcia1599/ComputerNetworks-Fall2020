
'''
Usage:

python3 fifo.py 16 0.5 1
'''
import random
import sys

class Packet:
  def __init__(self, input_port, output_port, arrival_tick):
    self.input_port  = input_port
    self.output_port = output_port
    self.arrival_tick= arrival_tick
  def __str__(self):
    return f'Packet received at @ {self.arrival_tick} from port {self.input_port} destined to port {self.output_port}'

# User-supplied parameters
NUM_PORTS    = int(sys.argv[1])
ARRIVAL_PROB = float(sys.argv[2])
SEED         = int(sys.argv[3])

# Total number of simulation ticks
NUM_TICKS    = 20000

# Seed random number generator
random.seed(SEED)

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
    if (random.random() < ARRIVAL_PROB):
      # If so, pick output port uniformly at random
      output_port = random.randint(0, NUM_PORTS - 1)
      input_queues[input_port] += [Packet(input_port, output_port, tick)]
  # TODO: Implement FIFO algorithm:
  # First, look at all the head packets, i.e., packets at the head of each of the input_queues
  # Second, If multiple inputs have head packets destined to the same output port,
  # pick an input port at random, and deq from that. Repeat for each output port.
 
  # More detailed instructions for FIFO algorithm:
  # First, populate a dictionary d that maps an output port to the list of all packets destined to that output.
  # Second, for each output port o, pick one of the packets in the list d[o] at random
  # To pick one packet out of a list at random, you can use the random.choice function.
  # Note: To complete the matching for an input port i that was picked and hence matched to an output port,
  # dequeue from that input port's queue (input_queues[i])
  d = {}
  for queue in input_queues:
    if queue:
      # only grab the first one 
      packet = queue[0]
      try:
        d[packet.output_port].append(packet)
      except KeyError:
        d[packet.output_port] = [packet]
    
## Debugging statements
  # print('INPUT QUEUES ARE: ')
  # for input_queue in range(len(input_queues)):
  #   if input_queues[input_queue]:
  #     print(f'Input queue {input_queue}')
  #     for packet in input_queues[input_queue]:
  #       print(packet)
  # print()
  # print('OUTPUT QUEUES ARE')
  # for o_index in d.keys():
  #   print(f'output queue {o_index}')
  #   if d[o_index]:
  #     for packet in d[o_index]:
  #       print(packet)

  # print('NOW DEQUEING AND ENQUEIONG accordingly')
  for o_index in d.keys():
    # print(f'DEQUEUE {o_index}')
    if d[o_index]:
      # chosen_packet_index = random.randint(0,len(d[o_index])-1)
      chosen_packet = random.choice(d[o_index])
      # chosen_packet_input_queue_index = d[o_index][chosen_packet_index][1]

      # print(chosen_packet)

      delay = tick - chosen_packet.arrival_tick
      delay_sum += delay
      delay_count += 1


      # print(f'Input queue {chosen_packet.input_port}')
      # for x in input_queues[chosen_packet.input_port]:
      #   print(x)
      #dequeue from input queue 
      # print(f'input queue length before {len(input_queues[chosen_packet.input_port])}')
      input_queues[chosen_packet.input_port].remove(chosen_packet)
      # print(f'input queue length after {len(input_queues[chosen_packet.input_port])}')

      # print(f'Input queue {chosen_packet.input_port}')
      # for x in input_queues[chosen_packet.input_port]:
      #   print(x)
      #dequeue from output queue
      # print(f'output queue length before {len(d[o_index])}')
      # print(f'output queue length after {len(d[o_index])}')




  # TODO: Update the average delay based on the packets that were just dequeued.
  # Otherwise, your average delay will be 0/0 because no samples would have been accumulated.

  # Average delay printing
  if (tick % 100 == 0):
    print ("Average delay after ", tick, " ticks = ", delay_sum / delay_count, " ticks")
print()
