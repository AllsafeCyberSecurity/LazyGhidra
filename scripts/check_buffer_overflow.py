# Check Buffer Overflow
# @author: tkmru
# @category: LazyGhidra

from ghidra.program.model.listing import CodeUnit

# potentially vulnerable functions
sinks = [
    "getpw",
    "gets",
    "sprintf",
    "strcat",
    "strcpy",
    "vsprinf"
]

def add_bookmark_comment(address, category, description):
    cu = currentProgram.getListing().getCodeUnitAt(address)
    createBookmark(address, category, description)
    cu.setComment(CodeUnit.EOL_COMMENT, description)

def find_danger_func():
    addresses = {}
    function = getFirstFunction()
    while function is not None:
        if monitor.isCancelled():
            return doCancel()

        if function.getName() in sinks:
            try:
                addresses[function.getName()].append(function.getEntryPoint())
            except:
                addresses[function.getName()] = []
                addresses[function.getName()].append(function.getEntryPoint())
            
        function = getFunctionAfter(function)

    return addresses

if __name__=='__main__':
    print('[+] Checking possibility of buffer overflow....')
    print('--------')
    listing = currentProgram.getListing() 
    addresses = find_danger_func()
    count = 0
    for func_name in addresses:
        for address in addresses[func_name]:
            references = getReferencesTo(address)
            for ref in references:
                from_addr = ref.getFromAddress()
                to_addr = ref.getToAddress()
                from_ins = listing.getInstructionAt(from_addr)
                to_ins = listing.getInstructionAt(to_addr)
                if (from_ins is not None) and (to_ins is not None):
                    print('Address: {}'.format(from_addr))
                    print('Instruction: {}({})'.format(from_ins.toString(), func_name))
                    add_bookmark_comment(from_addr, 'Possibility of buffer overflow', func_name + ' is unsafe...')
                    count += 1
                    print('--------')
    print("[!] Done! {} possible vulnerabilities found.".format(count))
