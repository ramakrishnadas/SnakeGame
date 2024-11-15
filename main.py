import arcade
import random
import arcade.color

# ---- Constants ----
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Snake Game"
SNAKE_SIZE = 20
MOVEMENT_SPEED = SNAKE_SIZE

# ---- Paths to images for snake graphics and food ----
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
    "body_bottomleft": "graphics/body_bottomleft.png",
    "apple": "graphics/apple.png"
}

# ---- Game window class ----
class gameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True, update_rate=0.3, vsync=True)

        # Set the background color of the game window
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Load the sound effects that will be used in the game
        self.eat_sound = arcade.load_sound("sound_effects/eat.wav")
        self.game_over_sound = arcade.load_sound("sound_effects/game_over.mp3")

    def setup(self):
        # Create instance of Snake and Food classes
        self.snake = Snake()
        self.food = Food()

        # Create game attributes
        self.game_over = False
        self.score = 0
        self.final_score = 0
        self.game_speed = 0.3
        self.speed_updated = False
        self.button_width = 100
        self.button_height = 40
        self.restart_button_x = SCREEN_WIDTH // 2 - 60
        self.quit_button_x = SCREEN_WIDTH // 2 + 60
        self.button_y = SCREEN_HEIGHT // 2 - 50

        # Spawn food for the first time
        self.food.spawn_food(self.snake.segments)

    def on_draw(self):
        arcade.start_render()

        if not self.game_over:
            # If the game is not over, draw the snake, the food, and the score
            for segment in self.snake.segments:
                segment.draw()
            self.food.apple.draw()

            score_text = f"{self.score}"
            text = arcade.Text(score_text, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 35, arcade.color.WHITE, 20, anchor_x="right")
            text.draw()
        else:
            # When the game is over, display "Game Over" and the final score
            arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, arcade.color.RED, 24, anchor_x="center")
            score_text = f"Final Score: {self.final_score}"
            arcade.draw_text(score_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20, arcade.color.WHITE, 16, anchor_x="center")
            
            # Draw Restart and Quit buttons
            arcade.draw_rectangle_filled(self.restart_button_x, self.button_y, self.button_width, self.button_height, arcade.color.GREEN)
            arcade.draw_rectangle_filled(self.quit_button_x, self.button_y, self.button_width, self.button_height, arcade.color.RED)
            
            # Draw button text
            arcade.draw_text("Restart", self.restart_button_x, self.button_y, arcade.color.WHITE, 14, anchor_x="center", anchor_y="center")
            arcade.draw_text("Quit", self.quit_button_x, self.button_y, arcade.color.WHITE, 14, anchor_x="center", anchor_y="center")
    
    def on_update(self, delta_time):
        # Increase the game speed every time the score reaches a multiple of 200 (max game speed: 0.06)
        if self.score % 200 == 0 and self.score > 0 and not self.speed_updated:
            if self.game_speed > 0.06:
                self.game_speed -= 0.02

            self.set_update_rate(self.game_speed)
            self.speed_updated = True

        # Reset the speed_updated flag to ensure the game speed is updated only once
        if self.score % 200 != 0:
            self.speed_updated = False

        # Every frame, move the snake and check for collision with food and with itself
        self.snake.move()
        self.check_collision_with_food()
        self.check_collision_with_self()

    def check_collision_with_food(self):
        # Check if the snake's head collides with food
        if arcade.check_for_collision(self.snake.segments[0], self.food.apple):
            # Play eating sound effect
            arcade.play_sound(self.eat_sound)

            # Update the score, grow the snake, and reset the food's position
            self.score += 100
            self.snake.grow()
            self.food.spawn_food(self.snake.segments)
              
    def check_collision_with_self(self):
        # Check if the snake's head collides with its body
        head = self.snake.segments[0]
        for segment in self.snake.segments[1:]:
            if arcade.check_for_collision(head, segment):
                # Play game over sound effect
                arcade.play_sound(self.game_over_sound)

                # Set game over flag to true for Game Over logic to execute, and store final score to display
                self.game_over = True
                self.final_score = self.score
                break

    def on_key_press(self, key, modifiers):
        # Enable user to change the snake's direction using the keyboard (up, down, left, and right arrows)
        if key == arcade.key.UP:
            self.snake.change_direction("UP")
        elif key == arcade.key.DOWN:
            self.snake.change_direction("DOWN")
        elif key == arcade.key.LEFT:
            self.snake.change_direction("LEFT")
        elif key == arcade.key.RIGHT:
            self.snake.change_direction("RIGHT")
                
    def on_mouse_press(self, x, y, button, modifiers):
        # Enable user to click on the Restart and Quit buttons
        if self.game_over:
            # Check if the Restart button was clicked
            if (self.restart_button_x - self.button_width / 2 < x < self.restart_button_x + self.button_width / 2 and
                self.button_y - self.button_height / 2 < y < self.button_y + self.button_height / 2):
                self.restart_game()
            
            # Check if the Quit button was clicked
            elif (self.quit_button_x - self.button_width / 2 < x < self.quit_button_x + self.button_width / 2 and
                self.button_y - self.button_height / 2 < y < self.button_y + self.button_height / 2):
                arcade.close_window()

    def restart_game(self):
        # Reset game logic, game score, and game speed so that the user can start playing again
        self.game_over = False
        self.score = 0
        self.game_speed = 0.3
        self.set_update_rate(self.game_speed)
        self.snake.reset()
        self.food.spawn_food(self.snake.segments)

