
"""
bad_words = ['TIMESTEP', 'naughty']

with open('log.txt') as oldfile, open('log2.txt', 'w') as newfile:
	for line in oldfile:
		if  any(bad_word in line for bad_word in bad_words):
			try:
				s=line.split( )

				state =s[4]

				#if state=='observe' :
				#	continue 
				x =s[1]
				reward=s[13]
				q=s[16]
				score=s[19]
				newfile.write(x)
				newfile.write(" ")
				newfile.write(reward)
				newfile.write(" ")
				newfile.write(q)
				newfile.write(" ")
				newfile.write(score)
				newfile.write("\n")
			except Exception as e:
				print (line)
				continue

"""

 
 
with open('keras.10.txt') as f:
    lines = f.readlines()
    x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]
    z = [line.split()[2] for line in lines]
    #    t = [line.split()[3] for line in lines]




 
import matplotlib
matplotlib.use('Agg')

import pylab

 
pylab.subplot(3, 1, 1)
pylab.plot(x , y, "r")

pylab.subplot(3, 1, 2)
axes = pylab.subplot(132)

axes.set_ylim([-10,100])

pylab.plot(x, z, "b")
#pylab.subplot(3, 1, 3)
#pylab.plot(x , t, "g")

pylab.savefig('relu.png')

