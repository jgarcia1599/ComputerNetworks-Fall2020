import sys
from packet import *
from timeout_calculator  import *

#  python3 simulator.py --seed 1 --host_type SlidingWindow --rtt_min 10 --ticks 50 --window_size 5
class UnackedPacket:
  """
  Structure to store information associated with an unacked packet
  so that we can maintain a list of such UnackedPacket objects.

  This structure is different from the packet structure that is used
  by the simulator. Be careful to not mix Packet and UnackedPacket
  
  The network does not understand an UnackedPacket. It is only used by
  sliding window host for bookkeeping.
  """
  def __init__(self, seq_num):
    self.seq_num      = seq_num # sequence number of unacked packet
    self.num_retx     = 0       # how many times it's been retransmitted so far
    self.timeout_duration = 0   # what is the duration of its timeout
    self.timeout_tick     = 0   # at what tick does this packet timeout?
  def __str__(self):            # string representation of unacked packet for debugging
    return str(self.seq_num)

class SlidingWindowHost:
  """
  This host follows the SlidingWindow protocol. It maintains a window size and the
  list of unacked packets. The algorithm itself is documented with the send method
  """
  def __init__(self, window_size):
    self.unacked = []           # list of unacked packets
    self.window = window_size   # window size
    self.max_seq = -1           # maximum sequence number sent so far
    self.in_order_rx_seq = -1   # maximum sequence number received so far in order
    self.timeout_calculator = TimeoutCalculator() # object for computing timeouts
    # utility cache to store all received packets to deter
    self.received_cache = []

    #below variables are for data collection purposes
    self.originalpacketssent = 0
    self.originalpacketsreceived = 0
    self.retransmittedpactekssent = 0
    self.retransmittedpacteksreceived = 0



  def send(self, tick):
    """
    Method to send packets on to the network. Host must first check if there are any
    unacked packets, it yes, it should retransmist those first. If the window is still
    empty, the host can send more new packets on to the network.

    Args:
        
        **tick**: Current simulated time

    Returns:
        A list of packets that need to be transmitted. Even in case of a single packet,
        it should be returned as part of a list (i.e. [packet])
    """
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
        network_packet_retransmission = Packet(tick,unacked_pkt.seq_num)
        network_packet_retransmission.retx = True
        packets_to_send.append(network_packet_retransmission)
        # (4) Backing off the timer

        #DONT PRINT WHEN COLLECTING DATA FOR GRAPHS
        print("---------------------")
        print(f"Retransmitting @ tick {tick} packet with sequence number {unacked_pkt.seq_num} ")
        timeout = self.timeout_calculator.exp_backoff()
        print("---------------------")

        # Track Retransmitted Packet Sent
        self.retransmittedpactekssent+=1

        # (5) Updating timeout_tick and timeout_duration appropriately after backing off the timer
        retransmit_unacked_pkt.timeout_duration = timeout
        retransmit_unacked_pkt.timeout_tick = tick + timeout
        # (6) Updating num_retx
        self.unacked[i] = retransmit_unacked_pkt

    assert(len(self.unacked) <= self.window)

    # Now fill up the window with new packets
    while (len(self.unacked) < self.window):
      # TODO: Create new packets, set their retransmission timeout, and add them to the list

      sequence_number = self.max_seq+1
      #Unacked Packet for bookeping
      new_unacked_packet = UnackedPacket(sequence_number)
      new_unacked_packet.timeout_duration = self.timeout_calculator.timeout
      new_unacked_packet.timeout_tick = self.timeout_calculator.timeout + tick

      #Normal Packet for network
      new_packet = Packet(tick,sequence_number)
      packets_to_send.append(new_packet)
      #DONT PRINT WHEN COLLECTING DATA FOR GRAPHS
      print("---------------------")
      print(f'Sent packet @ {tick} with sequence number {sequence_number}')
      print("---------------------")

      # Track Original Packet sent
      self.originalpacketssent +=1

      # TODO: Remember to update self.max_seq and add the just sent packet to self.unacked
      self.max_seq +=1
      self.unacked.append(new_unacked_packet)
     


    # window must be filled up at this point
    assert(len(self.unacked) == self.window)

    # TODO: return the list of packets that need to be transmitted on to
    # the network
    return packets_to_send

  def recv(self, pkt, tick):
    """
    Function to get a packet from the network.

    Args:
        
        **pkt**: Packet received from the network

        **tick**: Simulated time
    """

    assert(tick > pkt.sent_ts)
    # TODO: Compute RTT sample
    rtt_sample = tick - pkt.sent_ts
    # TODO: Update timeout
    timeout = self.timeout_calculator.update_timeout(rtt_sample)
    # TODO: Remove received packet from self.unacked
    for unacked in self.unacked:
      if unacked.seq_num == pkt.seq_num:
        self.unacked.remove(unacked)

    if pkt.retx == True:
      self.retransmittedpacteksreceived +=1
    else:
      self.originalpacketsreceived +=1
    #DONT PRINT WHEN COLLECTING DATA FOR GRAPHS
    print("---------------------")
    print(f"Received packet @ {tick} with sequence number {pkt.seq_num}")
    print("---------------------")
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


    assert(len(self.unacked) <= self.window)
