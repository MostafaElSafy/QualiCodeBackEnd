import ast

def count_nested_structures(code):
    tree = ast.parse(code)
    
    class StructureVisitor(ast.NodeVisitor):
        def __init__(self):
            self.nested_loops = 0
            self.nested_ifs_inside_loops = 0
            self.nested_ifs_outside_loops = 0
            self.for_loops_count = 0
            self.while_loops_count = 0
            self.current_depth = 0
            self.is_outer_loop = True

        def visit_For(self, node):
            if self.is_outer_loop:
                self.nested_loops += 1
                self.is_outer_loop = False

            self.for_loops_count += 1
            self.current_depth += 1
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_While(self, node):
            self.nested_loops += 1
            self.while_loops_count += 1
            self.current_depth += 1
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_If(self, node):
            if self.current_depth > 0:
                self.nested_ifs_inside_loops += 1
            else:
                self.nested_ifs_outside_loops += 1
            self.current_depth += 1
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_Else(self, node):
            # Additional handling for the 'else' clause
            self.generic_visit(node)

    visitor = StructureVisitor()
    visitor.visit(tree)
    
    return {
        'nested_loops': visitor.nested_loops,
        'nested_ifs_inside_loops': visitor.nested_ifs_inside_loops,
        'nested_ifs_outside_loops': visitor.nested_ifs_outside_loops,
        'for_loops_count': visitor.for_loops_count,
        'while_loops_count': visitor.while_loops_count,
    }

# Example usage
code_example = """
num = 337

if num > 1:
   for i in range(2, num//2 + 1):
       if (num % i) == 0:
           print(num,"is not a prime number")
           print(f"{i} times {num//i} is {num}")
           break
   else:
       print(f"{num} is a prime number")

else:
   print(f"{num} is not a prime number")
"""

result = count_nested_structures(code_example)
print("Number of nested loops:", result['nested_loops'])
print("Number of 'if' conditions:", result['nested_ifs_inside_loops']+result['nested_ifs_outside_loops'])
print("Number of 'for' loops:", result['for_loops_count'])
print("Number of 'while' loops:", result['while_loops_count'])
