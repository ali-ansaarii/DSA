import java.util.*;

public class PreorderTraversal {
    public static List<Integer> PreorderTraversal(int[] leftChildren, int[] rightChildren, int root) {
        List<Integer> order = new ArrayList<>();
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(root);

        while (!stack.isEmpty()) {
            int node = stack.pop();
            order.add(node);

            int rightChild = rightChildren[node];
            if (rightChild != -1) {
                stack.push(rightChild);
            }

            int leftChild = leftChildren[node];
            if (leftChild != -1) {
                stack.push(leftChild);
            }
        }

        return order;
    }
}
