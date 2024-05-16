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

    def _test_epsilon_states(self, temp_current_state, temp_stack):
        for key in self.CONST_DPA_DICT.keys():
            if temp_current_state in key and "$" in key:
                if temp_stack[0] in key:
                    transition = self.CONST_DPA_DICT[key].split(",")
                    if temp_current_state in self.acc_states_arr and transition[0] not in self.acc_states_arr:
                        continue
                    temp_stack.pop(0)
                    temp_stack[:0] = [*transition[1]]
                    temp_current_state = transition[0]
                    if len(temp_stack) > 0:
                        current_string = temp_current_state + "#" + "".join(temp_stack)
                    else:
                        current_string = temp_current_state + "#" + "$"
                    print(current_string, end="|")
                    continue
                else:
                    return temp_current_state, temp_stack, False
        return temp_current_state, temp_stack, True
    
    # Format dpa dictionarija: [trenutno_stanje, trenutni_simbol, vrh_stoga -> sljedece_stanje, novi_vrh_stoga]
    # Format ulaza: a,b,c,a,c,a,b,...
    def simulate(self, input):
        current_state = self.CONST_CURRENT_STATE
        stack = self.CONST_STACK.copy()
        success = False
        print(current_state + "#" + stack[0] + "|", end="")
        for idx, el in enumerate(input): # Enumeriram da znam kad sam u zadnjoj iteraciji           
            
            if not success:
                current_state, stack, success = self._test_epsilon_states(current_state, stack.copy())

            current_key = ",".join([current_state, el , stack.pop(0)])
            if current_key in self.CONST_DPA_DICT.keys():
                next_state = self.CONST_DPA_DICT[current_key].split(",")
                current_state = next_state[0]
                if next_state[1] != "$":
                    stack[:0] = [*next_state[1]]
                if len(stack) > 0:
                    current_string = current_state + "#" + "".join(stack)
                else:
                    current_string = current_state + "#" + "$"
                print(current_string, end="|")
            else:
                print("fail|", end="")
                current_state = "-"
                break
            
            if idx != len(input) - 1 or current_state not in self.acc_states_arr:
                current_state, stack, success = self._test_epsilon_states(current_state, stack.copy())

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