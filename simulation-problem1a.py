import random
'''
Libary for python2 that holds most of the functions that
'''


#function declarations

def simulate_single_season(games=82, winning_pct=80):
	'''
	Simulates a single nba season, assuming a default of 82 games
	per year, just as the nba has, and a winning percent of 80, but 
	both can be changed

	This is mostly here to check the randomness of the rng in order
	to make sure that we have the winning percentage we want 
	'''
	#array that holds all of the season results
	season_wins = [0 for i in range(games)]
	for i in range(games):
		# random.randint is inclusive, so this should be the pct
		season_wins[i] = int(random.randint(0,99)) < winning_pct
	return season_wins

def count_number_of_two_consecutive_losses(season):
	'''
	Given a simulated season, this counts the number of two loss
	streaks a team has in that season.

	This is mostly here to test the next function.

	>>>count_number_of_two_consecutive_losses([])
	0
	>>>count_number_of_two_consecutive_losses([1,0,0,1])
	1
	>>>count_number_of_two_consecutive_losses([0,0,0])
	2
	>>>count_number_of_two_consecutive_losses([0,0,1,0,0])
	2
	'''
	count = 0
    for i in range(len(arr)-1):
    	# loops through two game windows
        if arr[i] == 0 and arr[i+1] == 0:
            count += 1
    return count

def count_consecutive_losses_season(games=82, winning_pct=80):
	'''
	Basically combines the previous two functions, to remove
	the array buffer. Used when simulating many seasons.

	This is the IMPORTANT function
	'''
	prev_game = int(random.randint(0,99) < winning_pct) # first game
	count = 0
	for i in range(games-1):
		next_game = int(random.randint(0,99) < winning_pct)
		#games stored in temporary buffer
		if prev_game == 0 and next_game == 0:
			count += 1
		prev_game = next_game
	return count

def consecutive_losses_season_return_season(games=82, winning_pct=80):
	'''
	Similar to the previous function, except it also returns the
	"season" for testing purposes.
	'''
	prev_game = int(random.randint(0,99) < winning_pct) # first game
	count = 0
	enum_games = 1
	#array to hold games
	game_list = [0 for i in range(games)]
	game_list[0] = prev_game
	for i in range(games-1):
		next_game = int(random.randint(0,99) < winning_pct)
		game_list[i+1] = next_game
		#games stored in temporary buffer
		if prev_game == 0 and next_game == 0:
			count += 1
		prev_game = next_game
		enum_games += 1
	assert(enum_games == games)
	return count, game_list

def TEST_consecutive_losses_season(num_iter=10000):
	'''
	function that tests the above 2 functions
	'''
	for i in range(num_iter):
		count, game_list = consecutive_losses_season_return_season()
		count2 = count_number_of_two_consecutive_losses(game_list)
		assert(count == count2)
	print("Completed consecutive losses function test.")

def TEST_rng_many_seasons(num_iter=1000000, winning_pct=80, num_games=82):
	'''
	tests the rng to see if the average number of wins are within 
	tolerance (~0.01%)
	'''
	tolerance = 0.01
	seasons_wins = 0
	for i in range(num_iter):
		seasons_wins += sum(simulate_single_season(num_games, winning_pct))
	assert( (winning_pct - tolerance) <=
		(float(seasons_wins)/(num_games*num_iter))*100 <=
		(winning_pct+tolerance))
	print("Completed RNG test")

def main():
	TEST_consecutive_losses_season()
	TEST_rng_many_seasons()

if __name__ == '__main__':
	main()