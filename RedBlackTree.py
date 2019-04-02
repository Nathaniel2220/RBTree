# -*- coding: utf-8 -*-
"""
Nathaniel Livingston
Algorithms 361
Fall 2017
Homework 5
Adam Smith
"""


# The node class, contains all the information you will need for a red black tree. For color, True means Red.
class Node:
    
    __slots__ = {'_left', '_right', '_parent', '_key', '_color','_freq'} # the information you'll need

    def __init__(self, parent, key, left, right): # initalize it
        self._right = right
        self._left = left
        self._parent = parent
        self._key = key
        self._color = True
        self._freq = 1    

    # methods for node properties
    def getKey(self):
        return self._key
    def setKey(self, key):
        self._key = key
    def delKey(self):
        del self._key
    def getRight(self):
        return self._right
    def setRight(self, right):
        self._right = right
    def delRight(self):
        del self._right
    def getLeft(self):
        return self._left
    def setLeft(self, left):
        self._left = left
    def delLeft(self):
        del self._left
    def getParent(self):
        return self._parent
    def setParent(self, parent):
        self._parent = parent
    def delParent(self):
        del self._parent
    def getColor(self):
        return self._color
    def setColor(self, color):
        self._color = color
    
    # node properties
    key = property(getKey, setKey, delKey)
    left = property(getLeft, setLeft, delLeft)  
    right = property(getRight, setRight, delRight)
    parent = property(getParent, setParent, delParent)
    color = property(getColor, setColor)

