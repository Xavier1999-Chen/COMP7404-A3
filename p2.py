import sys, grader, parse
from copy import deepcopy
ENSW = {'E': (0,1), 'N': (-1,0), 'S': (1,0), 'W': (0,-1)}
NOISE_DI = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}  

def value_next(player, direction, grid, valueState):
    if player[0] + ENSW[direction][0] >= 0 and player[0] + ENSW[direction][0] < len(grid) and \
            player[1] + ENSW[direction][1] >= 0 and \
                player[1] + ENSW[direction][1] < len(grid[player[0] + ENSW[direction][0]]):
        # check wall
        if grid[player[0] + ENSW[direction][0]][player[1] + ENSW[direction][1]] != '#':
            return valueState[player[0]+ENSW[direction][0]][player[1]+ENSW[direction][1]]
    return valueState[player[0]][player[1]]


def policy_evaluation(problem):
    # return_value = ''
    return_value = "V^pi_k=0"
    for i in range(len(problem.valueState)):
        return_value += '\n'
        for j in range(len(problem.valueState[i])):
            if problem.policy[i][j] == "#":
                return_value += '| ##### |'
            else:
                return_value += '|{:7.2f}|'.format(problem.valueState[i][j])

    for k in range(1, problem.iterations):
        return_value += "\nV^pi_k=%d"%k
        new_valueState = deepcopy(problem.valueState)
        for i in range(len(problem.valueState)):
            return_value += '\n'
            for j in range(len(problem.valueState[i])):
                if problem.policy[i][j] == "#":
                    return_value += '| ##### |'
                else:
                    if problem.policy[i][j] == "exit":
                        new_valueState[i][j] = float(problem.grid[i][j])
                    else:
                        intend_dir = problem.policy[i][j]
                        new_valueState[i][j] = (1-2*problem.noise)*(problem.livingReward+\
                            problem.discount*value_next([i,j], intend_dir, problem.grid, problem.valueState)) + \
                                problem.noise*(problem.livingReward+problem.discount*value_next([i,j], NOISE_DI[intend_dir][1], problem.grid, problem.valueState)) + \
                                    problem.noise*(problem.livingReward+problem.discount*value_next([i,j], NOISE_DI[intend_dir][2], problem.grid, problem.valueState))
                    return_value += '|{:7.2f}|'.format(new_valueState[i][j])
        problem.valueState = new_valueState
    return return_value

if __name__ == "__main__":
    try: test_case_id = int(sys.argv[1])
    except: test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)