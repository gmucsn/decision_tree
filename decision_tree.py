import random

"""
A tree is represented as a list of dictionaries.
Each dictionary represents a node in the tree.  
Every node has the following key value pairs:

    'name': string (name of node)
    'type': string (type of node d = decision, n = nature, and t = terminal)
  'filled': bolean value (True if all data is filled in; False otherwise)
    'used': boolean value (True if node has already been used in current backwards induction; false otherwise)
'subvalue': value of node if strategy is optimal beyond this node 
'ancestor': integer (index of node that brancehed to this node)

Additional key:value pairs in a dictionary depend on the value of 'type'.

if the value of 'type' equals 'd'

    'descendants': list (of node indexes that this node branches to)

if the value of 'type' equals 'n'

    'descendants': list (of node indexes that this node branches to)
    'probabilities': list ( of probabilities of reaching each descendant node)

if the value of 'type' equals 't'

    'pay': float (payoff if terminal node is reached) 
"""


def short_menu():
    """Print menu choices on console"""
    print()
    print('            MENU')
    print('-----------------------------')
    print('help  | exit | load | save  | calc |')
    print('build | show | edit | solve | see  |')
    print('strat | path | play | sim   |')
    print('-----------------------------')


def get_menu_choice(key_words):
    """ Gets choice and checks against key_words list"""
    while True:
        choice = input('Please enter your choice?\n ')
        if choice in key_words.keys():
            return choice
        else:
            print("Your choice: " + choice)
            print("Is not available.  Please try again")
            return ""


#  The following are a set of functions used by the fill_node function to get input
#  and test it for validity.


def get_node_name():
    """Used by fill_node to get node name"""
    while True:
        name = input("Node Name: ")
        # only test if name is not empty
        if len(name) > 0:
            break
    return name


def get_node_type():
    """Used by fill_node to get node name"""
    while True:
        typ = input("Node Type (d)ecision, n)ature, t)erminal: ")
        if typ == 'd' or typ == 'n' or typ == 't':
            return typ


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_node_pay():
    """Used by fill_node to get node name"""
    while True:
        pay = input("Enter payoff for reaching node:")
        if is_number(pay):
            return pay


def get_new_node(next_node):
    """Used by fill_node to get node name"""
    while True:
        new_node = input("Enter {} for descendant node or 'x' for done"
                         .format(next_node))
        if new_node == next_node or new_node == 'x' or new_node == 'X':
            return new_node


def get_node_descendants(tree_length, node_index):
    """Used by fill_node to get descendants of node"""
    des = []
    descendants = []
    count_descendants = 0
    while True:
        next_node = tree_length + count_descendants
        new_node = get_new_node(str(next_node))
        if new_node == "x" or new_node == "X":
            break
        count_descendants += 1
        des.append({"ancestor": node_index, 'filled': False})
        descendants.append(next_node)
    return des, descendants


def get_new_probability(k):
    """Used by get_node_probabilities to get valis probability"""
    while True:
        prob = float(input("Probability of node {} = "
                           .format(k)))
        if 0.0 <= prob <= 1.0:
            return prob


def get_node_probabilities(descendants):
    """Used by fill_node to get probability distribution for nature node choices"""
    while True:
        probabilities = []
        for k in range(len(descendants)):
            prob = get_new_probability((descendants[k]))
            probabilities.append(prob)
        sum_of_probs = 0.0
        for p in probabilities:
            sum_of_probs += p
        tollerance = .000001
        if 1.0 + tollerance > sum_of_probs > 1 - tollerance:
            return probabilities
        else:
            print("probabilites dont sum to 1", probabilities)


def fill_node(tree, node_index):
    """ Used by build_tree to populates a node in the decision tree

        args:  tree: a list of dictionaries
               node_index:  current node or dictionary item in list
        return: tree
    """

    print("Prepare Node {}. \n ------------- \n".format(node_index))
    tree[node_index]['name'] = get_node_name()
    tree[node_index]['type'] = get_node_type()

    # Process terminal node
    if tree[node_index]['type'] == "t":
        tree[node_index]['pay'] = get_node_pay()
        tree[node_index]['used'] = True
        tree[node_index]['subvalue'] = tree[node_index]['pay']
        tree[node_index]['filled'] = True
        print("\n ------------ \n")
        return tree

    #  The remainder of this code processes decision nodes and nature nodes
    #  First we start with descendants since both kinds of nodes have descendant

    des, tree[node_index]['descendants'] = get_node_descendants(len(tree), node_index)

    #  Next we populate tree with the descendant node dictionaries

    for k in des:
        tree.append(k)

    # This block of code asks the user for the probability that nature
    # will choose a descendant node

    if tree[node_index]['type'] == 'n':
        tree[node_index]['probabilities'] = get_node_probabilities(tree[node_index]['descendants'])
    tree[node_index]['subvalue'] = 0.0
    tree[node_index]['used'] = False
    tree[node_index]['filled'] = True
    print("\n ------------ \n")

    return tree


