import math
import matplotlib.pyplot as plt

class Matrix:
    """ Matrix Class for creating a matrices that we can then manipulate with basic functions
    
    Attributes:
        numbers: List of all numeric values in matrix. No row/column structure
        row: Number of rows in matrix
        col: Number of columns in matrix
    """
    def __init__(self, numbers, rows, columns):
        self.numbers = numbers  
        self.row = rows
        self.col = columns
        try:
            self.check_if_real_matrix()
        except AssertionError as error:
            raise
    

    def check_if_real_matrix(self):
        """Function to check if newly created matrix is a real/valid matrix
        Args: 
            None
        
        Returns: 
            None
        """
        if (self.row*self.col) != len(self.numbers):
            raise Exception('Uneven matrix. Number or rows and columns does not match input')

    def display_matrix(self):
        """ Function to print out the matrix in the proper format
        Args: 
            None
        
        Returns: 
            output of matrix
        """
        for i in range(self.row):
            index = i*self.col
            print(self.numbers[index:(index+self.col)])
    
    def __add__(self, other):
        """Function to calculate the addition of two matrices
        Args: 
            None
        
        Returns: 
            New matrix with values of the two matrices added together
        """
        if (self.row != other.row or self.col != other.col):
            raise Exception('Matrix not the same sizes')
        new_numbers = []
        for i in range(len(self.numbers)):
            new_numbers.append(self.numbers[i] + other.numbers[i])
        
        new_matrix = Matrix(new_numbers, self.row, self.col)
        return new_matrix

    def __sub__(self, other):
        """Function to calculate the difference of two matrices
        Args: 
            None
        
        Returns: 
            New matrix with values of the difference between the first and second matrix
        """
        if (self.row != other.row or self.col != other.col):
            raise Exception('Matrix not the same sizes')
        new_numbers = []
        for i in range(len(self.numbers)):
            new_numbers.append(self.numbers[i] - other.numbers[i])
        
        new_matrix = Matrix(new_numbers, self.row, self.col)
        return new_matrix

    def __mul__(self, other):
        """Function to calculate a matrix multiplied by a number or another matrix
        Args: 
            None
        
        Returns: 
            New matrix with values of the two values multiplied together
        """
        # For multiplication by integer or float values
        if (isinstance(other,float) == True) or (isinstance(other,int) == True):
            new_numbers = [i * other for i in self.numbers]
            new_matrix = Matrix(new_numbers, self.row, self.col)
            return new_matrix
         
        # For multiplication by other matrix objects
        if (self.col != other.row):
            raise Exception('Matrix sizes not complient with multiplication laws')
        new_numbers = []
        # new shape will be self.row by other.col
        for i in range(self.row):
            index = i*self.col
            temp_list = self.numbers[index:(index+self.col)]
            for k in range(other.col):
                temp_list2 = other.numbers[k::other.col]
                val = 0
                for l in range(len(temp_list)):
                    val = val + temp_list[l]*temp_list2[l]
                new_numbers.append(val)

        new_matrix = Matrix(new_numbers, self.row, other.col)
        return new_matrix
    
'''
matrix = Matrix([1,1,2,3,3,4], 3,2)
matrix2 = Matrix([1,1,1,1], 2,2)
matrix3 = matrix2 * 2
matrix3.display_matrix()
print('\n')
matrix4 = matrix*matrix2
matrix4.display_matrix()
'''

       
    