import sys, random, grader, parse
from copy import deepcopy
ENSW = {'E': (0,1), 'N': (-1,0), 'S': (1,0), 'W': (0,-1)}
NOISE_DI = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}

class State:
    def __init__(self, layout, player, policy, cum_reward=0.0):
        self.layout = layout
        self.player = player
        self.policy = policy
        self.cum_reward = cum_reward
    def printState(self) -> str:
        out = []
        for row in range(len(self.layout)):
            out_row = ''
            for col in range(len(self.layout[row])):
                if self.player != [row, col]:
                    out_row += f'{self.layout[row][col]:>5}'
                else:
                    out_row += '    P'
            out.append(out_row)
        return '\n'.join(out) + "\nCumulative reward sum: " + str(round(self.cum_reward,2))

    def move(self, intend_direction, noise, livingReward) -> str:
        direction = random.choices(NOISE_DI[intend_direction], weights=[1 - noise*2, noise, noise])[0]
        # check if within the map
        if self.player[0] + ENSW[direction][0] >= 0 and self.player[0] + ENSW[direction][0] < len(self.layout) and \
            self.player[1] + ENSW[direction][1] >= 0 and \
                self.player[1] + ENSW[direction][1] < len(self.layout[self.player[0] + ENSW[direction][0]]):
            # check wall
            if self.layout[self.player[0] + ENSW[direction][0]][self.player[1] + ENSW[direction][1]] != '#':
                self.player = [self.player[0]+ENSW[direction][0], self.player[1]+ENSW[direction][1]]
        self.cum_reward += livingReward
        # print experience
        experience = "Taking action: %s (intended: %s)\n"%(direction, intend_direction)
        experience += "Reward received: " + str(round(livingReward,2)) + '\nNew state:\n'
        return experience + self.printState()

    def exit(self) -> str:
        reward = float(self.layout[self.player[0]][self.player[1]])
        self.cum_reward += reward
        self.player = []
        # print experience
        experience = "Taking action: exit (intended: exit)\n"
        experience += "Reward received: " + str(round(reward,2)) +'\nNew state:\n'
        return experience + self.printState()


class Problem:
    def __init__(self, seed, noise, livingReward, state: State, policy, exit=0):
        self.seed = seed
        self.noise = noise
        self.livingReward = livingReward
        self.state = state
        self.policy = policy
        self.exit = exit
    def act(self) -> str:
        player_loc = self.state.player
        policy = self.policy[player_loc[0]][player_loc[1]]
        if policy != "exit":
            return self.state.move(policy, self.noise, self.livingReward)
        else:
            self.exit = 1
            return self.state.exit()
        
def play_episode(problem):
    # experience = ''
    experience = ["Start state:\n" + problem.state.printState()]
    if problem.seed !=-1:
        random.seed(problem.seed, version=1)
    while problem.exit == 0:
        experience.append(problem.act())
    return "\n-------------------------------------------- \n".join(experience)
    return experience

if __name__ == "__main__":
    try: test_case_id = int(sys.argv[1])
    except: test_case_id = -8
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)