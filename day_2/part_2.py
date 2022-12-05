def score(opponent, result):
    opp_index = 'ABC'.index(opponent)
    match result:
        # loose
        case 'X':
            return 1 + (opp_index - 1) % 3
        # draw
        case 'Y':
            return 1 + 3 + opp_index
        # win
        case 'Z':
            return 1 + 6 + (opp_index + 1) % 3

total_score = 0
with open('input.txt') as f:
    for line in f.read().splitlines():
        total_score += score(*line.split(' '))
print(total_score)
