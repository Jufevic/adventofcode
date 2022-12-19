from pathlib import Path

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

faces = set()
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        x, y, z = map(int, line.split(','))
        for face in (
            (x, y, z, 0),
            (x, y, z, 1),
            (x, y, z, 2),
            (x + 1, y, z, 0),
            (x, y + 1, z, 1),
            (x, y, z + 1, 2),
        ):
            if face not in faces:
                faces.add(face)
            else:
                faces.remove(face)

print(len(faces))
