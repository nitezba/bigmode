import pygame, os, random, math, json

from constants import *

# SPACE PARTITIONING TREE - just somewhere to put leaves an the whole tree together
class Tree:
    def __init__(self, tree : list, leaves : list) -> None:
        self.tree : list    = tree
        self.leaves: list   = leaves

    # TODO: FINISH THIS SHIT LMFAO
    def connect(self) -> None:
        # treat it almost like frontier
        tree_dup : list = self.tree.copy()
        frontier : list = self.leaves.copy()

        # NOTE: WHEN WE FINISH THE BOTTOM LAYER AND CYCLE BACK
        # AROUND TO FORMER PARENT NODES, THOSE PARENT NODES
        # DONT HAVE ANY CHILDREN, WHICH IS WHY I THINK THIS FAILS
        while frontier :
            node : partitionCell = frontier[0]

            if node.parent == None:
                if len(frontier) == 1:
                    break
                else :
                    frontier.remove(node)
                    frontier.append(node)
                    continue
            # remove node we're checking, as well as its sibling!!

            # now that we know this node has a parent
                # obtain the parent
            parent : partitionCell = node.parent
                # remove its children from the frontier
            children : list = parent.children

            for child in children :
                if child in frontier :
                    frontier.remove(child)
                # add the former parent to the frontier
            frontier.append(parent)
            # identify siblings

            
            # pop siblings from frontier, add the former parent, establish bridge

# =====================================================
# ============ PARTITION CELL CLASS ===================
# =====================================================
class partitionCell :
    def __init__(self, topLeft : tuple, bottomRight : tuple, parent = None) -> None:
        self.topLeft                = topLeft
        self.bottomRight            = bottomRight
        self.children : list        = None
        self.parent : partitionCell = parent    # NOTE: could use this for some postprocessing too

    # TODO: CHECK IF THIS WORKS LMFAO
    # given orientation, returns a list of children 
    def split(self, orientation : bool, spliceLocation : int) -> None:
        # NOTE: if you need to copy paste this back into the BSP code, change self to node
        self.children = [ # horizontal range -> vertical cut
            partitionCell(
                self.topLeft, 
                (spliceLocation, self.bottomRight[1]), 
                self
            ), partitionCell(
                (spliceLocation + 1, self.topLeft[1]), 
                self.bottomRight, 
                self
            )
        ] if orientation == 0 else [ # vertical range -> horizontal cut
            partitionCell(
                self.topLeft, 
                (self.bottomRight[0], spliceLocation), 
                self
            ), partitionCell(
                (self.topLeft[0], spliceLocation + 1), 
                self.bottomRight, 
                self
            )
        ]

    # returns tuple of leftmost and rightmost y-values
    def getHorizontalRange(self) -> tuple:
        return (self.topLeft[0], self.bottomRight[0])
    
    def getVerticalRange(self) -> tuple:
        return (self.topLeft[1], self.bottomRight[1])
    
    # return tuple of x, y dimensions
    def getDimensions(self) -> tuple:
        return (self.bottomRight[0] - self.topLeft[0], self.bottomRight[1] - self.topLeft[1])

    # return a list of the x,y coordinates that are contained in the cell
    def getInternalCoords(self) -> list: # given the topLeft and bottomRight coords
        ret = []
        x_start = self.topLeft[0]
        y_start = self.topLeft[1]
        x_bound = self.bottomRight[0] - x_start
        y_bound = self.bottomRight[1] - y_start

        r = 0
        while r < x_bound :
            c = 0
            while c < y_bound :
                coord = (x_start + r, y_start + c)
                ret.append(coord)
                c += 1
            r += 1

        return ret


    def isDonePartitioning(self) -> bool:
        dims : tuple = self.getDimensions()
        if dims[0] <= 5 or dims[1] <= 5:
            return True
        
        return False

    # TODO: splitvertical/horizontal functions

    def printData(self) -> None :
        print("Top left: ", self.topLeft, "Bottom right: ", self.bottomRight)
        print("Dimensions: ", self.getDimensions())
        if self.children != None :
            print("Children:", len(self.children))
            for node in self.children:
                print("    topLeft:", node.topLeft, "    bottomRight:", node.bottomRight)
        else:
            print("no more")
        print("Parent Node (topLeft & dimension):" , self.topLeft, self.getDimensions())
        print("==============================")

        