def build():
    """ Builds a tree using user input """

    # Initialize first node in tree
    tree = [{'ancestor': -1, 'filled': False}]
    node_index = 0
    tree = fill_node(tree, node_index)

    # go thru the tree and process any new nodes
    # that were added by the descendant processing
    # in fill_node.

    done = False
    while not done:
        k = len(tree)
        done = True
        for j in range(k):
            if not tree[j]['filled']:
                done = False
                tree = fill_node(tree, j)  # Note more descendants could be added at this point

    return tree


def show(tree, node_index = 0, level = 0):
    """Recursive function to print the tree on the console with indentations for levels of the tree"""
    print('   ' * level + '{}-'.format(node_index), end="")
    print('{}'.format(tree[node_index]['name']), end="")
    # note end = "" does not move to the next line
    print('#{}'.format(tree[node_index]['ancestor']), end="")
    if tree[node_index]['type'] == 't':
        print("(t){}".format(tree[node_index]['pay']))
        return
    elif tree[node_index]['type'] == 'd':
        print("(d)")
    elif tree[node_index]['type'] == 'n':
        print("(n)[", end="")
        for k in range(len(tree[node_index]['descendants'])):
            print("{}".format(tree[node_index]['probabilities'][k]), end="")
            if k < len(tree[node_index]['descendants']) - 1:
                print(',', end="")
        print(']')
    for k in tree[node_index]['descendants']:
        show(tree, k, level + 1)


def show_computed_values(tree, node_index, level):
    print('   ' * level + '{}-'.format(node_index), end="")
    print('{}'.format(tree[node_index]['name']), end="")
    # note end = "" does not move to the next line
    print('#{}'.format(tree[node_index]['ancestor']), end="")
    if tree[node_index]['type'] == 't':
        print("(t){} (V){}".format(tree[node_index]['pay'], tree[node_index]['subvalue']))
        return
    elif tree[node_index]['type'] == 'd':
        print("(d) (V){}".format(tree[node_index]['subvalue']))
    elif tree[node_index]['type'] == 'n':
        print("(n)[", end="")
        for k in range(len(tree[node_index]['descendants'])):
            print("{}".format(tree[node_index]['probabilities'][k]), end="")
            if k < len(tree[node_index]['descendants']) - 1:
                print(',', end="")
        print('](V){}'.format(tree[node_index]['subvalue']))
    for k in tree[node_index]['descendants']:
        show_computed_values(tree, k, level + 1)


def show_strategy(strategy, next_choice, tree, node_index, level):
    """Recursive function to print the tree and show the strategy with *
        arg: strategy, list of decisions
        arg: next_choice, node to *
        arg: tree, decision tree list of dictionary nodes
        arg: node_index, current node to work on
        arg: level, current level of the tree to work on"""

    if node_index == next_choice:
        print("*", end="")
    else:
        print(" ", end="")
    print('   ' * level + '{}-'.format(node_index), end="")
    if node_index == next_choice:
        print("*", end="")
    else:
        print(" ", end="")

    print('{}'.format(tree[node_index]['name']), end="")
    # note end = "" does not move to the next line
    if tree[node_index]['type'] == 't':
        print("(t){}".format(tree[node_index]['pay']))
        return
    elif tree[node_index]['type'] == 'd':
        print("(d)")
        next_choice = strategy[node_index]
    elif tree[node_index]['type'] == 'n':
        print("(n)[", end="")
        for k in range(len(tree[node_index]['descendants'])):
            print("{}".format(tree[node_index]['probabilities'][k]), end="")
            if k < len(tree[node_index]['descendants']) - 1:
                print(',', end="")
        print(']')
    for k in tree[node_index]['descendants']:
        show_strategy(strategy, next_choice, tree, k, level + 1)


