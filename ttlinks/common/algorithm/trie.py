from abc import ABC, abstractmethod


class TrieNode(ABC):
    @abstractmethod
    def __init__(self):
        """
        Abstract base class for a TrieNode used in a Trie (prefix tree) structure.
        This constructor initializes a node with an empty dictionary for child nodes
        and a flag to mark if the current node is the end of a sequence (e.g., word, phrase).

        Parameters:
        self.children: A dictionary where keys represent characters or portions of the word/identifier
                       and values are instances of TrieNode representing child nodes.
        self.is_end_of_oui: A boolean flag that indicates if the current node is the end of a word/sequence.
                            True if it is, False otherwise.

        Returns:
        None: The constructor doesn't return any value but initializes the TrieNode.
        """
        self.children = {}
        self.is_end_of_oui = False
