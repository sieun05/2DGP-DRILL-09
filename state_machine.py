from event_to_string import event_to_string

class StateMachine:
    def __init__(self, start_state, rules):     #rules: {state: {event:state}}
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter()

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    #Sleep <--> Idle
    def handle_state_event(self, state_event):
        #if로 처리하기보다 더 효과적인 상태변환규칙테이블 등을 만들어 처리한다.
        #dictionary, 2D array, ...

        #조건은 함수로 체크

        pass

