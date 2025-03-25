# ============================================================================
# Author      : Milton Francisco
# Version     : 1.1
# Description : Advising Assistance Program
# ============================================================================
import csv

class Course:
    def __init__(self, course_title, prereqs=None):
        self.course_title = course_title
        self.prereqs = prereqs if prereqs is not None else []
    
    def __str__(self):
        prereq_str = ", ".join(self.prereqs) if self.prereqs else "None"
        return f"{self.course_title}\nPrerequisites: {prereq_str}"

class AVLNode:
    def __init__(self, key, value):
        self.key = key            # Course number
        self.value = value        # Course object
        self.left = None
        self.right = None
        self.height = 1

# -------------------------------
# AVL Tree
# -------------------------------
class AVLTree:
    def __init__(self):
        self.root = None
    
    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        
        # Perform rotation
        x.right = y
        y.left = T2
        
        # Update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        
        return x
    
    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        
        # Perform rotation
        y.left = x
        x.right = T2
        
        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        
        return y
    
    # Root Node Insertion
    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)
    
    # Recursive insertion of a node in the subtree 
    def _insert(self, node, key, value):
        # Normal BST insertion
        if not node:
            return AVLNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node
        
        # Update the node's height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        
        # Check the balance factor to see if this node addition caused imbalance
        balance = self.get_balance(node)
        
        #Rotations
        if balance > 1:
            #Left-Left Case
            if key < node.left.key:
                return self.right_rotate(node)
            # Left-Right Case
            else:
                node.left = self.left_rotate(node.left) #Change to Left-Left Case
                return self.right_rotate(node)
        if balance < -1:
            # Right-Right Case
            if key > node.right.key:
                return self.left_rotate(node)
            # Right-Left Case
            else:
                node.right = self.right_rotate(node.right) #Change to Right-Right Case
                return self.left_rotate(node)
        
        return node
    
    def search(self, key):
        return self._search(self.root, key)
    
    # Recursive search for a key
    def _search(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    
    # Prints all of the course numbers & titles in order
    def in_order_traversal(self, node):
        if node:
            self.in_order_traversal(node.left)
            print(node.key, " - " , node.value.course_title)
            self.in_order_traversal(node.right)
    
    # Hidden function to ensure tree structure populates correctly
    def print_tree_structure(self, node=None, level=0):
        if node is None:
            return
        self.print_tree_structure(node.right, level + 1)
        print("          " * level + f"{node.key} (H={node.height})") # Displays visual representation of tree structure
        self.print_tree_structure(node.left, level + 1)
            
# -------------------------------
# File Verification
# -------------------------------
def load_courses(file_name):
    courses = {}
    try:
        with open(file_name, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Each row must have at least course number and title.
                if len(row) < 2:
                    raise ValueError("Improper file format: Each line must have at least 2 parameters (course number and title).")
                course_number = row[0].strip().upper()
                course_title = row[1].strip()
                
                # Any additional fields are prerequisites
                prereqs = [pr.strip() for pr in row[2:] if pr.strip() != '']

                courses[course_number] = Course(course_title, prereqs)

        # Check if all prereqs are valid course numbers in the file
        missing_prereqs = {pr for course in courses.values() for pr in course.prereqs if pr not in courses}

        if missing_prereqs:
            print(f"Missing prerequisite(s): {', '.join(missing_prereqs)}")
            raise ValueError("Improper file format: Some prerequisites do not have a corresponding course in the file.") 
    except FileNotFoundError:
        raise FileNotFoundError("Could not open input file.")
    
    return courses

# -------------------------------
# Main function
# -------------------------------
def main():
    print("*" * 31)
    print("* Advising Assistance Program *")
    print("*" * 31)
    print()
    
    while True:
        file_name = input("Please enter the file name that contains the course data (or type 'exit' to exit): ")
        if file_name.lower() == "exit":
            print("Good bye.")
            return
        try:
            print("Loading courses...")
            courses = load_courses(file_name)
            break
        except Exception as e:
            print(e)
            print("Please try again or type 'exit' to quit.\n")
    
    # Build the AVL tree
    tree = AVLTree()
    for course_number, course in courses.items():
        tree.insert(course_number, course)
    
    print("\nWelcome to the course planner.")
    
    # Main Menu
    while True:
        print("\nMain Menu:")
        print("  1. Print Course List")
        print("  2. Find Specific Course Details")
        print("  9. Exit")
        choice = input("\nWhat would you like to do? ")
        
        if choice == "1":
            # In-order traversal prints courses in sorted order.
            print("\nCourse List:")
            tree.in_order_traversal(tree.root)

            input("\nPress Enter to continue...")
        
        elif choice == "2":
            course_choice = input("What course do you want to know about? ").upper().strip()
            course = tree.search(course_choice)
            if course:
                print("\nCourse Details:")
                print(course.key, "- ", course.value)
                
            else:
                print(f"Course {course_choice} not found.")
                   
            input("\nPress Enter to continue...")

        elif choice == "3":
            # Hidden choice to display tree structure
            tree.print_tree_structure(tree.root)
            input("\nPress Enter to continue...")
        
        elif choice == "9":
            print("Thank you for using the course planner!")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
