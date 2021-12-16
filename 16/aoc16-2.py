
binaryformat = "{:04b}"
types = {"sum": 0, "product": 1, "minimum": 2, "maximum": 3, "literal": 4, "greater_than": 5, "less_than": 6, "equal_to": 7}
import numpy

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
            # print("found literal:",packet)
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
                # print("expected subpacket length in packets:",subpacket_length)
                packet["length_subpackets"] = subpacket_length
                
                new_subpackets = parse_sub_packets(bits[cursor:], offset=offset+cursor, packet_max=subpacket_length)
                # print("resulting raw subpackets:", new_subpackets)
                if len(new_subpackets) < subpacket_length:
                    raise ValueError("expected " + str(subpacket_length) + " packets, got " + str(len(new_subpackets)) + " packets in " + str(new_subpackets) + ", current offset " + str(offset + cursor))
                # print("got subpackets:", new_subpackets)
                if len(new_subpackets) > 0:
                    new_subpackets = new_subpackets[0:subpacket_length]
                    subpackets.extend(new_subpackets)
                    # print("filtered subpackets:", new_subpackets)
                    # print("cursor", cursor, "max end", get_max_end(new_subpackets), ", will increase cursor by", get_max_end(new_subpackets) + 1 )
                    cursor += (get_max_end(new_subpackets)) + 1
                else:
                    cursor += 18
                    raise ValueError("A 0-length subpacket was specified")
                    # print("strange, 0 subpackets specified...")

            else:    
                subpacket_length = intify_bits(bits[cursor:cursor+15])
                cursor += 15
                # print("expected subpacket length in bits:",subpacket_length)
                if subpacket_length==0:
                    raise ValueError("A 0-bit subpacket was specified")
                else:
                    packet["length_subpacket_bits"] = subpacket_length
                    subpackets.extend(parse_sub_packets(bits[cursor:cursor+subpacket_length], offset=offset+cursor))
                    # print("got subpackets:", subpackets)
                    cursor += subpacket_length 
            values = [i["value"] for i in subpackets]
            if packettype==types["sum"]:
                value = sum(values)
            elif packettype==types["product"]:
                value = int(numpy.product(values))
            elif packettype==types["minimum"]:
                value = min(values)
            elif packettype==types["maximum"]:
                value = max(values)
            elif packettype==types["greater_than"]:
                value = 1 if values[0] > values[1] else 0 
            elif packettype==types["less_than"]:
                value = 1 if values[0] < values[1] else 0 
            elif packettype==types["equal_to"]:
                value = 1 if values[0] == values[1] else 0 

            packet.update({"version": version, "start":  packetstart, "end": cursor - 1, "start_abs": packetstart + offset, "end_abs": cursor - 1 + offset, "type": packettype, "value": value, "children": subpackets })
            packets.append(packet)

    # print("returning:",packets)
    return packets
    
packets = parse_sub_packets(read_file("data.txt"))
print(packets[0]["value"])
