import java.util.ArrayList;
import java.util.List;

public final class KMP {
    private KMP() {}

    public static int[] buildLPS(String pattern) {
        int[] lps = new int[pattern.length()];
        int length = 0;

        for (int i = 1; i < pattern.length(); i++) {
            while (length > 0 && pattern.charAt(i) != pattern.charAt(length)) {
                length = lps[length - 1];
            }
            if (pattern.charAt(i) == pattern.charAt(length)) {
                length++;
                lps[i] = length;
            }
        }

        return lps;
    }

    public static List<Integer> search(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();

        if (pattern.isEmpty()) {
            for (int i = 0; i <= text.length(); i++) {
                matches.add(i);
            }
            return matches;
        }

        int[] lps = buildLPS(pattern);
        int matched = 0;

        for (int i = 0; i < text.length(); i++) {
            while (matched > 0 && text.charAt(i) != pattern.charAt(matched)) {
                matched = lps[matched - 1];
            }

            if (text.charAt(i) == pattern.charAt(matched)) {
                matched++;
            }

            if (matched == pattern.length()) {
                matches.add(i + 1 - pattern.length());
                matched = lps[matched - 1];
            }
        }

        return matches;
    }
}
