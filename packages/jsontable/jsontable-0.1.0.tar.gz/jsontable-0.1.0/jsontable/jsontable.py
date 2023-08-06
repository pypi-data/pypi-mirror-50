# -*- coding: utf-8 -*-
"""
JSON to Table converter
Author: Ernesto Monroy
Created: 10/06/2019
"""
class converter:
    
    def __init__(self):
        self.tree=dict()
        self.paths=[]
        
    #User funcions
    def set_paths(self, paths):
        self.paths = paths
        for p in self.paths:
            self.tree=self.tree_generator(next(iter(p)).split('.'),self.tree,[])   
        
    def convert_json (self, in_content):
        records=self.recurse(self.tree["$"],in_content)
        self.records=records
        columns={records[0][i]:i for i in range(len(records[0]))}
        return [[list(p.values())[0] for p in self.paths]] + [[r[columns[next(iter(p))]] for p in self.paths] for r in records[1:]]
        
    #Auxiliary functions
    def tree_generator(self, nodes,in_tree,previous_nodes):
        if len(nodes)==1:
            new_tree = {None:'.'.join(previous_nodes+nodes)}
        else:        
            if nodes[0] in in_tree:
                new_tree=self.tree_generator(nodes[1:],in_tree[nodes[0]],previous_nodes+[nodes[0]])
            else:
                new_tree=self.tree_generator(nodes[1:],dict(),previous_nodes+[nodes[0]])
        if nodes[0] in in_tree:
            new_tree = {**in_tree[nodes[0]], **new_tree}
        return {nodes[0]:new_tree}
    
    def convert_output(self, in_content):
        #Convert types
        if in_content==None:
            in_content=in_content
        elif type(in_content)==int:
            in_content=in_content
        else:
            in_content=str(in_content)
        return in_content

    def recurse (self, tree,in_content,k=0):
        #print(tree,in_content,k)
        original_content=in_content
        if type(in_content)!= list:
            in_content=[in_content]
        only_header= (in_content==[])

        if only_header:
            in_content=[[]]
        records=[]
        for i in range(len(in_content)):
            row=[[]]
            for node in tree:
                #Final value
                if node == None:
                    #If its the only node
                    if len(tree)==1:
                        return [[tree[node]],[self.convert_output(original_content)]]
                    else:
                        new_result = [[tree[node]],[self.convert_output(original_content)]]
                elif node == '~':
                    if type(original_content)==dict:
                        new_result = self.recurse ({'*':tree[node]},list(original_content.keys()),k+1)
                    else:
                        new_result = self.recurse (tree[node],i,k+1)
                elif node == '*':
                    if type(original_content)==dict:
                        new_result = self.recurse ({'*':tree[node]},list(original_content.values()),k+1)
                    else:
                        new_result = self.recurse (tree[node],in_content[i],k+1)
                elif in_content[i] == None:
                    new_result = self.recurse (tree[node],None,k+1) 
                elif type(in_content[i])==dict and node in in_content[i]:
                    new_result = self.recurse (tree[node],in_content[i][node],k+1)
                else:
                    new_result = self.recurse (tree[node],None,k+1)           

                if only_header:
                    new_result=[new_result[0]]

                if (len(row)>1 or (row[0]==[])) and (len(new_result)>1 or (new_result[0]==[])):
                    row=row+[row[-1] for _ in range (len(new_result)-len(row))]
                    new_result=new_result+[new_result[-1] for _ in range (len(row)-len(new_result))]
                    row=[row[i]+new_result[i] for i in range(len(new_result))]
                else:
                    row=[row[0]+new_result[0]]

            records= [row[0]]+records[1:]+row[1:]

        if only_header:
            return [records[0]]
        else:
            return records