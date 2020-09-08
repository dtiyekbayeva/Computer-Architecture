#creating class for main memory
class MM:
    def __init__(self, data1, data2, data3):
        self._data1 = data1
        self._data2 = data2
        self._data3 = data3

    def get_data1(self):
        return self._data1
    def get_data2(self):
        return self._data2
    def get_data3(self):
        return self._data3
    def set_data1(self, x):
        self._data1 = x
    def set_data2(self, x):
        self._data2 = x
    def set_data3(self, x):
        self._data3 = x

#creating class for cache
class Cache:
    def __init__(self, slot, valid, tag, dirty_bit):
        self._slot = slot
        self._valid = valid
        self._tag = tag
        self._dirty_bit = dirty_bit

#this is my all 0's cache data
    data = []
    for i in range(0x0, 0xF+1):
        data.append(hex(0))

    def get_dirty_bit(self):
        return self._dirty_bit
    def get_tag(self):
        return self._tag
    def get_valid(self):
        return self._valid
    def get_data(self):
        return self.data
    def get_slot(self):
        return self._slot
    def get_data1(self, number):
        return self.data[number]

    def set_dirty_bit(self, x):
        self._dirty_bit = x
    def set_tag(self, x):
        self._tag = x
    def set_valid(self, x):
        self._valid = x
    def set_data(self, x):
        self.data = x
    def set_slot(self, x):
        self._slot = x
    def set_data1(self, number, value):
        self.data[number] = value


#bringing cache to live
list=[]
for i in range (0x0, 0xF+1):
    cache = Cache(slot=i, valid = 0, tag = 0, dirty_bit = 0)
    list.append(cache)
    list[i].set_slot(hex(i))
#bringing memory to live
list1 = []
for k in range(0x0, 0x7FF + 1):
    main_memory = MM(data1=0, data2=0, data3=0)
    main_memory.set_data1(k>>4)
    main_memory.set_data2(k)
    main_memory.set_data3(k ^ ((k >> 8) << 8))
    list1.append(main_memory)

#list of test operations
OPERATIONS = ['R', 0x5, 'R', 0x6, 'R', 0x7, 'R', 0x14C, 'R', 0x14D, 'R', 0x14E,
              'R', 0x14F, 'R', 0x150, 'R', 0x151, 'R', 0x3A6, 'R', 0x4C3, 'D', 'W',
              0x14C, 0x99, 'W', 0x63B, 0x7, 'R', 0x582, 'D', 'R', 0x348, 'R', 0x3F,
              'D', 'R', 0x14B, 'R', 0x14C, 'R', 0x63F, 'R', 0x83, 'D']
#iteration through test operations
for i in range(0, len(OPERATIONS)):
    if OPERATIONS[i] == 'R':
        address = OPERATIONS[i + 1]
        tag = address >> 8
        slot = (address & 0x0F0) >> 4
        offset = (address & 0x00F)
        if list[slot].get_valid() == 0:
            tmp = []
            for j in range(0, len(list1)):
                if list1[j].get_data1() == address>>4:
                    tmp.append(hex(list1[j].get_data3()))
            list[slot].set_data(tmp)
            list[slot].set_tag(tag)
            list[slot].set_valid(1)
            print("Reading ", hex(OPERATIONS[i + 1]), "It is a Cache miss", "At that address we have:", list[slot].get_data1(offset))
        elif list[slot].get_tag() == tag  and list[slot].get_valid() == 1:
            print("Reading ", hex(OPERATIONS[i + 1]), "It is a Cache hit", "At that address we have:", list[slot].get_data1(offset))
            list[slot].set_tag(tag)
            list[slot].set_valid(1)
        elif list[slot].get_tag() != tag  and list[slot].get_valid() == 1:
            if list[slot].get_dirty_bit() == 1:
#writing to the MM, this part took a long time for me to figure out code wise
                tmp1 = [x for x in range(0, len(list1)) if list1[x].get_data1() == address >> 4]
                for a, b in enumerate(tmp1):
                    list1[b].set_data3(list[slot].get_data1(a))
                list[slot].set_dirty_bit(0)
                tmp = []
                for p in range(0, len(list1)):
                    if list1[p].get_data1() == address >> 4:
                        tmp.append(list1[p].get_data3())
                list[slot].set_data(tmp)
                list[slot].set_tag(tag)
                print("Reading ", hex(OPERATIONS[i + 1]), "It is a Cache miss", "At that address we have:", list[slot].get_data1(offset))
            else:
                tmp = []
                for p in range(0, len(list1)):
                    if list1[p].get_data1() == address >> 4:
                        tmp.append(hex(list1[p].get_data3()))
                list[slot].set_data(tmp)
                list[slot].set_tag(tag)
                print("Reading ", hex(OPERATIONS[i + 1]), "It is a Cache miss", "At that address we have:", list[slot].get_data1(offset))
    elif OPERATIONS[i] =='W':
        address = OPERATIONS[i + 1]
        value = hex(OPERATIONS[i + 2])
        tag = address >> 8
        slot = (address & 0x0F0) >> 4
        offset = (address & 0x00F)

        if list[slot].get_valid() == 0:
            print("Writing Value ", value, "to",  hex(address), "It is a Cache miss")
            tmp = []
            for i in range(0, len(list1)):
                if list1[i].get_data1() == address >> 4:
                    tmp.append(hex(list1[i].get_data3()))
            list[slot].set_data(tmp)
            list[slot].set_tag(tag)
            list[slot].set_valid(1)
            list[slot].set_data1(offset, value)
            list[slot].set_dirty_bit(1)
        elif list[slot].get_tag() == tag and list[slot].get_valid() == 1:
            list[slot].set_data1(offset, value)
            list[slot].set_dirty_bit(1)
            print("Writing Value ", value, "to",  hex(address), "It is a Cache hit")

    elif OPERATIONS[i] == 'D':
        print "\nDispalying current cache"
        print " Slot Valid Tag DirtyBit Data"
        for i in range(0, len(list)):
            print (list[i].get_slot(), list[i].get_valid(), hex(list[i].get_tag()), list[i].get_dirty_bit(), list[
            i].get_data())












