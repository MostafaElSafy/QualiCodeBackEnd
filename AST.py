import ast

def count_nested_structures(code):
    tree = ast.parse(code)
    
    class StructureVisitor(ast.NodeVisitor):
        def __init__(self):
            self.nested_loops = 0
            self.nested_ifs = 0
            self.nested_whiles = 0
            self.nested_fors = 0
            self.current_depth = 0

        def visit_For(self, node):
            self.current_depth += 1
            self.nested_loops = max(self.nested_loops, self.current_depth)
            self.nested_fors += 1
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_While(self, node):
            self.current_depth += 1
            self.nested_loops = max(self.nested_loops, self.current_depth)
            self.nested_whiles += 1
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_If(self, node):
            self.current_depth += 1
            self.nested_ifs = max(self.nested_ifs, self.current_depth)
            self.generic_visit(node)
            self.current_depth -= 1

    visitor = StructureVisitor()
    visitor.visit(tree)
    
    return {
        'nested_loops': visitor.nested_loops,
        'nested_ifs': visitor.nested_ifs,
        'nested_whiles': visitor.nested_whiles,
        'nested_fors': visitor.nested_fors
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
print("Number of nested ifs:", result['nested_ifs'])
print("Number of nested while loops:", result['nested_whiles'])
print("Number of nested for loops:", result['nested_fors'])