# Convert to Python list (BYTE)
# @category: LazyGhidra

if currentSelection is None:
    print 'Error: Please select something on Listing View...'
    import sys
    sys.exit(1)

start = currentSelection.getMinAddress()
end = currentSelection.getMaxAddress()
size = end.offset - start.offset + 1
print '\n[+] Dump 0x%X - 0x%X (%u bytes) :' % (start.offset, end.offset, size)

listing = currentProgram.getListing()
name = listing.getCodeUnitAt(start).getPrimarySymbol()
if name is None:
    name = 'data'

# Python list
output = '%s = [' % name
count = 0
while True:
    bytes_data = listing.getCodeUnitAt(start).getBytes()
    for b in bytes_data:
        if count % 16 == 0:
            output += '\n    '

        if (256 + b) < 256:
            b += 256

        output += '0x%02X, ' % b
        count += 1

    if listing.getCodeUnitAt(start).getMaxAddress() >= end:
        break

    start = listing.getCodeUnitAt(start).getMaxAddress().add(1)

output = output[:-2] + '\n]'
print output
