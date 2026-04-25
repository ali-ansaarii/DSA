import java.util.ArrayList;
import java.util.List;

public final class Trie {
    public static final class Operation {
        public final String command;
        public final String value;

        public Operation(String command, String value) {
            this.command = command;
            this.value = value;
        }
    }

    private static final class Node {
        private final Node[] children = new Node[26];
        private boolean isWord;
    }

    private final Node root = new Node();

    public void insert(String word) {
        Node current = root;
        for (int i = 0; i < word.length(); i++) {
            int index = letterIndex(word.charAt(i));
            if (current.children[index] == null) {
                current.children[index] = new Node();
            }
            current = current.children[index];
        }
        current.isWord = true;
    }

    public boolean search(String word) {
        Node node = findNode(word);
        return node != null && node.isWord;
    }

    public boolean startsWith(String prefix) {
        return findNode(prefix) != null;
    }

    private Node findNode(String text) {
        Node current = root;
        for (int i = 0; i < text.length(); i++) {
            int index = letterIndex(text.charAt(i));
            if (current.children[index] == null) {
                return null;
            }
            current = current.children[index];
        }
        return current;
    }

    private static int letterIndex(char ch) {
        int index = ch - 'a';
        if (index < 0 || index >= 26) {
            throw new IllegalArgumentException("Trie only supports lowercase English letters");
        }
        return index;
    }

    public static List<String> executeCommands(List<Operation> operations) {
        Trie trie = new Trie();
        List<String> output = new ArrayList<>();

        for (Operation operation : operations) {
            switch (operation.command) {
                case "insert" -> trie.insert(operation.value);
                case "search" -> output.add(trie.search(operation.value) ? "true" : "false");
                case "starts_with" -> output.add(trie.startsWith(operation.value) ? "true" : "false");
                default -> throw new IllegalArgumentException("Unknown trie command: " + operation.command);
            }
        }

        return output;
    }
}
