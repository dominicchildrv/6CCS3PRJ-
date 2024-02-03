

class BooleanFormula:

    def __init__(self):
        #list of clauses
        self.clauses = []

    def add_clause(self, *literals):
        #Checks that the clauses isn't in the list already
        clause = list(literals)
        if clause not in self.clauses:
            self.clauses.append(clause)

    def print_formula(self):
        # Print each clause with AND between them
        print(" AND ".join(["(" + " OR ".join(map(str, clause)) + ")" for clause in self.clauses]))

    def print_clause_list(self):
        print(self.clauses)