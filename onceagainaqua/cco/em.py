FLAGS = {'Z': False, 'G': False, 'L': False}
call_stack = []
instructions = []
REGISTER_WIDTHS = {
    'RAX': 64, 'RBX': 64, 'RCX': 64, 'RDX': 64,
    'RSI': 64, 'RDI': 64, 'RBP': 64, 'RSP': 64,
    'R1': 64, 'R2': 64, 'R3': 64, 'R4': 64, 'R5': 64, 'R6': 64, 'R7': 64,
    'R8': 64, 'R9': 64, 'R10': 64, 'R11': 64, 'R12': 64, 'R13': 64, 'R14': 64, 'R15': 64,
    'RIP': 64, 'RFLAGS': 32, 'CS': 16, 'DS': 16, 'SS': 16, 'ES': 16, 'FS': 16, 'GS': 16
}

def initialize_registers(names):
    return {name: 0 for name in names}

def load_instruction_map(file_path):
    with open(file_path, 'r') as f:
        return {line.split(':')[0].strip(): line.split(':')[1].strip() for line in f if ':' in line}

def load_address_map(file_path):
    with open(file_path, 'r') as f:
        return {
            line.split('->')[0].strip(): int(line.split('->')[1].strip(), 16)
            for line in f if '->' in line
        }

def mask(value, reg):
    if isinstance(value, str):
        return value
    width = REGISTER_WIDTHS.get(reg, 64)
    return value & ((1 << width) - 1)

def interpret_line(line, instruction_map):
    line = line.strip().split('|')[0]
    if not line: return None, None
    if ':' in line and not line.startswith(('0x', 'JMP', 'JE', 'JG', 'JL', 'CALL', 'SWAP')):
        return 'LABEL', line.strip()
    if line.startswith('0x'):
        parts = line.split(None, 1)
        return instruction_map.get(parts[0]), parts[1] if len(parts) > 1 else None
    return tuple(line.split(None, 1)) if ' ' in line else (line, None)

def resolve_target(dest, labels, address_map):
    return labels.get(dest) or address_map.get(dest) or int(dest, 0)

def execute_instruction(mnemonic, args, registers, labels, ip_ref, address_map, instruction_map):
    def get_value(arg):
        return registers.get(arg, int(arg) if arg.isdigit() else arg)

    dest, src = None, None
    flags = []
    signed = False

    if args:
        parts = [p.strip() for p in args.split(',')]
        flags = [p.upper() for p in parts if p.upper() not in registers and not p.isdigit()]
        signed = 'SIGNED' in flags
        parts = [p for p in parts if p.upper() != 'SIGNED']
        if len(parts) >= 2:
            dest, src = parts[:2]
        elif parts:
            dest = parts[0]

    if mnemonic == 'NOP': return
    elif mnemonic == 'LOAD':
        registers[dest] = mask(get_value(src), dest)
    elif mnemonic == 'MOV':
        registers[dest] = mask(registers.get(src, 0), dest)
    elif mnemonic in ['ADD', 'SUB', 'MUL']:
        val1 = int(registers[dest]) if signed else registers[dest]
        val2 = int(get_value(src)) if signed else get_value(src)
        result = val1 + val2 if mnemonic == 'ADD' else val1 - val2 if mnemonic == 'SUB' else val1 * val2
        registers[dest] = result if signed else mask(result, dest)
    elif mnemonic == 'DIV':
        val1 = int(registers[dest]) if signed else registers[dest]
        val2 = int(get_value(src)) if signed else get_value(src)
        if val2: registers[dest] = val1 // val2 if signed else mask(val1 // val2, dest)
    elif mnemonic == 'OUT': print(registers.get(dest, 'N/A'))
    elif mnemonic == 'IN': registers[dest] = mask(int(input()), dest)
    elif mnemonic == 'INS': registers[dest] = input()
    elif mnemonic == 'OUTS': print(registers.get(dest, ''))
    elif mnemonic in ['AND', 'OR', 'XOR']:
        op = {'AND': '&', 'OR': '|', 'XOR': '^'}[mnemonic]
        registers[dest] = mask(eval(f'registers[dest] {op} get_value(src)'), dest)
    elif mnemonic == 'NOT': registers[dest] = mask(~registers[dest], dest)
    elif mnemonic == 'SHL': registers[dest] = mask(registers[dest] << get_value(src), dest)
    elif mnemonic == 'SHR': registers[dest] = mask(registers[dest] >> get_value(src), dest)
    elif mnemonic == 'CMP':
        val1, val2 = get_value(dest), get_value(src)
        FLAGS['Z'], FLAGS['G'], FLAGS['L'] = val1 == val2, val1 > val2, val1 < val2
    elif mnemonic in ['JE', 'JG', 'JL']:
        if (mnemonic == 'JE' and FLAGS['Z']) or \
           (mnemonic == 'JG' and FLAGS['G']) or \
           (mnemonic == 'JL' and FLAGS['L']):
            ip_ref[0] = resolve_target(dest, labels, address_map)
    elif mnemonic == 'JMP':
        ip_ref[0] = resolve_target(dest, labels, address_map)
    elif mnemonic == 'CALL':
        call_stack.append(ip_ref[0] + 1)
        ip_ref[0] = resolve_target(dest, labels, address_map)
    elif mnemonic == 'RET':
        ip_ref[0] = call_stack.pop() if call_stack else ip_ref[0] + 1
    elif mnemonic == 'SWAP':
        try:
            with open(dest.strip(), 'r') as f:
                new_lines = [line.strip() for line in f if line.strip()]
            for line in new_lines:
                mnem, args_ = interpret_line(line, instruction_map)
                if mnem == 'LABEL':
                    label_name = line.replace(':', '').strip()
                    labels[label_name] = len(instructions)
                elif mnem:
                    instructions.append((mnem, args_))
            ip_ref[0] = len(instructions) - len(new_lines)
        except Exception: pass
    elif mnemonic == 'HALT':
        ip_ref[0] = len(instructions)

def run_program(opcodes_path, code_path, custom_registers, map_path=None):
    registers = initialize_registers(custom_registers)
    instruction_map = load_instruction_map(opcodes_path)
    address_map = load_address_map(map_path) if map_path else {}

    with open(code_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    labels = {}
    for line in lines:
        mnemonic, args = interpret_line(line, instruction_map)
        if mnemonic == 'LABEL':
            label_name = line.replace(':', '').strip()
            labels[label_name] = len(instructions)
        else:
            instructions.append((mnemonic, args))

    ip = [0]
    while ip[0] < len(instructions):
        mnemonic, args = instructions[ip[0]]
        execute_instruction(mnemonic, args, registers, labels, ip, address_map, instruction_map)
        if mnemonic not in ['JMP', 'JE', 'JG', 'JL', 'CALL', 'RET', 'SWAP', 'HALT']:
            ip[0] += 1

custom_registers = [  # Full register list
    'RAX', 'RBX', 'RCX', 'RDX', 'RSI', 'RDI', 'RBP', 'RSP',
    'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7',
    'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15',
    'RIP', 'RFLAGS', 'CS', 'DS', 'SS', 'ES', 'FS', 'GS'
]

run_program('opcodes.txt', 'start.cco', custom_registers, 'memory_map.txt')