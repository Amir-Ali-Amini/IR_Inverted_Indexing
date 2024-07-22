
# BSBI Algorithm for Inverted Indexing

## Project Details

**Author:** AmirAli Amini  
**Student ID:** 610399102  
**Project:** HW2  

### Overview

This project implements the Blocked Sort-Based Indexing (BSBI) algorithm, a foundational technique for constructing inverted indexes. Inverted indexing is a crucial component of information retrieval systems, enabling efficient search and retrieval of documents that contain specific words or phrases.

### Key Features

- **Gamma Coding**: The algorithm includes a custom implementation for converting numbers to gamma codes and vice versa. This technique is used to compress index data efficiently.
- **Binary Search**: A binary search function is implemented to locate words within posting lists, optimizing the indexing process.
- **Tokenization and Preprocessing**: Utilizes the Natural Language Toolkit (NLTK) for tokenizing input documents, removing stopwords, and handling punctuation, ensuring a clean and efficient indexing process.
- **Sub-posting List Merging**: Handles the merging of sub-posting lists by maintaining and updating document indices.

### Libraries Used

- **NLTK**: Used for tokenizing text and handling stopwords.
- **NumPy**: Utilized for mathematical operations on arrays.
- **Pickle**: For saving and loading intermediate posting lists to and from disk.
- **Shutil**: To handle directory operations, such as removing and creating folders.

### Implementation Details

- **searchEngine Class**: The core of the implementation. Handles all functionalities from tokenizing text to merging posting lists and encoding document indices with gamma codes.
- **Input Functionality**: Reads and processes documents, tokenizes text, and constructs sub-posting lists. It saves each sub-posting list to a file after processing a batch of documents.
- **Merging Functionality**: Reads saved sub-posting lists from files, merges them into a main posting list, and encodes indices using gamma coding.

### Challenges and Improvements

- **Merging Sub-Posting Lists**: One of the main challenges was efficiently merging sub-posting lists and converting indices to gamma codes. A custom function was created to handle these operations.
- **Efficient Indexing**: Developed a function to compute the distance from the first element to a reference point and update the index with the difference from the previous element.

### Usage

To use this implementation, input document files should be placed in the designated folder, and the main script should be executed. The system will output indexed data and allow query-based searches.

### Conclusion

This project successfully demonstrates the implementation of the BSBI algorithm for inverted indexing, handling large datasets efficiently and showcasing improvements in gamma coding and merging techniques.

## How to Run

1. Ensure that all dependencies are installed:

   ```bash
   pip install nltk numpy
    ```

2. Download the nltk datasets:

    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    ```

3. Use the searchEngine class to create an index and perform queries:

    ```python
    import os
    directory_input = ['docs/'+path for path in os.listdir('docs') if path.endswith('.txt')]

    engine = searchEngine(tempDirectory="postingLists")
    engine.input(directory_input)
    engine.mergePostingLists()

    results = engine.find("your query here")
    print(results)
    ```
