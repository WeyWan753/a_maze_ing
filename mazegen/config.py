"""Configuration loading and validation for maze generation.

Defines the Config class, which reads a plain-text KEY=VALUE
configuration file, validates the required parameters (dimensions,
entry/exit points, output file, perfect/non-perfect mode, animation
delay, and random seed), and writes the generated maze and its
solution to the configured output file.
"""


class Config:
    """Loads, validates, and exposes maze generation settings from a
    configuration file.

    Reads a plain-text KEY=VALUE configuration file (with '#'
    comments supported), validates the required keys and their
    formats, and exposes them as typed attributes.

    Attributes:
        required (list[str]): Keys that must be present in the
            configuration file.
        config (dict[str, str]): Raw key-value pairs as read from
            the file, before type conversion.
        WIDTH (int): Maze width in cells.
        HEIGHT (int): Maze height in cells.
        ENTRY (tuple[int, int]): Entry coordinates (row, col).
        EXIT (tuple[int, int]): Exit coordinates (row, col).
        OUTPUT_FILE (str): Path to the output file.
        PERFECT (bool): Whether to generate a perfect maze.
        DELAY (float): Animation delay in seconds.
        SEED (int): Seed value for reproducible random generation.
    """

    def __init__(self, filename: str) -> None:
        """Load, parse, and validate a configuration file.

        Args:
            filename: Path to the configuration file to load.

        Raises:
            Exception: If a required key is missing or a value is
                malformed or invalid.
        """

        self.required = [
            "WIDTH", "HEIGHT", "ENTRY", "EXIT",
            "OUTPUT_FILE", "PERFECT", "DELAY", "SEED"
        ]
        self.config = self.load_config(filename)
        self.parse_config()
        self.validate_config_format()

    def load_config(self, filename: str = "config.txt") -> dict[str, str]:
        """Read raw KEY=VALUE pairs from a configuration file.

        Blank lines and lines starting with '#' are ignored.

        Args:
            filename: Path to the configuration file.

        Returns:
            A dict mapping each key found in the file to its raw
            string value.
        """

        config = {}

        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue
                split = line.split("=")
                if len(split) != 2:
                    raise Exception(
                        f"Error: {split}, follow this format: 'KEY=VALUE'")
                key, value = split
                config[key] = value

        return config

    def parse_config(self) -> None:
        """Verify that all required configuration keys are present and valid.

        Raises:
            Exception: If a required key is missing from the loaded
                configuration, or if PERFECT is not "true"/"false"
                (case-insensitive).
        """
        for key in self.required:
            value = self.config.get(key)
            if value is None:
                raise Exception(f"Missing key: {key}")
        perfect = self.config["PERFECT"].lower()
        if not (perfect == "true" or perfect == "false"):
            raise Exception(
                "PERFECT must either be true or false only, case insensitive"
            )

    def validate_config_format(self) -> None:
        """Convert and validate raw configuration values into typed attributes.

        Populates WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT,
        DELAY, and SEED from the raw config dict, and checks that
        entry/exit points are in bounds, distinct, not inside the
        "42" pattern, and compatible with the requested maze size
        and perfection mode.

        Raises:
            Exception: If any value is invalid (e.g. non-positive
                dimensions, entry/exit out of bounds or identical,
                entry/exit inside the "42" pattern, or a maze too
                small for a non-perfect layout).
        """

        self.WIDTH = int(self.config["WIDTH"])
        self.HEIGHT = int(self.config["HEIGHT"])
        entry = tuple(int(x) for x in self.config["ENTRY"].split(","))
        if len(entry) != 2:
            raise Exception(
                "Error: entry must be in coordinate of "
                "the the form: column,row")
        c, r = entry
        self.ENTRY = (r, c)
        _exit = tuple(int(x) for x in self.config["EXIT"].split(","))
        if len(_exit) != 2:
            raise Exception(
                "Error: exit must be in coordinate of the the form: column,row"
            )
        c, r = _exit
        self.EXIT = (r, c)
        self.OUTPUT_FILE = self.config["OUTPUT_FILE"].strip("\"'")
        self.PERFECT = self.config["PERFECT"].strip("\"'").lower() == "true"
        self.DELAY = float(self.config["DELAY"])
        self.SEED = int(self.config["SEED"])

        if self.HEIGHT <= 0:
            raise Exception("Height must be positive integer")
        if self.WIDTH <= 0:
            raise Exception("Width must be positive integer")

        _42 = set()
        if self.HEIGHT >= 6 and self.WIDTH >= 9:
            (r, c) = (self.HEIGHT//2, self.WIDTH//2)
            _42 = {
                    (r - 2, c - 3), (r - 1, c - 3), (r, c - 3), (r, c - 2),
                    (r, c - 1), (r + 1, c - 1), (r + 2, c - 1),
                    (r - 2, c + 1), (r - 2, c + 2), (r - 2, c + 3),
                    (r - 1, c + 3), (r, c + 3), (r, c + 2), (r, c + 1),
                    (r + 1, c + 1), (r + 2, c + 1),
                    (r + 2, c + 2), (r + 2, c + 3)}

        if self.ENTRY in _42:
            raise Exception("Entry Cant be in 42 pattern")
        if self.EXIT in _42:
            raise Exception("Exit Cant be in 42 pattern")
        if self.ENTRY == self.EXIT:
            raise Exception("Entry and Exit cant be the same")
        if not (0 <= self.ENTRY[0] < self.HEIGHT and
                0 <= self.ENTRY[1] < self.WIDTH):
            raise Exception("Entry is out of bound")
        if not (0 <= self.EXIT[0] < self.HEIGHT and
                0 <= self.EXIT[1] < self.WIDTH):
            raise Exception("Exit is out of bound")
        if not self.PERFECT and ((self.HEIGHT - 1) * (self.WIDTH - 1) < 2):
            raise Exception("Maze is too small for a non-perfect maze")

    def save_output(
        self, maze_hex: str,
        solution_path: list[tuple[tuple[int, int], str | None]]
    ) -> None:
        """Write the maze and its solution to the configured output file.

        Writes the hexadecimal maze grid, a blank line, the entry
        coordinates, the exit coordinates, and the solution path
        encoded as a string of direction letters (N/E/S/W).

        Args:
            maze_hex: The maze encoded as a hexadecimal grid string
                (see Maze.maze_to_hex).
            solution_path: Ordered list of (coordinates, direction)
                pairs describing the shortest path from entry to
                exit, as produced by MazeSolver.solver.
        """
        with open(self.OUTPUT_FILE, "w") as file:
            file.write(
                maze_hex + "\n\n" +
                f"{self.ENTRY[1]},{self.ENTRY[0]}" +
                "\n" + f"{self.EXIT[1]},{self.EXIT[0]}"
                + "\n" +
                "".join(
                    [item[1] for item in solution_path
                     if item[1] is not None])
                + "\n"
            )
