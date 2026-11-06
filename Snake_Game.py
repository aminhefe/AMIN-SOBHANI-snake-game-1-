
import tkinter as tk
import numpy as np

from SnakeAgent import SnakeAgent


class SnakeGame:

    def __init__(self):

        self.width = 20
        self.height = 20
        self.cell_size = 25

        self.window_width = self.width * self.cell_size
        self.window_height = self.height * self.cell_size

        self.snake = [
            (5, 10),
            (4, 10),
            (3, 10)
        ]

        self.score = 0
        self.game_over = False
        self.won = False

        self.agent = SnakeAgent()

        self.apple = None

        # ساخت پنجره
        self.root = tk.Tk()
        self.root.title("Snake AI Agent")
        self.root.resizable(False, False)
        self.root.configure(bg="#17202A")

        # عنوان بازی
        self.title_label = tk.Label(
            self.root,
            text="SNAKE AI AGENT",
            font=("Arial", 20, "bold"),
            bg="#17202A",
            fg="white"
        )
        self.title_label.pack(pady=10)

        # امتیاز
        self.score_label = tk.Label(
            self.root,
            text="Score: 0",
            font=("Arial", 14, "bold"),
            bg="#17202A",
            fg="#F1C40F"
        )
        self.score_label.pack(pady=5)

        # صفحه بازی
        self.canvas = tk.Canvas(
            self.root,
            width=self.window_width,
            height=self.window_height,
            bg="#1C2833",
            highlightthickness=0
        )
        self.canvas.pack(padx=15, pady=10)

        # پیام پایان بازی
        self.message_label = tk.Label(
            self.root,
            text="AI is playing...",
            font=("Arial", 12),
            bg="#17202A",
            fg="#58D68D"
        )
        self.message_label.pack(pady=10)

        self.spawn_apple()

        self.draw_game()

        # شروع بازی
        self.root.after(200, self.update)

        self.root.mainloop()

    def spawn_apple(self):

        empty_cells = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in self.snake
        ]

        if not empty_cells:
            self.apple = None
            self.game_over = True
            self.won = True
            return

        index = np.random.randint(len(empty_cells))

        self.apple = empty_cells[index]

    def draw_game(self):

        self.canvas.delete("all")

        # رسم خطوط شبکه
        for x in range(self.width + 1):

            self.canvas.create_line(
                x * self.cell_size,
                0,
                x * self.cell_size,
                self.window_height,
                fill="#283747"
            )

        for y in range(self.height + 1):

            self.canvas.create_line(
                0,
                y * self.cell_size,
                self.window_width,
                y * self.cell_size,
                fill="#283747"
            )

        # رسم مار
        for i, (x, y) in enumerate(self.snake):

            padding = 2

            color = "#2ECC71" if i == 0 else "#82E0AA"

            self.canvas.create_rectangle(
                x * self.cell_size + padding,
                y * self.cell_size + padding,
                (x + 1) * self.cell_size - padding,
                (y + 1) * self.cell_size - padding,
                fill=color,
                outline=""
            )

        # رسم سیب
        if self.apple is not None:

            x, y = self.apple

            padding = 4

            self.canvas.create_oval(
                x * self.cell_size + padding,
                y * self.cell_size + padding,
                (x + 1) * self.cell_size - padding,
                (y + 1) * self.cell_size - padding,
                fill="#E74C3C",
                outline=""
            )

    def update(self):

        if self.game_over:
            return

        # دریافت حرکت از Agent
        action = self.agent.get_action(
            self.snake,
            self.apple,
            self.width,
            self.height
        )

        if action is None:

            self.game_over = True
            self.message_label.config(
                text="GAME OVER!",
                fg="#E74C3C"
            )
            return

        head_x, head_y = self.snake[0]

        dx, dy = action

        new_head = (
            head_x + dx,
            head_y + dy
        )

        eating = new_head == self.apple

        if eating:

            self.snake.insert(0, new_head)

            self.score += 1

            self.score_label.config(
                text=f"Score: {self.score}"
            )

            self.spawn_apple()

        else:

            self.snake.insert(0, new_head)
            self.snake.pop()

        self.draw_game()

        if self.game_over and self.won:

            self.message_label.config(
                text="YOU WIN!",
                fg="#F1C40F"
            )

            return

        # اجرای حرکت بعدی
        self.root.after(150, self.update)


if __name__ == "__main__":

    game = SnakeGame()
