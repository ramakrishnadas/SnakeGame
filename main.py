import arcade

# ---- Constants ----
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Snake Game"
SNAKE_SIZE = 20
MOVEMENT_SPEED = SNAKE_SIZE

IMAGE_PATHS = {
    "head_up": "graphics/head_up.png",
    "head_down": "graphics/head_down.png",
    "head_left": "graphics/head_left.png",
    "head_right": "graphics/head_right.png",
    "tail_up": "graphics/tail_up.png",
    "tail_down": "graphics/tail_down.png",
    "tail_left": "graphics/tail_left.png",
    "tail_right": "graphics/tail_right.png",
    "body_horizontal": "graphics/body_horizontal.png",
    "body_vertical": "graphics/body_vertical.png",
    "body_topright": "graphics/body_topright.png",
    "body_topleft": "graphics/body_topleft.png",
    "body_bottomright": "graphics/body_bottomright.png",
    "body_bottomleft": "graphics/body_bottomleft.png"
}

class gameWindow(arcade.Window):
    def __init__(self):
        # TRY
        # vsync=True !!!!!
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True, update_rate=0.1)
        arcade.set_background_color(arcade.csscolor.BLACK)

    def setup(self):
        self.snake = Snake()

    def on_draw(self):
        arcade.start_render()
        for segment in self.snake.segments:
            segment.draw()
    
    def on_update(self, delta_time):
        self.snake.move()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.snake.change_direction("UP")
        elif key == arcade.key.DOWN:
            self.snake.change_direction("DOWN")
        elif key == arcade.key.LEFT:
            self.snake.change_direction("LEFT")
        elif key == arcade.key.RIGHT:
            self.snake.change_direction("RIGHT")
        
    
class Snake(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.segments = []
        self.direction = "UP"
        self.create_initial_snake()

    def create_initial_snake(self):
        self.snake_length = 5
        # Create a snake with a few initial segments
        for i in range(self.snake_length):
            x = SCREEN_WIDTH // 2
            y = SCREEN_HEIGHT // 2 - i * SNAKE_SIZE

            if i == 0:
                segment = arcade.Sprite(IMAGE_PATHS["head_up"], scale=0.5)
            elif i == self.snake_length - 1:
                segment = arcade.Sprite(IMAGE_PATHS["tail_down"], scale=0.5)
            else:
                segment = arcade.Sprite(IMAGE_PATHS["body_vertical"], scale=0.5)

            segment.center_x = x
            segment.center_y = y
            self.segments.append(segment)

    def move(self):
        # Move each segment of the snake
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].center_x = self.segments[i - 1].center_x
            self.segments[i].center_y = self.segments[i - 1].center_y

        # Move head based on direction
        head = self.segments[0]
        if self.direction == "UP":
            head.center_y += MOVEMENT_SPEED
        elif self.direction == "DOWN":
            head.center_y -= MOVEMENT_SPEED
        elif self.direction == "LEFT":
            head.center_x -= MOVEMENT_SPEED
        elif self.direction == "RIGHT":
            head.center_x += MOVEMENT_SPEED

        # Screen wrapping: Check if the snake goes off the edges of the window
        if head.center_x > SCREEN_WIDTH:  # If the snake moves off the right side
            head.center_x = 0  # Wrap to the left side
        elif head.center_x < 0:  # If the snake moves off the left side
            head.center_x = SCREEN_WIDTH  # Wrap to the right side

        if head.center_y > SCREEN_HEIGHT:  # If the snake moves off the top side
            head.center_y = 0  # Wrap to the bottom
        elif head.center_y < 0:  # If the snake moves off the bottom side
            head.center_y = SCREEN_HEIGHT  # Wrap to the top

        # Update segment images
        self.update_segment_images()

    def update_segment_images(self):
        # Update head
        head = self.segments[0]
        head.texture = arcade.load_texture(IMAGE_PATHS[f"head_{self.direction.lower()}"])

        # Update tail
        tail = self.segments[-1]
        tail_direction = self.get_tail_direction()
        tail.texture = arcade.load_texture(IMAGE_PATHS[f"tail_{tail_direction.lower()}"])

        # Update body segments
        for i in range(1, len(self.segments) - 1):
            prev_segment = self.segments[i -1]
            current_segment = self.segments[i]
            next_segment = self.segments[i + 1]

            segment_type = self.get_body_segment_type(prev_segment, current_segment, next_segment)
            current_segment.texture = arcade.load_texture(IMAGE_PATHS[segment_type])

    def get_tail_direction(self):
        # Get direction based on last two segments
        tail = self.segments[-1]
        prev = self.segments[-2]
        if tail.center_y > prev.center_y:
            return "up"
        elif tail.center_y < prev.center_y:
            return "down"
        elif tail.center_x > prev.center_x:
            return "right"
        else:
            return "left"

    def get_body_segment_type(self, prev_segment, current_segment, next_segment):
        # Determine if segment is horizontal, vertical or turning
        if prev_segment.center_y == next_segment.center_y:
            return "body_horizontal"
        elif prev_segment.center_x == next_segment.center_x:
            return "body_vertical"
        else:
            # Turning conditions
            if prev_segment.center_y < current_segment.center_y and current_segment.center_x < next_segment.center_x or prev_segment.center_x > current_segment.center_x and current_segment.center_y > next_segment.center_y:
                return "body_bottomright"  # Turning left-down or up-right
            elif prev_segment.center_y < current_segment.center_y and current_segment.center_x > next_segment.center_x or prev_segment.center_x < current_segment.center_x and current_segment.center_y > next_segment.center_y:
                return "body_bottomleft"  # Turning right-down or up-left
            elif prev_segment.center_y > current_segment.center_y and current_segment.center_x > next_segment.center_x or prev_segment.center_x < current_segment.center_x and current_segment.center_y < next_segment.center_y:
                return "body_topleft"  # Turning right-up or down-left
            elif prev_segment.center_x > current_segment.center_x and current_segment.center_y < next_segment.center_y or prev_segment.center_y > current_segment.center_y and current_segment.center_x < next_segment.center_x:
                return "body_topright"  # Turning down-right or left-up
            return "body_horizontal"  # Default if no turn is detected
        
    def change_direction(self, new_direction):
        opposite_directions = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction


def main():
    window = gameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()