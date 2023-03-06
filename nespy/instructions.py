from nespy.cmp_6502 import Cmp6502
from nespy.addr_modes import *

def AND(cpu: Cmp6502) -> int:
    cpu.a &= cpu.fetched
    cpu.set_flag(cpu.flags.Z, cpu.a == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.a & 0x80)

    return 1

def ASL(cpu: Cmp6502) -> int:
    t = cpu.fetched << 1

    cpu.set_flag(cpu.flags.C, (t & 0xFF00) > 0)
    cpu.set_flag(cpu.flags.Z, (t & 0x00FF) == 0x00)
    cpu.set_flag(cpu.flags.N, t & 0x80)

    if cpu.addr_mode == IMP:
        cpu.a = t & 0x00FF
    else:
        cpu.write(cpu.addr_abs, t & 0x00FF)
    
    return 0

def CLC(cpu: Cmp6502) -> int:
    cpu.status &= ~cpu.flags.C
    return 0

def CLD(cpu: Cmp6502) -> int:
    cpu.status &= ~cpu.flags.D
    return 0

def CLI(cpu: Cmp6502) -> int:
    cpu.status &= ~cpu.flags.I
    return 0

def CLV(cpu: Cmp6502) -> int:
    cpu.status &= ~cpu.flags.V
    return 0

def SEC(cpu: Cmp6502) -> int:
    cpu.status |= cpu.flags.C
    return 0

def SED(cpu: Cmp6502) -> int:
    cpu.status |= cpu.flags.D
    return 0

def SEI(cpu: Cmp6502) -> int:
    cpu.status |= cpu.flags.I
    return 0

def CMP(cpu: Cmp6502) -> int:
    t = cpu.a - cpu.fetched
    cpu.set_flag(cpu.flags.Z, t == 0)
    cpu.set_flag(cpu.flags.C, cpu.a >= cpu.fetched)
    cpu.set_flag(cpu.flags.N, t & 0x80) 
    
    return 1

def CPX(cpu: Cmp6502) -> int:
    t = cpu.x - cpu.fetched
    cpu.set_flag(cpu.flags.Z, t == 0)
    cpu.set_flag(cpu.flags.C, cpu.x >= cpu.fetched)
    cpu.set_flag(cpu.flags.N, t & 0x80) 
    
    return 0

def CPY(cpu: Cmp6502) -> int:
    t = cpu.y - cpu.fetched
    cpu.set_flag(cpu.flags.Z, t == 0)
    cpu.set_flag(cpu.flags.C, cpu.y >= cpu.fetched)
    cpu.set_flag(cpu.flags.N, t & 0x80) 
    
    return 0

def DEC(cpu: Cmp6502) -> int:
    t = (cpu.fetched - 1) & 0xFF
    cpu.set_flag(cpu.flags.Z, t == 0x00)
    cpu.set_flag(cpu.flags.N, t & 0x80)
    cpu.write(cpu.addr_abs, t)

    return 0

def DEX(cpu: Cmp6502) -> int:
    cpu.x = (cpu.x - 1) & 0xFF
    cpu.set_flag(cpu.flags.Z, cpu.x == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.x & 0x80)

    return 0

def DEY(cpu: Cmp6502) -> int:
    cpu.y = (cpu.y - 1) & 0xFF
    cpu.set_flag(cpu.flags.Z, cpu.y == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.y & 0x80)

    return 0

def EOR(cpu: Cmp6502) -> int:
    cpu.a = cpu.a ^ cpu.fetched
    cpu.set_flag(cpu.flags.Z, cpu.a == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.a & 0x80)

    return 1

def ORA(cpu: Cmp6502) -> int:
    cpu.a |= cpu.fetched
    cpu.set_flag(cpu.flags.Z, cpu.a == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.a & 0x80)

    return 1

def INC(cpu: Cmp6502) -> int:
    t = cpu.fetched + 1
    cpu.set_flag(cpu.flags.Z, (t & 0x00FF) == 0x00)
    cpu.set_flag(cpu.flags.N, t & 0x80)
    cpu.write(cpu.addr_abs, t & 0x00FF)

    return 0

def INX(cpu: Cmp6502) -> int:
    cpu.x += 1
    cpu.set_flag(cpu.flags.Z, cpu.x == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.x & 0x80)

    return 0

def INY(cpu: Cmp6502) -> int:
    cpu.y += 1
    cpu.set_flag(cpu.flags.Z, cpu.y == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.y & 0x80)
    
    return 0

def JMP(cpu: Cmp6502) -> int:
    cpu.pc = cpu.addr_abs
    return 0

