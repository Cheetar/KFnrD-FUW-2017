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

    def sol_to_bool(self, sol):
        if sol in ["UNSAT", "UNKNOWN"]:
            return sol
        return [x >= 0 for x in sol]

    def get_explicit_solution(self):
        cnf = self.get_cnf()
        solution = pycosat.solve(cnf)
        return self.sol_to_bool(solution)

    def solve(self):
        solution = self.get_explicit_solution()
        self.printout_solution(solution)

    def get_all_solutions(self):
        cnf = self.get_cnf()
        return [self.sol_to_bool(sol) for sol in pycosat.itersolve(cnf)]

    def to_array(self, sol):
        return [sol[(i - self.n):i] for i in range(self.n**2, 0, -self.n)]

    def unarray(self, arr):
        return reduce(lambda x, y: y + x, arr)

    def rotate(self, arr):
        return [list(a) for a in zip(*arr[::-1])]

    def rotate_sol(self, sol, deg):
        arr = self.to_array(sol)
        # rotate
        for i in range(deg / 90):
            arr = self.rotate(arr)
        sol = self.unarray(arr)
        return sol

    def flip_sol(self, sol, horizontal=True):
        """ The flip can be either horizontal (horizontal = True) or
            vertical (horizontal=False)
        """
        out = []
        for num in range(1, self.n**2 + 1):
            x, y = self.get_coord(num)
            if horizontal:
                corresponding_field = self.get_num((self.n - x + 1), y)
            else:
                corresponding_field = self.get_num(x, (self.n - y + 1))
            # -1 because we're counting from 1 not 0
            out.append(sol[corresponding_field - 1])
        return out

    def get_all_unique_solutions(self):
        unique_solutions = []
        all_solutions = self.get_all_solutions()
        for sol in all_solutions:
            unique = True
            for deg in [90, 180, 270]:
                if self.rotate_sol(sol, deg) in unique_solutions:
                    unique = False
                    break
            for horizontal in [True, False]:
                if self.flip_sol(sol, horizontal) in unique_solutions:
                    unique = False
                    break
            for deg in [90, 180, 270]:
                for horizontal in [True, False]:
                    if self.rotate_sol(self.flip_sol(sol, horizontal), deg) in unique_solutions:
                        unique = False
                        break
            if unique:
                unique_solutions.append(sol)
        return unique_solutions

    def printout_solution(self, solution):
        if solution == "UNSAT" or solution == "UNKNOWN":
            print solution
        else:
            board = ""
            for i, val in enumerate(solution):
                if i % self.n == 0:
                    board += "\n"

                if val <= 0:
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
        return (y - 1) * self.n + x

    def get_coord(self, num):
        # Let's count fields from 0
        num -= 1
        x = num % self.n
        y = num / self.n
        return (x + 1, y + 1)

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
