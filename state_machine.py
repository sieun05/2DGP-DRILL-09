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

        for check_event in self.rules[self.cur_state].keys():   #[space_down]
            if check_event(state_event):        #만약 True라면
                self.next_state = self.rules[self.cur_state][check_event]   #상태변화 next == IDLE
                self.cur_state.exit()
                self.next_state.enter()

                #디버그 용도
                #현재 상태가 어떤 이벤트에 의해 다음 상태로 바뀌었는지 정보를 표시한다.
                print(f'{self.cur_state.__class__.__name__} ==== {event_to_string(state_event)} ====> {self.next_state.__class__.__name__}')

                self.cur_state = self.next_state
