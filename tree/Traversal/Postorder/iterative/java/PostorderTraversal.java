import java.util.*;

public class PostorderTraversal {
    private static final class Frame {
        final int node;
        final boolean expanded;

        Frame(int node, boolean expanded) {
            this.node = node;
            this.expanded = expanded;
        }
    }

    public static List<Integer> PostorderTraversal(int[] leftChildren, int[] rightChildren, int root) {
        List<Integer> order = new ArrayList<>();
        Deque<Frame> stack = new ArrayDeque<>();
        stack.push(new Frame(root, false));

        while (!stack.isEmpty()) {
            Frame frame = stack.pop();
            if (frame.expanded) {
                order.add(frame.node);
                continue;
            }

            stack.push(new Frame(frame.node, true));

            int rightChild = rightChildren[frame.node];
            if (rightChild != -1) {
                stack.push(new Frame(rightChild, false));
            }

            int leftChild = leftChildren[frame.node];
            if (leftChild != -1) {
                stack.push(new Frame(leftChild, false));
            }
        }

        return order;
    }
}
