Compare three different Identity-based schemes: full Identity-Based proxy Re-Encryption (fIBRE), half Identity-Based proxy Re-Encryption (hIBRE) and Identity-Based License Encryption (IBLE).

File Description:
-->
fibre.py	: implementation of fIBRE
hibre.py	: implementation of hIBRE
ible		: implementation of IBLE
test_fibre.py: test main function calling fibre,
			   output log (fibre_XXX.log, xxx is length of input
			   message in bytes.)
test_hibre.py: test main function calling hibre, output
			   log (hibre_XXX.log)
test_ible.py: test main function calling ible, output
			  log (ible_XXX.log)

testall: all-in-one shell containing above, output dat file
		 for ploting.
		 
process.py: log processing definition, obtain average of each
			algorithms, 0 given to missing one.
			e.g. ./test_ible.py *.log ible.out


processall: batch of shell command to process
			ible, fibre and hibre.

plot.py: transform 3 outputs of processall into a plot.dat file
			  for ploting. ouptut in plot.dat



Usage:
>>>./testall

>>> ./processall

>>> ./plot.py