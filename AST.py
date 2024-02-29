# import ast

# def count_nested_structures(code):
#     tree = ast.parse(code)
#     print(ast.dump(tree, indent=4))
    
#     class StructureVisitor(ast.NodeVisitor):
#         def __init__(self):
#             self.nested_loops = 0
#             self.nested_ifs_inside_loops = 0
#             self.nested_ifs_outside_loops = 0
#             self.for_loops_count = 0
#             self.while_loops_count = 0
#             self.current_depth = 0
#             self.is_outer_loop = True

#         def visit_For(self, node):
#             if self.is_outer_loop:
#                 self.nested_loops += 1
#                 self.is_outer_loop = False

#             self.for_loops_count += 1
#             self.current_depth += 1
#             self.generic_visit(node)
#             self.current_depth -= 1

#         def visit_While(self, node):
#             self.nested_loops += 1
#             self.while_loops_count += 1
#             self.current_depth += 1
#             self.generic_visit(node)
#             self.current_depth -= 1

#         def visit_If(self, node):
#             if self.current_depth > 0:
#                 self.nested_ifs_inside_loops += 1
#             else:
#                 self.nested_ifs_outside_loops += 1
#             self.current_depth += 1
#             self.generic_visit(node)
#             self.current_depth -= 1

#         def visit_Else(self, node):
#             # Additional handling for the 'else' clause
#             self.generic_visit(node)

#     visitor = StructureVisitor()
#     visitor.visit(tree)
    
#     return {
#         'nested_loops': visitor.nested_loops,
#         'nested_ifs_inside_loops': visitor.nested_ifs_inside_loops,
#         'nested_ifs_outside_loops': visitor.nested_ifs_outside_loops,
#         'for_loops_count': visitor.for_loops_count,
#         'while_loops_count': visitor.while_loops_count,
#     }

# # Example usage
# code_example = """
# num = 337

# if num > 1:
#    for i in range(2, num//2 + 1):
#        if (num % i) == 0:
#            print(num,"is not a prime number")
#            print(f"{i} times {num//i} is {num}")
#            break
#    else:
#        print(f"{num} is a prime number")

# else:
#    print(f"{num} is not a prime number")
# """

# result = count_nested_structures(code_example)
# print("Number of nested loops:", result['nested_loops'])
# print("Number of 'if' conditions:", result['nested_ifs_inside_loops']+result['nested_ifs_outside_loops'])
# print("Number of 'for' loops:", result['for_loops_count'])
# print("Number of 'while' loops:", result['while_loops_count'])



# code_example = """
# for i in range(3):
#    if i > 1:
#        while i < 5:
#            print(i)
# """


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
            self.function_definitions = {}  # Dictionary to store function definitions
            self.recursion_count = 0
            self.loop_depth = 0  # Track the depth of nested loops
            self.break_count = 0  # Track the number of break statements
            self.hash_map_count = 0  # Track the number of hash map creations
            self.hash_set_count = 0  # Track the number of hash set creations
            self.priority_queue_count = 0  # Track the number of PriorityQueue creations
            self.sort_count = 0  # Track the number of sorting operations

        def visit_For(self, node):
            self.for_loops_count += 1
            self.loop_depth += 1  # Increment loop depth
            self.nested_loops = max(self.nested_loops, self.loop_depth)  # Update nested loops count
            self.generic_visit(node)
            self.loop_depth -= 1  # Decrement loop depth

        def visit_While(self, node):
            self.while_loops_count += 1
            self.loop_depth += 1  # Increment loop depth
            self.nested_loops = max(self.nested_loops, self.loop_depth)  # Update nested loops count
            self.generic_visit(node)
            self.loop_depth -= 1  # Decrement loop depth

        def visit_If(self, node):
            if self.loop_depth > 0:
                self.nested_ifs_inside_loops += 1
            else:
                self.nested_ifs_outside_loops += 1
            self.generic_visit(node)

        def visit_Break(self, node):
            if self.loop_depth > 0:
                self.break_count += 1
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            # Store function definition in the dictionary
            self.function_definitions[node.name] = node
            self.parent_function = node  # Update parent_function attribute
            self.generic_visit(node)

        def visit_Call(self, node):
            # Check if the function call is recursive
            if isinstance(node.func, ast.Name) and node.func.id in self.function_definitions:
                func_def = self.function_definitions[node.func.id]
                if func_def == self.parent_function:
                    self.recursion_count += 1
                # Check for sorting operations using sorted() function
            if isinstance(node.func, ast.Name) and node.func.id == 'sorted':
                self.sort_count += 1

            # Check for sorting operations using sort() method
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if node.func.attr == 'sort':
                    self.sort_count += 1

            self.generic_visit(node)

        def visit_Dict(self, node):
            # Count dictionary creations
            self.hash_map_count += 1
            self.generic_visit(node)

        def visit_Set(self, node):
            # Count set creations
            self.hash_set_count += 1
            self.generic_visit(node)

        def visit_Name(self, node):
            # Count PriorityQueue creations
            if node.id == 'PriorityQueue':
                self.priority_queue_count += 1
            self.generic_visit(node)

    visitor = StructureVisitor()
    visitor.visit(tree)
    
    return {
        'nested_loops': visitor.nested_loops,
        'nested_ifs_inside_loops': visitor.nested_ifs_inside_loops,
        'nested_ifs_outside_loops': visitor.nested_ifs_outside_loops,
        'for_loops_count': visitor.for_loops_count,
        'while_loops_count': visitor.while_loops_count,
        'recursion_count': visitor.recursion_count,
        'break_count': visitor.break_count,
        'hash_map_count': visitor.hash_map_count,
        'hash_set_count': visitor.hash_set_count,
        'priority_queue_count': visitor.priority_queue_count,
        'sort_count': visitor.sort_count
    }

# Example usage
code_example = """
num = 337
my_dict = {'a': 1, 'b': 2}
my_set = {1, 2, 3}
my_queue = PriorityQueue()

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

my_list = [3, 1, 4, 1, 5, 9]
sorted_list = sorted(my_list)
my_list.sort()
"""

result = count_nested_structures(code_example)
print("Number of nested loops:", result['nested_loops'])
print("Number of 'if' conditions:", result['nested_ifs_inside_loops']+result['nested_ifs_outside_loops'])
print("Number of 'for' loops:", result['for_loops_count'])
print("Number of 'while' loops:", result['while_loops_count'])
print("Number of recursive calls:", result['recursion_count'])
print("Number of break statements:", result['break_count'])
print("Number of hash map creations:", result['hash_map_count'])
print("Number of hash set creations:", result['hash_set_count'])
print("Number of PriorityQueue creations:", result['priority_queue_count'])
print("Number of sorting operations:", result['sort_count'])
