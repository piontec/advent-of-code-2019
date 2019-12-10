from typing import List
from itertools import permutations


class CPU:
    def __init__(self, strcode: str, inputs: List[int]):
        super().__init__()
        self._ip: int = 0
        self._code = [int(x) for x in str.split(strcode, ",")]
        self._input_index = 0
        self.outputs: List[int] = []
        self.inputs: List[int] = inputs

    def _parse_instruction(self) -> (int, int, List[int]):
        instruction = self._code[self._ip]
        opcode = instruction % 100
        no_args = 0
        if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
            no_args = 3
        elif opcode == 3 or opcode == 4:
            no_args = 1
        elif opcode == 5 or opcode == 6:
            no_args = 2
        else:
            assert False
        modes: List[int] = []
        mds = instruction // 100
        for i in range(no_args):
            mode = mds % 10
            mds //= 10
            modes.append(mode)
        return (opcode, no_args, modes)

    def _get_argument(self, arg_modes: List[int], offset: int) -> int:
        # position mode
        if arg_modes[offset] == 0:
            return self._code[self._code[self._ip + 1 + offset]]
        # immediate mode
        if arg_modes[offset] == 1:
            return self._code[self._ip + 1 + offset]
        raise AssertionError(str.format(
            "Unknown arg mode: {}", arg_modes[offset]))

    def run(self) -> List[int]:
        while self._code[self._ip] != 99:
            opcode, no_args, modes = self._parse_instruction()
            if opcode == 1 or opcode == 2:
                assert modes[2] == 0
                v1 = self._get_argument(modes, 0)
                v2 = self._get_argument(modes, 1)
                self._code[self._code[self._ip + 3]] = v1 + \
                    v2 if opcode == 1 else v1 * v2
            elif opcode == 3:
                assert modes[0] == 0
                self._code[self._code[self._ip + 1]
                           ] = self.inputs[self._input_index]
                self._input_index += 1
            elif opcode == 4:
                if modes[0] == 0:
                    self.outputs.append(self._code[self._code[self._ip + 1]])
                elif modes[0] == 1:
                    self.outputs.append(self._code[self._ip + 1])
            elif opcode == 5 or opcode == 6:
                val = self._get_argument(modes, 0)
                if (opcode == 5 and val != 0) or (opcode == 6 and val == 0):
                    self._ip = self._get_argument(modes, 1)
                    continue
            elif opcode == 7 or opcode == 8:
                assert modes[2] == 0
                v1 = self._get_argument(modes, 0)
                v2 = self._get_argument(modes, 1)
                res = (opcode == 7 and v1 < v2) or (opcode == 8 and v1 == v2)
                self._code[self._code[self._ip + 3]] = int(res)
            else:
                print(str.format("ERROR: unknown op code: {}",
                                 self._code[self._ip]))
                return
            self._ip += no_args + 1
        return self.outputs


def find_max(strcode: str) -> int:
    comb = permutations(range(0, 5))
    max_val = 0
    best_cb = -1
    for cb in comb:
        in_val = 0
        for c in cb:
            cpu = CPU(strcode, [c, in_val])
            in_val = cpu.run()[0]
        if in_val > max_val:
            max_val = in_val
            best_cb = cb
    return max_val


assert find_max("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0") == 43210
with open("i7.txt") as f:
    lines = f.readlines()
res = find_max(lines[0])
print(str.format("Part 1: {}", res))
