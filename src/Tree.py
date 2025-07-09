#Required for timestamp creation for when notes were created hence allow hierarchical organisation.
from datetime import datetime

#This class represents a single note in the app.
class NoteNode:

    #Constructor method that is called when a new object is created from the class.
    #Used to assign initial values to variables when declared (initialisation of variables).
    def __init__(self, title, content=None, parent=None, created_at= None, tags=None):

        #Instance variables - specified within a class & specific to each object of the said class.
        #Title of the note
        self.title = title

        #Content within the note
        self.content = content

        #Reference to the parent NoteNode (Set to None if it's the root)
        self.parent = parent

        #List of child NoteNode objects
        self.children = []

        #Timestamp for when the note was created
        self.created_at = created_at or datetime.now()

        #Tags for categorisation - allows for easier searching
        self.tags = tags or []

    #Adds a child NoteNode under this (the referenced) NoteNode.
    def add_child_node(self, child_node):
        self.children.append(child_node) #Adds/appends a child NoteNode onto this NoteNode's children object list
        child_node.parent = self #Makes sure the appended child NoteNode points back to its parent. Sets the referenced NoteNode as the parent.

    #Removes a child from this (the referenced) NoteNode.
    def delete_child_node(self, child_node):
        if child_node in self.children: #Check whether there exists a child NoteNode
            self.children.remove(child_node) #Removes a specific child NoteNode from the current NoteNode's children object list.
            child_node.parent = None #Clears the parent reference.

    #Searches for a NoteNode from this NoteNode by its title recursively
    def find_child_node(self, title):
        if self.title == title: #Checks whether this NoteNode is the one being looked for.
            return self #Returs the said NoteNode if it's the one.
        for child in self.children: #Loops across the list of child NoteNode
            found = child.find_child_node(title) #Uses the earlier defined if statement to check whether this child NoteNote is the one being looked for & stores the result in found.
            if found: #If the value in found == title...
                return found
        return None #If the NoteNode being sought is not found

    #Builds a path from the this NoteNode to its parent NoteNode then reverses the order.
    def get_path(self):
        path = [] #A list to store the titles being 'collected'
        current =  self #The variable current serves as a temporary reference to this NoteNode
        while current: #While the reference is on this NoteNode...
            path.append(current.title) #We append the title of this NoteNode to the path list.
            current = current.parent #Reassigns the current reference to the parent NoteNode of this NoteNode.
        return " > ".join(reversed(path)) #Returns the titles in the path list joined in reverse order

    #Sorts children NoteNodes either by title or by the time created.
    def sort_children_nodes(self, by = "title"): #The optional variable by sorts the NoteNodes by title by default
        if by == "title": #Checks whether the user wants to sort by title
            self.children.sort(key=lambda node: node.title) #Sorts the children NoteNodes by title
        elif by == "date": #Checks whether the user wants to sort by date created
            self.children.sort(key=lambda node: node.created_at) #Sorts the children NoteNodes by date


#This class manages the whole tree data structure in which the NoteNodes are organised.
class NoteTree:

    #Constructor method that is called to initialise variables whenever the class is instantiated.
    def __init__(self):
        self.root = NoteNode("Root") #The topmost NoteNode (root node) is created with the title "Root"

    #Adds a new NoteNode under a parent NoteNode upon searching for it using its title
    def add_note(self, parent_title, title, content = None, tags = None):

        #Uses the function to find a NoteNode from the root NoteNode using its title & stores it in the variable parent_node.
        parent_node = self.root.find_child_node(parent_title)

        if parent_node: #Once the parent NoteNode is found...
            new_note = NoteNode(title, content = content, tags = tags) #Creates a new NoteNode, stored in the new_note variable, with the given information.
            parent_node.add_child_node(new_note) #We then attach it to its parent NoteNode
            return new_note
        return None #If the parent NoteNode isn't found, we return None

    #Deletes a NoteNode by its title except the root node.
    def delete_note(self, title):

        #Searches through the whole tree from the root NoteNode using the title & stores its value in the node_to_delete variable.
        node_to_delete = self.root.find_child_node(title)

        #Checks if the NoteNode exists & whether it has a parent (it is not a root node)
        if node_to_delete and node_to_delete.parent:

            #Deletes the node/Removes it from its parent's child NoteNode list
            node_to_delete.parent.delete_child_node(node_to_delete)
            return True
        return False #If the NoteNode doesn't exist or is a root NoteNode

    #Searches for a NoteNode by its title
    def find_note(self, title):
        return self.root.find_child_node(title) #Returns a NoteNode by its title using the find_child_node function & does so by its title

    #Recursively prints the full tree structure from the specified node
    def display_tree(self, node=None, level=0):
        if node is None: #If no specific start NoteNode is given...
            node = self.root #The default is root
        print (" " * level + f"- {node.title}") #Prints an indented list of titles based on the level/depth of the tree
        for child in node.children: #For each child NoteNode of this NoteNode...
            self.display_tree(child, level + 1) #Recursively call the same function to print out the title