import sys, grader, parse
from copy import deepcopy
import random, p1
ENSW = {'E': (0,1), 'N': (-1,0), 'S': (1,0), 'W': (0,-1)}
NOISE_DI = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']} 

def move(player, intend_dir, noise, grid):
    direction = random.choices(NOISE_DI[intend_dir], weights=[1 - noise*2, noise, noise])[0]
    if player[0] + ENSW[direction][0] >= 0 and player[0] + ENSW[direction][0] < len(grid) and \
            player[1] + ENSW[direction][1] >= 0 and \
                player[1] + ENSW[direction][1] < len(grid[player[0] + ENSW[direction][0]]):
        # check wall
        if grid[player[0] + ENSW[direction][0]][player[1] + ENSW[direction][1]] != '#':
            return [player[0]+ENSW[direction][0], player[1]+ENSW[direction][1]]
    return player

# set show_converged_results = True if you want to print the converged policy and Q values
def td_learning(problem, show_converged_results = False):
    grid = problem.grid
    discount = problem.discount
    noise = problem.noise
    livingReward = problem.livingReward
    
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'S':
                start = [row, col]
                break
    # initialize Q values
    Q = []
    for i in range(len(grid)):
        Q_row = []
        for j in range(len(grid[i])):
            if grid[i][j] == '#':
                Q_row.append('#')
            elif grid[i][j] == 'S' or grid[i][j] == '_':
                Q_row.append({'E': 0.0, 'N': 0.0, 'S': 0.0, 'W': 0.0})
            else: # exit grid
                Q_row.append(0.0)
        Q.append(Q_row)

    alpha = 0.5
    epsilon = 0.9
    converge = False
    episode = 0

    while (converge != True):
        episode += 1
        # decrease learning rate and epsilon every 10 episodes
        if episode%10 == 0:
            alpha *= 0.9
            epsilon *= 0.9
        player = start
        converge = True
        while (True):
            # exit grid
            if grid[player[0]][player[1]] not in ('#', 'S', '_'):
                new_Q = float(grid[player[0]][player[1]])
                if abs(new_Q - Q[player[0]][player[1]]) > 1e-4: converge = False
                Q[player[0]][player[1]] = (1-alpha)*Q[player[0]][player[1]] + alpha*new_Q
                break
            
            # using epsilon greedy to force exploration
            random_act = random.choices([True, False], weights=[epsilon, 1-epsilon])
            # randomly explore other actions with probability epsilon
            if random_act:   
                intend_dir = random.choice(('N','E','S','W'))
                player_new = move(player, intend_dir, noise, grid)
                # if arrived at exit grid
                if grid[player_new[0]][player_new[1]] not in ('#', 'S', '_'):
                    new_Q = livingReward + discount*Q[player_new[0]][player_new[1]]
                else:
                    new_Q = livingReward + discount*max(Q[player_new[0]][player_new[1]].values())
                if abs((1-alpha)*Q[player[0]][player[1]][intend_dir] + alpha*new_Q - Q[player[0]][player[1]][intend_dir]) > 1e-4: converge = False
                Q[player[0]][player[1]][intend_dir] = (1-alpha)*Q[player[0]][player[1]][intend_dir] + alpha*new_Q
                player = player_new

            # follow the current best policy with probability 1-epsilon
            else:
                best_policy = max(Q[player[0]][player[1]], key=Q[player[0]][player[1]].get)
                player_new = move(player, best_policy, noise, grid)
                # if arrived at exit grid
                if grid[player_new[0]][player_new[1]] not in ('#', 'S', '_'):
                    new_Q = livingReward + discount*Q[player_new[0]][player_new[1]]
                else:
                    new_Q  = livingReward + discount*max(Q[player_new[0]][player_new[1]].values())
                if abs((1-alpha)*Q[player[0]][player[1]][best_policy] + alpha*new_Q - Q[player[0]][player[1]][best_policy]) > 1e-4: converge = False
                Q[player[0]][player[1]][best_policy] = (1-alpha)*Q[player[0]][player[1]][best_policy] + alpha*new_Q
                player = player_new
                  
    optimal_policy = ''
    converged_optimal_policy = ''
    for i in range(len(Q)):
        for j in range(len(Q[i])):
            if Q[i][j] == '#':
                optimal_policy += '| # |'
                converged_optimal_policy += '| ################################ |'
            elif isinstance(Q[i][j], float):
                optimal_policy += '| x |'
                # Q_X = "{:>6}".format(str(round(Q[i][j], 3))[:6], "6")
                Q_X = "{: >6.3f}".format(Q[i][j])[:6]
                converged_optimal_policy += f'|x{Q_X}                           |'
            else:
                policy = max(Q[i][j], key = Q[i][j].get)
                optimal_policy += '| %s |' % policy

                Q_N = "{: >6.3f}".format(Q[i][j]['N'])[:6]
                Q_E = "{: >6.3f}".format(Q[i][j]['E'])[:6]
                Q_S = "{: >6.3f}".format(Q[i][j]['S'])[:6]
                Q_W = "{: >6.3f}".format(Q[i][j]['W'])[:6]
                converged_optimal_policy += f'|N{Q_N}  E{Q_E}  S{Q_S}  W{Q_W}|'

        optimal_policy += '\n'
        converged_optimal_policy += '\n'
    # print(optimal_policy[:-1])
    if show_converged_results:
        return_value = converged_optimal_policy[:-1]
    else:
        return_value = optimal_policy[:-1]
    return return_value


if __name__ == "__main__":
    try: test_case_id = int(sys.argv[1])
    except: test_case_id = -5
    problem_id = 4
    grader.grade(problem_id, test_case_id, td_learning, parse.read_grid_mdp_problem_p4)