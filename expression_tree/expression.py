#Expression class
class Expression:
    
    class Stack:
        
        def __init__(self):
            self.stacklist = []
            self.size = 0

        def push(self,item):
            self.stacklist.append(item)
            self.size += 1
        
        def pop(self):
            item = self.stacklist.pop()
            self.size -= 1
            return item

        def top(self):
            item = self.stacklist[-1]
            return item
        
        def is_empty(self):
            state = self.size == 0
            return state

    class Expression_Tree:    
        
        def __init__(self, value, left=None, center=None, right=None):
            self.value = value
            self.left = left
            self.center = center
            self.right = right
    
    def __init__(self,infix):
        self.infix = list(infix.replace(' ',''))
        self.operator_stack = self.Stack()
        self.tree_stack = self.Stack()
        self.precedence = {'!':4, '&':3, '+':2, '(':1}
        self.postfix = []
        self.pre_order_list = []
        self.expression_tree = None

    def is_number(self, token):
        number = '0123456789'
        return token in number
    
    def is_alphabet(self, token):
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return token in alphabet
    
    def is_openbracket(self, token):
        return token == '('
    
    def is_closebracket(self, token):
        return token == ')'
    
    def is_negation(self, token):
        return token == '!'

    def is_operator(self, token):
        operator = '!&+'
        return token in operator

    def is_operand(self, token):
        return not self.is_operator(token) 
    
    def infix_to_postfix(self):
        operand = ''
        temp = ''
        
        for item in self.infix:
            
            if self.is_alphabet(item) or self.is_number(item):
                temp = item
                operand += temp
            
            else:
                
                if operand !='':
                    self.postfix.append(operand)
                    operand = ''
                
                if self.is_openbracket(item):
                    self.operator_stack.push(item)
                
                elif self.is_closebracket(item):
                    token = self.operator_stack.pop()
                    
                    while not self.is_openbracket(token):
                        self.postfix.append(token)
                        token = self.operator_stack.pop()
                
                elif self.is_operator(item):
                    
                    if self.operator_stack.is_empty():
                        self.operator_stack.push(item)
                    
                    else:
                        token = self.operator_stack.top()
                        
                        if self.precedence[item] > self.precedence[token]:
                            self.operator_stack.push(item)
                        
                        else:
                            state = True
                            
                            while (not self.operator_stack.is_empty()) and self.precedence[item] < self.precedence[token] and state:
                                temp = self.operator_stack.pop()
                                
                                if not self.operator_stack.is_empty():
                                    token = self.operator_stack.top()
                                
                                else:
                                    state = False
                                
                                self.postfix.append(temp)
                            
                            self.operator_stack.push(item)
        
        while not self.operator_stack.is_empty():
            token = self.operator_stack.pop()
            self.postfix.append(token)
    
    def create_tree(self):
        for item in self.postfix:

            if self.is_negation(item):
                center_child = self.tree_stack.pop()
                tree = self.Expression_Tree(item)
                tree.center = center_child
                self.tree_stack.push(tree)
            
            elif self.is_operator(item):
                right_child = self.tree_stack.pop()
                left_child = self.tree_stack.pop()
                tree = self.Expression_Tree(item)
                tree.left = left_child
                tree.right = right_child
                self.tree_stack.push(tree)
            
            else:
                tree = self.Expression_Tree(item)
                self.tree_stack.push(tree)
        
        self.expression_tree = self.tree_stack.pop()
    
    def pre_order(self, root):
        if root:
            self.pre_order_list.append(root.value)
            self.pre_order(root.left)
            self.pre_order(root.center)
            self.pre_order(root.right)
        
        else:
            pass