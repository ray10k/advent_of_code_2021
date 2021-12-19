from tree import LeafNode,TreeNode
from math import ceil,floor

def parse_string(to_parse:str):
    iterator = iter(to_parse)
    next(iterator)
    current_node = TreeNode(None)
    current_leaf = LeafNode(0)
    build_stack = [current_node]
    for character in iterator:
        if character == "[":
            #New layer to add.
            new_layer = TreeNode(current_node)
            current_node.insert(new_layer)
            build_stack.append(current_node)
            current_node = new_layer
            continue
        if character == ",":
            if current_leaf >= 0:
                current_node.insert(current_leaf)
            current_leaf = LeafNode(0)
            continue
        if character == "]":
            #Drop down a layer.
            current_node.insert(current_leaf)
            current_leaf = LeafNode(-1)
            current_node = build_stack.pop()
            continue
        current_leaf.append(character)
        
    return current_node

def explode_number(tree:TreeNode) -> TreeNode:
    #Start by tracing the tree left-to-right until an excessively
    #deeply nested pair is found.

    #There is no way for an un-reduced snail number to be nested more
    #than 5 layers deep, so 4 tries should get me the deepest snail number.
    current_layer = tree
    for layer in range(tree.depth()-1):
        #Step 1: if the left node is a leaf, it can't possibly be the target node.
        if isinstance(current_layer.left,LeafNode):
            current_layer = current_layer.right
            continue
        #Step 2: if the *right* node is a leaf, it also can't possibly be the target node.
        if isinstance(current_layer.right,LeafNode):
            current_layer = current_layer.left
            continue
        #Step 3: If *both* nodes are further nodes, pick the left unless the right goes deeper.
        depth_l = current_layer.left.depth()
        depth_r = current_layer.right.depth()
        if (depth_r>depth_l):
            current_layer = current_layer.right
            continue
        current_layer = current_layer.left
    #current_layer is now the pair that needs to explode, tree_trace is all the nodes leading up to there.
    exploding_node = current_layer

    #Worst-case scenario:[0,[0,[0,[0,1]]],[[[[2,3],0],0],0]] should lead to [0,[0,[0,[0,3]]],[[[0,3],0],0]].
    #More recursive nonsense.

    #Handle left-hand side
    num_left = current_layer.left
    num_right = current_layer.right
    #print("exploding:", str(num_left),",",str(num_right),end="")

    leaves = tree.get_leaves()
    exploding_index = leaves.index(num_left)
    if exploding_index > 0:
        left_leaf = leaves[exploding_index-1]
        left_leaf += num_left
    exploding_index = leaves.index(num_right)
    if exploding_index+1 < len(leaves):
        right_leaf = leaves[exploding_index+1]
        right_leaf += num_right

    #Finish by replacing the exploded node with a zero.
    if exploding_node.parent.left is exploding_node:
        exploding_node.parent.left = LeafNode(0)
    else:
        exploding_node.parent.right = LeafNode(0)
    return tree

def split_number(tree:TreeNode) -> None:
    #Thankfully, this *should* be easier than explosions.
    #Find the left-most number that is greater than 9, turn it
    #into a new TreeNode.
    #print(tree.get_leaves())
    for node in tree.iterate():
        if isinstance(node.left,LeafNode) and node.left > 9:
            new_node = TreeNode(node)
            new_node.insert(int(floor(node.left/2)))
            new_node.insert(int(ceil(node.left/2)))
            node.left = new_node
            break
        if isinstance(node.right,LeafNode) and node.right > 9:
            new_node = TreeNode(node)
            new_node.insert(int(floor(node.right/2)))
            new_node.insert(int(ceil(node.right/2)))
            node.right = new_node
            break
    return tree

def reduce(tree:TreeNode) -> TreeNode:
    splits,explos = 0,0
    while True:
        #Repeatedly try to reduce the snail number until it sticks.
        if tree.depth() <= 4 and max(int(x) for x in tree.get_leaves()) <= 9:
            break
        #*FIRST* check if anything needs to explode, *THEN* check for splits.
        if tree.depth() > 4:
            explos += 1
            explode_number(tree)
        else:
            splits += 1
            split_number(tree)
    print(f"exploded {explos}; split {splits}")
    return tree

def calculate_magnitude(tree:TreeNode) -> int:
    #Fuck it. Recursion time.

    left,right = 0,0
    if isinstance(tree.left,LeafNode):
        left = 3*int(tree.left)
    else:
        left = 3*calculate_magnitude(tree.left)
    if isinstance(tree.right,LeafNode):
        right = 2*int(tree.right)
    else:
        right = 2*calculate_magnitude(tree.right)
    return left + right
