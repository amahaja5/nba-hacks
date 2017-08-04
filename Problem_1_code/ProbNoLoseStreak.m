function [ prob] = ProbNoLoseStreak(pwin,games)
% I'm dividing the season up into 81 two-game windows. So Window 1 will be
% games 1 and 2; Window 2 will be games 2 and 3. I will then, for each window,
% calculate the probability of NOT losing both games in a window GIVEN you 
% have not lost both games in any of the previous windows.

% Then to calculate the probability of never losing two consecutive games
% in the entire season, you multiply all of the conditional probabilities
% explained above together.
windows = games-1;
ploss = 1-pwin;
condprobs = zeros(windows,1);
% The conditional probability of not losing both games in window w (given a
% both games in window w-1 were not losses) depends on whether the 2nd game
% in window w was a win or a loss.
% fine(i) represents the probability of a team winning the 2nd game of
% window i given the team did not lose both games in window i.
fine = zeros(windows,1);
% problematic(i) represents the probability of a team lossing the 2nd game
% of window i given the team did not lose both games in window i.
problematic= zeros(windows,1);
condprobs(1) = pwin^2 + 2*pwin*ploss;
fine(1) = (pwin^2 + pwin*ploss)/(pwin^2 + 2*pwin*ploss);
problematic(1) = (pwin*ploss)/(pwin^2+2*pwin*ploss);
for i = 2:windows
    condprobs(i)= fine(i-1) + problematic(i-1)*pwin;
    fine(i) = (fine(i-1)*pwin + problematic(i-1)*pwin)/condprobs(i);
    problematic(i) = fine(i-1)*ploss/condprobs(i);
end
prob = prod(condprobs);