def path(strategy, tree, node = 0, indent = ""):
    """Recursive function to print the tree and show the strategy with *
        arg: strategy, list of decisions
        arg: next_choice, node to *
        arg: tree, decision tree list of dictionary nodes
        arg: node_index, current node to work on
        arg: level, current level of the tree to work on"""

    print(indent + tree[node]['name'], end = "")
    if tree[node]['type'] == 't':
        print(" " + str(tree[node]['pay']), end = "")
        print()
        return
    elif tree[node]['type'] == 'd':
        print()
        indent = indent + "  "
        path(strategy, tree, strategy[node], indent)
    elif tree[node]['type']  == 'n':
        print(" " + str(tree[node]['probabilities']), end = "")
        print()
        indent = indent + "  "
        for k in tree[node]['descendants']:
            path(strategy, tree, k, indent)


def save_tree(tree):
    """Saves a tree.  Will ask for filename.  Filename must not already exist"""

    file_name = input('Enter a file name ')
    try:
        file = open(file_name + '.txt', 'r')
        file.close()
        print("File {} already exists".format(file_name))
        return
    except IOError:
        print('File {} will now be written.'.format(file_name))

    file = open(file_name + '.txt', 'w')
    for k, val in enumerate(tree):
        file.write('node,' + str(k) + '\n')
        file.write('name,' + tree[k]['name'] + '\n')
        file.write('type,' + tree[k]['type'] + '\n')
        if tree[k]['type'] == 't':
            file.write('pay,' + str(tree[k]['pay']) + '\n')
        else:
            des_length = len(tree[k]['descendants'])
            file.write('length,' + str(des_length) + '\n')
            for j in range(des_length):
                file.write('descendant,' + str(tree[k]['descendants'][j]) + '\n')
            if tree[k]['type'] == 'n':
                for j in range(des_length):
                    file.write('prob,' + str(tree[k]['probabilities'][j]) + '\n')
    file.close()
    print(file_name + ".txt has been saved")


def parse_line(line):
    """Parses input line for load_tree"""
    x = line.split(',')
    return x[0], x[1]


def get_ancestory(tree):
    """Calculates all the ancestors in a tree"""
    # now caluclate ancestory
    ancestory = [-1 for k in range(len(tree))]
    for k, node in enumerate(tree):
        if node['type'] != "t":
            for j in node['descendants']:
                ancestory[j] = k
        for k, node in enumerate(tree):
            node['ancestor'] = int(ancestory[k])
    return tree


def load():
    """Loads a tree.  Will ask for filename.  Checks that .txt file exists"""
    print("Enter a file name:")
    file_name = input('')
    try:
        file = open(file_name + '.txt', 'r')
        file.close()
        print("File {} will now be loaded".format(file_name))
    except IOError:
        print('File {} does note exist.'.format(file_name))
        return
    tree = []
    file = open(file_name + '.txt', 'r')
    des = []
    pr = []
    cur_node = -1
    for line in file:
        header, val = parse_line(line)
        if header == 'node':
            cur_node = int(val)
            tree.append({})
            des = []
            pr = []
        elif header == 'name':
            tree[cur_node]['name'] = val[0:len(val) - 1]
        elif header == 'type':
            tree[cur_node]['type'] = val[0]
        elif header == 'pay':
            tree[cur_node]['pay'] = float(val)
        elif header == 'length':
            des = []
            pr = []
        elif header == 'descendant':
            des.append(int(val))
        elif header == 'prob':
            pr.append(float(val))
        else:
            print('***** error {}, {}'.format(header, val))
        if len(des) > 0:
            tree[cur_node]['descendants'] = des
        if len(pr) > 0:
            tree[cur_node]['probabilities'] = pr
    file.close()
    return get_ancestory(tree)


def get_strategy(tree):
    """Allows user to input a strategy for a tree.  A strategy is a
    choice of descendant node at each decision node."""
    strategy = []
    for node in tree:
        if node['type'] == 'd':
            try_again = True
            while try_again:
                print('at node {}.  Your choices are'.format(node['name']))
                print(node['descendants'])
                decision = input("Which node do you want to go to? ")
                if int(decision) in node['descendants']:
                    try_again = False
                    strategy.append(int(decision))
        else:
            strategy.append(-1)  # -1 means no decision here.
    return strategy


