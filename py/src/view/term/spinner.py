class Spinner:
    __states = ['\\', '|', '/', '-']

    def __init__(self):
        self.state_index = 0

    def get_next_state(self):
        spinner_symbol = self.__states[self.state_index]
        self.state_index = (self.state_index + 1) % len(self.__states)
        return spinner_symbol

    @staticmethod
    def get_symbol_for_index(index):
        return Spinner.__states[index % len(Spinner.__states)]