# Catalog Design

## Purpose
The automation catalog is not just a queue file.

It is the canonical contract for:

- what the project includes
- what a single automation run is responsible for delivering
- when multiple checklist labels map to the same implementation unit
- when one algorithm should be modeled as a parent topic with variants
- which naming, layout, and documentation conventions apply before code generation begins

The checklist answers "what should exist in the collection."
The catalog answers "what exactly are we building, how is it organized, and what counts as one deliverable unit."

## Design Principles

### 1. One Catalog Entry Equals One Delivery Unit
A catalog entry should correspond to one automation run and one PR-sized deliverable.

That unit may be:

- a single-topic algorithm such as `Trie`
- a parent topic with variants such as `Sliding Window`

But it should not be:

- an arbitrary bundle of unrelated algorithms
- a vague family without fixed scope

### 2. The Catalog Must Decide Scope Up Front
Before an item is added to the runnable catalog, the design must already answer:

- single topic or parent-with-variants?
- shared inputs or variant-specific inputs?
- which variants are in scope?
- which checklist labels are aliases of the same deliverable?
- what is the canonical baseline problem and input contract?

The automation should not have to invent these decisions mid-run.

### 3. Prefer Canonical Baselines Before Expansions
For most families, the first runnable entry should be the most canonical, teachable baseline.

Examples:

- `Merge Sort`: top-down baseline before bottom-up variants
- `Matrix Multiplication`: `classical` before `blocked`
- `Topological Sort`: Kahn baseline already exists; `DFS-based` remains a distinct later topic

### 4. Variants Must Represent Real Structural Differences
Use parent-with-variants only when the variants share the same conceptual algorithm family but differ in execution strategy or operational behavior.

Good variant splits:

- `DFS`: `recursive`, `iterative`
- `Sliding Window`: `fixed_size`, `variable_size`
- `Matrix Multiplication`: `classical`, `blocked`

Bad variant splits:

- `Hash Table` and `Hash Set`
- `Fenwick Tree` and `Segment Tree`
- `KMP` and `Z-Algorithm`

Those are separate topics, not sibling variants of one deliverable.

### 5. The Catalog Should Be Stable Enough To Audit
Catalog entries should be reviewable as design artifacts.
They should not be generated on the fly from prompt text.

That means:

- explicit topic paths
- explicit branch names
- explicit PR titles
- explicit aliases
- explicit notes about constraints or benchmark expectations

## Entry Kinds

### Single Topic
Use a single topic when one algorithm maps cleanly to one folder and one baseline runner shape.

Examples:

- `Trie`
- `KMP`
- `Fenwick Tree`
- `Merge Sort`

### Parent With Variants
Use a parent topic when one conceptual algorithm family should ship as one deliverable containing multiple tightly related variants.

Examples:

- `graph/DFS/{recursive,iterative}`
- `array/SlidingWindow/{fixed_size,variable_size}`
- `array/MatrixMultiplication/{classical,blocked}` once implemented that way

Design rule:
- shared inputs and parent-level orchestration live at the parent
- each child variant still owns its own code and variant-specific problem explanation

### Alias Labels
Multiple checklist labels may map to one catalog entry when they represent the same implementation unit.

Example:

- catalog entry name: `KMP`
- primary checklist label: `KMP`
- alias checklist label: `KMP Prefix Function`

Aliases are allowed only when the repository should not create a second topic or second PR.

## Naming Rules

### Catalog Key
The top-level catalog key should be the user-facing algorithm name that the automation accepts.

Examples:

- `Trie`
- `Merge Sort`
- `Topological Sort, DFS-based`

### Branch Name
Branch names must follow repo policy:

- lowercase
- kebab-case
- no slash-separated namespaces

Examples:

- `merge-sort`
- `topological-sort-dfs-based`
- `matrix-multiplication`

### Topic Path
Topic paths must reflect repository structure, not branch names.

Examples:

- `string/Trie`
- `sorting/MergeSort`
- `graph/DFS`

For parent-with-variants, the catalog entry points to the parent topic path.

## What Belongs In Catalog Design

Each entry must define at least:

- `checklist_label`
- `checklist_aliases` when needed
- `topic_path`
- `display_name`
- `algo_id`
- `binary_name`
- `time_flag`
- `branch_name`
- `pr_title`
- `prompt_notes`

Recommended design-only metadata, even if the current runner does not yet consume all of it:

- `entry_kind`
  - `single_topic`
  - `variant_parent`
- `family`
  - `sorting`
  - `string`
  - `graph`
  - `tree`
  - `array-search`
- `canonical_problem`
  - one sentence defining the baseline task
- `input_contract`
  - short description of expected input shape
