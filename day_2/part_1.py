def score(opponent, me):
    opp_index = 'ABC'.index(opponent)
    my_index = 'XYZ'.index(me)
    # base score for the selected shape
    my_score = my_index + 1  
    match (my_index - opp_index) % 3:
        # draw
        case 0:
            return my_score + 3
        # win
        case 1:
            return my_score + 6
        # loose
        case 2:
            return my_score

total_score = 0
with open('input.txt') as f:
    for line in f.read().splitlines() :
        total_score += score(*line.split(' '))
print(total_score)
