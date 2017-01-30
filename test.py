import unittest

from n_queens import NQueensProblem


class TestNQueenProblem(unittest.TestCase):

    def test_get_num(self):
        p = NQueensProblem(8)
        self.assertEqual(p.get_num(1, 1), 1)
        self.assertEqual(p.get_num(2, 5), 13)
        self.assertEqual(p.get_num(8, 8), 64)

    def test_solve(self):
        p = NQueensProblem(1)
        self.assertTrue(p.is_solvable())
        self.assertEqual(p.get_explicit_solution(), [1])

        p = NQueensProblem(2)
        self.assertFalse(p.is_solvable())
        self.assertEqual(p.get_explicit_solution(), "UNSAT")

        p = NQueensProblem(3)
        self.assertFalse(p.is_solvable())
        self.assertEqual(p.get_explicit_solution(), "UNSAT")

        p = NQueensProblem(8)
        self.assertTrue(p.is_solvable())

    def test_number_of_solutions_for_n_equal_8(self):
        p = NQueensProblem(8)
        self.assertEqual(len(p.get_all_solutions()), 92)


if __name__ == "__main__":
    unittest.main()
