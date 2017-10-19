Code is still fragile

Requires that the csv samples names contains exactly every sample you are concatenating. No more; no less.

Use:
	copy the whole directory into its own directory on the HPC
	populate toBeConcat with ONLY -Sequences.txt files of the samples
	Edit concat output so that
		1st line = experiment number
		2nd line = folder full of -Sequences.txt
		3rd line = where the concatenated files should be outputted
		4th line = samples names and barcode information

	submit the whole job with: qsub -q bio main.sh

concatInput.txt is pre-populated with file names for reference
		