def JSR(cpu: Cmp6502) -> None:
    t = (cpu.pc - 1) & 0xFFFF

    cpu.write(0x0100 + cpu.s, (t >> 8) & 0x00FF)
    cpu.s -= 1
    cpu.write(0x0100 + cpu.s, t & 0x00FF)
    cpu.s -= 1

    cpu.pc = cpu.addr_abs

    return 0

def LDA(cpu: Cmp6502) -> int:
    cpu.a = cpu.fetched
    cpu.set_flag(cpu.flags.Z, cpu.a == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.a & 0x80)

    return 1

def LDX(cpu: Cmp6502) -> int:
    cpu.x = cpu.fetched
    cpu.set_flag(cpu.flags.Z, cpu.x == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.x & 0x80)

    return 1

def LDY(cpu: Cmp6502) -> int:
    cpu.y = cpu.fetched
    cpu.set_flag(cpu.flags.Z, cpu.y == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.y & 0x80)

    return 1

def NOP(cpu: Cmp6502) -> None:
    # NOP has weird behavior on specific opcodes where it has potential to add a cycle on page boundary, specicaly on any ABX opcodes
    if cpu.addr_mode == ABX:
        return 1

    return 0


def PHA(cpu: Cmp6502) -> int: #pushes the content of the Accumulator onto the stack structure
    cpu.write(0x0100 + cpu.s, cpu.a)
    cpu.s -= 1
    return 0

def PHP(cpu: Cmp6502) -> int: 
    cpu.write(0x0100 + cpu.s, cpu.status | (cpu.flags.B|cpu.flags.U))
    cpu.status &= ~(cpu.flags.B|cpu.flags.U)
    cpu.s -= 1

    return 0

def PLA(cpu: Cmp6502) -> int:
    cpu.s += 1
    cpu.a = cpu.read(0x0100 + cpu.s)
    cpu.set_flag(cpu.flags.Z, cpu.a == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.a & 0x80)

    return 0

def PLP(cpu: Cmp6502) -> int:
    cpu.s += 1
    cpu.status = cpu.read(0x100 + cpu.s)
    cpu.status |= cpu.flags.U

    return 0

def RTI(cpu: Cmp6502) -> None:
    cpu.s += 1
    cpu.status = cpu.read(0x0100 + cpu.s)
    cpu.status &= ~cpu.flags.B
    cpu.status &= ~cpu.flags.U

    cpu.s += 1
    cpu.pc = cpu.read(0x0100 + cpu.s)
    cpu.s += 1
    cpu.pc |= cpu.read(0x0100 + cpu.s) << 8

    return 0

def RTS(cpu: Cmp6502) -> None:
    cpu.s += 1
    cpu.pc = cpu.read(0x0100 + cpu.s)
    cpu.s += 1
    cpu.pc |= cpu.read(0x0100 + cpu.s) << 8

    return 0

def STA(cpu: Cmp6502) -> None:
    cpu.write(cpu.addr_abs, cpu.a)
    return 0

def STX(cpu: Cmp6502) -> None:
    cpu.write(cpu.addr_abs, cpu.x)
    return 0

def STY(cpu: Cmp6502) -> None:
    cpu.write(cpu.addr_abs, cpu.y)
    return 0

def TAX(cpu: Cmp6502) -> int:
    #transers accumulator's value to X
    cpu.x = cpu.a
    cpu.set_flag(cpu.flags.Z, cpu.x == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.x & 0x80)    

    return 0

def TXA(cpu: Cmp6502) -> int:
    #transers X to A
    cpu.a = cpu.x
    cpu.set_flag(cpu.flags.Z, cpu.a == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.a & 0x80)    

    return 0

def TAY(cpu: Cmp6502) -> int:
    #transers accumulator's value to Y
    cpu.y = cpu.a
    cpu.set_flag(cpu.flags.Z, cpu.y == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.y & 0x80)    

    return 0

def TYA(cpu: Cmp6502) -> int:
    #transers Y to A
    cpu.a = cpu.y
    cpu.set_flag(cpu.flags.Z, cpu.a == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.a & 0x80)    

    return 0

def TSX(cpu: Cmp6502) -> int:
    cpu.x = cpu.s
    cpu.set_flag(cpu.flags.Z, cpu.x == 0x00)
    cpu.set_flag(cpu.flags.N, cpu.x & 0x80)    

    return 0

def TXS(cpu: Cmp6502) -> int:
    cpu.s = cpu.x
    return 0

def UNK(cpu: Cmp6502) -> int:
    # placeholder for opcodes that dont exist (but we still need to handle just in case)
    return 0
