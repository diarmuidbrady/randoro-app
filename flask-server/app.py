from flask import Flask, request, render_template
import random
from itertools import accumulate

app = Flask(__name__)

class RandoroWorkout:
    def __init__(self, w: int, N: int, r: int, t: int, n: int, d: int, c: int):
        """
        Initialize workout parameters.
        :param w: Warmup duration in seconds
        :param N: Number of rounds
        :param r: Rest duration between rounds in seconds
        :param t: Total duration of each round in seconds
        :param n: Number of intervals in each round
        :param d: Minimum duration of intervals in seconds
        :param c: Cool down duration in seconds
        """
        self.warmup = w
        self.num_rounds = N
        self.rest = r
        self.round_duration = t
        self.num_intervals = n
        self.min_interval_duration = d
        self.cooldown = c

    @staticmethod
    def generate_randoro_intervals(t: int, n: int, d: int):
        """
        Generates a series of random intervals within a given range.
        """
        # Input validation
        if n < 1 or d < 1 or t < n * d:
            return []
        elif t == n * d:
            return list(range(0, t + 1, d))
        else:
            random_time = t - (n * d)
            start_intervals = [random.uniform(0, random_time) for i in range(n)]
            scalar = sum(start_intervals) / random_time
            random_intervals = [
                round((x / scalar) + d, 3) if i > 0 else round(x / scalar, 3)
                for (i, x) in enumerate(start_intervals)
            ]
            intervals = [0] + list(accumulate(random_intervals)) + [t]
        return intervals

    def generate_randoro_workout(self):
        """
        Generates the full workout including warmup, random intervals, and cooldown.
        :return: Dictionary containing warmup, main rounds with rest, and cooldown.
        """
        self.workout = {"warmup": [0, self.warmup], "rounds": [], "cooldown": []}
        current_time = self.warmup

        # Generate rounds with rest
        for i in range(self.num_rounds):
            round_intervals = self.generate_randoro_intervals(
                self.round_duration, self.num_intervals, self.min_interval_duration
            )
            round_intervals = [current_time + t for t in round_intervals]  # Offset by current time
            self.workout["rounds"].append(round_intervals)
            current_time = round_intervals[-1] + self.rest

        # Add cooldown
        self.workout["cooldown"] = [current_time, current_time + self.cooldown]

        return self.workout

    @staticmethod
    def generate_table(warmup, num_rounds, rest, cooldown, round_duration, num_intervals, min_interval_duration):
        """
        Generates a formatted table as a string with specific column padding using string formatting and join.
        :return: Formatted table as a string.
        """
        # Total workout duration calculation
        total_duration = warmup + (num_rounds * round_duration) + ((num_rounds - 1) * rest) + cooldown

        # Table header and data
        headers = ["Warm up", "Main work", "Cool down"]
        data = [
            [f"{warmup}s", f"{num_rounds} rounds, {rest}s rest", f"{cooldown}s"],
            ["", f"Total duration: {round_duration}s", ""],
            ["", f"Intervals: {num_intervals}", ""],
            ["", f"Minimum duration: {min_interval_duration}s", ""],
        ]

        # Format row with specific column widths
        def format_row(row):
            return f"| {row[0]:<10} | {row[1]:<25} | {row[2]:<12} |"

        # Generate table rows
        header_row = format_row(headers)
        separator_row = "-" * len(header_row)
        data_rows = "\n".join(format_row(row) for row in data)

        # Combine all rows and append total duration
        table = "\n".join([header_row, separator_row, data_rows])
        return f"{table}\n{'-' * len(header_row)}\nTotal workout duration: {total_duration}s"

    def generate_detailed_table(self, workout):
        """
        Generates a detailed table displaying all workout intervals, wrapping intervals to show a maximum of 5 per row,
        and dynamically pads the middle column based on the longest row.
        :param workout: The workout dictionary with warmup, rounds, and cooldown data.
        :return: Formatted detailed table as a string.
        """
        # Table headers
        headers = ["Warm up", "Main workout", "Cool down"]

        # Format the warmup and cooldown
        warmup = ", ".join(map(str, workout['warmup']))
        cooldown = ", ".join(map(str, workout['cooldown']))

        # Helper to format intervals with wrapping
        def format_intervals(intervals, max_per_row=5):
            rows = []
            for i in range(0, len(intervals), max_per_row):
                row = ", ".join(f"{x:.1f}" for x in intervals[i:i + max_per_row])
                rows.append(row)
            return rows

        # Prepare the data rows for the rounds
        round_rows = []
        max_length = 0
        all_wrapped_intervals = []

        for i, round_intervals in enumerate(workout['rounds'], start=1):
            wrapped_intervals = format_intervals(round_intervals)
            all_wrapped_intervals.append((f"Round {i}", wrapped_intervals))
            max_length = max(max_length, *[len(row) for row in wrapped_intervals])

        # Format the rows
        def format_row(left, middle, right):
            return f"| {left:<10} | {middle:<{max_length}} | {right:<12} |"

        # Header and separator rows
        header_row = format_row(*headers)
        separator_row = "-" * len(header_row)

        # Warmup and cooldown rows
        warmup_row = format_row(warmup, "", cooldown)

        # Add round rows with dynamic padding
        for round_label, wrapped_intervals in all_wrapped_intervals:
            round_rows.append(format_row("", round_label, ""))
            for row in wrapped_intervals:
                round_rows.append(format_row("", row, ""))

        # Combine all rows
        detailed_table = "\n".join(
            [header_row, separator_row, warmup_row, separator_row] + round_rows + [separator_row]
        )
        return detailed_table

    def process_workout_sounds(self):
        # initialise sounds
        self.sounds = []
        self.intervals = []

        # add the warmup phase
        if self.workout['warmup'][-1] > 0:
            self.intervals.append(self.workout['warmup'][0])
            self.sounds.append('ready')
        
        # add the main phase
        for i, round in enumerate(self.workout['rounds']):
            self.intervals+=round
            self.sounds.append('go')
            self.sounds+=(['bell']*(len(round)-2))
            self.sounds.append('rest')

        if (self.workout['cooldown'][-1] - self.workout['cooldown'][0]) > 0:
            self.intervals+=self.workout['cooldown']
            self.sounds+=['relax', 'complete']
        else:
            self.intervals.append(self.workout['cooldown'][0])
            self.sounds.append('complete')
        
        return self.intervals, self.sounds

@app.route('/')
def index():
    return render_template('index.html', intervals=[])


# Process Input and Generate Intervals
@app.route('/generate_random_intervals', methods=['POST'])
def get_intervals():
    try:
        w = int(request.form['w'])
        N = int(request.form['N'])
        r = int(request.form['r'])
        t = int(request.form['t'])  # Total duration
        n = int(request.form['n'])  # Number of intervals
        d = int(request.form['d'])  # Minimum interval duration
        c = int(request.form['c'])

        if N <= 0 or t <= 0 or n <= 0 or d <= 0:
            raise ValueError("Inputs must be positive integers.")
        if n * d > t:
            raise ValueError("The total duration must be >= n * d.")

        randoro = RandoroWorkout(w, N, r, t, n, d, c)
        workout = randoro.generate_randoro_workout()
        intervals, sounds = randoro.process_workout_sounds()
        return render_template('index.html', intervals=intervals, sounds=sounds)

    except ValueError as e:
        return render_template('index.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