- `variants`
  - ordered list for parent topics
- `shared_inputs`
  - whether inputs live at parent level
- `design_status`
  - `ready`
  - `needs_variant_decision`
  - `needs_prompt_refinement`

## Variant Decision Policy By Family

### Graph Traversal
- `Depth-First Search, recursive` and `Depth-First Search, iterative`
  - already modeled as one parent family with two child variants
- `Breadth-First Search`
  - separate single topic
- `Bidirectional BFS`
  - separate topic, not a BFS variant child

Reason:
- DFS recursive/iterative differ mainly in traversal mechanism while preserving one family identity
- Bidirectional BFS changes the algorithmic strategy enough to deserve its own topic

### Graph Algorithms
Split this family into:

- traversal/search topics
- shortest-path topics
- spanning-tree topics
- connectivity/decomposition topics
- DAG-specialized topics

Ready graph entries include:

- parent-with-variants:
  - `Depth-First Search`
    - `recursive`
    - `iterative`
- ready single-topic baselines:
  - `Breadth-First Search`
  - `Dijkstra`
  - `Bellman-Ford`
  - `Floyd-Warshall`
  - `Topological Sort`
  - `Topological Sort, DFS-based`
  - `Shortest Path in DAG`
  - `Bidirectional BFS`
  - `A* Search`
  - `Kruskal Minimum Spanning Tree`
  - `Prim Minimum Spanning Tree`
  - `Strongly Connected Components, Kosaraju`
  - `Strongly Connected Components, Tarjan`
  - `Bridges`
  - `Articulation Points`
  - `Eulerian Path, Hierholzer`

Graph-family entries that should remain non-runnable until their baseline is fixed:

- `DAG Dynamic Programming`

Reason:
- the name still describes a broad technique family rather than one precise runner contract

Cross-family note:
- `Disjoint Set Union` remains a standalone data-structure topic in repo layout, but catalogued as graph-relevant because of its direct role in graph algorithms such as Kruskal.

### Sliding Window
- one parent family
- variants:
  - `fixed_size`
  - `variable_size`

Reason:
- these are standard sibling formulations of one pattern family

### Array And Search Patterns
Split this family into three subgroups:

- concrete single-topic techniques with a clear runner contract
- parent-with-variants families
- broad patterns that should not become runnable until one canonical baseline is fixed

Ready single-topic baselines include:

- `Prefix Sum`
- `Suffix Sum`
- `Difference Array`
- `Interval Merge`
- `Boyer-Moore Majority Vote`
- `Quickselect`
- `Kadane's Algorithm`
- `2D Prefix Sum`
- `Binary Search on Answer`
- `Ternary Search`

Ready parent-with-variants families include:

- `Binary Search`
  - `exact_match`
  - `boundary`
- `Sliding Window`
  - `fixed_size`
  - `variable_size`
- `Matrix Multiplication`
  - `classical`
  - `blocked`

Pattern-level topics that should remain non-runnable until their baseline is fixed:

- `Two Pointers`
- `Fast and Slow Pointers`
- `Sweep Line`

Reason:
- these names describe broad techniques rather than one self-evident runner contract
- the catalog must choose a canonical baseline explicitly before automation can generate a high-quality topic

### Sorting
Treat each major sort as a separate single-topic entry.

Examples:

- `Insertion Sort`
- `Selection Sort`
- `Merge Sort`
- `Quick Sort`
- `Heap Sort`
- `Counting Sort`
- `Radix Sort`

Reason:
- each sort has its own algorithm identity, input expectations, and teaching story
- bundling them into one parent topic would make delivery units too large and reduce queue clarity

### Tree Traversals
Use parent-with-variants when the repo is intentionally teaching one traversal family through multiple forms.

Examples:

- `Binary Tree Traversals, recursive`
- `Binary Tree Traversals, iterative`

But keep structurally different tree problems separate:

- `Binary Tree Level Order Traversal`
- `Validate Binary Search Tree`
- `Lowest Common Ancestor in Binary Tree`

Current repo-design wrinkle:

- the implemented binary-tree traversal topics are currently nested by traversal order:
  - `Preorder`
  - `Inorder`
  - `Postorder`
- and then by execution style:
  - `recursive`
  - `iterative`

So the catalog should not pretend that `Binary Tree Traversals` is already a clean runnable unit.
It should remain a design-level entry until we deliberately decide whether:

- one nested parent topic is acceptable as a delivery unit
- or preorder/inorder/postorder should each become their own top-level parent topics

### Tree And Range Structures
This family should be split into:

- traversal and structural tree topics
- search-tree topics
- ancestor/query topics
- tree-DP topics
- range-query structures that the checklist groups here

