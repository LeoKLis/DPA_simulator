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
        if stack_state < 'A' and stack_state > 'Z':
            self.stack.insert(0, stack_state)
        self.dpa_dict = self._build_dpa()
    
    def _build_dpa(self):
        for line in sys.stdin:
            temp = line.split("->")
            self.dpa_dict[temp[0]] = temp[1]

    def simulate(self, input):
        for el in input:
            current_key = ",".join([self.current_state, el , self.stack.pop(0)])
            if current_key in self.dpa_dict:
                if self.stack:
                    current_string = self.current_state + "#" + "".join(self.stack) + "|"
                else:
                    current_string = self.current_state + "#" + "$" + "|"
                transition = self.dpa_dict[current_key].split(",")
                self.current_state = transition[0]
                if transition[1] != "$":
                    self.stack[:0] = [*transition[1]]
                print(current_string, end="")
            else:
                current_string = "fail|"
                self.current_state = "-"
                success = 0
                break
        if self.current_state in self.acc_states_arr:
            success = 1
        print(success)

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
