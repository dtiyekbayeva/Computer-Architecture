Input = [0x032BA020, 0x8CE90014, 0x12A90003, 0x022DA822, 0xADB30020, 0x02697824, 0xAE8FFFF4,
0x018C6020, 0x02A4A825, 0x158FFFF7, 0x8ECDFFF0]

Opcodes_R = {0x20:"add", 0x22:"sub", 0x24:"and", 0x25:"or", 0x28:"slt"}
Opcodes_I = {0x23:"lw", 0x2b:"sw"}
Opcodes_I_Branching = {0x4:"beq", 0x5:"bne"}
Address = 0x9A040 - 4
maskS1=0x03E00000
maskS2Dst=0x001F0000
maskDst=0x0000F800
maskFunc=0x0000003F
maskOpCode=0xFC000000
maskOffset=0x0000FFFF

for i in Input:
    opcode = (i & maskOpCode) >> 26
    if opcode == 0x0:
        S1 = (i & maskS1) >> 21
        S2Dst = (i & maskS2Dst) >> 16
        Dst = (i & maskDst) >> 11
        Func = (i & maskFunc)
        Address = Address + 4
        print (hex(Address) + " " + Opcodes_R[Func] + " $" + str(Dst) +  ", $" + str(S1) + ", $" + str(S2Dst))
    elif opcode in Opcodes_I.keys():
        S1 = (i & maskS1) >> 21
        S2Dst = (i & maskS2Dst) >> 16

    #since python doesn't have 16-bit data type have to use 32-bit data type for offset
    #checking most significant bit and if it is more than 0 it is negative
        if (i & maskOffset) >> 15 > 0:
            Address = Address + 4
            Offset = -2**16 + (((i & maskOffset) << 1) >> 1)
            print(hex(Address) + " " + Opcodes_I[opcode] + " $" + str(S2Dst) + ", " +str(Offset) + ", ($" + str(S1) + ")")
        else:
            Address = Address + 4
            Offset = i & maskOffset
            print(hex(Address) + " " + Opcodes_I[opcode] + " $" + str(S2Dst) + ", " +str(Offset) + ", ($" + str(S1) + ")")

    #trying to incorporate branching techniques here
    elif opcode in Opcodes_I_Branching.keys():
        S1 = (i & maskS1) >> 21
        S2Dst = (i & maskS2Dst) >> 16
        if (i & maskOffset) >> 15 > 0:
            Address = Address + 4
            Offset = (-2 ** 16 + (((i & maskOffset) << 1) >> 1)) >>  2
            Offset1 = Offset * 4 + Address + 4
            print(hex(Address) + " " + Opcodes_I_Branching[opcode] + " $" + str(S1) + " $" + str( S2Dst) + ", address " +  hex(Offset1))
        else:
            Address = Address + 4
            Offset = (i & maskOffset) >>  2
            Offset1 = Offset * 4 + Address + 4
            print(hex(Address) + " " + Opcodes_I_Branching[opcode] + " $" + str(S1) + " $" + str(S2Dst) + ", address " +  hex(Offset1))
