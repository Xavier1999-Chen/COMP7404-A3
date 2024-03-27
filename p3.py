import sys, grader, parse
from  p2 import value_next
from copy import deepcopy
ENSW = {'E': (0,1), 'N': (-1,0), 'S': (1,0), 'W': (0,-1)}
NOISE_DI = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']} 

def value_iteration(problem):
    # return_value = ''
    return_value = "V_k=0"
    for i in range(len(problem.valueState)):
        return_value += '\n'
        for j in range(len(problem.valueState[i])):
            if problem.grid[i][j] == "#":
                return_value += '| ##### |'
            else:
                return_value += '|{:7.2f}|'.format(problem.valueState[i][j])

    for k in range(1, problem.iterations):
        return_value += "\nV_k=%d"%k
        new_valueState = deepcopy(problem.valueState)
        pi_k = problem.policy
        for i in range(len(problem.valueState)):
            return_value += '\n'
            for j in range(len(problem.valueState[i])):
                if problem.grid[i][j] == "#":
                    return_value += '| ##### |'
                else:
                    if problem.grid[i][j] != "_" and problem.grid[i][j] != "S":
                        new_valueState[i][j] = float(problem.grid[i][j])
                        pi_k[i][j] = 'x'
                    else:
                        max = -10000
                        for intend_dir in ['N','E','S','W']:
                            new_value = (1-2*problem.noise)*(problem.livingReward+\
                                problem.discount*value_next([i,j], intend_dir, problem.grid, problem.valueState)) + \
                                    problem.noise*(problem.livingReward+problem.discount*value_next([i,j], NOISE_DI[intend_dir][1], problem.grid, problem.valueState)) + \
                                        problem.noise*(problem.livingReward+problem.discount*value_next([i,j], NOISE_DI[intend_dir][2], problem.grid, problem.valueState))
                            if new_value > max:
                                max = new_value
                                pi_k[i][j] = intend_dir
                        new_valueState[i][j] = max
                    return_value += '|{:7.2f}|'.format(new_valueState[i][j])
        return_value += '\npi_k=%d'%k
        for i in range(len(pi_k)):
            return_value += '\n'
            for j in range(len(pi_k[i])):
                return_value += '| %s |'%pi_k[i][j]
        problem.valueState = new_valueState
    return return_value

if __name__ == "__main__":
    try: test_case_id = int(sys.argv[1])
    except: test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)