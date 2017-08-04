from simulation_library import count_consecutive_losses_season
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stat
import sys
'''
Driver code to derive sample, and then run tests on the sample
Uses matplotlib to visualize the problem.  

Usage:
python simulation_driver_problem.py [num_sim]

num_sim is optional parameter for number of simulations. 

Output:
Prints stats and displays histogram
'''


def two_loss_sample_sim(num_sim = 1000000, winning_pct=80):
    '''
    simulates num_sim number of seasons,
    and holds a buffer of the counts of two losses
    returns the array of counts

    >>>two_loss_sample_sim(0)
    []
    '''

    counts = [0 for i in range(num_sim)]
    for i in range(num_sim):
        counts[i] = count_consecutive_losses_season(winning_pct*100)
        if (i+1) % int(num_sim/10) == 0:
            print("simulation %d" % (i+1))
    return counts

def t_testing(arr, null_hyp):
    '''
    run and output t-tests for testing hypothesis
    '''
    t, prob = stat.ttest_1samp(arr, null_hyp)
    print("value of t-statistic %1.8f\n p-value: %1.8f" % (t, prob/2))
    return t, prob

def display_stats(counts):
    '''
    Displays some stats that are relevant to the write-up
    '''
    stats = (np.mean(counts), 
        np.std(counts), 
        float(count_zero_loss_seasons(counts))/len(counts)*100)

    print("Sample Mean: %1.4f\n Standard Deviation: %1.4f\n pct of 0 cons losses: %1.4f" %
        stats)
    return stats

def count_zero_loss_seasons(counts):
    '''
    simply checks for 0 losses in a single series of counts
    '''
    num_zero_loss = 0
    for cons_loss in counts:
        if cons_loss == 0:
            num_zero_loss += 1
    return num_zero_loss        

def print_hist(counts, sample_avg):
    '''
    generates a histogram of counts, with average marked
    '''
    plt.hist(counts, bins=max(counts), color='c')
    plt.axvline(sample_avg, color='b', linestyle='dashed', linewidth=2)
    plt.xlabel('Consecutive Losses')
    plt.ylabel('Frequency')
    plt.title(r'Consecutive Loss Frequencies, p=0.8')
    plt.show()

def main():
    if len(sys.argv) == 1:
        counts = two_loss_sample_sim()
    else:
        try:

        except ValueError:
            print("Invalid input. Please enter an int.")
            return
    print("n = %d" % len(counts))
    (sample_avg, sample_std, pct) = display_stats(counts)
    t_testing(counts, 0)
    print_hist(counts, sample_avg)

if __name__ == '__main__':
    main()

