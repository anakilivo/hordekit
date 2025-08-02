# Affine Cipher

## History

The Affine cipher is a type of substitution cipher that combines the mathematical properties of both the Caesar cipher and the multiplicative cipher. It was first described by mathematician Al-Kindi in the 9th century and later formalized by Leon Battista Alberti in the 15th century.

The name "Affine" comes from the mathematical concept of an affine transformation, which is a linear transformation followed by a translation.

## Concept

The Affine cipher uses a mathematical function to transform each letter in the plaintext. The encryption function is:

**E(x) = (ax + b) mod 26**

And the decryption function is:

**D(x) = a^(-1)(x - b) mod 26**

Where:
- **a** and **b** are the key parameters
- **a** must be coprime with 26 (gcd(a, 26) = 1)
- **a^(-1)** is the modular multiplicative inverse of a modulo 26
- **x** represents the position of a letter in the alphabet (A=0, B=1, ..., Z=25)

### Key Requirements

1. **Parameter a**: Must be coprime with 26 (gcd(a, 26) = 1)
   - Valid values: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
   - Invalid values: 2, 4, 6, 8, 10, 12, 13, 14, 16, 18, 20, 22, 24, 26

2. **Parameter b**: Can be any integer from 0 to 25

## Encryption Process

1. **Convert letters to numbers**: A=0, B=1, ..., Z=25
2. **Apply the formula**: E(x) = (ax + b) mod 26
3. **Convert back to letters**: 0=A, 1=B, ..., 25=Z

### Example

Let's encrypt "HELLO" with a=5, b=8:

| Letter | Position (x) | Calculation | Result | Cipher |
|--------|--------------|-------------|--------|--------|
| H      | 7            | (5×7+8) mod 26 = 43 mod 26 = 17 | 17 | R |
| E      | 4            | (5×4+8) mod 26 = 28 mod 26 = 2  | 2  | C |
| L      | 11           | (5×11+8) mod 26 = 63 mod 26 = 11 | 11 | L |
| L      | 11           | (5×11+8) mod 26 = 63 mod 26 = 11 | 11 | L |
| O      | 14           | (5×14+8) mod 26 = 78 mod 26 = 0  | 0  | A |

**Result**: "HELLO" → "RCLLA"

## Decryption Process

1. **Convert letters to numbers**: A=0, B=1, ..., Z=25
2. **Apply the formula**: D(x) = a^(-1)(x - b) mod 26
3. **Convert back to letters**: 0=A, 1=B, ..., 25=Z

### Finding the Modular Inverse

To decrypt, we need a^(-1) such that (a × a^(-1)) mod 26 = 1.

For a=5, we need to find a^(-1) where (5 × a^(-1)) mod 26 = 1.
Testing: 5 × 21 = 105, 105 mod 26 = 1, so a^(-1) = 21.

### Example

Let's decrypt "RCLLA" with a=5, b=8:

| Letter | Position (x) | Calculation | Result | Plain |
|--------|--------------|-------------|--------|-------|
| R      | 17           | 21(17-8) mod 26 = 21×9 mod 26 = 189 mod 26 = 7 | 7 | H |
| C      | 2            | 21(2-8) mod 26 = 21×(-6) mod 26 = 21×20 mod 26 = 420 mod 26 = 4 | 4 | E |
| L      | 11           | 21(11-8) mod 26 = 21×3 mod 26 = 63 mod 26 = 11 | 11 | L |
| L      | 11           | 21(11-8) mod 26 = 21×3 mod 26 = 63 mod 26 = 11 | 11 | L |
| A      | 0            | 21(0-8) mod 26 = 21×(-8) mod 26 = 21×18 mod 26 = 378 mod 26 = 14 | 14 | O |

**Result**: "RCLLA" → "HELLO"

## Attack Methods

### 1. Brute Force Attack

**Description**: Try all possible combinations of a and b values.

**Complexity**: O(312) - 12 possible values for a × 26 possible values for b

**Process**:
1. Test all valid a values (coprime with 26)
2. For each a, test all b values (0-25)
3. Check if decrypted text makes sense

**Example**:
```
Ciphertext: "RCLLA"
Possible keys: a=1,b=0; a=1,b=1; ...; a=5,b=8; ...
Found: a=5, b=8 → "HELLO"
```

### 2. Frequency Analysis

**Description**: Analyze letter frequency patterns in the ciphertext.

**Process**:
1. Calculate letter frequencies in ciphertext
2. Compare with known English letter frequencies
3. Try different a,b combinations
4. Score results using n-gram analysis
5. Select the most likely key

**Advantages**:
- Works well with longer texts
- Can identify the correct key even without knowing the plaintext

### 3. Known Plaintext Attack

**Description**: Use known plaintext-ciphertext pairs to recover the key.

**Mathematical Process**:
1. Find two different letters in plaintext and their ciphertext equivalents
2. Set up system of equations:
   - c₁ = (a × p₁ + b) mod 26
   - c₂ = (a × p₂ + b) mod 26
3. Solve for a and b:
   - a = (c₁ - c₂) × (p₁ - p₂)^(-1) mod 26
   - b = (c₁ - a × p₁) mod 26

**Example**:
```
Known: plaintext="HE", ciphertext="RC"
H=7, E=4, R=17, C=2
a = (17-2) × (7-4)^(-1) mod 26 = 15 × 9 mod 26 = 5
b = (17 - 5×7) mod 26 = (17-35) mod 26 = (-18) mod 26 = 8
Key: a=5, b=8
```

## Security Analysis

### Strengths

1. **Larger key space**: 312 possible keys vs 25 for Caesar cipher
2. **Mathematical complexity**: Requires understanding of modular arithmetic
3. **Non-linear transformation**: Not a simple shift like Caesar

### Weaknesses

1. **Still vulnerable to frequency analysis**
2. **Known plaintext attack is very effective**
3. **Limited key space compared to modern ciphers**
4. **Deterministic**: Same plaintext always produces same ciphertext

### Comparison with Other Ciphers

| Cipher | Key Space | Attack Resistance | Complexity |
|--------|-----------|-------------------|------------|
| Caesar | 25 | Very Low | Very Low |
| Affine | 312 | Low | Low |
| Vigenère | 26^key_length | Medium | Medium |
| Modern | 2^128+ | Very High | Very High |

## Real-World Applications

### Historical Use

- **Diplomatic communications** in the Renaissance period
- **Military communications** before the 20th century
- **Educational tool** for teaching cryptography concepts

### Modern Relevance

- **CTF (Capture The Flag) challenges**
- **Educational cryptography courses**
- **Historical cryptography research**
- **Foundation for understanding more complex ciphers**

## Conclusion

The Affine cipher represents an important step in the evolution of cryptography, introducing mathematical concepts that would later be fundamental to more advanced ciphers. While no longer secure for modern applications, it serves as an excellent educational tool for understanding:

- Modular arithmetic
- Linear transformations
- Key space analysis
- Attack methodologies

Its mathematical elegance and historical significance make it a valuable subject of study in cryptography education. 