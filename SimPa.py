import sys

class DPA:
    CONST_DPA_DICT = {}
    CONST_STACK = []

    def __init__(self, init_state, stack_state, acc_states_arr):
        self.acc_states_arr = acc_states_arr
        self.CONST_CURRENT_STATE = init_state
        self.CONST_STACK.insert(0, stack_state)
        self._init_dpa()

    def _init_dpa(self):
        for line in sys.stdin:
            temp = line[:-1].split("->")
            self.CONST_DPA_DICT[temp[0]] = temp[1]

    def _test_epsilon_states(self, temp_current_state, temp_initial_stack):
        for k in self.CONST_DPA_DICT.keys():
            if temp_current_state in k and "$" in k and temp_initial_stack[0] in k:
                transition = self.CONST_DPA_DICT[k].split(",")
                if temp_current_state in self.acc_states_arr and transition[0] not in self.acc_states_arr:
                    continue
                temp_initial_stack.pop(0)
                temp_initial_stack[:0] = [*transition[1]]
                temp_current_state = transition[0]
                if len(temp_initial_stack) > 0:
                    current_string = temp_current_state + "#" + "".join(temp_initial_stack)
                else:
                    current_string = temp_current_state + "#" + "$"
                print(current_string, end="|")
                continue
        return temp_current_state, temp_initial_stack
    
    # Format dpa dictionarija: [trenutno_stanje, trenutni_simbol, vrh_stoga -> sljedece_stanje, novi_vrh_stoga]
    # Format ulaza: a,b,c,a,c,a,b,...
    def simulate(self, input):
        current_state = self.CONST_CURRENT_STATE
        initial_stack = self.CONST_STACK.copy()
        print(current_state + "#" + initial_stack[0] + "|", end="")
        for idx, el in enumerate(input): # Enumeriram da znam kad sam u zadnjoj iteraciji           
            
            current_state, initial_stack = self._test_epsilon_states(current_state, initial_stack.copy())

            current_key = ",".join([current_state, el , initial_stack.pop(0)])
            if current_key in self.CONST_DPA_DICT.keys():
                next_state = self.CONST_DPA_DICT[current_key].split(",")
                current_state = next_state[0]
                if next_state[1] != "$":
                    initial_stack[:0] = [*next_state[1]]
                if len(initial_stack) > 0:
                    current_string = current_state + "#" + "".join(initial_stack)
                else:
                    current_string = current_state + "#" + "$"
                print(current_string, end="|")
            else:
                print("fail|", end="")
                current_state = "-"
                break
            
            if idx != len(input) - 1 or current_state not in self.acc_states_arr:
                current_state, initial_stack = self._test_epsilon_states(current_state, initial_stack.copy())

        if current_state in self.acc_states_arr:
            print(1)
        else:
            print(0)

def main():
    input_arr = input().split("|")
    states_arr = input().split(",")
    symbols_arr = input().split(",")
    stack_arr = input().split(",")
    acc_states_arr = input().split(",")
    init_state = input()
    stack_state = input()

    automata = DPA(init_state, stack_state, acc_states_arr)

    for el in input_arr:
        automata.simulate(el.split(","))

if __name__ == "__main__":
    main()