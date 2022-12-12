from pathlib import Path

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')
START = 'S'
END = 'E'

grid = []
with open(INPUT_FILE) as f:
    for row, line in enumerate(f.read().splitlines()):
        grid.append(list(line))
        if START in line:
            start_pos = row, line.index(START)
        if END in line:
            end_pos = row, line.index(END)

grid[start_pos[0]][start_pos[1]] = 'a'
grid[end_pos[0]][end_pos[1]] = 'z'


def neighbours(pos, grid):
    height = len(grid)
    width = len(grid[0])
    row, col = pos
    current = grid[row][col]
    for new_row, new_col in ((row - 1, col), (row, col + 1), (row + 1, col),
            (row, col - 1)):
        if 0 <= new_row < height and 0 <= new_col < width:
            new_val = grid[new_row][new_col]
            if ord(new_val) - ord(current) >= -1:
                yield new_row, new_col

# Follow the track in the opposite way
visited = {end_pos}
frontier = [end_pos]
steps = -1
while frontier:
    new_frontier = []
    for current in frontier:
        if grid[current[0]][current[1]] == 'a':
            new_frontier = []
            break
        for neighbour in neighbours(current, grid):
            if neighbour not in visited:
                new_frontier.append(neighbour)
                visited.add(neighbour)
    frontier = new_frontier
    steps += 1

print(steps)