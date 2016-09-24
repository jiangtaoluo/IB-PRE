#!/usr/bin/python3

''' Transform the data in 3 *.out files
 to generate *.dat file for plotting
input Format
fibre.out: #GenRK	IBE	RE	IBD (in milli-seconds)
hibre.out: #SymE	GenRK	KeyIBE	KeyRE	KeyIBD	SymD
ible.out: #SymE	KeyIBE	KeyIBD	SymD

output file: plot.dat
format:
               fibre    hibre    ible
SymE
GenRK
IBE
RE
IBD
SymD

or

         SymE	GenRK	IBE	RE	IBD	SymD

fibre
hibre
ible
'''

# fibre
with open("fibre.out", "r") as fibre:
    for line in fibre:
        if line[0] != '#':
            # Add 0 both at head and tail
            line1 = "fIBRE\t0.0000\t" + line +"0.0000"

#hibre
with open("hibre.out", "r") as hibre:
    for line in hibre:
        if line[0] != '#':
            # Add 0 both at head and tail
            line2 = "hIBRE\t" + line
#ible
val = "\t0.0000\t"
with open("ible.out", "r") as ible:
    for line in ible:
        if line[0] != '#':
            # Add 0 both at head and tail
            symE, keyIBE, keyIBD, symD = line.split()
            line3 = "IBLE\t"+symE + val + keyIBE +val +keyIBD + "\t"+symD


fo = open("plot.dat", "w")
fo.write("Scheme\tSymE\tGenRK\tIBE\tRE\tIBD\tSymD\n")

fo.write(line1)
fo.write("\n")
fo.write(line2)
fo.write("\n")
fo.write(line3)


fibre.close()
hibre.close()
ible.close()
fo.close()
