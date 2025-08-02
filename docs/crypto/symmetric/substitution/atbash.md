# Atbash Cipher

## History

The Atbash cipher is one of the oldest known substitution ciphers, dating back to ancient Hebrew times. It was originally used to encode the Hebrew alphabet, where the first letter (Aleph) was replaced by the last letter (Tav), the second letter (Bet) by the second-to-last letter (Shin), and so on.

The name "Atbash" comes from the Hebrew words "Aleph-Tav-Bet-Shin" (א-ת-ב-ש), representing the first, last, second, and second-to-last letters of the Hebrew alphabet.

## Concept

The Atbash cipher is a simple substitution cipher that replaces each letter with the letter that is symmetric about the center of the alphabet.

**Mathematical Representation:**
- For uppercase letters: `E(x) = (25 - (x - 65)) + 65 = 90 - x + 65 = 155 - x`
- For lowercase letters: `E(x) = (25 - (x - 97)) + 97 = 122 - x + 97 = 219 - x`

Where:
- `x` is the ASCII value of the input character
- 65 is the ASCII value of 'A'
- 97 is the ASCII value of 'a'
- 25 is the position of 'Z' in a 0-indexed alphabet

**Important Note:** Atbash is a special case of the Affine cipher where `a = 25` and `b = 25`. The transformation can be written as: `E(x) = (25x + 25) mod 26`

## Encryption Process

1. **Alphabet Mapping:**
   ```
   A ↔ Z, B ↔ Y, C ↔ X, D ↔ W, E ↔ V, F ↔ U, G ↔ T, H ↔ S, I ↔ R, J ↔ Q, K ↔ P, L ↔ O, M ↔ N
   a ↔ z, b ↔ y, c ↔ x, d ↔ w, e ↔ v, f ↔ u, g ↔ t, h ↔ s, i ↔ r, j ↔ q, k ↔ p, l ↔ o, m ↔ n
   ```

2. **Example:**
   ```
   Plaintext:  "ATBASH CIPHER"
   Encrypted:  "ZGYZHS XRKSVI"
   
   A → Z, T → G, B → Y, A → Z, S → H, H → S
   C → X, I → R, P → K, H → S, E → V, R → I
   ```

## Decryption Process

Since Atbash is its own inverse, the decryption process is identical to encryption:

```
Ciphertext: "ZGYZHS XRKSVI"
Decrypted:  "ATBASH CIPHER"
```

## Relationship to Affine Cipher

Atbash is a special case of the Affine cipher with parameters `a = 25` and `b = 25`:

- **Affine transformation:** `E(x) = (ax + b) mod 26`
- **Atbash transformation:** `E(x) = (25x + 25) mod 26`

This means that Atbash inherits all the mathematical properties of the Affine cipher while being constrained to a specific parameter set.

## No Attack Methods

Atbash has no meaningful attack methods because it has no variability - it's a fixed algorithm without a key. The transformation is deterministic and known:

- **No Key Space:** Only one possible configuration
- **No Brute Force:** Only one transformation to try
- **No Frequency Analysis:** The transformation is fixed and known
- **No Known Plaintext:** Any known plaintext immediately reveals the algorithm

Any attempt to "attack" Atbash would simply be applying the transformation to see if it produces meaningful text, which is not a cryptographic attack in the traditional sense.

## Security Analysis

### Strengths
- **Simplicity:** Easy to implement and understand
- **Deterministic:** Same input always produces same output
- **Self-inverse:** Same operation for encryption and decryption
- **Mathematical Foundation:** Based on well-understood Affine cipher

### Weaknesses
- **No Key:** Only one possible configuration
- **Predictable:** Easy to break with any attack method
- **Pattern Preservation:** Letter frequencies and patterns remain recognizable
- **Trivial Brute Force:** Only one transformation to try

### Security Level: **Very Low**

Atbash provides no real security and should only be used for educational purposes or as a component in more complex ciphers.

### Performance
- **Time Complexity:** O(n) where n is the length of the text
- **Space Complexity:** O(1) - fixed translation tables
- **Memory Usage:** Minimal - only translation tables

## Real-World Applications

### Historical Uses
- **Ancient Hebrew:** Original use for encoding Hebrew text
- **Religious Texts:** Used in some religious manuscripts
- **Educational:** Teaching basic cryptography concepts

### Modern Uses
- **Educational:** Learning substitution ciphers
- **Puzzles:** Simple encoding for games and puzzles
- **CTF Challenges:** Basic cryptography challenges
- **Component Ciphers:** Building block for more complex systems

## Code Example

```python
from hordekit.crypto.symmetric.substitution.atbash import AtbashCipher

# Create Atbash cipher instance
atbash = AtbashCipher()

# Encrypt a message
message = "ATBASH CIPHER"
encrypted = atbash.encode(message)
print(f"Encrypted: {encrypted}")  # Output: ZGYZHS XRKSVI

# Decrypt the message
decrypted = atbash.decode(encrypted)
print(f"Decrypted: {decrypted}")  # Output: ATBASH CIPHER

# Verify symmetry
twice_encrypted = atbash.encode(encrypted)
print(f"Symmetry: {message == twice_encrypted}")  # Output: True

# Demonstrate inheritance from AffineCipher
print(f"Is instance of AffineCipher: {isinstance(atbash, AffineCipher)}")  # Output: True
```

## Conclusion

The Atbash cipher is a fundamental example of substitution ciphers that demonstrates:
- The concept of symmetric encryption
- The importance of key space in cryptography
- The relationship between simplicity and security
- The power of inheritance in cryptographic implementations

While not suitable for secure communication, Atbash serves as an excellent educational tool for understanding basic cryptographic principles and the evolution of encryption methods from ancient times to modern cryptography. Its relationship to the Affine cipher also demonstrates how complex ciphers can be built from simpler components. 