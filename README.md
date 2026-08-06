*This project has been created as part of the 42 curriculum by asmounci.*

# Fly-in ✈️

## Description

**Fly-in** is a drone routing simulator. The goal of the project is to move a fleet of
drones from a single **start zone** to a single **end zone** through a network of
connected zones (a graph), in the fewest possible simulation turns, while respecting a
set of movement and occupancy constraints.

The project reads a custom text file describing the map: zones (with a type, a color,
and an optional capacity), and connections between them (with an optional capacity).
It then computes a route through the network and simulates, turn by turn, drones
moving simultaneously from the start zone to the end zone.

Each zone type affects how drones can use it:

| Zone type    | Movement cost | Notes                                   |
|--------------|----------------|------------------------------------------|
| `normal`     | 1 turn         | Default type                             |
| `priority`   | 1 turn         | Should be preferred by the pathfinding   |
| `restricted` | 2 turns        | Drone must commit and cannot wait mid-way|
| `blocked`    | -              | Cannot be entered at all                 |

The simulation also enforces zone capacity (`max_drones`) and connection capacity
(`max_link_capacity`), so that drones do not collide or overload the network.

Once the route is computed, the simulation is displayed through a **graphical
interface** built with `pygame`, showing the zones, the connections, and the drones
moving live across the map.

## Instructions

### Requirements

- Python 3.10 or later
- Dependencies listed in `requirements.txt` (`flake8`, `mypy`, `pygame`)

### Installation

Install project dependencies with:

```bash
make install
```

This runs `python3 -m pip install -r requirements.txt`.

### Running the simulation

```bash
make run FILE=<path_to_map_file>
```

Example:

```bash
make run FILE=maps/easy_1.txt
```

The program parses the given map file, computes a route, and opens a `pygame` window
to display the simulation.

### Other Makefile commands

| Command             | Description                                                |
|----------------------|-------------------------------------------------------------|
| `make install`       | Install project dependencies                                |
| `make run FILE=...`  | Run the simulation on the given map file                    |
| `make debug FILE=...`| Run the simulation under Python's built-in debugger (`pdb`) |
| `make clean`         | Remove `__pycache__` and `.mypy_cache` directories           |
| `make lint`          | Run `flake8` and `mypy` with the required flags             |
| `make lint-strict`   | Run `flake8` and `mypy --strict` for stricter checking      |

### Map file format

A map file starts with the number of drones, followed by zone and connection
definitions:

```
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]

connection: hub-roof1
connection: hub-corridorA
connection: corridorA-goal [max_link_capacity=2]
```

- `zone=` accepts `normal`, `blocked`, `restricted`, `priority`.
- `max_drones=` sets how many drones a zone can hold at once (ignored on start/end
  zones, which always have unlimited capacity).
- `max_link_capacity=` sets how many drones can travel through a connection at once.
- Lines starting with `#` are treated as comments and ignored.

## Algorithm choices and implementation strategy

The project is fully **object-oriented**, without using any graph library (no
`networkx`, no `graphlib`). The main components are:

- **`Zone`**: represents a single node of the graph (name, coordinates, type, color,
  capacity).
- **`Connection`**: represents a bidirectional edge between two zones, with its own
  capacity.
- **`Graph`**: stores zones and connections and exposes an adjacency structure
  (`neighbors`, `get_connection`) built by hand, without relying on any external graph
  library.
- **`Parser`**: reads the map file line by line, validates its syntax strictly (unique
  zone names, valid coordinates, valid zone types, no duplicate connections, valid
  metadata, etc.) and raises a `ParserError` with a clear message on any invalid input.
- **`Pathfinder`**: implements **Dijkstra's algorithm from scratch** (no
  `heapq`/library shortcuts) to compute the shortest weighted path from the start zone
  to the end zone. Zone types are turned into edge weights (`normal`/`restricted`
  cost more, `priority` is favored with a lower cost), and `blocked` zones are
  excluded from the search entirely.
- **`Drone`**: a lightweight object tracking a drone's position along a path (current
  zone, next zone, progress index).
- **`Visualizer`**: owns the simulation loop. At every simulated turn, it tries to
  move every drone one step further along the computed path, but only if:
  - the destination zone still has free capacity (`max_drones`), and
  - the connection used still has free capacity (`max_link_capacity`).

  If a drone cannot move (destination full, or link saturated), it simply waits for
  the next turn — this is how the project handles capacity constraints and avoids
  zone/connection overload without deadlocking the simulation.

### Complexity and performance

- Dijkstra's algorithm runs in `O(V^2)` in this implementation (a simple linear scan
  is used to pick the minimum-distance node instead of a priority queue), which is
  more than sufficient given the size of the maps used in this project.
- The path is computed **once** at the start of the simulation and then reused for
  every drone (cached), instead of being recalculated turn by turn, which keeps the
  simulation loop lightweight (`O(nb_drones)` work per turn).
- Memory usage stays low: the graph is stored as a simple adjacency list, and each
  drone only stores its path and current index into it, no duplicated state.

## Visual representation

The simulation uses a **graphical interface** built with `pygame` rather than a
terminal-only output, in order to make the network topology and the drone movement
easier to follow at a glance:

- Each zone is drawn as a circle at its `(x, y)` coordinates (scaled to fit the
  window), using the zone's configured color, and labeled with its name.
- Connections are drawn as lines between zones.
- Drones are rendered as small animated quadcopters (four arms with spinning
  propellers) positioned around the zone they currently occupy, each with a unique
  color and its own `D<id>` label, so multiple drones sharing a zone remain
  distinguishable.
- The current occupancy of each zone (`current / max_drones`) is displayed under the
  zone, making capacity constraints and congestion immediately visible.
- The simulation window is resizable, and pressing `F5` resets the simulation from
  the beginning.
- Each simulated turn is also printed to the terminal in the required
  `D<ID>-<zone>` format, so the output can be checked or logged independently of the
  graphical view.

This visual feedback makes it much easier to verify — both for the developer and
during peer review — that the pathfinding and capacity rules are being respected
in real time, rather than having to trace through raw text output.

## Resources

- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [pygame official documentation](https://www.pygame.org/docs/)
- [Python `typing` module documentation](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

### AI usage

AI (Claude) was used during this project as a support tool, following the AI usage
guidelines given in the subject:

- Discussing and reviewing the **Makefile** structure to make sure it matched all the
  mandatory rules from the subject (`install`, `run`, `debug`, `clean`, `lint`,
  `lint-strict`) and followed good practices (e.g. using `python3 -m pip` instead of
  `pip3` directly for consistency with the interpreter used to run the project).
- Getting help drafting and structuring this `README.md` file according to the
  subject's requirements.

All AI-assisted output was reviewed, understood, and adapted before being included in
the project, and no core algorithm or simulation logic was generated by AI without
being fully understood first.