# The Rakdos Tree Class! Self balancing BST.
class RedBlackTree:
    
    __slots__ = {'_root', '_nil', '_size'} # the info you'll need
  
    def __init__(self): # let's begin
        self._nil = Node(None, None, None, None)
        self._nil.parent = self._nil
        self._nil.left = self._nil
        self._nil.right = self._nil
        self._nil.color = False
        self._root = self._nil
        self._size = 0
    
    # inserts a value into the tree, maintains balance
    def put(self, key):
        if (self._root.key == None):
            self._root = Node(self._nil, key, self._nil, self._nil)
            self._root.color = False
        else:
            newNode = Node(self._nil, key, self._nil, self._nil)
            self.insert(newNode)
    
    # returns the node with given key
    def get(self, key):
        node = self.findKey(key, self._root) 
        if (node != None):
            return node
        return None
    
    # returns true iff a node with the given key is in the tree
    def contains(self, key):
        if (self.get(key).getKey() != self._root.getKey() and self.get(key).getKey() != None):
            return True
        else: return False
      
    # deletes a node with the given key, returns false if it's not there
    def delete(self, key):
        if not (self.contains(key)):
            return False
        else:
            self.deleteNode(self.get(key))

    # returns the size of the tree
    def size(self):
        return self._size
  
    # returns true iff the tree is empty
    def isEmpty(self):
        if(self.size() == 0):
            return True
        else: return False
     
    # returns the value of the minimum node
    def getMinKey(self):
        node = self._root
        while(node.left != self._nil):
            node = node._left
        return(node.getKey())
    
    # returns the value of the maximum node
    def getMaxKey(self):
        node = self._root
        while(node.right != self._nil):
            node = node._right
        return(node.getKey())
  
    # returns the key of the predecessor of the given node, or false if there isn't one
    def findPredecessor(self, node):
        current = node
        if (current.left != self._nil):
            current = node._left
            while (current.right != self._nil):
                current = current._right
        while True:
            current = current._parent
            if not current:
                return None
            if (current.getKey() < node.getKey()):
                return current  
            
    # returns the key of the predecessor of the given node, or false if there isn't one
    def findSucessor(self, node):
        current = node
        if (current.right != self._nil):
            current = node._right
            while (current.left != self._nil):
                current = current._left
        while True:
            current = current._parent
            if not current:
                return None
            if (current.getKey() > node.getKey()):
                return current

    # inserts the node into the tree, method for 'put' to use
    def insert(self, node):
        emptyNode = self._nil
        checkNode = self._root
        while (checkNode != self._nil):
            emptyNode = checkNode
            if (node.key < checkNode.key):
                checkNode = checkNode.left
            else:
                checkNode = checkNode.right
        node.parent = emptyNode
        if (emptyNode == self._nil):
            self._root = node
        elif (node.key < emptyNode.key):
            emptyNode.left = node
        else:
            emptyNode.right = node
        self.recoverInsert(node)
        
    # recovers balance after an insert
    def recoverInsert(self, node):
        while (node.parent.color == True): 
            if (node.parent == node.parent.parent.left):
                checkNode = node.parent.parent.right
                if (checkNode.color == True):
                    node.parent.color = False
                    checkNode.color = False
                    node.parent.parent.color = True
                    node = node.parent.parent
                else:
                    if (node == node.parent.right):
                        node = node.parent
                        self.rotateLeft(node)
                    node.parent.color = False
                    node.parent.parent.color = True
                    self.rotateRight(node.parent.parent)
            else:
                checkNode = node.parent.parent.left
                if (checkNode.color == True):
                    node.parent.color = False
                    checkNode.color = False
                    node.parent.parent.color = True
                    node = node.parent.parent
                else:
                    if (node == node.parent.left):
                        node = node.parent
                        self.rotateRight(node)
                    node.parent.color = False
                    node.parent.parent.color = True
                    self.rotateLeft(node.parent.parent)
        self._root.color = False  
    


    # deletes a node, method for 'remove'
    def deleteNode(self, node):
        startColor = node.color
        if (node.left == self._nil):
            fixNode = node.right
            self.swap(node, node.right)

        elif (node.right == self._nil):
            fixNode = node.left
            self.swap(node, node.left)
            if (node.left != self._nil):
                node.left.parent = node.parent

        else:
            checkNode = self.localMin(node.right)
            startColor = checkNode.color
            fixNode = checkNode.right
            if (checkNode.parent == node):
                fixNode.parent = checkNode

            else:
                self.swap(checkNode, checkNode.right)
                checkNode.right.parent = checkNode.parent 
                checkNode.right = node.right
                checkNode.right.parent = checkNode
            checkNode.parent = node.parent
            self.swap(node, checkNode)
            checkNode.left = node.left
            checkNode.left.parent = checkNode
            checkNode.color = node.color
        del node
        if (startColor == False):
            self.recoverDelete(fixNode)
            
    # recover balance after a delete
    def recoverDelete(self, node):
        while (node != self._root and node.color == False): 
            if (node == node.parent.left):
                checkNode = node.parent.right
                if (checkNode.color == True): 
                    checkNode.color = False
                    node.parent.color = True
                    self.rotateLeft(node.parent)
                    checkNode = node.parent.right
                if (checkNode.left.color == False and checkNode.right.color == False):
                    checkNode.color = True
                    node = node.parent
                else:
                    if (checkNode.right.color == False):
                        checkNode.left.color = False
                        checkNode.color = True 
                        self.rotateRight(checkNode)
                        checkNode = node.parent.right
                    checkNode.color = node.parent.color
                    node.parent.color = False
                    checkNode.right.color = False
                    self.rotateLeft(node.parent)
                    node = self._root
            else:
                checkNode = node.parent.left
                if (checkNode.color == True):
                    checkNode.color = False
                    node.parent.color = True
                    self.rotateRight(node.parent)
                    checkNode = node.parent.left
                if (checkNode.right.color == False and checkNode.left.color == False):
                    checkNode.color = True
                    node = node.parent
                else:
                    if (checkNode.left.color == False):
                        checkNode.right.color = False
                        checkNode.color = True
                        self.rotateLeft(checkNode)
                        checkNode = node.parent.left
                    checkNode.color = node.parent.color
                    node.parent.color = False
                    checkNode.left.color = False
                    self.rotateRight(node.parent)
                    node = self._root
        node.color = False

    # finds a key in the tree, node is normally the root to begin
    def findKey(self, key, node):
        while (node._key != None and key != node.key):
            if (key < node.key):
                node = node.left
            else:
                node = node.right
        return node
    
    # swaps nodes
    def swap(self, node, swapNode):
        if (node.parent == self._nil):
            self._root = swapNode
            swapNode.parent = self._nil
        elif (node == node.parent.left):
            node.parent.left = swapNode
        else:
            node.parent.right = swapNode
        swapNode.parent = node.parent
      
    # returns the lesser of the given node or it's left child
    def localMin(self, node):
        while (node.left != self._nil):
            node = node.left
        return node
    
    # rotates the nodes to the left
    def rotateLeft(self, node):
        tempNode = node.right
        node.right = tempNode.left
        if (tempNode.left != self._nil):
            tempNode.left.parent = node
        tempNode.parent = node.parent
        if (node.parent == self._nil):
            self._root = tempNode    
        elif (node == node.parent.left):
            node.parent.left = tempNode
        else:
            node.parent.right = tempNode
        tempNode.left = node
        node.parent = tempNode
        
    # rotates the nodes to the right
    def rotateRight(self, node):
        tempNode = node.left
        node.left = tempNode.right
        if (tempNode.right != self._nil):
            tempNode.right.parent = node
        tempNode.parent = node.parent
        if (node.parent == self._nil):
            self.root = tempNode
        elif (node == node.parent.right):
            node.parent.right = tempNode
        else:
            node.parent.left = tempNode
        tempNode.right = node
        node.parent = tempNode