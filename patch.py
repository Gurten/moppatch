'''
Author: Gurten

This python script uses the executable 'SpinTires.exe' of the tech demo 
retrieved from: 'http://www.uraldev.ru/articles/files/28/spin_tires_bin.zip' 

It should be run in the same directory as 'SpinTires.exe'.

After running this script, a new .exe named 'MoppCompiler.exe' will be placed
in the directory.

When run, 'MoppCompiler.exe' will create one file named 'mopp_0' in
the executable directory. 

To change the input mesh, replace the file "\spin_tires_bin\Media\Terrain\Mesh.X"
with a directX model. It does not matter if the model file is binary or ascii. A 
.X file can be created using a default Blender export script (which must be 
enabled in User Preferences>Add-ons) or using the Pandasoft DirectX plugin for 3dsMax.
'''

#open the file, which should be in the current directory
f = open("SpinTires.exe", "rb")
data = f.read(); f.close()
bytes = [b for b in data] # unpack the bytes to a list of mutable numbers
#These are patches to the exe
patches = { 
    #    OPCODE PATCHES
	#Modify the subdivision parameters of the terrain to be within a 1x1 grid 
	# (no subdivision required) to change the program from producing many mopp 
	# files (per cell of the grid) to only one mopp file. 
    0x9DAA : [0x31, 0xC9,0x41],  # xor ecx, ecx;inc ecx 
    0x9DD9 : [0x31, 0xC0, 0x40], # xor eax, eax;inc eax
	#return NULL in 'TERRAIN::Load' even after a successful 'TERRAIN_BASE::Initialise' 
	# to prevent the simulation from starting. 
	0x27FB : [0x90, 0x31, 0xC0, 0xC3],	#nop;xor eax, eax;ret
	#    TEXT PATCHES
	#Change the output directory to root (location of the .exe)
	0x1EE070 : b"/../../mopp_\x00"
    }

for addr in patches:
    patch = patches[addr] # the patch list of bytes
    for i, b in enumerate(patch):
        bytes[addr + i] = b

data = bytearray(bytes)
f = open("MoppCompiler.exe", "wb")
f.write(data)
f.close()

