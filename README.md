# get_from_fasta_gui
A python script used to extract specific sequences from a fasta file based on ID or keyword.

## Background
Next Generation Sequences produce large fasta files that are too large to be handled in graphical user interface (GUI) text editors. Quite often these files need to be filtered based on ID list produced by other tools' output (gene expression results, anootation results, etc.).
This script provides a simple GUI to allow researchers to retrieve specific sequences from big fasta files (genome/transcriptome assemblies) without the hassle of using Unix command line scripts and tools. 

## Usage
Run the script get_from_fasta_gui.py from command line or your favourite Python IDE.

### Requirements
1. List of sequence IDs, one in a line, in a csv file
2. Fasta database to look for the sequences 
3. [Python 2.7](https://www.python.org/download/releases/2.7/) with [easygui](http://easygui.sourceforge.net/) and [BioPython](http://biopython.org/wiki/Biopython) packages installed
4. Graphical terminal access (windows on linux machines).

### TODO
1. Add exception handling for long fasta headers
2. Add exception handling for program abort (no input files selection)
3. Tidy up functions
4. Keyword list support
5. Command line version
