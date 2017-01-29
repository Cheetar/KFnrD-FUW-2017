import n_queens


class TestNQueenProblem(object):

    def Test_get_num():
        p = NQueensProblem(8)
        assert(p.get_num(1, 1) == 1)
        assert(p.get_num(2, 5) == 13)
        assert(p.get_num(8, 8) == 64)
