from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

from state_machine import StateMachine

#이벤트 체크 함수
def space_down(e):      #e가 space key input인가를 확인. T/F return
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

class Sleep:

    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.dir = 0

    def exit(self):
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

    def enter(self):
        self.boy.dir = 0

    def exit(self):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

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
        #self.state_machine = StateMachine(self.IDLE)
        self.state_machine = StateMachine(
            self.SLEEP,     #초기상태
            {       #상태 다이어그램을 딕셔너리 형태로 표현
                self.SLEEP: {space_down: self.IDLE},
                self.IDLE: {}
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

