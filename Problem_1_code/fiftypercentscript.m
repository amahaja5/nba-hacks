ProbNoLoseStreak(.8,82) %0.0588
% The probability of a team not having a 2 game losing streak in an 82-game
% season (assuming they have an 80% chance of winning each game) is 5.88%

test = .8:.000001:1;
results = zeros(length(test),1);
for i = 1:length(test)
    results(i) = ProbNoLoseStreak(test(i),82);
end
bad = results(results<=.5);
minimumind = find(bad == max(bad));
minimum = test(minimumind); %0.9038
% In order for a team to have a 50% chance of never losing 2 consecutive
% games in a season, they would need to have a 90.38% chance to win every
% game