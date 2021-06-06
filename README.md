# E-VOLVE Sim (ALPHA)
E-volve is a project initially created for my MP3 quarterly for Biology. It aims to act as a tool for accurately simulating the evolution of a population over time.


## TERMINOLOGY
Pop: Population member.

ID: Identification code assigned to each pop. The first pop is always given the ID 10000000.


## META-NOTATION
[] = optional

|| = or

() = indication of order of operations

## COMMANDS
### spawn x [-c y [w z]]
x pops are added, all of which are automatically assigned generation F0 and a random gender.

WITH -c && y: y is a color code (see terminology). All pops spawned will be color y.

WITH -c && y && w && z: y, w, and z comprise a space delimited RGB color code. All pops spawned will be said RGB value.

ELSE: All pops spawned will be blue unless another command has dictated otherwise.


### kill x [-r]
WITH -r: Kills x random pops.

W/OUT -r: Kills pop with ID x.


### paint x [-a] || (([-d] || [-r]) ([-m] || [-f]))
Paints pops color code x.

WITH -a: Paints all pops.

WITH -d: Paints all pops with a dominant phenotype.

WITH -r: Paints all pops with a recessive phenotype.

WITH -m: Paints all male pops.

WITH -f: Paints all female pops.

W/OUT ANY: No pops are painted.

### x && y
Binary operation that concatenates two [2x] commands x and y into one [1x] line.
IE: spawn 50 && paint -f pink && clear

### ls
List data about all pops

### clear
Clears the terminal screen.

### VARIABLE BASED
### Varlist:
p (Frequency of dominant alleles) [WARNING: UNTESTED; UNLIKELY TO FUNCTION AS INTENDED]

q (Frequency of recessive alleles) [WARNING: UNTESTED; UNLIKELY TO FUNCTION AS INTENDED]

tick (Controls the wait time between each action, Default: 1) [UNSTABLE]

maxgen (The maximum generation a population can reach before ceasing reproduction)

#### x [set] || [=] y
The value of x is changed to y

#### x [sub] || [-] y
The value of x is subtracted from y

#### x [add] || [+] y
The value of y is added to x
