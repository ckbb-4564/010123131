from expression import Expression
from read_file import read_file

class Truthtable(Expression):
    
    def __init__(self, infix):
        super().__init__(infix)
        self.operand = []
        self.operand_size = 0
        self.operand_value = {}
        self.operation_group = []
        self.operation_truth = []
        self.prob = None
        self.sample_space = None
        self.bit = None
        self.operation_value = {}
        self.group_len = []
   
    def count_operand(self):
        self.infix_to_postfix()
        for item in self.postfix:
            
            if not self.is_operator(item) and item not in '01':
                
                if item not in self.operand:
                    self.operand.append(item)
                    self.operand_size += 1
        
        self.operand.sort()
        
        for item in self.operand:
            self.operand_value[item] = None
    
    def create_bit(self):
        self.count_operand()
        self.prob = 2 ** self.operand_size
        self.sample_space = [None] * self.prob
        self.bit = bin(self.prob - 1).replace('0b', '')
        
        for i in range(0, self.prob):
            binary = bin(i).replace('0b', '')
            
            if len(binary) == len(self.bit):
                self.sample_space[i] = list(binary)
            
            else:
                bit_diff = len(self.bit) - len(binary)
                zeroes = '0' * bit_diff
                binary = zeroes + binary
                self.sample_space[i] = list(binary)
    
    def create_operation_group(self, root):
        if root.left == None and root.center == None and root.right == None:
            return root.value
        else:
            if self.is_negation(root.value):
                center = self.create_operation_group(root.center)
                temp = root.value + '(' + center + ')'
                self.operation_group.append(temp)

                return temp
            
            elif self.is_operator(root.value):    
                left = self.create_operation_group(root.left)
                right = self.create_operation_group(root.right)
                temp = '(' + left + root.value + right + ')'
                self.operation_group.append(temp)

                return temp

    def format_operation_group(self):
        for i in range(len(self.operation_group)):
            state = True
            temp = self.operation_group[i]
                
            if temp[0] == '(':
                temp = temp[1:-1]
            
            self.operation_group[i] = temp
        
        for item in self.operation_group:
            self.operation_value[item] = None
    
    def solve(self, root):
        if root.left == None and root.center == None and root.right == None:
            return root.value
        
        else:
            if self.is_negation(root.value):
                center = self.solve(root.center)
                temp = str(int(not int(center)))
                self.operation_truth.append(temp)

                return temp
            
            elif self.is_operator(root.value):    
                left = self.solve(root.left)
                right = self.solve(root.right)
                if root.value == '+':
                    temp = str(int(left) or int(right)) 
                elif root.value == '&':
                    temp = str(int(left) and int(right))
                self.operation_truth.append(temp)

                return temp
    
    def create_table(self):
        self.count_operand()
        self.create_bit()
        self.create_tree(self.postfix)
        self.create_operation_group(self.expression_tree)
        self.format_operation_group()
        self.group_len = []

        temp_list = self.postfix
        for item in self.operand_value:
            print('| ' + item + ' |',end='')
        
        for item in self.operation_group:
            print('| ' + item + ' |',end='')
            self.group_len.append(len(item))

        for sample in self.sample_space:
            print()
            self.operation_truth = []
            for i in range(len(self.operand)):
                self.operand_value[self.operand[i]] = sample[i]
                
                for j in range(len(temp_list)):
                    
                    if self.operand[i] == temp_list[j]:
                        temp_list[j] = self.operand_value[self.operand[i]]
                
                print('| ' + self.operand_value[self.operand[i]] + '  |',end='')
        
            self.create_tree(temp_list)
            self.solve(self.expression_tree)
            for i in range(len(self.operation_truth)):
                front_space = self.group_len[i] // 2
                back_space = self.group_len[i] - front_space - 1
                print('| '+ ' ' * front_space + self.operation_truth[i] + ' ' * back_space + ' |',end='')

if __name__ == '__main__':

    read_path = r'Expression.txt' #FULL PATH TO READ FILE
    data = read_file(read_path)

    for line in data:
        print(line)
        truth_table = Truthtable(line)
        truth_table.create_table()
        print()
        print()
