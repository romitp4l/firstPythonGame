import tkinter as tk
import random
import pygame

class TargetGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Target Game")
        
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()
        
        self.score = 0
        self.high_score = self.load_high_score()
        
        self.score_label = tk.Label(root, text="Score: 0")
        self.score_label.pack()
        
        self.high_score_label = tk.Label(root, text=f"High Score: {self.high_score}")
        self.high_score_label.pack()
        
        self.timer_label = tk.Label(root, text="Timer: ")
        self.timer_label.pack()
        
        self.target_radius = 20
        self.target = self.canvas.create_oval(0, 0, self.target_radius * 2, self.target_radius * 2, fill="red")
        
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.move_target()
        
        self.timer = 10
        self.update_timer()
        
        pygame.mixer.init()
        self.hit_sound = pygame.mixer.Sound("hit.wav")
        
        self.countdown_target()
    
    def move_target(self):
        x = random.randint(self.target_radius, 400 - self.target_radius * 2)
        y = random.randint(self.target_radius, 400 - self.target_radius * 2)
        self.canvas.coords(self.target, x, y, x + self.target_radius * 2, y + self.target_radius * 2)
        
    def on_click(self, event):
        target_coords = self.canvas.coords(self.target)
        target_x = (target_coords[0] + target_coords[2]) / 2
        target_y = (target_coords[1] + target_coords[3]) / 2
        
        click_distance = ((target_x - event.x) ** 2 + (target_y - event.y) ** 2) ** 0.5
        
        if click_distance < self.target_radius:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            
            # Play sound effect
            self.hit_sound.play()
            
        self.move_target()
        
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score(self.high_score)
            self.high_score_label.config(text=f"High Score: {self.high_score}")
        
    def countdown_target(self):
        if self.timer <= 0:
            self.game_over()
            return
        
        self.timer -= 1
        self.update_timer()
        
        self.move_target()
        self.root.after(1000, self.countdown_target)
    
    def update_timer(self):
        self.timer_label.config(text=f"Timer: {self.timer}")
        
    def game_over(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.delete("all")
        
        game_over_label = tk.Label(self.root, text="Game Over!", font=("Arial", 24))
        game_over_label.pack()
        
        final_score_label = tk.Label(self.root, text=f"Final Score: {self.score}", font=("Arial", 18))
        final_score_label.pack()
        
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                high_score = int(file.read())
                return high_score
        except (FileNotFoundError, ValueError):
            return 0
        
    def save_high_score(self, high_score):
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))

root = tk.Tk()
game = TargetGame(root)
root.mainloop()


