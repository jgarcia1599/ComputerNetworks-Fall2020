from packet import *
from timeout_calculator  import *  # Import timeout calculator for StopAndWait

# Usage:
# python3 simulator.py --seed 1 --host_type StopAndWait --rtt_min 10 --ticks 50
# python3 simulator.py --seed 1 --host_type StopAndWait --rtt_min 10 --ticks 50 --loss_ratio 0.5

class StopAndWaitHost:
  """
  This host implements the stop and wait protocol. Here the host only
  sends one packet in return of an acknowledgement.
  """
  def __init__(self):
    self.in_order_rx_seq = -1      # maximum sequence number received so far in order
    self.ready_to_send = True      # can we send a packet or are we still waiting for an ACK?
    self.packet_sent_time   = -1   # when was this packet sent out last?
    self.timeout_calculator = TimeoutCalculator() # initialize TimeoutCalculator
    #dictionary to store sequence numbers
    self.sequence_number = 0

  def send(self, tick):
    """
    Function to send a packet with the next sequence number on to the network.
    """
    # print(tick)
    # print(self.timeout_calculator.timeout)
    if (self.ready_to_send):
      sequence_number = self.in_order_rx_seq + 1
      # TODO: Send next sequence number by creating a packet
      next_packet = Packet(tick,sequence_number)
      # TODO: Remember to update packet_sent_time and ready_to_send appropriately
      self.packet_sent_time = tick
      self.ready_to_send = False
      # TODO: Return the packet
      self.sequence_number +=1
      print(f"sent packet @ {tick} with sequence number {next_packet.seq_num}")
      return next_packet
    elif (tick - self.packet_sent_time >= self.timeout_calculator.timeout):
      # TODO: Timeout has been exceeded, retransmit packet
      
      sequence_number = self.in_order_rx_seq + 1
      # following the same procedure as above when transmitting a packet for the first time
      next_packet = Packet(tick,sequence_number)
      self.packet_sent_time = tick
      self.ready_to_send = False
      print(f"Retransmitting packet @ {tick} with sequence number {next_packet.seq_num}")
      # TODO: Exponentially back off the timer
      self.timeout_calculator.exp_backoff()
      # TODO: Set retx field on packet to detect retransmissions for debugging
      next_packet.rtx = True
      # TODO: Return the packet
      return next_packet

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

    # print("hiii")

    # TODO: Update timeout based on RTT sample
    timeout = self.timeout_calculator.update_timeout(rtt_sample)

    print(f"@ {tick} timeout computed to be {timeout}")

    print(f"received packet @ {tick} with sequence number {pkt.seq_num}")
    print("----------------------------------------------------------------")
    # print("Packet sequencce number {}".format(pkt.seq_num))
    # print("Maximum sequence number so far received {}".format(self.in_order_rx_seq))
    # TODO: Update self.in_order_rx_seq and self.ready_to_send depending on pkt.seq_num
    if pkt.seq_num == (self.in_order_rx_seq + 1):
      self.in_order_rx_seq = pkt.seq_num
      self.ready_to_send = True
      
