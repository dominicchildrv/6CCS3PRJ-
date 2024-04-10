
import re

class BooleanFormula:
    def __init__(self):
        self.clauses = []


    # Adds a clause to the formula
    def add_clause(self, *literals):
        valid_literals = [lit for lit in literals if self.validate_literal(lit)]
        if not valid_literals:
            return False  # Indicate failure due to invalid literals
        clause = valid_literals
        if clause not in self.clauses:
            self.clauses.append(clause)
            return True  # Clause added successfully
        return False  # Clause was not added

    def validate_literal(self, literal):
        # literal must contain at least one alphabetic character
        # and may optionally start with '~' and include numbers.
        if re.match(r'^~?[A-Za-z]+\w*$', literal):
            return True
        else:
            print(f"Invalid literal: {literal}")
            return False

    def print_formula(self):
        print(self.to_string())

    def print_clause_list(self):
        print(self.clauses)

    def return_clause_list(self):
        return self.clauses

    def to_string(self):
        # Returns a string representation of the formula
        return " AND ".join(["(" + " OR ".join(clause) + ")" for clause in self.clauses])
