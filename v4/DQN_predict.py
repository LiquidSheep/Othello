from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils import plot_model
from collections import deque
import numpy as np
import main

BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4


class QNetwork:

    def __init__(self, learning_rate=0.01, state_size=16, action_size=16, hidden_size=10):

        self.model = Sequential()
        self.model.add(Dense(hidden_size, activation='relu', input_dim=state_size))
        self.model.add(Dense(hidden_size, activation='relu'))
        self.model.add(Dense(action_size, activation='linear'))
        self.optimizer = Adam(lr=learning_rate)  # 誤差を減らす学習方法はAdam
        self.model.compile(loss='mse', optimizer=self.optimizer)
        #self.model.compile(loss=huberloss, optimizer=self.optimizer)

    # 重みの学習
    def replay(self, memory, batch_size, gamma, targetQN):

        inputs = np.zeros((batch_size, 16))
        targets = np.zeros((batch_size, 16))
        mini_batch = memory.sample(batch_size)

        for i, (state_b, action_b, reward_b, next_state_b) in enumerate(mini_batch):
            inputs[i:i + 1] = state_b
            target = reward_b

            if not (next_state_b == np.zeros(state_b.shape)).all(axis=1):
                # 価値計算（DDQNにも対応できるように、行動決定のQネットワークと価値観数のQネットワークは分離）
                retmainQs = self.model.predict(next_state_b)[0]
                next_action = np.argmax(retmainQs)  # 最大の報酬を返す行動を選択する
                target = reward_b + gamma * targetQN.model.predict(next_state_b)[0][next_action]

            targets[i] = self.model.predict(state_b)    # Qネットワークの出力
            targets[i][action_b] = target               # 教師信号

        # shiglayさんよりアドバイスいただき、for文の外へ修正しました
        self.model.fit(inputs, targets, epochs=1, verbose=0)  # epochsは訓練データの反復回数、verbose=0は表示なしの設定

class Actor:
    def get_action(self, state, episode, mainQN):   # [C]ｔ＋１での行動を返す
        # 徐々に最適行動のみをとる、ε-greedy法
        epsilon = 0.001 + 0.9 / (1.0+episode)
        othello.board_class.find_placeable(BLACK if t%2==1 else WHITE)
        placeable_list = [i for i, stone in enumerate(return_board(othello.board_class.board)) if stone==PLACEABLE]
        othello.board_class.delete_placeable()

        if epsilon <= np.random.uniform(0, 1):
            retTargetQs = mainQN.model.predict(state)[0]
            #action = np.argmax(retTargetQs)  # 最大の報酬を返す行動を選択する
            sorted_Q = np.argsort(retTargetQs)
            for i in range(16):
                action = sorted_Q[i]
                if action in placeable_list:
                    break
                elif i==15:
                    action = -1
        else:
            action = -1  # ランダムに行動する

        return action

class Memory:
    def __init__(self, max_size=1000):
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        idx = np.random.choice(np.arange(len(self.buffer)), size=batch_size, replace=False)
        return [self.buffer[ii] for ii in idx]

    def len(self):
        return len(self.buffer)

def return_board(board):

    return_board = []
    for i in range(36):
        if board[i]!=4:
            return_board.append(board[i])

    return return_board

def convert_state(observation):

    return sum([stone * (3 ** i) for i, stone in enumerate(observation)])



player_list = ["player", "random"]
othello = main.Othello(player_list[1], player_list[1])
q_turn = WHITE

max_num_of_turn = 16
num_consecutive_iterations = 100
num_episodes = 100
goal_average_reward = 90
total_reward_vec = np.zeros(num_consecutive_iterations)
gamma = 0.99
islearned = False

hidden_size = 16               # Q-networkの隠れ層のニューロンの数
learning_rate = 0.00001         # Q-networkの学習係数
batch_size = 16

mainQN = load_model("./dqn_model_100_1.h5")
targetQN = QNetwork(hidden_size=hidden_size, learning_rate=learning_rate)
actor = Actor()
memory = Memory(10000)

win = 0
lose = 0
even = 0

for episode in range(num_episodes):  # 試行数分繰り返す
    #env.reset()  # cartPoleの環境初期化
    othello.reset()
    #state, reward, done, _ = env.step(env.action_space.sample())  # 1step目は適当な行動をとる
    winner = othello.game_loop(4)
    state = return_board(othello.board_class.board)
    state = np.reshape(state, [1, 16])   # list型のstateを、1行4列の行列に変換
    episode_reward = 0

    targetQN.model.set_weights(mainQN.model.get_weights())

    for t in range(max_num_of_turn + 1):  # 1試行のループ

        if (t+1)%2==q_turn%2:
            action = actor.get_action(state, episode, mainQN)   # 時刻tでの行動を決定する
            #next_state, reward, done, info = env.step(action)   # 行動a_tの実行による、s_{t+1}, _R{t}を計算する
            winner = othello.game_loop((action // 4 + 1) * 6 + (action % 4 + 1))
            next_state = return_board(othello.board_class.board)
            next_state = np.reshape(next_state, [1, 16]) # list型のstateを、1行4列の行列に変換

            reward = 0
            if winner!=-1:
                next_state = np.zeros(state.shape)
                if winner==q_turn:
                    reward = 1
                elif winner==q_turn%2+1:
                    reward = -1

            episode_reward += reward

            memory.add((state, action, reward, next_state))     # メモリの更新する
            state = next_state  # 状態更新


            # Qネットワークの重みを学習・更新する replay
            if (memory.len() > batch_size) and not islearned:
                mainQN.replay(memory, batch_size, gamma, targetQN)
        else:
            winner = othello.game_loop(4)

        # 1施行終了時の処理
        if winner!=-1:
            total_reward_vec = np.hstack((total_reward_vec[1:], episode_reward))  # 報酬を記録
            if q_turn%2==(t+1)%2:
                action = -1
            if winner==q_turn:
                win += 1
            elif winner==q_turn%2+1:
                lose += 1
            elif winner==0:
                even += 1
            print('%d Episode finished after %d time steps / mean %f' % (episode, t + 1, total_reward_vec.mean()), end=" ")
            print("win:{}".format(win), "lose:{}".format(lose), "even:{}".format(even))
            break

    # 複数施行の平均報酬で終了を判断
    if total_reward_vec.mean() >= goal_average_reward:
        print('Episode %d train agent successfuly!' % episode)
        islearned = 1

mainQN.model.save("./dqn_model_100_1.h5")