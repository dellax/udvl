#!/bin/env python3

import traceback
import time
import itertools

"""
    Testovaci program pre toCnf
"""


""" Nastavte na True ak chcete aby testy zastali na prvej chybe. """
stopOnError = False

""" Ci testovat aj 'tazsie' formuly, uzitocne, ak nechcete aby testy bezali dlho. """
tazsie = True

""" Ci testovat aj 'tazke' formuly, ktore pri jednoduchej implementacii nezbehnu. """
tazkeEquiv = False

from cnf import VariableMap, Cnf, CnfClause, CnfLit
from formula import Formula, Variable, Negation, Conjunction, Disjunction, Implication, Equivalence

def printException():
    print('ERROR: Exception raised in toCnf:\n%s\n%s\n%s' % (
        '-'*20,
        traceback.format_exc(),
        '-'*20)
    )

def now():
    try:
       return time.perf_counter() # >=3.3
    except AttributeError:
       return time.time() # this is not monotonic!

class FailedTestException(BaseException):
    pass

class Tester(object):
    def __init__(self):
        self.tested = 0
        self.passed = 0
        self.case = 0
        self.equiv = 0
        self.size = 0
        self.time = 0

    def compare(self, result, expected, msg):
        self.tested += 1
        if result == expected:
            self.passed += 1
            return True
        else:
            print("Failed: %s:" %  msg)
            print("    got %s  expected %s" % (repr(result), repr(expected)))
            print("")
            return False

    def status(self):
        print("TESTED %d" % (self.tested,))
        print("PASSED %d" % (self.passed,))
        print("SUM(equiv) %d" % (self.equiv,))
        print("SUM(time) %f" % (self.time,))
        print("SUM(size) %d" % (self.size,))
        if self.tested == self.passed:
            print("OK")
        else:
            print("ERROR")

    def cnfLitEval(self, lit, i):
        return bool(lit.neg) ^ bool(i[lit.name])

    def cnfClauseEval(self, cls, i):
        return any(self.cnfLitEval(l, i) for l in cls)

    def cnfEval(self, cnf, i):
        return all(self.cnfClauseEval(cls, i) for cls in cnf)

    def formulaDeg(self, f):
        if isinstance(f, Variable):
            return 0
        return sum(self.formulaDeg(sf) for sf in f.subf()) + 1

    def cnfSize(self, cnf):
        return sum(len(cls) for cls in cnf)

    def formulaEval(self, f, i):
        if   isinstance(f, Variable):
            return i[f.name]
        elif isinstance(f, Negation):
            return not self.formulaEval(f.subf()[0], i)
        elif isinstance(f, Conjunction):
            return all(self.formulaEval(sf, i) for sf in f.subf())
        elif isinstance(f, Disjunction):
            return any(self.formulaEval(sf, i) for sf in f.subf())
        elif isinstance(f, Implication):
            return  (not self.formulaEval(f.subf()[0], i)) or self.formulaEval(f.subf()[1], i)
        elif isinstance(f, Equivalence):
            return self.formulaEval(f.subf()[0], i) == self.formulaEval(f.subf()[1], i)
        else:
            raise TypeError("Formula expected, got %s" % repr(f))

    def formulaVars(self, f):
        """ List variables in formula f.

        This depends on correct implementation of subf() and Variable.name.
        """
        if isinstance(f, Variable):
            return set([f.name])
        return set.union(*( self.formulaVars(sf) for sf in f.subf() ))

    def cnfVars(self, cnf):
        """ List variables in the Cnf formula cnf. """
        s = set()
        for cl in cnf:
            for lit in cl:
                s.add(lit.name)
        return s

    def interpretations(self, vars):
        """ Generate all possible interpretations for vars. """
        vars = list(vars)
        ss = len(vars)
        i = dict((v,False) for v in vars)
        yield i
        for case in range(1,2**ss):
            x = 0
            while (x < ss) and (i[vars[x]]):
                i[vars[x]] = False
                x += 1
            i[vars[x]] = True
            yield i

    def satisfiableFormula(self, f):
        """ Return True if f is satisfiable. """
        return any(self.formulaEval(f, i) for i in self.interpretations(self.formulaVars(f)))

    def satisfiableCnf(self, cnf):
        """ Return True if cnf is satisfiable. """
        return any(self.cnfEval(cnf, i) for i in self.interpretations(self.cnfVars(cnf)))


    def test(self, f):
        self.case += 1
        self.tested += 1
        print("CASE %d: %s" % (self.case, f.toString()))
        cnf = CnfClause()
        try:
            start = now()
            cnf = f.toCnf()
            duration = now() - start
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except:
            printException()
            if stopOnError:
                raise FailedTestException()
            return

        deg = self.formulaDeg(f)
        size = self.cnfSize(cnf)

        print('CNF: time: %12.9f   f.deg: %3d   cnf.size: %3d' %
                (duration, deg, size))

        if not isinstance(cnf, Cnf):
            print('FAILED: not a Cnf: %s' % type(cnf))
            print()
            return

        start = now()
        equiSatisfiable = self.satisfiableFormula(f) == self.satisfiableCnf(cnf)
        equivalent = self.formulaVars(f).issubset(self.cnfVars(cnf)) and \
                all(self.formulaEval(f, i) == self.cnfEval(cnf, i) for i in self.interpretations(self.cnfVars(cnf)))
        duration = now() - start

        if equivalent:
            self.equiv += 1

        self.size += size
        self.time += duration

        if equiSatisfiable:
            self.passed += 1
            print('PASSED: testTime: %12.9f    equiSatisfiable %s' %
                    (duration, 'equivalent' if equivalent else ''))
        else:
            if len(cnf) < 20:
                print('FAILED: \n-----CNF-----\n%s%s' % (cnf.toString(), '-'*13))
            else:
                print('FAILED: \n-----CNF-----\n%s...\n%s' % (Cnf(cnf[:20]).toString(), '-'*13))
            if stopOnError:
                raise FailedTestException()
        print()

    def test2(self, f):
        self.test(f)
        self.test(Negation(f))



