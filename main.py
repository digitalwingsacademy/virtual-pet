from simulator import run, move, put_ball, turn_left, front_is_blocked

def program():
    for _ in range(4):
        move()
        put_ball()
    if front_is_blocked():
        turn_left()

run(program)
