
#include <iostream>
#include <fstream>
#include <cstdint>
#include <string>
#include <queue>
#include <vector>
#include <array>
#include <algorithm>
#include <iterator>

using namespace std;

struct Node {
    unsigned char ch;
    uint64_t freq;
    int minSymbol;
    Node* left;
    Node* right;

    Node(unsigned char c, uint64_t f)
        : ch(c), freq(f), minSymbol(c),
          left(nullptr), right(nullptr) {}

    Node(Node* l, Node* r)
        : ch(0), freq(l->freq + r->freq),
          minSymbol(min(l->minSymbol, r->minSymbol)),
          left(l), right(r) {}

    bool isLeaf() const {
        return left == nullptr && right == nullptr;
    }
};

struct Compare {
    bool operator()(Node* a, Node* b) const {
        if (a->freq != b->freq)
            return a->freq > b->freq;
        return a->minSymbol > b->minSymbol;
    }
};

void deleteTree(Node* root) {
    if (!root) return;
    deleteTree(root->left);
    deleteTree(root->right);
    delete root;
}

Node* buildTree(const array<uint64_t, 256>& freq) {
    priority_queue<Node*, vector<Node*>, Compare> pq;

    for (int i = 0; i < 256; i++) {
        if (freq[i] > 0)
            pq.push(new Node(static_cast<unsigned char>(i), freq[i]));
    }

    if (pq.empty()) return nullptr;

    while (pq.size() > 1) {
        Node* left = pq.top();
        pq.pop();

        Node* right = pq.top();
        pq.pop();

        pq.push(new Node(left, right));
    }

    return pq.top();
}

void generateCodes(Node* root, string code,
                   array<string, 256>& codes) {
    if (!root) return;

    if (root->isLeaf()) {
        codes[root->ch] = code.empty() ? "0" : code;
        return;
    }

    generateCodes(root->left, code + "0", codes);
    generateCodes(root->right, code + "1", codes);
}

int compressFile() {
    ifstream input("test_files/sample.txt", ios::binary);

    if (!input) {
        cerr << "Error: Cannot open test_files/sample.txt\n";
        return 1;
    }

    string text((istreambuf_iterator<char>(input)),
                 istreambuf_iterator<char>());
    input.close();

    array<uint64_t, 256> freq{};
    for (unsigned char ch : text)
        freq[ch]++;

    Node* root = buildTree(freq);

    array<string, 256> codes{};
    generateCodes(root, "", codes);

    string encoded;
    for (unsigned char ch : text)
        encoded += codes[ch];

    ofstream output("compressed.huff", ios::binary);

    if (!output) {
        cerr << "Error: Cannot create compressed.huff\n";
        deleteTree(root);
        return 1;
    }

    // File signature
    output.write("HUFF", 4);

    // Original file size
    uint64_t originalSize = text.size();
    output.write(reinterpret_cast<const char*>(&originalSize),
                 sizeof(originalSize));

    // Number of distinct byte values
    uint16_t uniqueChars = 0;
    for (uint64_t f : freq)
        if (f > 0) uniqueChars++;

    output.write(reinterpret_cast<const char*>(&uniqueChars),
                 sizeof(uniqueChars));

    // Store each byte and its frequency in ascending byte order
    for (int i = 0; i < 256; i++) {
        if (freq[i] > 0) {
            unsigned char ch = static_cast<unsigned char>(i);
            output.write(reinterpret_cast<const char*>(&ch), 1);
            output.write(reinterpret_cast<const char*>(&freq[i]),
                         sizeof(freq[i]));
        }
    }

    // Pack encoded bits into bytes
    unsigned char byte = 0;
    int bitCount = 0;

    for (char bit : encoded) {
        byte = static_cast<unsigned char>(
            (byte << 1) | (bit == '1' ? 1 : 0)
        );
        bitCount++;

        if (bitCount == 8) {
            output.put(static_cast<char>(byte));
            byte = 0;
            bitCount = 0;
        }
    }

    if (bitCount > 0) {
        byte <<= (8 - bitCount);
        output.put(static_cast<char>(byte));
    }

    output.close();
    deleteTree(root);

    if (!output) {
        cerr << "Error: Failed while writing compressed file\n";
        return 1;
    }

    ifstream original("test_files/sample.txt", ios::binary | ios::ate);
    ifstream compressed("compressed.huff", ios::binary | ios::ate);

    auto originalSizeBytes = original.tellg();
    auto compressedSizeBytes = compressed.tellg();

    cout << "Compression successful!\n";
    cout << "Original file size: " << originalSizeBytes << " bytes\n";
    cout << "Compressed file size: " << compressedSizeBytes << " bytes\n";

    if (originalSizeBytes > 0) {
        double reduction =
            (1.0 - static_cast<double>(compressedSizeBytes) /
             static_cast<double>(originalSizeBytes)) * 100.0;

        cout << "Size reduction: " << reduction << "%\n";
    }

    cout << "Saved to compressed.huff\n";
    return 0;
}

