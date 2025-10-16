from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

from state_machine import StateMachine

#이벤트 체크 함수
def space_down(e):      #e가 space key input인가를 확인. T/F return
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def time_out(e):        #외부 이벤트 --- idle state에서 5초가 지났는지 확인해야한다.
    return e[0] == 'TIME_OUT'

#이벤트 체크 - 방향키
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):        #enter시점에 오른쪽/왼쪽 결정해야함
        if right_down(e) or left_up(e):
            self.boy.dir = self.boy.face_dir = 1
        elif left_down(e) or right_up(e):
            self.boy.dir = self.boy.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x += self.boy.dir * 5

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)


class Sleep:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 300, 100, 100, 3.141592/2, '', self.boy.x-25, self.boy.y-25, 100, 100)
        else: # face_dir == -1: # left
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 200, 100, 100, -3.141592/2, '', self.boy.x+25, self.boy.y-25, 100, 100)


class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = 0
        self.wait_start_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        if get_time() - self.wait_start_time > 1000.0:       #경과시간
            #TIME_OUT 이벤트 발생
            self.boy.state_machine.handle_state_event(('TIME_OUT', 0))

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.RUN = Run(self)
        #self.state_machine = StateMachine(self.IDLE)
        self.state_machine = StateMachine(
            self.IDLE,     #초기상태
            {       #상태 다이어그램을 딕셔너리 형태로 표현
                self.SLEEP: {space_down: self.IDLE},
                self.IDLE: {left_up: self.RUN, right_up: self.RUN, left_down: self.RUN, right_down: self.RUN, time_out: self.SLEEP},     #TimeOut 이벤트
                self.RUN: {right_down: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, right_up: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        # state_machine에게 적합한 event를 만들어서 넘겨주는 것이 좋다.
        # 상태 이벤트와 get_events를 통해 얻는 입력이벤트와는 다르다.
        # 튜플을 이용하여 상태이벤트를 나타내도록 함 (PPT)

        self.state_machine.handle_state_event(('INPUT', event))

