import json


class TuringMachine:

    def __init__(self, blank_symbol=0, initial_tape_size=500):
        self.initial_tape_size = initial_tape_size
        self.tape = [blank_symbol for _ in range(initial_tape_size)]
        self.head_position = self.initial_tape_size // 2

    def load_program(self, program):
        if 'initial_tape_size' in program:
            self.initial_tape_size = program['initial_tape_size']
        if 'blank_symbol' in program:
            self.blank_symbol = program['blank_symbol']

        self.alphabet = program['alphabet']
        if self.blank_symbol not in self.alphabet:
            raise ValueError('Blank symbol must be included in alphabet.')

        self.tape = [self.blank_symbol for _ in range(self.initial_tape_size)]
        self.head_position = program['initial_tape_size'] // 2
        self.initial_state = program['initial_state']
        self.halt_state = program['halt_state']
        self.states = program['states']

    def load_program_from_file(self, state_file):
        with open(state_file, 'r') as f:
            self.load_program(json.load(f))

    def run(self, input_value):
        for c in set(input_value):
            if c not in self.alphabet:
                raise ValueError('Input contains characters not in alphabet.')

        for i, c in enumerate(input_value):
            self.tape[self.head_position + i] = c

        initial_print_pos = self.head_position - 10
        end_print_pos = self.head_position + len(input_value) + 10

        current_state_id = self.initial_state
        while True:
            if self.head_position == initial_print_pos:
                initial_print_pos -= 5
            if self.head_position == end_print_pos:
                end_print_pos += 5
            print(''.join(map(str,
                              self.tape[initial_print_pos:end_print_pos + 1])))
            header_row = ''.join([' ' for _ in range(initial_print_pos,
                                                     self.head_position)])
            print(header_row + '^')

            if current_state_id == self.halt_state:
                break

            state = self.states[current_state_id]
            read_symbol = self.tape[self.head_position]
            action = state[self.alphabet.index(read_symbol)]
            self.tape[self.head_position] = self.alphabet[action['write']]
            self.head_position += -1 if action['move'] == 'l' else 1
            current_state_id = action['next']