t = Tester()

Not = Negation
Var = Variable
Impl = Implication

def And(*args):
    if len(args)==1 and type(args[0]) is list:
        return Conjunction(args[0])
    return Conjunction(args)
def Or(*args):
    if len(args)==1 and type(args[0]) is list:
        return Disjunction(args[0])
    return Disjunction(args)

a = Var('a')
b = Var('b')
c = Var('c')
d = Var('d')


try:
    t.test2(a)

    t.test2(Not(a))

    t.test2(
            Conjunction([
                a,
                b,
            ]))

    t.test2(
            Conjunction([
                Not(a),
                a,
            ]))

    t.test2(
            Conjunction([
                a,
                Not(a),
            ]))

    t.test2(
            Conjunction([
                Not(a),
                Not(a),
            ]))

    t.test2(
            Disjunction( [ a, b ] )
            )

    t.test2(
            Implication( a, b )
            )

    t.test2(
            Equivalence( a, b )
            )

    t.test2(
            Disjunction([
                Negation(Implication(a,b)),
                Negation(Implication(b,a))
            ]))

    t.test2(
            Conjunction([
                Implication(a,b),
                Implication(Negation(a),c)
            ]))

    t.test2(
            Equivalence(
                Conjunction([
                    a,
                    Negation(b)
                ]),
                Disjunction([
                    a,
                    Implication(
                        b,
                        a
                    )
                ])
            ))


    # veeela premennych (no mozno nie az tak vela)
    nvars=17
    t.test2(Conjunction( [ Var(str(i)) for i in range(nvars) ] ))

    t.test2(Disjunction( [ Var(str(i)) for i in range(nvars) ] ))


    # some fun
    V = 3
    S = 2
    t.test2(
            Conjunction([
                Disjunction(vars)
                    for vars in itertools.permutations(
                        [Var(str(i)) for i in range(V)], S)
            ]))

    # toto by bolo faaaakt vela s test2 ;)
    t.test(
            Disjunction([
                Conjunction(vars)
                    for vars in itertools.permutations(
                        [Var(str(i)) for i in range(V)], S)
            ]))

    t.test2(
            Conjunction([
                Not(Disjunction(vars))
                    for vars in itertools.permutations(
                        [Var(str(i)) for i in range(V)], S)
            ]))

    # toto by bolo faaaakt vela s test2 ;)
    t.test(
            Disjunction([
                Not(Conjunction(vars))
                    for vars in itertools.permutations(
                        [Var(str(i)) for i in range(V)], S)
            ]))


    t.test(Not(Impl(a,a)))
    t.test(Not(Impl(a,Impl(b,a))))
    t.test(
        Not(Impl(
            Impl(a,Impl(b,c)),
            Impl(
                Impl(a,b),
                Impl(a,c)
            )
        )))
    t.test(Not(Impl(Impl(Not(a),Not(b)),Impl(b,a))))
    t.test(Not(Impl(Not(a),Impl(a,b))))

    t.test(Not(Equivalence(
        Not(And([a,b])),
        Or([Not(a),Not(b)])
        )))
    t.test(Not(Equivalence(
        Not(Or([a,b])),
        And([Not(a),Not(b)])
        )))
    t.test(
        Conjunction([
            Not(Or([a,b])),
            Not(And([Not(a),Not(b)]))
        ]))

    t.test(And(
        Or(
            Or(a,And(b,c)),
            And(Or(a,b),Or(a,c))
        ),
        Or(
            Not(Or(a,And(b,c))),
            Not(And(Or(a,b),Or(a,c)))
        )))

    t.test(And(
        Or(
            And(a,Or(b,c)),
            Or(And(a,b),And(a,c))
        ),
        Or(
            Not(And(a,Or(b,c))),
            Not(Or(And(a,b),And(a,c)))
        )))

    t.test(And(
        Or(
            Or(a,(Impl(b,c))),
            Impl(Or(a,b),Or(a,c))
        ),
        Or(
            Not(Or(a,(Impl(b,c)))),
            Not(Impl(Or(a,b),Or(a,c)))
        )))

    t.test(And(
        Or(
            Impl(a,Impl(b,c)),
            Impl(Impl(a,b),Impl(a,c))
        ),
        Or(
            Not(Impl(a,Impl(b,c))),
            Not(Impl(Impl(a,b),Impl(a,c)))
        )))

    if tazsie:
        t.test(Not(Impl(
            Or(a,And(b,c)),
            And(Or(a,b),Or(a,c))
            )))
        t.test(Not(Impl(
            And(a,Or(b,c)),
            Or(And(a,b),And(a,c))
            )))

        t.test(Not(Impl(
            Or(a,(Impl(b,c))),
            Impl(Or(a,b),Or(a,c))
            )))
        t.test(Not(Impl(
            Impl(a,Impl(b,c)),
            Impl(Impl(a,b),Impl(a,c))
            )))

    if tazkeEquiv:
        t.test(Not(Equivalence(
            Or(a,And(b,c)),
            And(Or(a,b),Or(a,c))
            )))
        t.test(Not(Equivalence(
            And(a,Or(b,c)),
            Or(And(a,b),And(a,c))
            )))

        t.test(Not(Equivalence(
            Or(a,(Equivalence(b,c))),
            Equivalence(Or(a,b),Or(a,c))
            )))
        t.test(Not(Equivalence(
            Impl(a,Equivalence(b,c)),
            Equivalence(Impl(a,b),Impl(a,c))
            )))

    t.test(Not(Equivalence(
        Or(a,Or(b,c)),
        Or(Or(a,b),c)
        )))
    t.test(Not(Equivalence(
        And(a,And(b,c)),
        And(And(a,b),c)
        )))


    t.test(Not(Equivalence(
        Impl(a, Impl(b, c)),
        Impl(b, Impl(a, c))
        )))

    t.test(Not(Equivalence(
        And(a, b),
        And(b, a)
        )))
    t.test(Not(Equivalence(
        Or(a, b),
        Or(b, a)
        )))

    t.test(Not(Impl(a,Or(a,b))))


    th1 = Conjunction([
        Impl(Var('dazdnik'), Not(Var('prsi'))),
        Impl(
            Var('mokraCesta'),
            Or( [ Var('prsi'), Var('umyvacieAuto') ] ),
        ),
        Impl(Var('umyvacieAuto'), Not(Var('vikend'))),
    ])

    t.test(th1)

    t.test(
            Conjunction([
                th1,
                Not(
                    Impl(
                        And( [ Var('dazdnik'), Var('mokraCesta') ] ),
                        Not(Var('vikend')),
                    )
                ),
            ]))

    th2 = Conjunction([
        Impl(Var('kim'), Not(Var('sarah'))),
        Impl(Var('jim'), Var('kim')),
        Impl(Var('sarah'), Var('jim')),
        Or([Var('kim'), Var('jim'), Var('sarah')]),
    ])

    t.test(And(th2, Not(Var('sarah'))))
    t.test(And(th2, Not(Var('kim'))))

    print("END")

except FailedTestException:
    print("Stopped on first failed test!")
finally:
    t.status()

# vim: set sw=4 ts=4 sts=4 et :
