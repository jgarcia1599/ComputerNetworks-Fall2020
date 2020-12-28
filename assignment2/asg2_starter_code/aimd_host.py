import sys
from packet import *
from timeout_calculator  import *
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use("Agg")
import os

# python3 simulator.py --seed 1 --host_type  Aimd --rtt_min 20 --ticks 1000 --queue_limit 10
class UnackedPacket:
  """
  Structure to store information associated with an unacked packet
  so that we can maintain a list of such UnackedPacket objects
  
  Data members of this class include

  seq_num:  Sequence number of the unacked packet

  num_retx: Number of times this packet has been retransmitted so far

  timeout_duration: Timeout duration for this packet

  timeout_tick: The time (in ticks) at which the packet timeout

  """

  def __init__(self, seq_num):
    """
    Constructor for UnackedPacket. This sets the default values for class data members

    """
    self.seq_num      = seq_num # sequence number of unacked packet
    self.num_retx     = 0       # how many times it's been retransmitted so far
    self.timeout_duration = 0   # what is the duration of its timeout
    self.timeout_tick     = 0   # at what tick does this packet timeout?

  def __str__(self):
    """
    String representation of unacked packet for debugging

    """
    return str(self.seq_num)

class AimdHost:
  """
  This class implements a host that follows the AIMD protocol.
  Data members of this class are

  **unacked**: List of unacked packets

  **window**: Size of the window at any given moment

  **max_seq**: Maximum sequence number sent so far

  **in_order_rx_seq**: Maximum sequence number received so far

  **slow_start**: Boolean to indicate whether algorithm is in slow start or not

  **next_decrease**: Time (in ticks) at which the window size should be descreased

  **timeout_calculator**: An object of class TimeoutCalculator
  (Refer to TimeoutCalculator class for more information)
    
  There are two member functions - send and recv that perform the task of sending
  and receiving packets respectively. All send and receive logic should be written
  within one of these two functions.

  """
  def __init__(self):
    self.unacked = []           # list of unacked packets
    self.window = 1             # We'll initialize window to 1
    self.max_seq = -1           # maximum sequence number sent so far
    self.in_order_rx_seq = -1   # maximum sequence number received so far in order
    self.slow_start = True      # Are we in slow start?
    self.next_decrease = -1     # When to next decrease your window; adds some hystersis
    self.timeout_calculator = TimeoutCalculator() # object for computing timeouts

    # utility cache to store all received packets to determine self.in_order_rx_seq
    self.received_cache = []
    # data collection lists for plotting purposes
    self.window_sizes = []
    self.window_sizes_ticks = []
    self.next_increase = -1

  def send(self, tick):
    """
    Function to send packet on to the network. Host should first retransmit any
    Unacked packets that have timed out. Host should also descrease the window size
    if it is time for the next decrease. After attempting retransmissions, if the window
    is not full, fill up the window with new packets.
    
    Args:

        **tick**: Simulated time

    Returns:
        
        A list of packets that the host wants to transmit on to the network
    """
    print("\n\n")
    print ("@ tick " + str(tick) + " window is " + str(self.window))
    print(f'Next Decrease: {self.next_decrease}')

    #collect data for plot
    self.window_sizes.append(self.window)
    self.window_sizes_ticks.append(tick)

    # TODO: Create an empty list of packets that the host will send
    packets_to_send = []
    # First, process retransmissions
    for i in range(0, len(self.unacked)):
      unacked_pkt = self.unacked[i]
      if (tick >= unacked_pkt.timeout_tick):
        # TODO: Retransmit any packet that has timed out
        # by doing the following in order
        # (1) creating a new packet,
        retransmit_unacked_pkt = UnackedPacket(unacked_pkt.seq_num)
        # (2) setting its retx attribute to True (just for debugging)
        retransmit_unacked_pkt.retx = True
        # (3) Append the packet to the list of packets created earlier
        packets_to_send.append(Packet(tick,unacked_pkt.seq_num))
        # (4) Backing off the timer
        print("---------------------------------------------------------------------------------")
        print(f"Retransmitting @ tick {tick} packet with sequence number {unacked_pkt.seq_num} ")
        timeout = self.timeout_calculator.exp_backoff()

        # (5) Updating timeout_tick and timeout_duration appropriately after backing off the timer
        retransmit_unacked_pkt.timeout_duration = timeout
        retransmit_unacked_pkt.timeout_tick = tick + timeout
        # (6) Updating num_retx]
        self.unacked[i] = retransmit_unacked_pkt
        
        # TODO: Multiplicative decrease, if it's time for the next decrease      
        print("First lost, we will move from slow start to congestion avoidance.")
        if tick >= self.next_decrease:
          self.window = max(int(self.window/2),1)
          self.next_decrease = tick + self.timeout_calculator.mean_rtt
          print(f"Scheduling next decrease for {self.next_decrease}")
        self.slow_start = False

      


        

    # Now fill up the window with new packets
    while (len(self.unacked) < self.window):
      # TODO: Create new packets, set their retransmission timeout, and transmit them
      sequence_number = self.max_seq+1
      #Unacked Packet for bookeping
      new_unacked_packet = UnackedPacket(sequence_number)
      new_unacked_packet.timeout_duration = self.timeout_calculator.timeout
      new_unacked_packet.timeout_tick = self.timeout_calculator.timeout + tick

      #Normal Packet for network
      new_packet = Packet(tick,sequence_number)
      packets_to_send.append(new_packet)
      print("---------------------------------------------------------------------------------")
      print(f'Sent packet @ tick {tick} with sequence number {sequence_number}')
      print("---------------------------------------------------------------------------------")
      # TODO: Remember to update self.max_seq and add the just sent packet to self.unacked
      self.max_seq +=1
      self.unacked.append(new_unacked_packet)
      
     
    
    # TODO: Return the list of packets that need to be sent on to the network
    return packets_to_send

  def recv(self, pkt, tick):
    """
    Function to get a packet from the network.

    Args:
        
        **pkt**: Packet received from the network

        **tick**: Simulated time
    """
    assert(tick > pkt.sent_ts)
    print(tick)
    
    # TODO: Compute RTT sample
    rtt_sample = tick - pkt.sent_ts
    # TODO: Update timeout
    timeout = self.timeout_calculator.update_timeout(rtt_sample)
    # TODO: Remove received packet from self.unacked
    for unacked in self.unacked:
      if unacked.seq_num == pkt.seq_num:
        self.unacked.remove(unacked)
    print("\n\n")
    print("---------------------------------------------------------------------------------")
    print(f"Received packet @ tick {tick} with sequence number {pkt.seq_num}")
    print(f"RTT Sample: {rtt_sample}  RTT_Mean: {self.timeout_calculator.mean_rtt}")
    # TODO: Update in_order_rx_seq to reflect the largest sequence number that you
    # have received in order so far

    self.received_cache.append(pkt.seq_num)
    self.received_cache.sort()
    if len(self.received_cache)!= 0:
      for received_packet_index in range(1,len(self.received_cache)):
        current = self.received_cache[received_packet_index]
        previous = self.received_cache[received_packet_index-1]
        if current - previous >= 2:
          # found largest sequence number received
          self.in_order_rx_seq = previous
          break
        else:
          self.in_order_rx_seq = current
    else:
      self.in_order_rx_seq = self.received_cache[-1]

    # TODO: Increase your window given that you just received an ACK. Remember that:
    # 1. The window increase rule is different for slow start and congestion avoidance.
    # 2. The recv() function is called on every ACK (not every RTT), so you should adjust your window accordingly.
    if self.slow_start == True:
      #During slow start, we increase the window by 1 for every acknowledgment
      previous_window = self.window
      self.window +=1
      self.next_increase = tick+self.timeout_calculator.mean_rtt
      print(f"slow start increase from {previous_window} to {self.window}")
    else:
      if tick >= self.next_increase:
        previous_window = self.window
        self.next_increase = tick+self.timeout_calculator.mean_rtt
        self.window +=1
        print(f"congestion avoidance, we will increase the window from {previous_window} to {self.window}")

    print("---------------------------------------------------------------------------------")
  def plot(self):
    '''
    Function to plot collected data during experiment.
    Creates a plot where the y-axis is the window size and thhe x-axis is time in ticks
    '''

    dirname = os.path.dirname(__file__)
    # print(self.window_sizes_ticks)
    # print(self.window_sizes)
    plt.figure(figsize=(100,20))
    plt.plot(self.window_sizes_ticks,self.window_sizes)
    plt.xticks(np.arange(0,10000,step=100))
    
    # plt.show()
    plt.savefig(os.path.join(dirname, 'figures/aimd.png'), format='png')
    plt.close()
