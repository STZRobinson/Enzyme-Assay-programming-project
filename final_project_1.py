# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 19:35:53 2016

@author: sam&jacob
"""

from J6305 import Spectrometer
spec = Spectrometer()
print(' ')
print('-------------------------------------')
print('    Jenway 6305 Spectrophotometer')
print('-------------------------------------')
print(' ')

'''This section of the code defines the calculation of initial velocity and 
rate of formation of product first part of the assay. Initially this was to be 
used to define the similar calculations in parts 2 and 3 also, however they
differ substantially enough to require their own code. Those are included in the
main body of the code later. This definition just keeps the first section of
the program clean.
Each input is run through a try/except loop, which prevent program from crashing
if an incorrect input occurs and provide the user with an opportunity to try 
again immediately. '''
def calc():
    print('Calculate initial velocity using results found in "results.txt":')
    while True:
        try:
            y2 = float(input('Input y2 value (Absorbance): '))
            break
        except ValueError:
            print('All values must be numbers') 
            # Gives the user advice about what they did wrong
    while True:
        try:
            y1 = float(input('Input y1 value (Absorbance): '))
            break          
        except ValueError:
            print('All values must be numbers.')
    while True:
        try:
            x2 = float(input('Input x2 value (min): '))
            break
        except ValueError:
            print('All values must be numbers.')
    while True:
        try:
            x1 = float(input('Input x1 value (min): '))
            break
        except ValueError:
            print('All values must be numbers.')
    '''The values entered are now used to calculate initial velocity of the 
    reaction and the rate of formation of product. Those are then written to the
    results file and printed on the screen.'''        
    V = (y2-y1)/(x2-x1) # Calculates initial velocity
    print('The initial velocity of the reaction is {}min^-1'.format(V))
    print(' ')
    print('Calculate rate of formation of product:')
    l = float(1.0) # Path length of J6305 spectrometer is 1cm
    while True:
        try:
            epsilon = float(input('Input molar extinction coefficient: '))
            break
        except ValueError:
            print('Molar extinction coefficient must be a floating point number')
    v = V/(l * epsilon) # calculates rate of formation of product
    print('The rate of formation of product is {}mol/l^-1/min^-1'.format(v))
    with open ('results.txt', 'a') as f:
        f.write('\n Initial velocity of reaction (V):\n')
        f.write(str(V))
        f.write('\n Rate of formation (v):\n')
        f.write(str(v))
        # writes out the results to a file. Using the "with open() as x:" line 
        # neatly opens the file for appending, writes the data, and them closes
        #the file automatically, thus saving system resources.
        
'''This section is what the user will see on running the program. The user is 
presented with the chance to enter some notes about their experiment. This 
information will then be written to the file which is created, "results.txt".'''
print('-------------------------- ')
print('       ENZYME ASSAY')
print('-------------------------- ')
print(' ')
notes = str(input('Enter experiment notes: \n'))
f  = open('results.txt', 'w') # creates and opens a file to which results can be saved
f.write('JENWAY 6305 SPECTROPHOTOMETER \n')
f.write('Notes :')
f.write(notes)
f.close() # closes the file for now
print(' ')
'''The user is now prompted to provide information that will be used to run the
first part of the assay. On entering a wavelength the spec will immediately set
to that wavelength which provides some tangible feedback that what they are 
doing is correct. Once again, try/except loops are used to catch errors.'''
while True:
    try:
        wave = int(input('Input a wavelength (nm): ')) # defines the wavelength to be used
        break
    except ValueError:
        print('Wavelength must be a whole number')
spec.set_wavelength(wave) # sets the spec to the desired wavelength  
while True:
    try:
        no_of_readings = int(input('Input the number of readings to be taken: ')) 
        break
    except ValueError:
        print('Number of readings must be a whole number')
while True:
    try:
        time_between_readings = int(input('Input the time between individual readings in seconds: ')) 
        # defines the length of time taken between readings thus the 
        #no_of_readings and time_between_readings together determine how long 
        #the spec should take readings for.
        break
    except ValueError:
        print('value must be a whole number')
        
'''The user must now press enter to begin analysis. This provides the user with
as much time as necessary to get ready.'''
input('Press Enter to take readings...') # prompts the user to begin analysis
print(' ')
spec.calibrate() # calibrates the spec to whatever is inside it.

'''The spectrometer is calibrated and the experiment begins. First a list is
created to contain the absorbance readings, then the readings themselves are 
collected.The readings are the absorbance values for the reaction mixture at the 
time intervals defined, which will be collected as many times as they have been
told to. The list is converted into a string, and this allows the absorbances
to be appended to the results file. The user may use this data to plot Absorbance
vs Time.'''
v_readings_list = []
for n in range(no_of_readings): # loops through taking absorbance readings based on the number in no_of_readings
    v_readings_list.append(spec.absorbance()[0]) # reads absorbance and adds values to v_readings_list
    spec.pause(time_between_readings) # pauses the spec, controlling the time between readings
rl = str(v_readings_list) # converts values in v_readings_list into a string
with open('results.txt', 'a') as f: # this opens the file for appending and closes it once finished
    f.write('\n Initial Velocity progress curve:\n')
    f.write(rl) # writes the absorbance values to the file
    
'''Here the initial velocity and rate of formation calculations are run. The
code requires the user to determine values for y2,y1,x2,x1 from the linear region
of their plot of Absorbance vs Time. This data can then be fed back into the
program allowing the calculation of initial velocity and rate of formation of 
product (which requires a molar extinction coefficient that the user should have.'''
calc() #runs the calculations
print(' ')

'''This is now the second part of the assay. The wavelngth remains the same as
specified by the user earlier. This part of the assay runs similarly to the first,
however the user has the option to specify the number of times to run the experiment
in order to measure more than one concentration of enzyme.'''
print('Variation of [enzyme]')
while True:
    try:
        no_of_readings = int(input('Input the number of readings to be taken: ')) # defines the number of readings the user wants to take
        break
    except ValueError:
        print('Number of readings must be a whole number')
while True:
    try:
        time_between_readings = int(input('Input the time between individual readings in seconds: '))
        break
    except ValueError:
        print('Value must be a number')
while True:
    try:
        no_of_readings_to_be_taken = int(input('Input the number of different repetitions [enzyme] to be used: '))
        break
    except ValueError:
        print('Number of repeats must be a whole number')
enz_initial_velocity = []
enz_rate_of_formation = []
#creates 2 lists to store the different values for v & V 
for n in range(no_of_readings_to_be_taken):
    input('Press Enter to take readings...') # prompts the user to begin analysis
    spec.calibrate() # calibrates the spec
    enzyme_v_readings_list = []
    for n in range(no_of_readings): # loops through taking absorbance readings based on the number in no_of_readings
        enzyme_v_readings_list.append(spec.absorbance()[0]) # reads absorbance and adds values to enzyme_v_readings_list
        spec.pause(time_between_readings) # pauses the spec, controlling the time between readings
    rl = str(enzyme_v_readings_list) # converts values in v_readings_list into a string
    with open('results.txt', 'a') as f: # this opens the file for appending and closes it once finished
        f.write('\n Initial velocity progress curve [enzyme]: \n')
        f.write(rl) # writes the absorbance values to the file
    print(' ')
    '''Here the user must obtain a graph of Absorbance vs Time for each concentration
    of enzyme and put the co-ordinates of the linear region into the program again
    to generate a value for initial velocity. Once multiple values for initial 
    velocity at various [enzyme] have been obtained, the user must then plot 
    Initial Velocity vs [enzyme]. From this the user must select an [enzyme] to
    use in part 3 of the assay.'''
    print('Calculate initial velocity using results found in "results.txt":') 
    # prompts the user to input values allowing for the calculation of initial velocity
    while True:
        try:
            y2 = float(input('Input y2 value (Absorbance): '))
            break
        except ValueError:
            print('All values must be numbers')
    while True:
        try:
            y1 = float(input('Input y1 value (Absorbance): '))
            break
        except ValueError:
            print('All values must be numbers.')
    while True:
        try:
            x2 = float(input('Input x2 value (min): '))
            break
        except ValueError:
            print('All values must be numbers.')
    while True:
        try:
            x1 = float(input('Input x1 value (min): '))
            break
        except ValueError:
            print('All values must be numbers.')

    V = (y2-y1)/(x2-x1) #calculates initial velocity
    print('The initial velocity of the reaction is {}min^-1'.format(V))
    print(' ')
    print('Calculate rate of formation of product:')
    l = float(1.0) # path length of J6305 spectrometer is 1cm
    while True:
        try:
            epsilon = float(input('Input molar extinction coefficient: ')) # asks for molar extinction coefficent
            break
        except ValueError:
            print('Molar extinction coefficient must be a floating point number')
    v = V/(l * epsilon) # calculates rate of formation of product

    
    enz_initial_velocity.append(V)
    enz_rate_of_formation.append(v)
    with open ('results.txt', 'a') as f:
        f.write('\n Initial velocity of reaction:\n')
        f.write(str(V))
        f.write('\n Rate of formation:\n')
        f.write(str(v))

print(' ')
'''Part 3 is identical to part 2, except this time substrate concentration is 
varied at a fixed enzyme concentration determined in part 2.'''
print('Variation [substrate]')
while True:
    try:
        no_of_readings = int(input('Input the number of readings to be taken: ')) # defines the number of readings the user wants to take
        break
    except ValueError:
        print('Number of readings must be a whole number')
while True:
    try:
        time_between_readings = int(input('Input the time between individual readings in seconds: '))
        break
    except ValueError:
        print('Value must be a whole number')
while True:
    try:
        no_of_readings_to_be_taken = int(input('Input the number of different repetitions [substrate] to be used: '))
        break
    except ValueError:
        print('Number of repeats must be a whole number')
sub_initial_velocity = []
sub_rate_of_formation = []
for n in range(no_of_readings_to_be_taken):
    input('Press Enter to take readings...') # prompts the user to begin analysis
    spec.calibrate() # calibrates the spec
    substrate_v_readings_list = []
    for n in range(no_of_readings): # loops through taking absorbance readings based on the number in no_of_readings
        substrate_v_readings_list.append(spec.absorbance()[0]) # reads absorbance and adds values to substrate_v_readings_list
        spec.pause(time_between_readings) # pauses the spec, controlling the time between readings
    rl = str(substrate_v_readings_list) # converts values in substrate_v_readings_list into a string
    with open('results.txt', 'a') as f: # this opens the file for appending and closes it once finished
        f.write('\n Initial velocity progress curve [substrate]:\n')
        f.write(rl) # writes the absorbance values to the file

    print(' ')
    print('Calculate initial velocity using results found in "results.txt":') 
    # prompts the user to input values allowing for the calculation of initial velocity
    while True:
        try:
            y2 = float(input('Input y2 value (Absorbance): '))
            break
        except ValueError:
            print('All values must be numbers')
    while True:
        try:
            y1 = float(input('Input y1 value (Absorbance): '))
            break
        except ValueError:
            print('All values must be numbers.')
    while True:
        try:
            x2 = float(input('Input x2 value (Seconds): '))
            break
        except ValueError:
            print('All values must be numbers.')
    while True:
        try:
            x1 = float(input('Input x1 value (Seconds): '))
            break
        except ValueError:
            print('All values must be numbers.')

    V = (y2-y1)/(x2-x1)
    print('The initial velocity of the reaction is {}sec^-1'.format(V))
    print(' ')
    print('Calculate rate of formation of product:')
    l = float(1.0)
    while True:
        try:
            epsilon = float(input('Input molar extinction coefficient: '))
            break
        except ValueError:
            print('Molar extinction coefficient must be a floating point number')
    v = V/(l * epsilon)
    print('The rate of formation of product is {}mol/l^-1/sec^-1'.format(v))
    sub_initial_velocity.append(V)
    sub_rate_of_formation.append(v)
    with open ('results.txt', 'a') as f:
        f.write('\n Initial velocity of reaction:\n')
        f.write(str(V))
        f.write('\n Rate of formation:\n')
        f.write(str(v))

'''Once all data has been collected, this code will determine the Vmax and Km
of the enzyme and write these values to the results file.'''
Vmax = max(sub_rate_of_formation) # calculates Vmax
Km = Vmax/2 # calculates Km
print(' ')
print('Vmax of reaction for enzyme is {} Units'.format(Vmax))
print(' ')
print('Km of reaction for enzyme is {} Units'.format(Km))
with open ('results.txt', 'a') as f:
    f.write('\n Vmax:\n')
    f.write(str(Vmax))
    f.write('\n Km:\n')
    f.write(str(Km))