def play_nature(probs):
    """Used by play_tree to play a nature node"""
    ran_num = random.random()
    down_range = 0
    up_range = 0
    for k, val in enumerate(probs):
        up_range += val
        if down_range <= ran_num <= up_range:
            return k
        down_range += val
    return len(probs)


def play(strategy, tree, cur_node = 0):
    """play tree using strategy while starting at cur_node"""
    while True:
        if tree[cur_node]['type'] == 't':
            # print(cur_node, tree[cur_node]['name'], tree[cur_node]['pay'])
            return [cur_node, tree[cur_node]['name'], tree[cur_node]['pay']]
        elif tree[cur_node]['type'] == 'd':
            cur_node = strategy[cur_node]
        elif tree[cur_node]['type'] == 'n':
            k = play_nature(tree[cur_node]['probabilities'])
            cur_node = tree[cur_node]['descendants'][k]
        else:
            print('***** error type {} unexpected'
                  .format(tree[cur_node]['type']))


def sim_decisions(num_trials, tree, strategy):
    """
    :param num_trials:
    :param tree:
    :param strategy:
    :return:
    """
    res = []
    for k in range(len(tree)):
        res.append(0)
    for k in range(num_trials):
        oc = play(strategy, tree, 0)
        res[oc[0]] += 1
    print(res)
    prob_outcome = [pr / num_trials for pr in res]
    payoffs = []
    for _ in res:
        payoffs.append(0)
    ev = 0
    for k, node in enumerate(tree):
        if node['type'] == 't':
            print(k, prob_outcome[k], node['pay'])
            print(prob_outcome[k], node['pay'])
            ev += prob_outcome[k] * node['pay']
            payoffs[k] = node['pay']
    return payoffs, ev


def sim(strategy, tree, num_trials = 20):
    """
    :param num_trials:
    :param tree:
    :param strategy:
    :return output
    """
    output = []
    for k in range(num_trials):
        output.append(play(strategy, tree))
    return output


def see(strategy, tree):
    tree = calc_values(strategy, tree)
    show_computed_values(tree, 0, 0)


def help():
    """
    Verbose help screen when 'help' is typed.
    """
    print('\n Decision Tree V1.0, built by Kevin McCabe \n')
    print("   1.  If you dont have a tree built yet you can,")
    print("       a.  type 'build' to build a tree,")
    print("       b.  type 'load' and you can load a tree.")
    print()
    print("   2.  Once you have a tree you can, ")
    print("       a.  type 'show' to show the tree on the console, or you can,")
    print("       b.  type 'save' to save the tree, or you can,")
    print("       c.  type 'solve' to solve for the optimal strategy, or you can,")
    print("       d.  type 'edit' to edit parts of the tree.")
    print()
    print("   3.  If you want to play or simulate a strategy you can, ")
    print("       a.  type 'path' to see your strategy path through the tree")
    print("       b.  type 'strat' to enter a strategy by hand,")
    print("       c.  type 'play' to play the strategy once.")
    print("       d.  type 'sim' to simulate a number of plays of the strategy")
    print("       e.  type 'value' to calculate the expected value of a strategy")
    print()
    print("   Future Relaese will allow an agent to play the tree. ")
    print("       ")


def check_all_descendants_used(node, tree):
    """Check to make sure all descendants have bben used

        arge: node, dictionary of node to check
              tree, list of dictioaries of all nodes

        return:  boolean True if all descendants have been used
        """
    for k in node['descendants']:
        if not tree[k]['used']:
            return False
    return True


def calc_expected_value(node, tree):
    """ Calculate expected value of nature node"""
    v = 0.0
    for j, k in enumerate(node['descendants']):
        v += float(tree[k]['subvalue'])*node['probabilities'][j]  # used subvalue mot payoff
    return v


def calc_max_value(node, tree):
    """ Calculate value of optimal move in a decison node

        args: node, the decision node to check
              tree, a list of dictionary nodes
        return: choice, integer best choice node in descendants
                float(v) the value associated with the best choice"""
    v = tree[node['descendants'][0]]['subvalue']  # get payoff of first descendant subscript zero
    choice = node['descendants'][0]
    for k in node['descendants']:
        if tree[k]['subvalue'] > v:  # if you find a better subval payoff
            v = tree[k]['subvalue']
            choice = k
    return choice, float(v)


