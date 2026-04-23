import java.util.*;

public class InorderTraversal {
    public static List<Integer> InorderTraversal(int[] leftChildren, int[] rightChildren, int root) {
        List<Integer> order = new ArrayList<>();
        Deque<Integer> stack = new ArrayDeque<>();
        int current = root;

        while (current != -1 || !stack.isEmpty()) {
            while (current != -1) {
                stack.push(current);
                current = leftChildren[current];
            }

            current = stack.pop();
            order.add(current);
            current = rightChildren[current];
        }

        return order;
    }
}
