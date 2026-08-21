class Config:
    def __init__(self, filename: str) -> None:
        self.required = [
            "WIDTH", "HEIGHT", "ENTRY", "EXIT",
            "OUTPUT_FILE", "PERFECT", "DELAY", "SEED"
        ]
        self.config = self.load_config(filename)
        self.parse_config()
        self.validate_config_format()

    def load_config(self, filename: str = "config.txt") -> dict[str, str]:
        config = {}

        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=", 1)
                config[key] = value

        return config

    def parse_config(self) -> None:
        for key in self.required:
            value = self.config.get(key)
            if value is None:
                raise Exception(f"Missing key: {key}")
        perfect = self.config["PERFECT"].lower()
        if not (perfect == "true" or perfect == "false"):
            raise Exception("PERFECT must either be true or false only, case insensitive")

    def validate_config_format(self) -> None:
        self.WIDTH = int(self.config["WIDTH"])
        self.HEIGHT = int(self.config["HEIGHT"])
        c, r = tuple(int(x) for x in self.config["ENTRY"].split(",", 1))
        self.ENTRY = (r, c)
        c, r = tuple(int(x) for x in self.config["EXIT"].split(",", 1))
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
        else:
            print("Error: maze is too small to display the 42 pattern")

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
