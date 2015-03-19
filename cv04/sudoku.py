import sys
import os
sys.path[0:0] = [os.path.join(sys.path[0], '../examples/sat')]

import sat

def sud(r, s, c): return int(r*9*9 + s*9 + c);

class SudokuSolver:
    def solve(self, sudoku):
        w = sat.DimacsWriter("sudoku_cnf_in.txt")

        ## zapis uz zadanych cisel
        for r in range(9):
            for s in range(9):
                if sudoku[r][s] > 0:
                    w.writeClause([sud(r, s, sudoku[r][s])])
        
        for r in range(9):
            for s in range(9):
                for c in range(1, 10):
                    w.writeLiteral(sud(r, s, c))
                w.finishClause()
                
        for r in range(9):
            for s in range(9):
                for c1 in range(1, 10):
                    for c2 in range(c1 + 1, 10):
                        w.writeClause([-sud(r,s,c1), -sud(r, s, c2)])

        for r in range(9):
            for s1 in range(9):
                for s2 in range(s1 + 1, 9):
                    for c in range(1, 10):
                        w.writeClause([-sud(r, s1, c), -sud(r, s2, c)])
                        
        for r1 in range(9):
            for r2 in range(r1 + 1, 9):
                for s in range(9):
                    for c in range(1, 10):
                        w.writeClause([-sud(r1, s, c), -sud(r2, s, c)])

        ################################
        for k in range(9):
            for blok_i in range(3):
                for blok_j in range(3):
                    for i in range(blok_i * 3, blok_i * 3 + 3):
                        for j in range(blok_j * 3, blok_j * 3 + 3):
                            w.writeLiteral(sud(i, j, k + 1) )
                    w.finishClause()             
        ##################################                

        ok, sol = sat.SatSolver().solve(w, 'sudoku_cnf_out.txt')

        ret = [[0]*9 for x in range(9)]
        if ok:
            for x in sol:
                if x > 0:
                    x -= 1
                    c = (x % 9) + 1
                    x //= 9
                    s = x % 9
                    x //= 9
                    r = x

                    ret[r][s] = c
        
        return ret
