You are fixing a generated DSA topic after local verification failed.

Repository instructions:
${repo_instructions}

Target algorithm:
- Algorithm name: ${algorithm_name}
- Display name: ${display_name}
- Topic path: ${topic_path}

Verification failure output:
${verification_output}

Current files for this topic:
${topic_files}

Task:
1. Fix only the issues needed to make local verification pass.
2. Preserve correct repository conventions and topic structure.
3. Do not write files outside `${topic_path}`.
4. Return only the files that need to change for the fix.

Return exactly one file bundle with the files to overwrite.
