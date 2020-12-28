'''
Usage:
python3 hash_tables.py 0.7 2left
python3 hash_tables.py 0.7 2choice

python3 hash_tables.py 0.7 standard


'''


import random
import sys

OCCUPANCY = float(sys.argv[1])  # How occupied is the table?
NUM_SLOTS = 100                 # number of slots
CAP_PER_SLOT = 5                # capacity of each slot
TOTAL_TRIALS = 1000             # total number of random trials
NUM_ELEMENTS = int(OCCUPANCY * NUM_SLOTS * CAP_PER_SLOT) # Compute total number of elements
assert(OCCUPANCY <= 1)          # there is enough storage for all elements

trials_with_collisions = 0
for seed in range(TOTAL_TRIALS):
  random.seed(seed)             # seed random number generator
  occupancy = [0] * NUM_SLOTS   # zero out occupancy
  for i in range(NUM_ELEMENTS): # hash each element
    if (sys.argv[2] == "standard"): # standard hash table
      #TODO: Implement standard hashing by picking a slot number randomly between 0 and NUM_SLOTS - 1
      #Write the final slot number that you pick into the variable slot_number, which is currently set to 0.
      slot_number = random.randint(0,NUM_SLOTS-1)


    elif (sys.argv[2] == "2choice"):# power of 2 choices hashing
      #TODO: Implement 2 choice hashing: pick two slot numbers randomly and then pick the less occupied of the 2
      #Break ties randomly.
      #Write the final slot number that you pick into the variable slot_number, which is currently set to 0.
      slot_number_1 =  random.randint(0,NUM_SLOTS-1)
      slot_number_2 = random.randint(0,NUM_SLOTS-1)
      if occupancy[slot_number_1] == occupancy[slot_number_2]:
        slot_number = random.choice([slot_number_1,slot_number_2])
      elif occupancy[slot_number_1] > occupancy[slot_number_2]:
        slot_number = slot_number_2
      elif occupancy[slot_number_1] < occupancy[slot_number_2]:
        slot_number = slot_number_1

    elif (sys.argv[2] == "2left"):  # 2-left hashing
      #TODO: Implement 2 left hashing: pick two slots numbers from two sub tables and pick the less occupied of the 2
      #Always break ties towards one sub table
      #Write the final slot number that you pick into the variable slot_number, which is currently set to 0.
      sub_table_1 = list(range(0,int((NUM_SLOTS)/2)))
      sub_table_2 = list(range(int((NUM_SLOTS/2)),NUM_SLOTS-1))

      slot_number_1 = random.choice(sub_table_1)
      slot_number_2 = random.choice(sub_table_2)

      if occupancy[slot_number_1]> occupancy[slot_number_2]:
        slot_number = slot_number_2
      elif occupancy[slot_number_1]< occupancy[slot_number_2]:
        slot_number = slot_number_1
      elif occupancy[slot_number_1] == occupancy[slot_number_2]:
        slot_number = slot_number_1

    else:
      assert(False)

    # Increment occupancy at slot_number
    occupancy[slot_number] += 1

  if any([counter > CAP_PER_SLOT for counter in occupancy]): # check if any slot has exceeded its capacity
    trials_with_collisions += 1

print ("Fraction of trials in which slot size did not exceed capacity ", 1.0 - (trials_with_collisions/TOTAL_TRIALS))
