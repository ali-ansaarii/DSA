import java.util.*;

public class PreorderTraversal {
    public static List<Integer> PreorderTraversal(int[] leftChildren, int[] rightChildren, int root) {
        List<Integer> order = new ArrayList<>();
        traverse(root, leftChildren, rightChildren, order);
        return order;
    }

    private static void traverse(int node, int[] leftChildren, int[] rightChildren, List<Integer> order) {
        order.add(node);

        int leftChild = leftChildren[node];
        if (leftChild != -1) {
            traverse(leftChild, leftChildren, rightChildren, order);
        }

        int rightChild = rightChildren[node];
        if (rightChild != -1) {
            traverse(rightChild, leftChildren, rightChildren, order);
        }
    }
}
