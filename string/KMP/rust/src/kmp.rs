pub fn build_lps(pattern: &str) -> Vec<usize> {
    let pattern_bytes = pattern.as_bytes();
    let mut lps = vec![0; pattern_bytes.len()];
    let mut length = 0usize;

    for i in 1..pattern_bytes.len() {
        while length > 0 && pattern_bytes[i] != pattern_bytes[length] {
            length = lps[length - 1];
        }
        if pattern_bytes[i] == pattern_bytes[length] {
            length += 1;
            lps[i] = length;
        }
    }

    lps
}

pub fn kmp(text: &str, pattern: &str) -> Vec<usize> {
    if pattern.is_empty() {
        return (0..=text.len()).collect();
    }

    let text_bytes = text.as_bytes();
    let pattern_bytes = pattern.as_bytes();
    let lps = build_lps(pattern);
    let mut matches = Vec::new();
    let mut matched = 0usize;

    for (i, &byte) in text_bytes.iter().enumerate() {
        while matched > 0 && byte != pattern_bytes[matched] {
            matched = lps[matched - 1];
        }

        if byte == pattern_bytes[matched] {
            matched += 1;
        }

        if matched == pattern_bytes.len() {
            matches.push(i + 1 - pattern_bytes.len());
            matched = lps[matched - 1];
        }
    }

    matches
}