# ---- Snake Sprite class ----
class Snake(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Declare Snake's attributes and create the initial snake
        self.segments = []
        self.direction = "UP"
        self.create_initial_snake()

    def create_initial_snake(self):
        # Create a snake with a few initial segments using images for the snake's head, tail, and body
        self.snake_length = 5
        
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

        # Move the snake's head based on direction
        head = self.segments[0]
        if self.direction == "UP":
            head.center_y += MOVEMENT_SPEED
        elif self.direction == "DOWN":
            head.center_y -= MOVEMENT_SPEED
        elif self.direction == "LEFT":
            head.center_x -= MOVEMENT_SPEED
        elif self.direction == "RIGHT":
            head.center_x += MOVEMENT_SPEED

        # Check if the snake goes off the edges of the window, and make it wrap to the opposite side (e. g. from left to right and top to bottom, and vice versa )
        if head.center_x > SCREEN_WIDTH:
            head.center_x = 0
        elif head.center_x < 0:
            head.center_x = SCREEN_WIDTH 

        if head.center_y > SCREEN_HEIGHT:
            head.center_y = 0
        elif head.center_y < 0:
            head.center_y = SCREEN_HEIGHT

        # Update segment images
        self.update_segment_images()

    def update_segment_images(self):
        # Update head image
        head = self.segments[0]
        head.texture = arcade.load_texture(IMAGE_PATHS[f"head_{self.direction.lower()}"])

        # Update tail image
        tail = self.segments[-1]
        tail_direction = self.get_tail_direction()
        tail.texture = arcade.load_texture(IMAGE_PATHS[f"tail_{tail_direction.lower()}"])

        # Update body images
        for i in range(1, len(self.segments) - 1):
            prev_segment = self.segments[i -1]
            current_segment = self.segments[i]
            next_segment = self.segments[i + 1]

            segment_type = self.get_body_segment_type(prev_segment, current_segment, next_segment)
            current_segment.texture = arcade.load_texture(IMAGE_PATHS[segment_type])

    def get_tail_direction(self):
        # Get tail's direction based on the last two segments
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
        # Determine if snake segment is horizontal, vertical or turning
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
        # Change the snake's direction attribute
        # Prevent snake from reversing its direction directly
        opposite_directions = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def grow(self):
        # Get the current tail segment and the one before it
        tail = self.segments[-1]
        prev_segment = self.segments[-2]

        # Determine where to place the new segment based on the direction of the tail
        if tail.center_x == prev_segment.center_x:
            # Tail is vertical
            new_segment = arcade.Sprite(IMAGE_PATHS["body_vertical"], scale=0.5)
        else:
            # Tail is horizontal
            new_segment = arcade.Sprite(IMAGE_PATHS["body_horizontal"], scale=0.5)

        # Insert the new segment before the tail
        self.segments.insert(-1, new_segment)

    def reset(self):
        # Reset the snake's attributes
        self.segments.clear()
        self.create_initial_snake()
        self.direction = "UP"

# ---- Food Sprite class ----
class Food(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # Create Sprite for the food (apple)
        self.apple = arcade.Sprite(IMAGE_PATHS["apple"], scale=0.5)

        # Set random food coordinates
        self.apple.center_x = random.randint(0, SCREEN_WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE
        self.apple.center_y = random.randint(0, SCREEN_HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE

    def spawn_food(self, snake_segments):
        # Ensure food does not spawn on top of the snake
        while True:
            self.apple.center_x = random.randint(0, SCREEN_WIDTH)
            self.apple.center_y = random.randint(0, SCREEN_HEIGHT)
            if not self.check_collision_with_snake(snake_segments):
                break

    def check_collision_with_snake(self, snake_segments):
        # Check if the food is colliding with any of the snake segments
        for segment in snake_segments:
            if segment.collides_with_sprite(self.apple):
                return True  # Food collides with the snake
        return False  # Food does not collide with the snake

# ---- Main program ----
def main():
    window = gameWindow()
    window.setup()

    # Start arcade game
    arcade.run()

if __name__ == "__main__":
    main()