Ready tree-family baselines include:

- `Rooted Tree Traversals, preorder`
- `Rooted Tree Traversals, postorder`
- `Binary Tree Level Order Traversal`
- `Binary Search Tree Search and Insert`
- `Validate Binary Search Tree`
- `Lowest Common Ancestor in Binary Tree`
- `Lowest Common Ancestor in Binary Search Tree`
- `Binary Lifting`
- `Tree Diameter`
- `Fenwick Tree`
- `Segment Tree`
- `Lazy Segment Tree`
- `Sparse Table`

Tree-family entries that should remain non-runnable until their baseline is fixed:

- `Binary Tree Traversals`
  - because the current nested variant shape has not been normalized into a stable delivery unit
- `Balanced Binary Search Tree`
  - because AVL vs Red-Black is still a design choice
- `Subtree Dynamic Programming`
- `Rerooting Dynamic Programming`

Reason:
- these names still hide important structural decisions that the automation should not invent during generation

### String Algorithms
Treat major algorithms as separate topics.

Examples:

- `Trie`
- `KMP`
- `Z-Algorithm`
- `Rabin-Karp`
- `Aho-Corasick`

Aliases are allowed only for naming overlap such as:

- `KMP`
- `KMP Prefix Function`

String-family design rules:

- `KMP`, `Z-Algorithm`, and `Rabin-Karp` should share one exact-matching baseline contract when practical:
  - one text
  - one pattern
  - report all match starting indices
- `Trie` is a dictionary/data-structure topic, so it should remain command-based instead of being forced into the exact-matching contract.
- `Aho-Corasick` is a multi-pattern matching topic and therefore needs its own input model.
- `Manacher` is a palindrome-analysis topic and should use a single-string input model.
- `Suffix Array` and `Suffix Automaton` are string-indexing/substring-structure topics; they should not become runnable until their observable output contract is fixed clearly enough for automation.

### Matrix Multiplication
Design as one parent family with sibling variants:

- `classical`
- `blocked`

Reason:
- same problem
- shared input model
- strong systems-comparison value
- shared parent orchestration and benchmark story

Checklist labels for `Matrix Multiplication, classical` and `Matrix Multiplication, blocked` should map to this one parent deliverable rather than to two unrelated PRs.

### Linked Structures
Treat these as separate topics:

- `Linked List, singly`
- `Linked List, doubly`
- `Linked List reversal`

Reason:
- different deliverable scopes and code structure
- reversal is an operation topic, not a sibling representation variant

### Search Variants
Treat these as separate topics:

- `Binary Search`
- `Binary Search on Answer`
- `Ternary Search`

Reason:
- despite naming similarity, they encode different problem contracts
- `Binary Search` itself may still be modeled as one parent family with `exact_match` and `boundary` child variants because those are closely related operational forms of the same lookup family

## Readiness Gates Before An Entry Becomes Runnable

An entry is ready for the runnable catalog only when all of the following are settled:

1. Topic path is final.
2. Delivery unit size is final.
3. Variant shape is final.
4. Checklist aliases are final.
5. Canonical baseline problem is final.
6. Input contract is clear enough for all four languages.
7. Prompt notes are specific enough to constrain generation toward repo conventions.

If any of those are unresolved, the entry is still in design, not in the runnable queue.

## Catalog Expansion Workflow

### Step 1. Family Design Pass
For a family such as sorting, graph traversal, or string algorithms:

- decide entry boundaries
- decide variants
- decide aliases
- decide canonical baseline problems

### Step 2. Encode Metadata
Add or update catalog entries with the agreed structure and notes.

### Step 3. Enable Only Ready Entries
Only entries with stable scope decisions should be considered runnable by the queue.

### Step 4. Let Live Runs Pressure-Test The Design
If repeated runs expose ambiguity in an entry, fix the catalog design before adding more neighboring entries from that family.

## Quality Bar For Catalog PRs

A catalog design PR is acceptable only if:

1. Entry boundaries are coherent and non-overlapping.
2. Variant decisions are explicitly justified for each family that needs them.
3. Aliases do not create duplicate deliverables.
4. Branch names and topic paths follow repo conventions.
5. Prompt notes are specific enough to produce consistent repo-shaped output.
6. New runnable entries are not added until their design is actually stable.

## Immediate Implications For This Repository

The next catalog expansion should happen family by family, not item by item.

Recommended order:

1. sorting
2. string
3. array/search
4. graph
5. tree
6. DP and math

This order is good because:

- it reuses prompt shape and input models
- it reduces ambiguity while the queue is still being hardened
- it keeps family-level design decisions coherent instead of retrofitting them later