int decompressFile() {
    ifstream input("compressed.huff", ios::binary);

    if (!input) {
        cerr << "Error: Cannot open compressed.huff\n";
        return 1;
    }

    char signature[4];
    input.read(signature, 4);

    if (!input || string(signature, 4) != "HUFF") {
        cerr << "Error: Invalid compressed file\n";
        return 1;
    }

    uint64_t originalSize = 0;
    uint16_t uniqueChars = 0;

    input.read(reinterpret_cast<char*>(&originalSize),
               sizeof(originalSize));
    input.read(reinterpret_cast<char*>(&uniqueChars),
               sizeof(uniqueChars));

    if (!input || uniqueChars > 256) {
        cerr << "Error: Invalid file header\n";
        return 1;
    }

    array<uint64_t, 256> freq{};

    for (uint16_t i = 0; i < uniqueChars; i++) {
        unsigned char ch;
        uint64_t count;

        input.read(reinterpret_cast<char*>(&ch), 1);
        input.read(reinterpret_cast<char*>(&count), sizeof(count));

        if (!input || count == 0 || freq[ch] != 0) {
            cerr << "Error: Invalid frequency table\n";
            return 1;
        }

        freq[ch] = count;
    }

    uint64_t totalFrequency = 0;
    for (uint64_t count : freq) {
        if (count > UINT64_MAX - totalFrequency) {
            cerr << "Error: Invalid original size\n";
            return 1;
        }
        totalFrequency += count;
    }

    if (totalFrequency != originalSize ||
        ((originalSize == 0) != (uniqueChars == 0))) {
        cerr << "Error: Inconsistent file header\n";
        return 1;
    }

    Node* root = buildTree(freq);

    ofstream output("decompressed.txt", ios::binary);
    if (!output) {
        cerr << "Error: Cannot create decompressed.txt\n";
        deleteTree(root);
        return 1;
    }

    // An empty input file needs no encoded data.
    if (originalSize == 0) {
        output.close();
        deleteTree(root);
        cout << "Decompression successful! Output: decompressed.txt\n";
        return 0;
    }

    // A one-character file has a tree with just one leaf.
    if (root->isLeaf()) {
        for (uint64_t i = 0; i < originalSize; i++)
            output.put(static_cast<char>(root->ch));

        output.close();
        deleteTree(root);
        cout << "Decompression successful! Output: decompressed.txt\n";
        return 0;
    }

    uint64_t decoded = 0;
    Node* current = root;
    char rawByte;

    while (decoded < originalSize && input.get(rawByte)) {
        unsigned char byte = static_cast<unsigned char>(rawByte);

        for (int bit = 7; bit >= 0 && decoded < originalSize; bit--) {
            bool one = ((byte >> bit) & 1) != 0;
            current = one ? current->right : current->left;

            if (!current) {
                cerr << "Error: Invalid encoded data\n";
                output.close();
                deleteTree(root);
                return 1;
            }

            if (current->isLeaf()) {
                output.put(static_cast<char>(current->ch));
                decoded++;
                current = root;
            }
        }
    }

    output.close();
    deleteTree(root);

    if (decoded != originalSize) {
        cerr << "Error: Compressed file ended unexpectedly\n";
        return 1;
    }

    cout << "Decompression successful!\n";
    cout << "Restored file: decompressed.txt\n";
    cout << "Restored size: " << decoded << " bytes\n";

    return 0;
}

int main(int argc, char* argv[]) {
    cout << "===== DAA TEXT COMPRESSION SYSTEM =====\n";

    if (argc > 1 && string(argv[1]) == "decompress")
        return decompressFile();

    return compressFile();
}
