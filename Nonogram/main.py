from nonogram import reduce_domain, solution, solve, constraint_satisfaction, nonoprint
from crawling import get_input
import time, sys

def GAC(variables, domains, constraints):
    # Generalized Arc Consistency를 통해 domain을 줄임
    reduced = reduce_domain(domains, constraints)
    problem = (variables, reduced, constraints)

    # CSP가 풀릴 수 없는 경우인지 체크
    if not solve(problem):
        print("THERE IS NO SOLUTION FOR THIS NONOGRAM")

    # search할 필요 없이 solution이 나온 경우 (3가지 중 1번의 경우)
    if solution(problem):
        nonoprint(problem)
    else:
        print("SOME DOMAINS HAVE MORE THAN ONE VALUES")

if __name__=="__main__":
    '''
    NONOGRAM SOLVER
    소프트웨어융합학과 2017103757 정희재
    
    https://www.nonograms.org/ 의 nonogram들을 크롤링하면 자동으로 .txt file이 작성되어 nonogram을 풀어주는 프로그램
    
    EX 1)
    https://www.nonograms.org/nonograms/i/23319 와 같이 마지막 뒤 존재하는 아이디 값으로 변경해주면 됩니다.
    >> python3 main.py 22860
    
    EX 2)
    input 폴더 내에 존재하는 .txt 파일로도 테스트가 가능합니다. 
    nonogram = {{원하는 텍스트파일 이름}}.txt 로 설정 후  #1 로 표시된 모든 부분은 주석처리 해주시면 됩니다.
    input folder의 디렉토리 설정 필요합니다.
    
    '''

    ################# 1 #################

    id = sys.argv[1]
    get_input(id)
    nonogram = str(id) + ".txt"

    #####################################

    ################# 2 #################
    #        nonogram = "3781.txt"
    #####################################

    start = time.time()

    # CSP 문제를 만들어서
    variables, domains, constraints = constraint_satisfaction(nonogram)
    # GAC로 domain을 줄여 solution 찾기

    GAC(variables, domains, constraints)

    # 소요시간 계산
    end = time.time()
    print((end - start))
