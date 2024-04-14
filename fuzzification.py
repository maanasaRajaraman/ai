import matplotlib.pyplot as plt
    
height = 1

membership_values = {
  "nm": [31, 61, 95],
  "ns": [61, 95, 127],
  "ze": [95, 127, 159],
  "ps": [127, 159, 191],
  "pm": [159, 191, 223],
  "nl": [0, 0, 31, 61],
  "pl": [191, 223, 255, 280],
}

rules = [["nl", "ze", "pl"],
         ["ze", "nl", "pl"],
         ["nm", "ze", "pm"],
         ["ns", "ps", "ps"],
         ["ps", "ns", "ns"],
         ["pl", "ze", "nl"],
         ["ze", "ns", "ps"],
         ["ze", "nm", "pm"]]
     

def is_valid_rule(speed_rule, speed, acc_rule, acc):
    speed_membership = membership_values[speed_rule]
    acc_membership = membership_values[acc_rule]

    if speed_membership[0] <= speed and speed <= speed_membership[-1]:
        if acc_membership[0] <= acc and acc <= acc_membership[-1]:
            return True
    
    return False
     

def fuzzyfication(rule, speed, acc):
    speed_mem = membership_values[rule[0]]
    acc_mem = membership_values[rule[1]]

    u_speed = max(min( (speed - speed_mem[0])/(speed_mem[1]- speed_mem[0]), (speed_mem[2]-speed)/(speed_mem[2]-speed_mem[1])), 0)
    u_acc = max(min((acc - acc_mem[0])/ (acc_mem[1] - acc_mem[0]), (acc_mem[2] - acc)/ (acc_mem[2]- acc_mem[1])), 0)

    return min(u_acc, u_speed)
     

def calculate_area_and_weighted_area(rule, fuzzy_value):
    throttle_mem = membership_values[rule[2]]
    
    m1 = (1 - 0)/(throttle_mem[1] - throttle_mem[0])
    m2 = (0 - 1)/(throttle_mem[2] - throttle_mem[1])
    
    a1 = (fuzzy_value - 0 + m1*throttle_mem[0])/m1
    a2 = (fuzzy_value - 1 + m2*throttle_mem[1])/m2
    
    a = a2 - a1
    b = throttle_mem[2] - throttle_mem[0]
    
    plt.plot([a1, a2], [fuzzy_value, fuzzy_value])
    
    area = 0.5 * fuzzy_value * (a + b)
    weighted_area = area * throttle_mem[1]
    
    return (area, weighted_area)
     

def plot_graph():

  for label in membership_values:
    if len(membership_values[label]) == 4:
      plt.plot(membership_values[label], [0, 1, 1, 0], label=label)
    else:
      plt.plot(membership_values[label], [0, 1, 0], label=label)  

     

def calculate_throttle_control(speed, acceleration):
    weighted_area_sum = 0
    area_sum = 0
    
    for rule in rules:
        if is_valid_rule(rule[0], speed, rule[1], acceleration):
            print(rule)
            fuzzy_value = fuzzyfication(rule, speed, acceleration)
            x, y = calculate_area_and_weighted_area(rule, fuzzy_value)
            area_sum+=x
            weighted_area_sum+=y
            
    print(weighted_area_sum/area_sum)
            
     

def fuzzy_control_system():
    plot_graph()
    
    plt.xlabel("throttle control")
    plt.ylabel("membership value")
    
    calculate_throttle_control(100, 70)

    plt.legend()
    plt.show()

fuzzy_control_system()
