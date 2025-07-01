# This class represents a single Note object with an ID, title, and content
class Note:
    def __init__(self, note_id, title, content):
        self.id = note_id       # Unique ID for the note
        self.title = title      # Title of the note
        self.content = content  # The actual content of the note


# Each node in our circular doubly linked list will hold one Note
class CircularListNode:
    def __init__(self, note):
        self.note = note              # The Note object stored in this node
        self.next_node = None         # Points to the next node in the list
        self.previous_node = None     # Points to the previous node in the list


# Circular doubly linked list that stores recent notes
class CircularDoublyLinkedNotesList:
    def __init__(self, capacity=None):
        self.start_node = None   # This will always point to the newest (most recent) note
        self.size = 0            # Keeps track of how many notes are in the list
        self.capacity = capacity # Optional: maximum number of notes we want to keep

    def insert_note(self, note):
        """
        Inserts a new note at the beginning of the list.
        If there's a limit and it's full, we remove the oldest note.
        Time: O(1), Space: O(1)
        """
        new_node = CircularListNode(note)  # Create a new node for the note

        if self.start_node is None:
            # List is empty, so the new node points to itself in both directions
            new_node.next_node = new_node
            new_node.previous_node = new_node
            self.start_node = new_node  # Set this node as the start
        else:
            # List is not empty, so we insert before the current start_node
            last_node = self.start_node.previous_node  # The last node in the list

            # Connect new_node between last_node and start_node
            new_node.next_node = self.start_node
            new_node.previous_node = last_node
            last_node.next_node = new_node
            self.start_node.previous_node = new_node

            # Now move the start pointer to the new node (since it's the most recent)
            self.start_node = new_node

        self.size += 1  # Increase the count of notes

        # If we have more notes than allowed, remove the oldest one
        if self.capacity and self.size > self.capacity:
            self.remove_oldest_note()

    def remove_oldest_note(self):
        """
        Removes the oldest note (the last node in the list).
        Time: O(1), Space: O(1)
        """
        if self.size == 0:
            return  # List is already empty

        if self.size == 1:
            # Only one note in the list, removing it makes the list empty
            self.start_node = None
        else:
            # Oldest note is the node before the start_node
            last_node = self.start_node.previous_node
            second_last = last_node.previous_node

            # Disconnect the last_node from the list
            second_last.next_node = self.start_node
            self.start_node.previous_node = second_last

        self.size -= 1  # Decrease size after removal

    def remove_note_by_id(self, note_id):
        """
        Searches for a note by ID and removes it if found.
        Time: O(n), Space: O(1)
        """
        if self.start_node is None:
            print("The list is empty.")
            return False

        current = self.start_node

        # We loop through the list exactly 'size' times (circular)
        for _ in range(self.size):
            if current.note.id == note_id:
                if self.size == 1:
                    # Only one node in the list
                    self.start_node = None
                else:
                    # Remove current node by connecting its neighbors together
                    current.previous_node.next_node = current.next_node
                    current.next_node.previous_node = current.previous_node

                    if current == self.start_node:
                        # If we're removing the start_node, move it forward
                        self.start_node = current.next_node

                self.size -= 1
                return True

            current = current.next_node

        print(f"No note found with ID {note_id}.")
        return False

    def find_note_by_title(self, title):
        """
        Looks for a note with a matching title (case-sensitive).
        Returns the note if found, or None.
        Time: O(n), Space: O(1)
        """
        if self.start_node is None:
            return None

        current = self.start_node

        for _ in range(self.size):
            if current.note.title == title:
                return current.note
            current = current.next_node

        return None

    def show_recent_notes(self, limit=5):
        """
        Returns a list of the most recent notes, up to the number 'limit'.
        Time: O(k), Space: O(k)
        """
        notes = []
        if self.start_node is None:
            return notes

        current = self.start_node
        count = 0

        while count < limit and count < self.size:
            notes.append(current.note)
            current = current.next_node
            count += 1

        return notes

    def show_list_forward(self):
        """
        Prints the list from the newest to the oldest note.
        Time: O(n), Space: O(n)
        """
        if self.start_node is None:
            print("The note list is empty.")
            return

        current = self.start_node
        result = []

        for _ in range(self.size):
            result.append(f"{current.note.id}: {current.note.title}")
            current = current.next_node

        print(" -> ".join(result))  # Show notes in forward order

    def show_list_backward(self):
        """
        Prints the list from the oldest to the newest note.
        Time: O(n), Space: O(n)
        """
        if self.start_node is None:
            print("The note list is empty.")
            return

        current = self.start_node.previous_node  # Start from the last node
        result = []

        for _ in range(self.size):
            result.append(f"{current.note.id}: {current.note.title}")
            current = current.previous_node

        print(" <- ".join(result))  # Show notes in backward order

    def __len__(self):
        """
        Allows us to use len() function to get number of notes in the list.
        Time: O(1), Space: O(1)
        """
        return self.size
