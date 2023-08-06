from .minisatbind import mklit, var, sign, Solver as _bind_Solver


def lit(v, sign=True):
    return mklit(v, sign)


def to_lit(solver_vars, var):
    if var < 0:
        return -lit(solver_vars[abs(var)])
    return lit(solver_vars[abs(var)])


class Solver:
    def __init__(self):
        self.solver = _bind_Solver()

    def new_var(self):
        return self.solver.new_var()

    def add_clause(self, clause):
        c = list(clause)
        return self.solver.add_clause_vec(c)

    def num_vars(self):
        return self.solver.num_vars()

    def num_clauses(self):
        return self.solver.num_clauses()

    def model_value(self, l):
        return self.solver.model_value(l)

    def solve(self):
        return self.solver.solve()


def create_solver(clauses):
    s = Solver()
    solver_vars = {}
    for clause in clauses:
        for c in clause:
            var = abs(c)
            if var not in solver_vars:
                solver_vars[var] = s.new_var()
        vars_ = [to_lit(solver_vars, var) for var in clause]
        s.add_clause(vars_)
    return s, solver_vars


def parse_dimacs(dimacs):
    clauses = []
    summary = []
    vars_ = set()
    for line in dimacs.split("\n"):
        line = line.strip()
        if not line or line in ("0", "%"):
            continue
        elif line.startswith("c"):
            continue  # comment
        elif line.startswith("p"):
            summary.append(line)
            continue
        else:
            data = line.split()
            for i in range(len(data) - 1):
                try:
                    data[i] = int(data[i])
                    vars_.add(abs(data[i]))
                except ValueError:
                    raise ValueError("Variables must be integers, was {}".format(line))
            if data[-1] != "0":
                raise ValueError("Clause line missing terminating 0")
            clauses.append(data[:-1])
    return clauses, summary, vars_


def create_dimacs_solver(dimacs):
    clauses, summary, vars_ = parse_dimacs(dimacs)
    solver = Solver()
    sat_vars = {}
    for e in vars_:
        sat_vars[e] = solver.new_var()

    def mklit(num):
        if num < 0:
            return -lit(sat_vars[abs(num)])
        return lit(sat_vars[abs(num)])

    for clause in clauses:
        lits = [mklit(c) for c in clause]
        solver.add_clause(lits)

    return clauses, summary, vars_, sat_vars, solver


def pyminisat():
    import sys

    lines = [line for line in sys.stdin]
    clauses, summary, vars_, sat_vars, solver = create_dimacs_solver("\n".join(lines))
    print("\n".join(summary))
    print(solver.solve())
