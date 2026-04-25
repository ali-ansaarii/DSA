You are fixing a generated DSA topic after Codex review feedback.

Repository instructions:
${repo_instructions}

Target algorithm:
- Algorithm name: ${algorithm_name}
- Display name: ${display_name}
- Topic path: ${topic_path}

Actionable review comments:
${review_comments}

Current files for this topic:
${topic_files}

Task:
1. Fix only the issues implied by the review comments.
2. Preserve existing correct behavior and repository conventions.
3. Do not write files outside `${topic_path}`.
4. Return only the files that need to change for the fix.

Return exactly one file bundle with the files to overwrite.
