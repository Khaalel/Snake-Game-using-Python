#Importing the needed libraries
import pygame,sys,random
from pygame.math import Vector2

#Implementing the Snake
class SNAKE:
	def __init__(self):
		#Will be using the vector cause it's easier to do opertation on it for further on when moving the snake *it will start with 3 blocks*
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]         	
		self.direction = Vector2(0,0)
		self.new_block = False

		#Visuals for head of the snake for every possible position
		self.head_up = pygame.image.load('Visuals/head_up.png').convert_alpha()
		self.head_down = pygame.image.load('Visuals/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('Visuals/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('Visuals/head_left.png').convert_alpha()
		
		#Visuals for tail of the snake for every possible position
		self.tail_up = pygame.image.load('Visuals/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('Visuals/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('Visuals/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('Visuals/tail_left.png').convert_alpha()

		#Visuals for body of the snake for straight positions
		self.body_vertical = pygame.image.load('Visuals/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('Visuals/body_horizontal.png').convert_alpha()
		
		#Visuals for head of the snake for curves 
		self.body_tr = pygame.image.load('Visuals/body_tr.png').convert_alpha()
		self.body_tl = pygame.image.load('Visuals/body_tl.png').convert_alpha()
		self.body_br = pygame.image.load('Visuals/body_br.png').convert_alpha()
		self.body_bl = pygame.image.load('Visuals/body_bl.png').convert_alpha()
		#Sound of crunch every time the snake eat an apple
		self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

	#Method for drwaing the snake
	def draw_snake(self):

		#updating the head/tail of the snake graphics based on its direction 
		self.update_head_graphics()
		self.update_tail_graphics()

		#Using enumerates here cause it'll be giving us index of where we are standing in the list which is basically the snake body
		for index,block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			#Index 0 indicating the snake head then printing it using screen.blit based on its direction obtained from update_head_graphics()
			if index == 0:
				screen.blit(self.head,block_rect)
			#Index length - 1 indicating the snake tail then printing it using screen.blit based on its direction obtained from update_tail_graphics()
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				#Index other than the above ones are the body of the snake, assigning visusals to them
    			#The snake is going straight then the 2 indices following each other must have the same value
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				#Going horizontal 
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				#Going vertical
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					#Handling the curves where the index of the block will be as follows 
    				#tl->top left where x=-1 and y=-1 then the snake is going right then up or the other way wher it's going down then left
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
    				#bl->bottom left where x=-1 and y=1 then the snake is going right then down or the other way wher it's going up then left
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
    				#tr->top left where x=1 and y=-1 then the snake is going left then up or the other way wher it's going down then right
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
    				#br->bottom right where x=1 and y=1 then the snake is going left then down or the other way wher it's going up then right
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)

	#Updating the value of the head based on the vector of the direction
	def update_head_graphics(self):
		#getting the dircetion of the head based on the first two indices
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down

	#Updating the value of the tail based on the vector of the direction
	def update_tail_graphics(self):
     	#getting the dircetion of the tail based on the last two indices
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down


	def move_snake(self):
		if self.new_block == True:
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]

	def add_block(self):
		self.new_block = True
  
	def play_crunch_sound(self):
		self.crunch_sound.play()

	def reset(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)


class FRUIT:
	def __init__(self):
		self.randomize()

	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		screen.blit(apple,fruit_rect)

	def randomize(self):
		self.x = random.randint(0,cell_number - 1)
		self.y = random.randint(0,cell_number - 1)
		self.pos = Vector2(self.x,self.y)

class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()

	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()

	def draw_elements(self):
		self.draw_grass()
		self.fruit.draw_fruit()
		self.snake.draw_snake()
		self.draw_score()

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()
			self.snake.add_block()
			self.snake.play_crunch_sound()

		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()

	def check_fail(self):
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()
		
	def game_over(self):
		self.snake.reset()

	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			

	def draw_score(self):
		score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text,True,(56,74,12))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

		pygame.draw.rect(screen,(167,209,61),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(apple,apple_rect)
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Visuals/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE:
			main_game.update()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if main_game.snake.direction.y != 1:
					main_game.snake.direction = Vector2(0,-1)
			if event.key == pygame.K_RIGHT:
				if main_game.snake.direction.x != -1:
					main_game.snake.direction = Vector2(1,0)
			if event.key == pygame.K_DOWN:
				if main_game.snake.direction.y != -1:
					main_game.snake.direction = Vector2(0,1)
			if event.key == pygame.K_LEFT:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = Vector2(-1,0)

	screen.fill((175,215,70))
	main_game.draw_elements()
	pygame.display.update()
	clock.tick(60)