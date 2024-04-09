from datetime import datetime, timedelta
import random
import tkinter as tk
from tkinter import simpledialog
import numpy as np
import pandas as pd

# Location to save score history
scores_folder = "./data"


class UltraMac:
    def __init__(self, username, game_root, font="Arial", font_size=20, time_limit=5):
        # Store scores and user data using username
        self.font = font
        self.font_size = font_size
        self.game_root = game_root
        self.username = username
        self.time_limit = time_limit  # in seconds

        # Create UI elements with padding to look pretty
        self.game_root.title("UltraMac")
        self.game_root.geometry("400x500")
        self.label_timer = tk.Label(
            self.game_root,
            text=f"Time: {self.time_limit}",
            font=(self.font, self.font_size),
        )
        self.label_timer.pack(pady=5)
        self.label_score = tk.Label(
            self.game_root, text="Score: 0", font=(self.font, self.font_size), fg="red"
        )
        self.label_score.pack(pady=5)
        self.button_start = tk.Button(
            self.game_root,
            text="Start Game",
            command=self.start_game,  # Start game once start button is pressed
            font=(self.font, self.font_size),
        )
        self.button_start.pack(pady=10)
        self.button_start.bind("<Return>", self.start_game)
        self.button_start.focus_set()

    def start_game(self, event=None):
        self.end_time = datetime.now() + timedelta(seconds=self.time_limit)
        self.score = 0
        # TODO implement more complex game logic for scoring, maybe based on problem difficulty
        # Update UI now that game is starting
        self.label_timer.config(text=f"Time: {self.time_limit}")
        self.button_start.destroy()
        self.label_question = tk.Label(
            self.game_root, text="Solve: ", font=(self.font, self.font_size)
        )
        self.label_question.pack(pady=5)
        # Load first problem into UI
        self.update_problem()
        self.entry_answer = tk.Entry(self.game_root, font=(self.font, self.font_size))
        self.entry_answer.pack(pady=5)
        self.entry_answer.bind("<Return>", self.check_answer)
        self.entry_answer.pack(pady=5)
        self.entry_answer.focus_set()
        # Start timer
        self.game_root.after(1000, self.check_timer)

    def update_problem(self):
        # Update the problem in the UI
        self.label_timer.config(
            text=f"Time: {(self.end_time - datetime.now()).seconds}"
        )
        self.problem_string, self.solution = self.generate_problem()
        self.label_question.config(text=f"Solve: {self.problem_string}")

    def generate_problem(self):
        # Generate a random quick math problem
        # Compound problems consist of multiple operations, which is not a feature that ZetaMac includes. So, this is a signfiicant upgrade we did, since it allows for substantially more challenging mental math (while each individual operation should still be simple enough to do in one's head). 
        # The base problems (consisting of just one operation) are designed to be approximately of similar difficulty in terms of mental math, so that they are all worth the same score. We do this by adjusting the upper bounds of the random numbers that are generated for each operation so that the difficulty is similar. Ex: Addition has a larger upper bound than multiplication, since multiplication is more difficult. Similarly, exponentiation has a smaller upper bound than multiplication, since exponentiation is more difficult.
        # TODO: We reward a higher score for compound problems, since they are more difficult.
        # For all the problems that involve subtraction, we want to ensure that the result is non-negative. So, we sometimes sort the numbers in descending order so smaller number gets subtracted from bigger number. Other times, we set the upper bound to be whatever the expression is that we are subtracting from.
        # For division, we want to ensure that the result is an integer, so we multiply two numbers together to get a bigger number that is for sure divisible by the second number. The logic behind ensuring that the result is an integer is tricky, so we do not include division when creating compound problems.
        # We also do not include exponentiation when creating compound problems because they are generally infeasible to solve using mental math. 
        problem_types = [
            "addition",
            "subtraction",
            "multiplication",
            "division",
            "exponentiation",
            "compound_add_then_multiply",
            "compound_multiply_then_add",
            "compound_add_then_subtract",
            "compound_subtract_then_add",
            "compound_subtract_then_multiply",
            "compound_multiply_then_subtract",
            "compound_add_then_add",
            "compound_multiply_then_multiply",
            "compound_add_then_add_then_add",
            "compound_multiply_then_multiply_then_multiply",
            "compound_add_then_subtract_then_multiply",
            "compound_subtract_then_add_then_multiply",
            "compound_add_then_add_then_subtract",
            "compound_subtract_then_add_then_add",
            "compound_subtract_then_multiply_then_add",
            "compound_multiply_then_subtract_then_add",
            "compound_multiply_then_multiply_then_subtract",
            "compound_multiply_then_subtract_then_multiply",
            "compound_subtract_then_multiply_then_multiply",
            "compound_subtract_then_multiply_then_subtract",
            "compound_add_then_multiply_then_add",
            "compound_add_then_multiply_then_subtract",
            "compound_add_then_subtract_then_multiply",
            "compound_add_then_subtract_then_add",
            "compound_multiply_then_add_then_multiply",
            "compound_multiply_then_add_then_add",
            "compound_multiply_then_subtract_then_multiply",
            "compound_multiply_then_subtract_then_add",
            "compound_subtract_then_add_then_multiply",
            "compound_subtract_then_add_then_subtract",
            "compound_subtract_then_multiply_then_add",
            "compound_subtract_then_multiply_then_subtract",
        ]
        lower_bound = 2
        upper_bound = 36
        problem_type = random.choice(problem_types)
        if problem_type == "addition":
            x, y = np.random.randint(low=lower_bound, high=upper_bound, size=2)
            solution = x + y
            problem_string = f"{x} + {y} = "
        elif problem_type == "subtraction":
            x, y = sorted(
                np.random.randint(low=lower_bound, high=upper_bound, size=2), reverse=True
            )  # Ensure non-negative result
            solution = x - y
            problem_string = f"{x} - {y} = "
        elif problem_type == "multiplication":
            x, y = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            solution = x * y
            problem_string = f"{x} x {y} = "
        elif problem_type == "division":
            x, y = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            x *= y  # Ensure integer result
            solution = x // y
            problem_string = f"{x} / {y} = "
        elif problem_type == "exponentiation":
            x = np.random.randint(2, 10, size=1)[0]
            if x >= 5:
                y = np.random.randint(2, 3, size=1)[0]
            else:
                y = np.random.randint(3, 5, size=1)[0]
            solution = x**y
            problem_string = f"{x} ^ {y} = "
        elif problem_type == "compound_add_then_multiply":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound, size=2)
            z = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = (x + y) * z
            problem_string = f"({x} + {y}) x {z} = "
        elif problem_type == "compound_multiply_then_add":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            z = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = (x * y) + z
            problem_string = f"({x} x {y}) + {z} = "
        elif problem_type == "compound_add_then_subtract":
            x, y, z  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=3), reverse = True)
            solution = (x + y) - z
            problem_string = f"({x} + {y}) - {z} = "
        elif problem_type == "compound_subtract_then_add":
            x, y, z  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=3), reverse = True)
            solution = (x - y) + z
            problem_string = f"({x} - {y}) + {z} = "
        elif problem_type == "compound_subtract_then_multiply":
            x, y  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=2), reverse = True)
            z = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = (x - y) * z
            problem_string = f"({x} - {y}) x {z} = "
        elif problem_type == "compound_multiply_then_subtract":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            z = np.random.randint(low=lower_bound, high=x * y, size=1)[0]
            solution = (x * y) - z
            problem_string = f"({x} x {y}) - {z} = "
        elif problem_type == "compound_add_then_add":
            x, y, z  = np.random.randint(low=lower_bound, high=upper_bound, size=3)
            solution = (x + y) + z
            problem_string = f"({x} + {y}) + {z} = "
        elif problem_type == "compound_multiply_then_multiply":
            x, y, z  = np.random.randint(low=lower_bound, high=upper_bound//3, size=3)
            solution = (x * y) * z
            problem_string = f"({x} x {y}) x {z} = "
        elif problem_type == "compound_add_then_add_then_add":
            x, y, z  = np.random.randint(low=lower_bound, high=upper_bound, size=3)
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = (x + y) + (z + w)
            problem_string = f"({x} + {y}) + ({z} + {w}) = "
        elif problem_type == "compound_multiply_then_multiply_then_multiply":
            x, y, z  = np.random.randint(low=lower_bound, high=upper_bound//3, size=3)
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = (x * y) * (z * w)
            problem_string = f"({x} x {y}) x ({z} x {w}) = "
        elif problem_type == "compound_add_then_subtract_then_multiply":
            x, y, z  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=3), reverse = True)
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = ((x + y) - z) * w
            problem_string = f"(({x} + {y}) - {z}) x {w} = "
        elif problem_type == "compound_subtract_then_add_then_multiply":
            x, y, z  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=3), reverse = True)
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = ((x - y) + z) * w
            problem_string = f"(({x} - {y}) + {z}) x {w} = "
        elif problem_type == "compound_add_then_add_then_subtract":
            x, y, z  = np.random.randint(low=lower_bound, high=upper_bound, size=3)
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = (x + y) + (z - w)
            problem_string = f"({x} + {y}) + ({z} - {w}) = "
        elif problem_type == "compound_subtract_then_add_then_add":
            x, y, z  = np.random.randint(low=lower_bound, high=upper_bound, size=3)
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = (x - y) + (z + w)
            problem_string = f"({x} - {y}) + ({z} + {w}) = "
        elif problem_type == "compound_subtract_then_multiply_then_add":
            x, y  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=2), reverse = True)
            z = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x - y) * z) + w
            problem_string = f"(({x} - {y}) x {z}) + {w} = "
        elif problem_type == "compound_multiply_then_subtract_then_add":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            z = np.random.randint(low=lower_bound, high=x * y, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x * y) - z) + w
            problem_string = f"(({x} x {y}) - {z}) + {w} = "
        elif problem_type == "compound_multiply_then_multiply_then_subtract":
            x, y, z  = np.random.randint(low=lower_bound, high=upper_bound//3, size=3)
            w = np.random.randint(low=lower_bound, high=(x * y) * z, size=1)[0]
            solution = ((x * y) * z) - w
            problem_string = f"(({x} x {y}) x {z}) - {w} = "
        elif problem_type == "compound_multiply_then_subtract_then_multiply":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            z = np.random.randint(low=lower_bound, high=x * y, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = ((x * y) - z) * w
            problem_string = f"(({x} x {y}) - {z}) x {w} = "
        elif problem_type == "compound_subtract_then_multiply_then_multiply":
            x, y  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=2), reverse = True)
            z = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = ((x - y) * z) * w
            problem_string = f"(({x} - {y}) x {z}) x {w} = "
        elif problem_type == "compound_subtract_then_multiply_then_subtract":
            x, y  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=2), reverse = True)
            z = np.random.randint(low=lower_bound, high=x - y, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = ((x - y) * z) - w
            problem_string = f"(({x} - {y}) x {z}) - {w} = "
        elif problem_type == "compound_add_then_multiply_then_add":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound, size=2)
            z = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x + y) * z) + w
            problem_string = f"(({x} + {y}) x {z}) + {w} = "
        elif problem_type == "compound_add_then_multiply_then_subtract":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound, size=2)
            z = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x + y) * z) - w
            problem_string = f"(({x} + {y}) x {z}) - {w} = "
        elif problem_type == "compound_add_then_subtract_then_multiply":
            x, y, z  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=3), reverse = True)
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = ((x + y) - z) * w
            problem_string = f"(({x} + {y}) - {z}) x {w} = "
        elif problem_type == "compound_add_then_subtract_then_add":
            x, y, z  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=3), reverse = True)
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x + y) - z) + w
            problem_string = f"(({x} + {y}) - {z}) + {w} = "
        elif problem_type == "compound_multiply_then_add_then_multiply":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            z = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = ((x * y) + z) * w
            problem_string = f"(({x} x {y}) + {z}) x {w} = "
        elif problem_type == "compound_multiply_then_add_then_add":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            z = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x * y) + z) + w
            problem_string = f"(({x} x {y}) + {z}) + {w} = "
        elif problem_type == "compound_multiply_then_subtract_then_multiply":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            z = np.random.randint(low=lower_bound, high=x * y, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = ((x * y) - z) * w
            problem_string = f"(({x} x {y}) - {z}) x {w} = "
        elif problem_type == "compound_multiply_then_subtract_then_add":
            x, y  = np.random.randint(low=lower_bound, high=upper_bound//3, size=2)
            z = np.random.randint(low=lower_bound, high=x * y, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x * y) - z) + w
            problem_string = f"(({x} x {y}) - {z}) + {w} = "
        elif problem_type == "compound_subtract_then_add_then_multiply":
            x, y, z  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=3), reverse = True)
            w = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            solution = ((x - y) + z) * w
            problem_string = f"(({x} - {y}) + {z}) x {w} = "
        elif problem_type == "compound_subtract_then_add_then_subtract":
            x, y, z  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=3), reverse = True)
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x - y) + z) - w
            problem_string = f"(({x} - {y}) + {z}) - {w} = "
        elif problem_type == "compound_subtract_then_multiply_then_add":
            x, y  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=2), reverse = True)
            z = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x - y) * z) + w
            problem_string = f"(({x} - {y}) x {z}) + {w} = "
        elif problem_type == "compound_subtract_then_multiply_then_subtract":
            x, y  = sorted(np.random.randint(low=lower_bound, high=upper_bound, size=2), reverse = True)
            z = np.random.randint(low=lower_bound, high=upper_bound//3, size=1)[0]
            w = np.random.randint(low=lower_bound, high=upper_bound, size=1)[0]
            solution = ((x - y) * z) - w
            problem_string = f"(({x} - {y}) x {z}) - {w} = "
        else:
            raise ValueError(f"Invalid problem type: {problem_type}")

        return problem_string, solution

    def check_answer(self, event=None):
        # Check user's answer, then update score and question
        self.label_timer.config(
            text=f"Time: {(self.end_time - datetime.now()).seconds}"
        )
        user_solution = self.entry_answer.get()
        if user_solution == str(self.solution):
            self.score += 1
            self.label_score.config(text=f"Score: {self.score}")
        self.update_problem()
        self.entry_answer.delete(0, tk.END)

    def check_timer(self):
        # Check if time is up every second: if so, end game then show and save results, otherwise keep checking
        if datetime.now() < self.end_time:
            self.game_root.after(1000, self.check_timer)
        else:
            self.label_question.config(text="Game Over!")
            self.entry_answer.destroy()
            self.label_timer.config(text="Time's up!")
            self.label_score.config(text=f"Final score: {self.score}")

            self.save_score()

    def save_score(self):
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Check if username exists already in scores folder to load previous scores, if not, create new file to track scores
        score_file = f"{scores_folder}/{self.username}.csv"
        try:
            scores = pd.read_csv(score_file)
        except FileNotFoundError:
            scores = pd.DataFrame(columns=["Username", "DateTime", "Score"])

        # Append new score data and save updated scores to CSV
        new_score = {
            "Username": self.username,
            "DateTime": current_timestamp,
            "Score": self.score,
        }
        scores = pd.concat(
            [scores, pd.DataFrame(new_score, index=[0])], ignore_index=True
        )
        scores.to_csv(score_file, index=False)

        self.display_scores(scores)

    def display_scores(self, scores):
        # For this user, display their 5 most recent scores, if available, and their top 5 scores of all time, if available in the UI
        self.label_recent_scores = tk.Label(
            self.game_root, text="Recent Scores:", font=(self.font, self.font_size)
        )
        self.label_recent_scores.pack(pady=5)
        # Get most recent scores from user's Dataframe and display them as rows in blue in the UI
        recent_scores = (
            scores[scores["Username"] == self.username]
            .sort_values(by="DateTime", ascending=False)
            .head(5)
        )
        recent_scores_str = "\n".join(
            [
                f"{row['DateTime']}: {row['Score']}"
                for _, row in recent_scores.iterrows()
            ]
        )
        self.label_recent_scores_values = tk.Label(
            self.game_root,
            text=recent_scores_str,
            font=(self.font, self.font_size),
            fg="blue",
        )
        self.label_recent_scores_values.pack(pady=5)

        self.label_top_scores = tk.Label(
            self.game_root, text="Top Scores:", font=(self.font, self.font_size)
        )
        self.label_top_scores.pack(pady=5)
        # Get highest scores from user's Dataframe and display them as rows in blue in the UI
        top_scores = (
            scores[scores["Username"] == self.username]
            .sort_values(by="Score", ascending=False)
            .head(5)
        )
        top_scores_str = "\n".join(
            [f"{row['DateTime']}: {row['Score']}" for _, row in top_scores.iterrows()]
        )
        self.label_top_scores_values = tk.Label(
            self.game_root,
            text=top_scores_str,
            font=(self.font, self.font_size),
            fg="green",
        )
        self.label_top_scores_values.pack(pady=5)


def launch_game():
    root = tk.Tk()
    root.withdraw()  # This hides the root window, which is kind of ugly - we use simpledialog instead
    username = simpledialog.askstring(
        title="UltraMac", prompt="Enter your desired username:", parent=root
    )
    if username:
        root.destroy()  # Destroy username window because no longer used
        game_root = tk.Tk()  # Create a new root for the main game window
        app = UltraMac(username=username, game_root=game_root)
        app.game_root.mainloop()  # Keep running the game until user closes the main game window
    else:
        print("You must provide a username. No username provided, so exiting.")


if __name__ == "__main__":
    launch_game()
