import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

public final class MonotonicQueue {
    private MonotonicQueue() {}

    public static List<Long> slidingWindowMaximum(List<Long> values, int windowSize) {
        Deque<Integer> candidateIndices = new ArrayDeque<>();
        List<Long> maxima = new ArrayList<>(Math.max(0, values.size() - windowSize + 1));

        for (int index = 0; index < values.size(); ++index) {
            while (!candidateIndices.isEmpty() && candidateIndices.peekFirst() <= index - windowSize) {
                candidateIndices.removeFirst();
            }

            while (!candidateIndices.isEmpty()
                    && values.get(candidateIndices.peekLast()) <= values.get(index)) {
                candidateIndices.removeLast();
            }

            candidateIndices.addLast(index);

            if (index + 1 >= windowSize) {
                maxima.add(values.get(candidateIndices.peekFirst()));
            }
        }

        return maxima;
    }
}
