import numpy as np
import main

BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4

def return_board(board):

    return_board = []
    for i in range(36):
        if board[i]!=4:
            return_board.append(board[i])

    return return_board

def convert_state(observation):

    return sum([stone * (3 ** i) for i, stone in enumerate(observation)])

def get_first_action(state, placeable_list):

    sorted_q_table = np.argsort(q_table[state])
    for i in range(16):
        action = sorted_q_table[i]
        if action in placeable_list:
            break
        elif i==15:
            action = -1

    return action

def get_action(next_state, episode, placeable_list):

    epsilon = 0.5 * (1 / (episode + 1))
    if epsilon <= np.random.uniform(0, 1):
        sorted_q_table = np.argsort(q_table[next_state])
        for i in range(16):
            next_action = sorted_q_table[i]
            if next_action in placeable_list:
                break
            elif i==15:
                next_action = -1
    else:
        next_action = np.random.choice(placeable_list)

    return next_action

def update_q_table(q_table, state, action, reward, next_state):

    gamma = 0.99
    alpha = 0.5
    next_max_q = max(q_table[next_state])
    q_table[state, action] = (1 - alpha) * q_table[state, action] + alpha * (reward + gamma * next_max_q)

    return q_table


player_list = ["player", "random"]
othello = main.Othello(player_list[1], player_list[1])
q_turn = WHITE

max_num_of_turn = 16
num_consecutive_iterations = 100
num_episode = 100
goal_average_reward = 90
q_table = np.random.uniform(low=-10, high=10, size=(3**16, 16))
total_reward_vec = np.zeros(num_consecutive_iterations)
final_board = np.zeros((num_episode, 16))
islearned = False
reward_coef = 5

win = 0
lose = 0
even = 0

for episode in range(num_episode):

    othello.reset()
    observation = return_board(othello.board_class.board)
    state = convert_state(observation)
    othello.board_class.find_placeable(BLACK)
    placeable_list = [i for i, stone in enumerate(return_board(othello.board_class.board)) if stone==PLACEABLE]
    othello.board_class.delete_placeable()
    action = get_first_action(state, placeable_list)
    episode_reward = 0

    for turn in range(max_num_of_turn):

        winner = othello.game_loop((action // 4 + 1) * 6 + (action % 4 + 1))
        observation = return_board(othello.board_class.board)

        reward = 0
        if winner!=-1:
            if winner==q_turn:
                reward = 10
            elif winner==q_turn%2+1:
                reward = -10

        episode_reward += reward

        next_state = convert_state(observation)
        q_table = update_q_table(q_table, state, action, reward, next_state)

        othello.board_class.find_placeable(BLACK if turn%2==1 else WHITE)
        placeable_list = [i for i, stone in enumerate(return_board(othello.board_class.board)) if stone==PLACEABLE]
        othello.board_class.delete_placeable()
        if len(placeable_list)>0:
            action = get_action(next_state, episode, placeable_list)
        else:
            action = -1


        if winner!=-1:
            total_reward_vec = np.hstack((total_reward_vec[1:], episode_reward))
            if q_turn%2==(turn+1)%2:
                action = -1

            if winner==q_turn:
                win += 1
            elif winner==q_turn%2+1:
                lose += 1
            elif winner==0:
                even += 1
            break

    if episode%1000==0:
        print("episode {}".format(episode), "win:{}".format(win), "lose:{}".format(lose), "even:{}".format(even))
        win = 0
        lose = 0
        even = 0