
binaryformat = "{:04b}"
types = {"literal": 4}

def read_file(fn):
    bits = []
    with open(fn, "r") as fh:
        data = fh.read().strip()
        for crumb in [int(i, 16) for i in data]:
            bits.extend([int(i) for i in binaryformat.format(crumb)])
    return bits
    
def get_version(parsed):
    version = 0
    for packet in parsed:
        if "children" in packet:
            version += get_version(packet["children"])
        version += packet["version"]
    return version

def get_max_end(parsed):
    max_end = 0
    for packet in parsed:
        if "children" in packet:
            max_end = max(get_max_end(packet["children"]), max_end)
        max_end = max(max_end,packet["end"])
    return max_end

def intify_bits(bits):
    return int("".join([str(i) for i in bits]), 2)

def parse_sub_packets(bits, offset=0, packet_max=9999999):
    cursor = 0
    value = None
    packets = []
    # print("looking at bits:", bits)

    if len(bits) < 7:
        if intify_bits(bits) > 0:
            raise ValueError("Packet is impossibly short")
        else:
            print("trailing zeros, I hope...?")

    while (cursor + 6 < len(bits) -1) and (len(packets) < packet_max):
        packetstart = cursor
        version = intify_bits(bits[cursor:cursor+3])
        packettype = intify_bits(bits[cursor+3:cursor+6])
        # print("version", version, "type", packettype)
        cursor += 6

        if packettype==types["literal"]:
            
            thisbit = bits[cursor]
            value = []
            while thisbit == 1:
                value += bits[cursor+1:cursor+5]
                cursor += 5
                if cursor >= len(bits):
                    raise ValueError("Overran input")
                thisbit = bits[cursor]  
                # print("value so far", value)
            value += bits[cursor+1:cursor+5]
            # print("final value:", value)
            value = intify_bits(value)

            cursor += 5
            # print("cursor loc:",cursor)
            packet = {"version": version, "start": packetstart, "end": cursor - 1, "start_abs": packetstart + offset, "end_abs": cursor - 1 + offset, "type": packettype, "value": value }
            print("found literal:",packet)
            packets.append(packet)

        else:
            length_type_id = bits[cursor]
            cursor += 1
            subpackets = []
            packet = {}

            if length_type_id == 1:
                # print(bits[cursor:cursor+11])
                subpacket_length = intify_bits(bits[cursor:cursor+11])
                cursor += 11
                print("expected subpacket length in packets:",subpacket_length)
                packet["length_subpackets"] = subpacket_length
                
                new_subpackets = parse_sub_packets(bits[cursor:], offset=offset+cursor, packet_max=subpacket_length)
                print("resulting raw subpackets:", new_subpackets)
                if len(new_subpackets) < subpacket_length:
                    raise ValueError("expected " + str(subpacket_length) + " packets, got " + str(len(new_subpackets)) + " packets in " + str(new_subpackets) + ", current offset " + str(offset + cursor))
                # print("got subpackets:", new_subpackets)
                if len(new_subpackets) > 0:
                    new_subpackets = new_subpackets[0:subpacket_length]
                    subpackets.extend(new_subpackets)
                    print("filtered subpackets:", new_subpackets)
                    print("cursor", cursor, "max end", get_max_end(new_subpackets), ", will increase cursor by", get_max_end(new_subpackets) + 1 )
                    cursor += (get_max_end(new_subpackets)) + 1
                else:
                    cursor += 18
                    print("strange, 0 subpackets specified...")

            else:    
                subpacket_length = intify_bits(bits[cursor:cursor+15])
                cursor += 15
                print("expected subpacket length in bits:",subpacket_length)
                if subpacket_length==0:
                    print("strange, 0 bits specified...")
                else:
                    packet["length_subpacket_bits"] = subpacket_length
                    subpackets.extend(parse_sub_packets(bits[cursor:cursor+subpacket_length], offset=offset+cursor))
                    print("got subpackets:", subpackets)
                    cursor += subpacket_length 
            packet.update({"version": version, "start":  packetstart, "end": cursor - 1, "start_abs": packetstart + offset, "end_abs": cursor - 1 + offset, "type": packettype, "value": value, "children": subpackets })
            packets.append(packet)

    # print("returning:",packets)
    return packets
    


expected = {"data.sample1.txt": 6, "data.sample2.txt": 9, "data.sample3.txt": 14, "data.sample4.txt": 16, "data.sample5.txt": 12, "data.sample6.txt": 23, "data.sample7.txt": 31 }
for fn, val in expected.items():
    bits = read_file(fn)
    packets = parse_sub_packets(bits)
    print(packets)
    result = get_version(packets)
    print(fn, val, result, result == val)
    if result != val:
        raise ValueError

print(get_version(parse_sub_packets(read_file("data.txt"))))