# Convert to hex string
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
output = ''
while True:
    bytes_data = listing.getCodeUnitAt(start).getBytes()
    for b in bytes_data:
        if (256 + b) < 256:
            b += 256

        output += "%02X" % b

    if listing.getCodeUnitAt(start).getMaxAddress() >= end:
        break

    start = listing.getCodeUnitAt(start).getMaxAddress().add(1)

print output
