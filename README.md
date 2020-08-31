# Fly-analysis
Contains programs to analyse various aspects of a tethered fly

So far, only codes that analyse winglengths have been added. There are conventions to be followed here but hopefully this can be made more
unbreakable in the future. I've got rid of the wing numbering convention, now you can enter whatever convention is used in the file you digitized.

Asymmetric wings: Points 1, 2 = left, right wing apices respectively. Points 3, 4 = left, right wing bases respectively. Point 5 = head base
Slit sc: Point 1 = head base. Point 2, 3 = left, right wing bases respectively. Point 4, 5 = left, right wing apices respectively. Point 6,7 = left, right haltere bases respectively. Point 8,9 = left, right haltere bases respectively.

How to write a data_organization file:

1) Avoid whitespace as much as possible - the code can deal with it to some extent, but not fully so.
2) Any comments MUST be preceded by a '#', otherwise it will create errors when the file is read.
3) The first argument is a declaration of the mode like so:
          mode='asym'
          # (just for example, you could also set mode equal to 'epi', 'sc', or 'halt'; but any other names would create an error.
4) The rest of the arguments set pointnames to points like so:
          pointname=<number>
          # Example:
          lwapex=1
          # The number must be an int and the pointname must have one of the following names: 'lwapex','rwapex','lwbase','rwbase','fixed',lhapex','rhapex','lwbase', or 'rhbase'; 
          # If not, errors will be generated.
5) Save the file as 'data_organization_mode.txt' (for instance, 'data_organization_asym.txt'. This is not necessary, but is used as a convention and that goes into making files like multiple_file_analysis.py
