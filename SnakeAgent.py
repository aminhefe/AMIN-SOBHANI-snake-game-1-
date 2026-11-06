
import numpy as np


class SnakeAgent:

    def __init__(self):
        self.actions = [
            (0, -1),  # بالا
            (0, 1),   # پایین
            (-1, 0),  # چپ
            (1, 0)    # راست
        ]

    def euclidean_distance(self, p1, p2):
        return np.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    def get_action(self, snake, apple, width, height):

        head = snake[0]
        candidates = []

        for action in self.actions:

            dx, dy = action

            new_head = (
                head[0] + dx,
                head[1] + dy
            )

            if not (
                0 <= new_head[0] < width and
                0 <= new_head[1] < height
            ):
                continue

            eating = new_head == apple

            occupied = snake if eating else snake[:-1]

            if new_head in occupied:
                continue

            distance = self.euclidean_distance(
                new_head,
                apple
            )

            candidates.append((distance, action))

        if not candidates:
            return None

        candidates.sort(key=lambda x: x[0])

        return candidates[0][1]
