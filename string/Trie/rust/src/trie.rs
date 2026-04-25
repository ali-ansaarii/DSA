#[derive(Clone, Copy)]
struct Node {
    children: [Option<usize>; 26],
    is_word: bool,
}

impl Node {
    fn new() -> Self {
        Self {
            children: [None; 26],
            is_word: false,
        }
    }
}

pub struct Operation {
    pub command: String,
    pub value: String,
}

pub struct Trie {
    nodes: Vec<Node>,
}

impl Trie {
    pub fn new() -> Self {
        Self {
            nodes: vec![Node::new()],
        }
    }

    pub fn insert(&mut self, word: &str) -> Result<(), String> {
        let mut current = 0usize;
        for byte in word.bytes() {
            let index = letter_index(byte)?;
            if self.nodes[current].children[index].is_none() {
                let next = self.nodes.len();
                self.nodes.push(Node::new());
                self.nodes[current].children[index] = Some(next);
            }
            current = self.nodes[current].children[index].expect("child was just created or already existed");
        }
        self.nodes[current].is_word = true;
        Ok(())
    }

    pub fn search(&self, word: &str) -> Result<bool, String> {
        Ok(self
            .find_node(word)?
            .is_some_and(|node_index| self.nodes[node_index].is_word))
    }

    pub fn starts_with(&self, prefix: &str) -> Result<bool, String> {
        Ok(self.find_node(prefix)?.is_some())
    }

    fn find_node(&self, text: &str) -> Result<Option<usize>, String> {
        let mut current = 0usize;
        for byte in text.bytes() {
            let index = letter_index(byte)?;
            match self.nodes[current].children[index] {
                Some(next) => current = next,
                None => return Ok(None),
            }
        }
        Ok(Some(current))
    }
}

fn letter_index(byte: u8) -> Result<usize, String> {
    if byte.is_ascii_lowercase() {
        Ok((byte - b'a') as usize)
    } else {
        Err(String::from("Trie only supports lowercase English letters"))
    }
}

pub fn execute_trie_commands(operations: &[Operation]) -> Result<Vec<String>, String> {
    let mut trie = Trie::new();
    let mut output = Vec::new();

    for operation in operations {
        match operation.command.as_str() {
            "insert" => trie.insert(&operation.value)?,
            "search" => output.push(if trie.search(&operation.value)? {
                String::from("true")
            } else {
                String::from("false")
            }),
            "starts_with" => output.push(if trie.starts_with(&operation.value)? {
                String::from("true")
            } else {
                String::from("false")
            }),
            _ => return Err(format!("Unknown trie command: {}", operation.command)),
        }
    }

    Ok(output)
}