def solve(tree):
    """ Uses backward induction to find the strategy in tree that maximizes expected value

        args: tree, a list of dictioanries
        return: strategy, a list of choices at decision nodes
                tree, updated tree with completed subvalue at every node

        tree[0]['subvalue'] contains the expected value of the optimal strategy
    """
    # initialize tree for backwards induction
    strategy = []
    for node in tree:
        if node['type'] == 't':
            node['used'] = True
            node['subvalue'] = float(node['pay'])
        else:
            node['used'] = False
            node['subvalue'] = 0.0
        strategy.append(-1)  # default all to terminal

    # solve for optimal strategy
    while not tree[0]['used']:
        for index, node in enumerate(tree):
            if not node['used']:
                if check_all_descendants_used(node, tree):
                    if node['type'] == 'n':
                        ev = calc_expected_value(node, tree)
                        node['used'] = True
                        node['subvalue'] = float(ev)
                    elif node['type'] == 'd':
                        choice, mv = calc_max_value(node, tree)
                        node['used'] = True
                        node['subvalue'] = float(mv)
                        strategy[index] = choice
    return strategy, tree


def calc_values(strategy, tree):
    for node in tree:
        if node['type'] == 't':
            node['used'] = True
            node['subvalue'] = float(node['pay'])
        else:
            node['used'] = False
            node['subvalue'] = 0.0

    while not tree[0]['used']:
        for index, node in enumerate(tree):
            if not node['used']:
                if check_all_descendants_used(node, tree):
                    if node['type'] == 'n':
                        ev = calc_expected_value(node, tree)
                        node['used'] = True
                        node['subvalue'] = float(ev)
                    elif node['type'] == 'd':
                        node['used'] = True
                        choice = strategy[index]
                        node['subvalue'] = tree[choice]['subvalue']
    return tree


def edit(tree):
    """Allows user to make a few edits to an existing tree
        parm: tree, a list of node dictionaries
        return: tree, updated version of tree"""

    if not tree:
        print("tree is empty")
        return
    print("input type pf edit:  pay, prob, name")
    type_of_edit = input('')

    if type_of_edit == 'pay':
        for index, node in enumerate(tree):
            if node['type'] == 't':
                print("{} {} has payoff {}".format(index, node['name'], node['pay']))
                inp = input('change payoff y/n')
                if inp == 'y':
                    print("Enter New Payoff")
                    node['pay'] = input('')

    if type_of_edit == 'prob':
        pass

    if type_of_edit == 'name':
        for index, node in enumerate(tree):
            print("{} has name {} ".format(index, node['name']))
            inp = input('change name y/n')
            if inp == 'y':
                print("Enter New Name")
                node['name'] = input('')

    return tree


def process_loop():
    """ Prints menu choices and accepts choice"""
    print()
    print("Welcome to the Decision Tree Processor.")
    print("-- Enter commands without any arguments.")
    print("-- If an argument is needed it will be requested.")
    print()
    key_words = {'build': True, 'show': True, 'strat': True,
                 'find': True, 'load': True, 'save': True,
                 'play': True, 'exit': True, 'edit': True,
                 'path': True, 'sim': True, 'help': True,
                 'solve': True, 'calc': True, 'see': True}

    tree = []
    strategy = []
    while True:
        short_menu()
        choice = get_menu_choice(key_words)
        if choice == "":
            continue
        print()
        if choice == 'exit':
            return
        elif choice == 'build':
            tree = build()
        elif choice == 'show':
            show(tree)
        elif choice == 'save':
            save_tree(tree)
        elif choice == 'load':
            tree = load()
        elif choice == 'strat':
            strategy = get_strategy(tree)
            print(strategy)
        elif choice == 'play':
            if strategy:
                oc = play(strategy, tree)
                print('oc = {}'.format(oc))
        elif choice == 'sim':
            payoffs, ev = sim_decisions(1000000, tree, strategy)
            print(payoffs)
            print('Expected value = {}'.format(ev))
            obs = sim(strategy, tree)
            print(obs)
        elif choice == 'solve':
            strategy, tree = solve(tree)
            print(strategy)
            print('ev = ' + str(tree[0]['subvalue']))
        elif choice == 'calc':
            tree = calc_values(strategy, tree)
        elif choice == 'see':
            see(strategy, tree)
        elif choice == 'path':
            path(strategy, tree)
        elif choice == 'edit':
            tree = edit(tree)
        elif choice == 'help':
            help()
        else:
            print('input {} is just wrong'.format(choice))
            return


if __name__ == '__main__':
    process_loop()
