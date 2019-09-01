# Convert to Python list (QWORD)
# @category: LazyGhidra

if currentSelection is None:
    print 'Error: Please select something on Listing View...'
    import sys
    sys.exit(1)

start = currentSelection.getMinAddress()
end = currentSelection.getMaxAddress()
size = end.offset - start.offset + 1
print "\n[+] Dump 0x%X - 0x%X (%u bytes) :" % (start.offset, end.offset, size)

listing = currentProgram.getListing()
name = listing.getCodeUnitAt(start).getPrimarySymbol()
if name is None:
    name = 'data'

# Python list (QWORD)
output = "%s = [" % name
listing = currentProgram.getListing()
hex_string = ''
while True:
    bytes_data = listing.getCodeUnitAt(start).getBytes()
    for b in bytes_data:
        if (256 + b) < 256:
            b += 256

        hex_string += "%02X" % b

    if listing.getCodeUnitAt(start).getMaxAddress() >= end:
        break

    start = listing.getCodeUnitAt(start).getMaxAddress().add(1)

hex_string += '00' * 7 # zero padding

for i in range(0, size*2, 16):
    if i % 64 == 0:
        output += "\n    "
    # little endian
    output += "0x" 
    output += hex_string[i+14:i+16]
    output += hex_string[i+12:i+14]
    output += hex_string[i+10:i+12]
    output += hex_string[i+8:i+10]
    output += hex_string[i+6:i+8]
    output += hex_string[i+4:i+6]
    output += hex_string[i+2:i+4]
    output += hex_string[i:i+2]
    output += ', '
output = output[:-2] + "\n]"
print output

