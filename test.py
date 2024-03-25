import tkinter as tk
from threading import Thread
from subprocess import Popen

class PacmanUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pacman Game")
        self.root.geometry("300x150")

        self.label = tk.Label(root, text="Welcome to Pacman!", font=("Arial", 14))
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game, font=("Arial", 12))
        self.start_button.pack(pady=10)

    def start_game(self):
        # Update UI to indicate the game is in progress
        self.label.config(text="Game in Progress...")
        self.start_button.config(state="disabled")

        # Start the game in a separate thread to keep UI responsive
        game_thread = Thread(target=self.run_pacman_game, daemon=True)
        game_thread.start()

        # Instead of checking the thread, directly wait for the process to finish in the thread
        # The UI will be updated once the game process finishes

    def run_pacman_game(self):
        # Command to run the pacman game
        command = ['python3', 'pacman.py', '-l', 'test']
        # Start the game process and wait for it to complete
        process = Popen(command)
        process.wait()

        # Once the game is over, update the UI in the main thread
        self.update_ui_after_game()

    def update_ui_after_game(self):
        # Ensure UI updates happen in the main thread
        self.label.config(text="Welcome to Pacman!")
        self.start_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = PacmanUI(root)
    root.mainloop()
