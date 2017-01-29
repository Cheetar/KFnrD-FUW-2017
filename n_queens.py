import itertools

import pycosat


class NQueensProblem(object):

    def __init__(self, n, knight_condition=False):
        self.n = n
        self.knight_condition = knight_condition

    def is_solvable(self):
        if self.solve == "UNSAT":
            return False
        return True

    def solve(self):
        # TODO manage n=2 and n=3
        if not self.is_solvable():
            print "UNSAT"
        else:
            cnf = self.get_cnf()
            solution = pycosat.solve(cnf)
            self.printout_solution(solution)

    def get_all_solutions(self):
        pass

    def printout_solution(self, solution):
        board = ""
        for i, val in enumerate(solution):
            if i % self.n == 0:
                board += "\n"

            if val < 0:
                board += "-"
            else:
                board += "Q"
        print board[1:]

    def get_cnf(self):
        def get_num(x, y):
            """ Each field has its own coordinates x and y. Thid method converts
                these coordinates into numbers used later on in cnf.
                x - row
                y - column
            """
            return (x - 1) * self.n + y

        n = self.n
        cnf = []
        # At least one quuen
        # at all rows
        for row in range(1, n + 1):
            clause = [get_num(row, y) for y in range(1, n + 1)]
            cnf.append(clause)
        # at all columns
        for column in range(1, n + 1):
            clause = [get_num(x, column) for x in range(1, n + 1)]
            cnf.append(clause)

        # Max one quuen
        # at rows
        for row in range(1, n + 1):
            fields = [-get_num(row, y) for y in range(1, n + 1)]
            for clause in itertools.combinations(fields, 2):
                cnf.append(list(clause))
        # at columns
        for column in range(1, n + 1):
            fields = [-get_num(x, column) for x in range(1, n + 1)]
            for clause in itertools.combinations(fields, 2):
                cnf.append(list(clause))

        def get_diagonal_fields(init_coord, right=True):
            x, y = init_coord
            fields = []
            while x <= n and y <= n and x >= 1 and y >= 1:
                fields.append(-get_num(x, y))
                x += (right * 2 - 1)
                y += 1
            return fields

        # at diagonals /
        initial_points = [(1, 1)]
        initial_points += [(1, y) for y in range(2, n + 1)]
        initial_points += [(x, 1) for x in range(2, n + 1)]
        for init_point in initial_points:
            fields = get_diagonal_fields(init_point)
            for clause in itertools.combinations(fields, 2):
                cnf.append(list(clause))

        # at diagonals \
        initial_points = [(n, 1)]
        initial_points += [(n, y) for y in range(2, n + 1)]
        initial_points += [(x, 1) for x in range(1, n)]
        for init_point in initial_points:
            fields = get_diagonal_fields(init_point, False)
            for clause in itertools.combinations(fields, 2):
                cnf.append(list(clause))

        return cnf

problem = NQueensProblem(8)
problem.solve()
