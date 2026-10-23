# DAA Text Compression System Using Huffman Coding

## 1. Project Overview

The DAA Text Compression System is a mini-project developed using C++ and Streamlit. It demonstrates the working of Huffman Coding, a greedy algorithm used to compress text by assigning variable-length binary codes to characters based on their frequencies.

The system allows users to select a text file, compress its contents, view compression statistics, and decompress the compressed data to recover the original text.

## 2. Objectives

- To implement Huffman Coding using a greedy algorithm.
- To reduce the storage space required for text files.
- To understand character frequency analysis and binary code generation.
- To demonstrate file compression and decompression.
- To compare the original and compressed file sizes.

## 3. Technologies Used

- **C++:** Implementation of the Huffman Coding algorithm.
- **Python:** Application integration and supporting logic.
- **Streamlit:** User interface for interacting with the system.
- **VS Code:** Development environment.

## 4. Algorithm Used: Huffman Coding

Huffman Coding is a lossless data compression algorithm. It creates a binary tree using the frequency of each character.

### Working Steps

1. Read the input text file.
2. Calculate the frequency of each character.
3. Create a leaf node for each character.
4. Insert the nodes into a priority queue.
5. Select the two nodes with the lowest frequencies.
6. Merge them into a new node and insert it back into the queue.
7. Repeat until a single Huffman tree remains.
8. Generate binary codes by traversing the tree.
9. Encode the original text using these codes.
10. Decode the compressed data to reconstruct the original text.

## 5. Features

- Text file input.
- Character frequency analysis.
- Huffman code generation.
- Text compression.
- Compressed file output.
- Decompression and recovery of original text.
- Display of compression statistics.
- Simple and interactive user interface.
- Sample text files for testing.

## 6. How to Run the Project

### Prerequisites

Install Python 3, a C++ compiler, and Streamlit. The application may also require the relevant C++ compiler tools available on your operating system.

### Installation

Install Streamlit in your active Python environment:

```bash
pip install streamlit
```

Ensure that the C++ source file and the Python application are present in the project directory.

### Execution

Open the project folder in the terminal and run:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to use the application.

**Note:** The C++ source code must be compiled or invoked according to the integration implemented in the application. Follow any additional compiler instructions required by your setup.

## 7. Testing

The application can be tested using sample text files containing short sentences, repeated characters, paragraphs, and longer text.

The following cases can be checked:

- Compress a valid text file.
- Verify that a compressed output is generated.
- Decompress the output.
- Compare the recovered text with the original.
- Check the displayed compression statistics.
- Test an empty or invalid input file, where supported.

## 8. Applications

- Reducing storage requirements for text data.
- Learning lossless compression techniques.
- Understanding greedy algorithms.
- Demonstrating data structures such as binary trees and priority queues.
- Studying algorithm design and analysis.

## 9. Advantages

- Lossless compression preserves the original information.
- Frequently occurring characters can receive shorter codes.
- The algorithm demonstrates an important application of greedy strategy.
- The project combines algorithm implementation with a user-friendly interface.

## 10. Limitations

- Compression efficiency depends on the input text.
- Small files may not become smaller after accounting for the metadata required for decompression.
- Huffman Coding is not equally effective for every type of data.
- Compression performance depends on the implementation and file format.

## 11. Future Scope

- Support for additional file formats.
- Improved compression and decompression speed.
- Comparison with other compression algorithms.
- Graphical visualization of the Huffman tree.
- Detailed performance analysis using different input sizes.

## 12. Conclusion

The DAA Text Compression System demonstrates the practical application of Huffman Coding, a greedy algorithm used for lossless data compression. It helps explain character frequencies, priority queues, binary trees, encoding, and decoding through a practical implementation. The project connects theoretical concepts from Design and Analysis of Algorithms with a working software application.

## Author

Developed as a mini-project for the Design and Analysis of Algorithms (DAA) subject.
