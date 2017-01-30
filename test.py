import unittest

from n_queens import NQueensProblem


class TestNQueenProblem(unittest.TestCase):

    def test_get_num(self):
        p = NQueensProblem(8)
        self.assertEqual(p.get_num(1, 1), 1)
        self.assertEqual(p.get_num(5, 2), 13)
        self.assertEqual(p.get_num(8, 8), 64)

        p = NQueensProblem(2)
        self.assertEqual(p.get_num(1, 1), 1)
        self.assertEqual(p.get_num(2, 1), 2)
        self.assertEqual(p.get_num(1, 2), 3)
        self.assertEqual(p.get_num(2, 2), 4)

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

    def test_number_of_solutions(self):
        p = NQueensProblem(8)
        self.assertEqual(len(p.get_all_solutions()), 92)

        p = NQueensProblem(4)
        self.assertEqual(len(p.get_all_solutions()), 2)

    def test_sol_to_bool(self):
        p = NQueensProblem(4)
        self.assertEqual(p.sol_to_bool([1, 2, -3]), [True, True, False])

    def test_get_coord(self):
        p = NQueensProblem(8)
        self.assertEqual(p.get_coord(11), (3, 2))
        self.assertEqual(p.get_coord(1), (1, 1))
        self.assertEqual(p.get_coord(8), (8, 1))
        self.assertEqual(p.get_coord(9), (1, 2))
        self.assertEqual(p.get_coord(64), (8, 8))

    def test_flip(self):
        p = NQueensProblem(2)
        self.assertEqual(p.flip_sol([True, False, True, False]), [
                         False, True, False, True])
        self.assertEqual(p.flip_sol([True, False, True, False], False), [
                         True, False, True, False])

    def test_rotate(self):
        p = NQueensProblem(2)
        self.assertEqual(p.rotate_sol([True, False, True, False], 90), [
                         False, False, True, True])
        self.assertEqual(p.rotate_sol([True, False, True, False], 180), [
                         False, True, False, True])
        self.assertEqual(p.rotate_sol([True, False, True, False], 270), [
                         True, True, False, False])

        p = NQueensProblem(4)
        self.assertEqual(p.rotate([[1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 0, 1], [1, 1, 1, 0]]), [
                         [1, 0, 1, 1], [1, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 1]])
        self.assertEqual(p.rotate_sol([1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1], 90), [
                         0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1])

    def test_arraying(self):
        p = NQueensProblem(2)
        self.assertEqual(p.to_array([True, False, True, False]), [
                         [True, False], [True, False]])
        self.assertEqual(p.rotate([[1, 1], [1, 0]]), [[1, 1], [0, 1]])
        self.assertEqual(p.unarray([[1, 1], [1, 0]]), [1, 0, 1, 1])

    def test_unique_solutions(self):
        p = NQueensProblem(8)
        self.assertEqual(len(p.get_all_unique_solutions()), 12)

if __name__ == "__main__":
    unittest.main()
