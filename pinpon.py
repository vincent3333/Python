# Implementation of classic arcade game Pong
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH,HEIGHT = 600, 400      
BALL_RADIUS = 20
PAD_WIDTH, PAD_HEIGHT = 8, 80
HALF_PAD_WIDTH, HALF_PAD_HEIGHT = PAD_WIDTH / 2, PAD_HEIGHT / 2
LEFT, RIGHT = False, True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, LEFT, RIGHT # these are vectors stored as lists   
    ball_pos = [WIDTH/2,HEIGHT/2]    
    if direction == 'RIGHT':
        LEFT, RIGHT = False, True
        ball_vel = [random.randrange(120, 240)/60.0,-1*random.randrange(60, 180)/60.0]
    elif direction == 'LEFT':   
        LEFT, RIGHT = True, False       
        ball_vel = [-1*random.randrange(120, 240)/60.0,-1*random.randrange(60, 180)/60.0]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos, paddle2_pos = [HALF_PAD_WIDTH,HEIGHT/2], [WIDTH-HALF_PAD_WIDTH,HEIGHT/2]
    paddle1_vel, paddle2_vel = 15, 15
    score1, score2 = 0, 0
    spawn_ball('RIGHT') 

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, LEFT, RIGHT
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball          
    ball_pos = [ball_pos[0]+ball_vel[0],ball_pos[1]+ball_vel[1]]     
    
    if ball_pos[1]+ball_vel[1] < BALL_RADIUS:
        ball_pos[1], ball_vel[1] = BALL_RADIUS, -1*ball_vel[1]
    elif ball_pos[1]+ball_vel[1] > HEIGHT-BALL_RADIUS:
        ball_pos[1], ball_vel[1] = HEIGHT - BALL_RADIUS , -1*ball_vel[1]                              
    
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,12,'Red','Red')
    # update paddle's vertical position, keep paddle on the screen    
    canvas.draw_polygon([[paddle1_pos[0]-HALF_PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT],[paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT],[paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT],[paddle1_pos[0]-HALF_PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT]],1,'White', 'White') 
    canvas.draw_polygon([[paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT],[paddle2_pos[0]+HALF_PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT],[paddle2_pos[0]+HALF_PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT],[paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT]],1,'White','White')    
    # draw scores
    canvas.draw_text(str(score1),((WIDTH/2 - PAD_WIDTH)/2,40),20,"White")
    canvas.draw_text(str(score2),(WIDTH/2+(WIDTH/2-PAD_WIDTH)/2,40),20,"White")
    
    if LEFT and (ball_pos[0]+ball_vel[0] < BALL_RADIUS+PAD_WIDTH):
        if is_touchpad([paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT],[paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT]):
            ball_pos[0], ball_vel[0] = BALL_RADIUS+PAD_WIDTH, -1*ball_vel[0]
            LEFT, RIGHT = False, True          
        else:
            score2 = score2 + 1 
            spawn_ball('RIGHT')    
    elif RIGHT and (ball_pos[0]+ball_vel[0] > WIDTH-PAD_WIDTH-BALL_RADIUS):
        if is_touchpad([paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT],[paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT]):        
            ball_pos[0], ball_vel[0] = WIDTH-PAD_WIDTH-BALL_RADIUS , -1*ball_vel[0]
            LEFT, RIGHT = True, False
        else:
            score1 = score1 + 1            
            spawn_ball('LEFT')         
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_pos[1] = limit(paddle1_pos[1] - paddle1_vel)
    elif key == simplegui.KEY_MAP['s']:
        paddle1_pos[1] = limit(paddle1_pos[1] + paddle1_vel)
    elif key == simplegui.KEY_MAP['up']:    
        paddle2_pos[1] = limit(paddle2_pos[1] - paddle2_vel)
    elif key == simplegui.KEY_MAP['down']:   
        paddle2_pos[1] = limit(paddle2_pos[1] + paddle2_vel)
    
def keyup(key):
    keydown(key)       

def limit(pos):
    if pos < HALF_PAD_HEIGHT:
        return HALF_PAD_HEIGHT
    if pos > (HEIGHT-HALF_PAD_HEIGHT):
        return HEIGHT-HALF_PAD_HEIGHT
    return pos

def is_touchpad(pad_pos1,pad_pos2):
    global ball_pos, ball_vel  
    if not (ball_pos[1] + BALL_RADIUS >= pad_pos2[1] and ball_pos[1] + BALL_RADIUS <= pad_pos1[1]):
        return False
    ball_vel = [ball_vel[0]*1.1,ball_vel[1]*1.1]
    return True
                 
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart',new_game,80)

# start frame
new_game()
frame.start()