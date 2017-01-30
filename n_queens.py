import itertools

import pycosat


class NQueensProblem(object):

    def __init__(self, n, knight_condition=False):
        self.n = n
        self.knight_condition = knight_condition

    def is_solvable(self):
        solution = self.get_explicit_solution()
        if solution in ["UNSAT", "UNKNOWN"]:
            return False
        return True

    def get_explicit_solution(self):
        cnf = self.get_cnf()
        solution = pycosat.solve(cnf)
        return solution

    def solve(self):
        solution = self.get_explicit_solution()
        self.printout_solution(solution)

    def get_all_solutions(self):
        cnf = self.get_cnf()
        return [sol for sol in pycosat.itersolve(cnf)]

    def rotate_sol(self, sol, deg):
        pass

    def flip_sol(self, sol, flip=True):
        """ The flip can be either horizontal (flip = True) or
            vertical (flip=False)
        """
        pass

    def get_all_unique_solutions(self):
        unique_solutions = set()
        cnf = self.get_cnf()
        for sol in pycosat.itersolve(cnf):
            for deg in [90, 180, 270]:
                if self.rotate_sol(sol, deg) in unique_solutions:
                    break
            for flip in [True, False]:
                if self.flip_sol(sol, flip) in unique_solutions:
                    break
            unique_solutions.add(sol)

    def printout_solution(self, solution):
        if solution == "UNSAT" or solution == "UNKNOWN":
            print solution
        else:
            board = ""
            for i, val in enumerate(solution):
                if i % self.n == 0:
                    board += "\n"

                if val < 0:
                    board += "-"
                else:
                    board += "Q"
            print board[1:]

    def get_num(self, x, y):
        """ Each field has its own coordinates x and y. Thid method converts
            these coordinates into numbers used later on in cnf.
            x - row
            y - column
        """
        return (x - 1) * self.n + y

    def get_cnf(self):
        get_num = self.get_num
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

if __name__ == "__main__":
    problem = NQueensProblem(8)
    problem.solve()
