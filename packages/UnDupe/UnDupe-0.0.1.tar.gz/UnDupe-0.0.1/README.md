# UnDupe

This is a tool to remove duplicate text with a focus on e-mails. It provides a starting point for data cleaning
and preprocessing in a natural language processing project and includes the following components:

- Preprocessor
    - Remove Email Addresses
    - Remove Hyperlinks
    - Remove Chains of hyphens, periods, underscores, and equal signs
    - Remove Phone Numbers
    - Remove Special Characters

- Filtering
    - Block Filter
    - Loop Filter




##Installation

To install this package using pip:

```bash
 $ pip install undupe
```

## Usage
    
### Pre-processing

The preprocess function consists of a chain of function calls to remove unwanted tokens.

```python
from undupe.preprocessing import preprocess_text

INPUT_FILE_PATH = r'' # Input text file to preprocess, delimited by new lines
OUTPUT_FILE_PATH = r'' # Output preprocessed file

texts = open(INPUT_FILE_PATH, 'r').readlines()

for i, text in enumerate(texts):
    text = preprocess_text.preprocess(text)
    texts[i] = text

with open(OUTPUT_FILE_PATH, 'w') as f:
    f.writelines(texts)
```

Example:

```
Input: _______ Hi this is a test. ======= Contact: (123) 555-6666 . Email: abcd@efg.com . Website: http://website.com
Output: hi this is a test. contact: . email: . website:
```

### Block filtering

Block filtering will remove texts within a contiguous block of similar texts using cosine similarity and works best for emails 
because of the thread like nature of emails whereby the first and last emails in a chain are most different.


This function takes either a preprocessed input file path or an unpreprocessed input file path, or both. 
```python
from undupe.preprocessing import remove_duplicates

remove_duplicates.block_filtering(r'PREPROCESSED_FILE_PATH',
                                   r'UNPROCESSED_FILE_PATH')
```

### Loop filtering

Loop filtering will remove similar texts dispersed throughout a file based on user selection. Another key feature allows
the user to save the current state of filtering.

This function takes either a preprocessed input file path, an unpreprocessed input file path, or both. Optionally, a saved file can be passed in as an argument
if some state was stored.

```python
from undupe.preprocessing import remove_duplicates

remove_duplicates.loop_filtering(r'PREPROCESSED_FILE_PATH',
                                  r'UNPROCESSED_FILE_PATH')
```

## Copyright & License
Copyright (c) 2019, Andrew Xiao, Rajat Bapuri, Sean Nordquist, MIT License.
