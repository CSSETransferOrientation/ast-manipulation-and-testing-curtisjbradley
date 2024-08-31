#!/usr/bin/python3

import os
from os.path import join as osjoin
import unittest

from enum import Enum

# Use these to distinguish node types, note that you might want to further
# distinguish between the addition and multiplication operators
NodeType = Enum('BinOpNodeType', ['number', 'operator'])

class BinOpAst():
    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.
    """
    def __init__(self, prefix_list):
        """
        Initialize a binary operator AST from a given list in prefix notation.
        Destroys the list that is passed in.
        """
        self.val = prefix_list.pop(0)
        if self.val.isnumeric():
            self.type = NodeType.number
            self.left = False
            self.right = False
        else:
            self.type = NodeType.operator
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)

    def __str__(self, indent=0):
        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """
        ilvl = '  '*indent
        left = '\n  ' + ilvl + self.left.__str__(indent+1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent+1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def prefix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

    def infix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'
    def postfix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

    def additive_identity(self):
        if(self == False or self.type is NodeType.number):
            return
        BinOpAst.additive_identity(self.left)
        BinOpAst.additive_identity(self.right)
        if self.type == NodeType.operator and self.val == "+":
            if self.left.val == "0":
                r = self.right
                self.val = r.val
                self.type = r.type
                self.left = r.left
                self.right = r.right
            elif self.right.val == "0":
                l = self.left
                self.val = l.val
                self.type = l.type
                self.left = l.left
                self.right = l.right
                        
    def multiplicative_identity(self):
        if(self == False or self.type is NodeType.number):
            return
        BinOpAst.multiplicative_identity(self.left)
        BinOpAst.multiplicative_identity(self.right)
        if self.type == NodeType.operator and self.val == "*":
            if self.left.val == "1":
                r = self.right
                self.type = r.type
                self.val = r.val
                self.right = r.right
                self.left = r.left
            elif self.right.val == "1":
                l = self.left
                self.type = l.type
                self.val = l.val
                self.left = l.left
                self.right = l.right
    
    
    def mult_by_zero(self):
        if(self == False or self.type is NodeType.number):
            return
        if self.type == NodeType.operator and self.val == "*":
            if self.left.val == "0" or self.right.val == "0":
                self.left = False
                self.right = False
                self.val = "0"
                self.type = NodeType.number

    
    def constant_fold(self):
        if (self == False or self.type is NodeType.number):
            return
        l = self.left
        r = self.right
        BinOpAst.constant_fold(l)
        BinOpAst.constant_fold(r)
        if (l.type == NodeType.number and r.type == NodeType.number):
            self.val = eval(l.val + self.val + r.val)
            self.type = NodeType.number
            self.left = False
            self.right = False
        """
        Fold constants,
        e.g. 1 + 2 = 3
        e.g. x + 2 = x + 2
        """
        # Optionally, IMPLEMENT ME! This is a bit more challenging. 
        # You also likely want to add an additional node type to your AST
        # to represent identifiers.
        pass            

    def simplify_binops(self):
        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """
        self.mult_by_zero()
        self.additive_identity()
        self.multiplicative_identity()
        self.constant_fold()

def test_folder(folder, func):
    for test_name in os.listdir(osjoin("testbench", folder, "inputs")):
        out = ""
        expected = ""
        with open(osjoin("testbench", folder, "inputs", test_name)) as testinput:
            tree = BinOpAst(testinput.read().split("\n"))
            func(tree)
            out = str(tree)
        with open(osjoin("testbench", folder, "outputs", test_name)) as testout:
            expected = testout.read()
        try:
            assert out.strip() == expected.strip()
        except AssertionError:
            raise Exception(f"{folder} - test {test_name} failed.\nExpected:\n{expected}\nReceived:\n{out}") 
   
class Tester(unittest.TestCase):
    def test_arithid(self):
       test_folder("arith_id", BinOpAst.additive_identity) 
    def test_multid(self):
        test_folder("mult_id", BinOpAst.multiplicative_identity)
    def test_simplify(self):
        test_folder("combined", BinOpAst.simplify_binops)
    def test_mult_zero(self):
        test_folder("mult_by_zero", BinOpAst.mult_by_zero)
    def test_fold(self):
        test_folder("constant_fold", BinOpAst.constant_fold)
if __name__ == "__main__":
    unittest.main()
