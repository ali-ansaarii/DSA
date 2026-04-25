You are generating a new DSA topic inside this repository.

Repository instructions:
${repo_instructions}

Target algorithm:
- Algorithm name: ${algorithm_name}
- Display name: ${display_name}
- Topic path: ${topic_path}
- Additional notes: ${prompt_notes}

Current scaffolded files for this topic:
${topic_files}

Task:
1. Replace the scaffold TODOs with a complete, repository-consistent implementation.
2. Produce all required files for the topic under `${topic_path}` only.
3. Keep the repository style consistent with existing topics:
   - 4 languages
   - topic-level Makefile
   - PROBLEM.md focused on understanding
   - USAGE.md focused on commands and inputs
   - small/default, large, and challenge inputs
   - expected_output.txt that matches inputs/input.txt
4. Keep core algorithm logic separate from `main` where practical.
5. Do not write files outside `${topic_path}`.

Return exactly one file bundle with every file that should be written or overwritten for this topic.

