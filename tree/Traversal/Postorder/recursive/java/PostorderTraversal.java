import java.util.*;

public class PostorderTraversal {
    public static List<Integer> PostorderTraversal(int[] leftChildren, int[] rightChildren, int root) {
        List<Integer> order = new ArrayList<>();
        traverse(root, leftChildren, rightChildren, order);
        return order;
    }

    private static void traverse(int node, int[] leftChildren, int[] rightChildren, List<Integer> order) {
        int leftChild = leftChildren[node];
        if (leftChild != -1) {
            traverse(leftChild, leftChildren, rightChildren, order);
        }

        int rightChild = rightChildren[node];
        if (rightChild != -1) {
            traverse(rightChild, leftChildren, rightChildren, order);
        }

        order.add(node);
    }
}
