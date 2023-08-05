#!/usr/bin/env python3
# -*-coding:Utf-8 -*
"""
This module provides all the function to handle fastq search with suffix tree
"""


def error_proba(phred):
    """
    Compute error proba from phred score

    params: phred int()
    return: proba double()
    """
    return 10 ** ((-phred)/10)


def distance(qual, pos):
    """
    Compute error proba from phred score

    params: phred int()
    return: proba double()
    """
    return 1 - error_proba(int(qual[pos]))


class Node:
    """
    Node of a suffixtree
    """

    def __init__(self, parent=None, base=None):
        """
        Initialisation of a Node

        params: start int() sarting position in the string
        params: end int() end position in the string
        """
        self.parent = parent
        self.base = base
        self.childs = dict()
        self.barcode = None

    def __del__(self):
        for child in self.childs:
            self.childs[child].__del__()

    def add_child(self, base):
        """
        return the base of a Node

        return: base char() sarting position in the string
        """
        if base not in self.childs:
            self.childs[base] = Node(parent=self, base=base)
        return self[base]

    def __getitem__(self, base):
        """
        return the child with the base 'base'

        params: base char()
        return: child Node()
        """
        if base in self.childs:
            return self.childs[base]
        return None

    def get_barcode(self, seq, pos=0):
        """
        recursive barcode search

        return: barcode str() the barcode corresponding to a string or None
        if not found
        """
        base = seq[pos]
        if base in self.childs:
            if self[base].barcode is None and len(seq) > pos+1:
                return self[base].get_barcode(seq=seq, pos=pos+1)
            if self[base].barcode is not None:
                return (self[base].barcode, pos, None)
        return (None, pos, self)

    def __str__(self):
        """
        display first sequence added to the tree
        """
        base = list(self.childs.keys())[0]
        if self[base].barcode is None:
            return (base +
                    str(self[base]))
        return base


class Tree:
    """
    General suffixtree
    """

    def __init__(self, mismatch=None):
        """
        Initialisation of a General suffixtree
        """
        self.size = 0
        self.root = Node()
        self.mismatch = mismatch
        self.crawler = TreeCrawler(tree=self, mismatch=self.mismatch)

    def __del__(self):
        self.root.__del__()

    def add_sequence(self, sequence, barcode):
        """
        Function to add a sequence to the general suffixtree

        params: sequence str()
        """
        curr_node = self.root
        for base in sequence:
            curr_node = curr_node.add_child(base)
        curr_node.barcode = barcode
        self.size = max([self.size, len(sequence)])

    def __str__(self):
        """
        display first sequence added to the tree
        """
        return str(self.root)

    def search_reads(self, seq, qual, cache=True, verbose=False):
        """
        Function to search a barcode in the suffixtree

        params: seq str()
        params: qual list()
        return: cache bool()
        """
        try:
            self.crawler.search_reads(
                seq=seq,
                qual=qual,
                cache=cache,
                verbose=verbose
            )
            if verbose:
                print(self.crawler.barcode)
            if self.crawler.barcode is None:
                return "unassigned"
            return self.crawler.barcode
        except IndexError:
            if verbose:
                print("error: Tree.search_read()")
            raise IndexError


class TreeCrawler:
    """
    Helper Class to search suffixtree
    """

    def __init__(self, tree, mismatch=None):
        """
        Initialisation of a General suffixtree
        """
        self.seq = str()
        self.qual = list()
        self.dists = list()
        self.barcodes = list()
        self.tree = tree
        self.barcode = None
        self.mismatch = mismatch

    def split_search(self, curr_node, pos, dist=0, verbose=False):
        """
        Multiply the barcode search in case of mismatch
        """
        if verbose:
            print((pos, self.seq[pos], curr_node.base,
                   list(curr_node.childs.keys()), dist, curr_node.barcode))
        if len(self.seq) > pos+1:
            # we search with n mismatch
            for base in curr_node.childs.keys():
                curr_dist = dist
                search_result = curr_node[base].get_barcode(
                    seq=self.seq,
                    pos=pos + 1
                )
                if search_result[0] is not None:
                    curr_dist += search_result[1] - pos
                    self.dists.append(curr_dist)
                    self.barcodes.append(search_result[0])
                else:
                    # if no results with one missmath we search with n+1
                    # mismatch
                    if self.mismatch is not None:
                        self.mismatch -= 1
                    curr_dist += distance(qual=self.qual, pos=pos + 1)
                    self.split_search(
                        curr_node=curr_node[base],
                        pos=pos + 1,
                        dist=curr_dist,
                        verbose=verbose
                    )

    def search_reads(self, seq, qual, cache=True, verbose=False):
        """
        Function to search a barcode in the suffixtree

        params: seq str()
        params: qual list()
        return: cache bool()
        """
        self.seq = str(seq)
        self.qual = qual
        if len(self.seq) != self.tree.size:
            if verbose:
                print("error: TreeCrawler.search_read() seq size (" +
                      str(len(self.seq)) +
                      ") different from tree size (" +
                      str(self.tree.size) +
                      ")")
            raise IndexError
        if len(self.qual) != self.tree.size:
            if verbose:
                print("error: TreeCrawler.search_read() qual size (" +
                      str(len(self.qual)) +
                      ") different from tree size (" +
                      str(self.tree.size) +
                      ")")
            raise IndexError

        self.barcode, pos, curr_node = self.tree.root.get_barcode(
            seq=self.seq,
            pos=0
        )
        if self.barcode is None:
            if self.mismatch is not None:
                self.mismatch -= 1
            dist = distance(qual=self.qual, pos=pos) + pos
            self.split_search(
                curr_node=curr_node,
                pos=pos,
                dist=dist,
                verbose=verbose
            )
            if verbose:
                print((self.barcodes, self.dists))
            if self.barcodes:
                min_dist = max(self.dists)
                min_dist_index = self.dists.index(min_dist)
                self.barcode = self.barcodes[min_dist_index]
                if cache:
                    self.tree.add_sequence(
                        sequence=self.seq,
                        barcode=self.barcode
                    )
                if self.mismatch is not None:
                    if self.mismatch < 0:
                        self.barcode = None


class Forest:
    """
    Forest of suffixtree
    """
    def __init__(self, mismatch=None):
        """
        Initialisation of a Forest
        """
        self.adaptators = dict()
        self.mismatch = mismatch

    def __del__(self):
        for adaptator in self.adaptators:
            self.adaptators[adaptator].__del__()

    def add_sequence(self, adaptator, sequence, barcode):
        """
        Function to add a sequence to the forest

        params: adaptator str()
        params: sequence str()
        params: barcode str()
        """
        if adaptator not in self.adaptators:
            self.adaptators[adaptator] = Tree(mismatch=self.mismatch)
        self.adaptators[adaptator].add_sequence(
            sequence=sequence,
            barcode=barcode
        )

    def search_reads(self, adaptator, seq, qual,
                     cache=True, verbose=False):
        """
        Function to search a barcode in the forest

        params: barcode str()
        params: seq str()
        params: qual list()
        return: cache bool()
        """
        if adaptator in self.adaptators:
            try:
                return self.adaptators[adaptator].search_reads(
                    seq=seq,
                    qual=qual,
                    cache=cache,
                    verbose=verbose
                )
            except IndexError:
                if verbose:
                    print("error: Forest.search_reads()")
                raise IndexError
        if verbose:
            print("error: Forest.search_reads() adaptator not found")
        raise KeyError
