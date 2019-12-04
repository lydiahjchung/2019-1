'''
    Generalized Arc Consistency Algorithm

    이전에는 consistent였는데 다른 arc를 arc consistent하게 만들다 보면 inconsistent하게 되는 경우가 생기므로
    queue를 도입하여 어떤 arc를 consistent하게 만들 때마다 이전의 arc들을 다시 한번 확인해 주어야 함
    유한개의 element가 존재하기에 결과적으로 'fixed point'에 도달하게 될 것

    모든 arc를 consistent하게 하여 domain 자체를 줄이고자 하는 알고리즘!

    모든 arc가 consistent하면, 결과는 세 가지가 나올 수 있음
    1. 각 domain이 single value를 가지는 경우
        => 이미 solution을 찾은 것
    2. 적어도 하나의 domain이 empty인 경우
        => solution이 없음
    3. 몇몇 domain들이 하나 이상의 value를 가지는 경우
        => search 하자 (새로운, 대부분 간단해진 Constraint Satisfaction Problem을 푸는 것 = constraints는 동일하지만 줄어든 domain)
'''
import itertools

def reduce_domain(domains, constraints):
    # queue에 모든 arc 추가
    queue = totalArcs(constraints)

    # queue에 element가 존재할 때까지 반복
    while queue:
        # queue의 앞부터 pop
        i, j = queue.pop(0)
        # 해당 arc가 consistent한지 체크한다
        revised = revision(domains, constraints, i, j) # checks if arc is consistent

        # consistent할 경우 neighboring arc 체크
        if revised:
            # neightboring arcs 다시 체크
            for (k, i) in adjacentArcs(constraints, i):
                # arc was not consistent all neighboring arcs therfore need to be arc-consistent checked again
                if k != i:
                    queue.append((k, i))
    return domains

def revision(domains, constraints, i, j):
    # arc가 consistent한가 체크함
    # 만족(check)하지 않을 경우 domain에서 제거
    revised = False

    for val in domains[i]:
        check = False
        for each in domains[j]:
            filtering = constraints[i][j]
            # 해당 값이 만족되는 경우
            if filtering(i, j, (val, each)):
                check = True
                break
        if not check: # value is not satisfiable
            # domain에서 해당 value 지움
            domains[i].remove(val)
            revised = True
    return revised


def totalArcs(constraints):
    # 모든 arc 구해줌
    return [(i, j) for i in constraints for j in constraints[i]]


def adjacentArcs(constraints, variable):
    # neighboring/adjacent arc를 구해줌
    result = [(i, variable) for i in constraints[variable]]
    result.extend([(variable, i) for i in constraints[variable]])
    return result

def solution(csp):
    # 3가지 경우 중 1번의 경우로 solution 존재
    variables, domains, constraints = csp
    for key, value in domains.items():
        if len(value) != 1:
            return False
    return True

def solve(csp):
    variables, domains, constraints = csp
    # 3가지 경우 중 2번의 경우 해결이 불가능
    for key, value in domains.items():
        if len(value) == 0:
            return False
    return True

def constraint_satisfaction(filename):
    # 각 row, col에 맞게 constraint를 만들어 줌
    f = open(filename,'r')
    lines = f.read().split("\n")
    lines[0] = lines[0].split()

    len_rows = int(lines[0][0])
    len_cols =  int(lines[0][1])

    rconstraints = [row for row in lines[1:len_rows + 1]]
    cconstraints = [col for col in lines[len_rows + 1:]]

    variables, domains, constraints = [], {}, {}

    # 각 row, col에 대해 domain 구함
    for i in range(len_rows):
        segment = map(int, list(rconstraints[i].split()))
        domain = generating_domains(len_cols, segment)
        variable = "R" + str(i)

        variables.append(variable)
        domains[variable] = domain
        constraints[variable] = {}

    for i in range(len_cols):
        segment = map(int, list(cconstraints[i].split()))
        domain = generating_domains(len_rows, segment)
        variable = "C" + str(i)

        variables.append(variable)
        domains[variable] = domain
        constraints[variable] = {}

    row_variables = filter(lambda x: 'R' in x, variables)
    col_variables = filter(lambda x: 'C' in x, variables)

    # R과 C가 쌍을 이루게 해줌
    # 후에 행과 열을 동시에 만족해야하기 때문
    for (row, col) in itertools.product(row_variables, col_variables):
        constraints[row][col], constraints[col][row] = pairing, pairing

    return (variables, domains, constraints)

def generating_domains(length, specifics):
    # constraints에 맞는 domain을 만들어줌
    domain = []
    minimum = []
    for spec in specifics:
        for i in range(spec):
            minimum.append(1)
        minimum.append(0)
    minimum.pop(len(minimum) - 1)

    insert = [i + 1 for i, x in enumerate(minimum) if x == 0]
    insert.extend([0, len(minimum)])
    combinations = itertools.combinations_with_replacement(insert, abs(length - len(minimum)))

    for combo in combinations:
        result = minimum[:]
        inserting = list(combo)
        inserting.sort()
        offset = 0
        for index in inserting:
            result.insert(index + offset, 0)
            offset += 1
        domain.append(result)
    return domain

def pairing(i, j, value_pair):
    # 서로 쌍을 만들어줌
    x, y = value_pair
    xidx = int(i[1:])
    yidx = int(j[1:])
    return x[yidx] == y[xidx]

def nonoprint(result):
    # 결과 프린트 함수
    variables, domains, constraints = result
    sorted_keys = []
    for key in domains.keys():
        if "R" in key:
            sorted_keys.append(int(key[1:]))
    sorted_keys.sort()
    for key in sorted_keys:
        for bit in domains['R' + str(key)][0]:
            if bit == 1:
                print('\033[0;100m' + "  " + '\033[0m', end="")
            else:
                print('\033[0;107m' + "  " + '\033[0m',end="")
        print()
    print()
