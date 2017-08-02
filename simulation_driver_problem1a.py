from simulation_problem1a import count_consecutive_losses_season
import matplotlib.pyplot as pyp
import numpy as np
'''
Driver code to derive sample, and then run tests on the sample
Uses matplotlib to visualize the problem.  
'''


def two_loss_sample_sim(num_sim = 10000000):
	'''
	simulates num_sim number of seasons,
	and holds a buffer of the counts of two losses
	returns the array of counts

	>>>two_loss_sample_sim(0)
	[]
	'''
    counts = [0 for i in range(num_sim)]
    for i in range(num_sim):
        counts[i] = count_consecutive_losses_season()
        if (i+1) % int(num_sim/10) == 0:
            print("simulation %d" % (i+1))
    return counts

def t_testing(arr, null_hyp):
	pass

def display_stats(counts, num_sim=10000000):
	stats = (np.mean(counts), 
		np.stddev(counts), 
		float(count_zero_loss_seasons(counts))/num_sim)

	print("Sample Mean: %d\n Standard Deviation: %d\n pct of 0 cons losses: %d" %
		stats)
	return stats

def count_zero_loss_seasons(counts):
	num_zero_loss = 0
	for cons_loss in counts:
		if cons_loss == 0:
			num_zero_loss += 1
	return num_zero_loss		

def print_hist(counts):
	plt.show()

def main():
	counts = two_loss_sample_sim()
	(sample_avg, sample_std, pct) = display_stats(counts)
	print_hist(counts)

