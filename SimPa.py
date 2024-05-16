import sys

class DPA:
    dpa_dict = {}
    stack = []

    def __init__(self, states_arr, symbols_arr, stack_arr, acc_states_arr, init_state, stack_state):
        self.states_arr = states_arr
        self.symbols_arr = symbols_arr
        self.stack_arr = stack_arr
        self.acc_states_arr = acc_states_arr
        self.current_state = init_state
        if stack_state > 'A' and stack_state < 'Z':
            self.stack.insert(0, stack_state)
        self._build_dpa()

    def _build_dpa(self):
        for line in sys.stdin:
            temp = line[:-1].split("->")
            self.dpa_dict[temp[0]] = temp[1]

    def simulate(self, input):
        print(self.current_state + "#" + self.stack[0] + "|", end="")
        for el in input:
            print(self.stack)
            stack_element = self.stack.pop(0)
            if self.current_state not in self.acc_states_arr:
                for k in self.dpa_dict.keys():
                    if self.current_state in k and "$" in k and stack_element in k:
                        # print("(U epsilon dijelu sam)", end="")
                        transition = self.dpa_dict[k].split(",")
                        self.stack[:0] = [*transition[1]]
                        self.current_state = transition[0]
                        current_string = self.current_state + "#" + "".join(self.stack)
                        print(current_string, end="|")
                        continue
            current_key = ",".join([self.current_state, el , stack_element])
            if current_key in self.dpa_dict.keys():
                # print("(U normalnom dijelu sam)", end="")
                transition = self.dpa_dict[current_key].split(",") # Sljedece stanje i upis na stog
                self.current_state = transition[0]
                if transition[1] != "$":
                    self.stack[:0] = [*transition[1]]
                if len(self.stack) > 0:
                    current_string = self.current_state + "#" + "".join(self.stack) + "|"
                else:
                    current_string = self.current_state + "#" + "$" + "|"
                print(current_string, end="")
            else:
                print("fail|", end="")
                self.current_state = "-"
                success = 0
                break
        if self.current_state in self.acc_states_arr:
            success = 1
        else:
            success = 0
        print(success)
# Rjesiti epsilon prijelaze, pa ce to bit pri kraju rjesavanja!!!!
def main():
    input_arr = input().split("|")
    states_arr = input().split(",")
    symbols_arr = input().split(",")
    stack_arr = input().split(",")
    acc_states_arr = input().split(",")
    init_state = input()
    stack_state = input()

    automata = DPA(states_arr, symbols_arr, stack_arr, acc_states_arr, init_state, stack_state)

    for el in input_arr:
        automata.simulate(el.split(","))

if __name__ == "__main__":
    main()
