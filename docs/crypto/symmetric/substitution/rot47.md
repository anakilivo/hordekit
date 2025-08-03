# ROT47 Cipher

## History

ROT47 is an extension of ROT13 that works with the entire printable ASCII character set (characters with ASCII values from 33 to 126). It was developed to provide a simple way to obfuscate text that includes numbers, punctuation, and special characters, not just letters.

The name "ROT47" comes from the fact that it rotates each character by 47 positions in the ASCII table. Since the printable ASCII character set has 94 characters (from position 33 to 126), applying ROT47 twice returns the original text, making it its own inverse.

## Concept

ROT47 is a simple substitution cipher that shifts each printable ASCII character by exactly 47 positions in the ASCII table.

**Mathematical Representation:**
- For any printable ASCII character: `E(x) = ((x - 33 + 47) mod 94) + 33`
- Where `x` is the ASCII value of the input character (33 ≤ x ≤ 126)

**Important Note:** ROT47 is a special case of the Caesar cipher where `shift = 47`, but works with the entire printable ASCII character set instead of just letters. The transformation can be written as: `E(x) = ((x - 33 + 47) mod 94) + 33`

## Encryption Process

1. **ASCII Character Mapping:**
   ```
   ! → P, " → Q, # → R, $ → S, % → T, & → U, ' → V, ( → W, ) → X, * → Y, + → Z, , → [, - → \, . → ], / → ^
   0 → O, 1 → P, 2 → Q, 3 → R, 4 → S, 5 → T, 6 → U, 7 → V, 8 → W, 9 → X
   : → Y, ; → Z, < → [, = → \, > → ], ? → ^, @ → _, A → p, B → q, C → r, D → s, E → t, F → u, G → v, H → w, I → x, J → y, K → z, L → {, M → |, N → }, O → ~, P → , Q → !, R → ", S → #, T → $, U → %, V → &, W → ', X → (, Y → ), Z → *
   [ → +, \ → ,, ] → -, ^ → ., _ → /, ` → 0, a → p, b → q, c → r, d → s, e → t, f → u, g → v, h → w, i → x, j → y, k → z, l → {, m → |, n → }, o → ~, p → , q → !, r → ", s → #, t → $, u → %, v → &, w → ', x → (, y → ), z → *
   { → +, | → ,, } → -, ~ → .
   ```

2. **Example:**
   ```
   Plaintext:  "ROT47!@#"
   Encrypted:  "edgszPQR"
   
   R → e, O → d, T → g, 4 → s, 7 → z, ! → P, @ → Q, # → R
   ```

## Decryption Process

Since ROT47 is its own inverse, the decryption process is identical to encryption:

```
Ciphertext: "edgszPQR"
Decrypted:  "ROT47!@#"
```

## Relationship to Caesar Cipher

ROT47 is a special case of the Caesar cipher with parameter `shift = 47`, but works with the entire printable ASCII character set:

- **Caesar transformation:** `E(x) = (x + shift) mod 26` (for letters only)
- **ROT47 transformation:** `E(x) = ((x - 33 + 47) mod 94) + 33` (for all printable ASCII)

This means that ROT47 inherits the mathematical properties of the Caesar cipher while being extended to work with a much larger character set.

## Comparison with ROT13

| Feature | ROT13 | ROT47 |
|---------|-------|-------|
| **Character Set** | Letters only (A-Z, a-z) | All printable ASCII (33-126) |
| **Shift Value** | 13 | 47 |
| **Alphabet Size** | 52 characters | 94 characters |
| **Numbers** | Preserved | Transformed |
| **Punctuation** | Preserved | Transformed |
| **Special Characters** | Preserved | Transformed |

## No Attack Methods

ROT47 has no meaningful attack methods because it has no variability - it's a fixed algorithm without a key. The transformation is deterministic and known:

- **No Key Space:** Only one possible configuration
- **No Brute Force:** Only one transformation to try
- **No Frequency Analysis:** The transformation is fixed and known
- **No Known Plaintext:** Any known plaintext immediately reveals the algorithm

Any attempt to "attack" ROT47 would simply be applying the transformation to see if it produces meaningful text, which is not a cryptographic attack in the traditional sense.

## Security Analysis

### Strengths
- **Simplicity:** Easy to implement and understand
- **Deterministic:** Same input always produces same output
- **Self-inverse:** Same operation for encryption and decryption
- **Mathematical Foundation:** Based on well-understood Caesar cipher
- **Extended Character Set:** Works with all printable ASCII characters

### Weaknesses
- **No Key:** Only one possible configuration
- **Predictable:** Easy to break with any attack method
- **Pattern Preservation:** Character frequencies and patterns remain recognizable
- **Trivial Brute Force:** Only one transformation to try
- **No Variability:** Fixed algorithm without any key space

### Security Level: **Very Low**

ROT47 provides no real security and should only be used for educational purposes or as a component in more complex ciphers.

**Note:** ROT47 has no attack methods because it has no variability - it's a fixed algorithm without a key. Any attempt to "attack" ROT47 would simply be applying the transformation to see if it produces meaningful text, which is not a cryptographic attack in the traditional sense.

## Real-World Applications

### Historical Uses
- **Early Internet:** Simple text obfuscation in forums and newsgroups
- **Programming:** Simple text transformation in code
- **Educational:** Teaching extended substitution ciphers
- **Data Hiding:** Basic obfuscation of sensitive data

### Modern Uses
- **Educational:** Learning extended substitution ciphers
- **Puzzles:** Simple encoding for games and puzzles
- **CTF Challenges:** Basic cryptography challenges
- **Component Ciphers:** Building block for more complex systems
- **Data Obfuscation:** Simple hiding of text in plain sight

## Complete ASCII Mapping

### Key Character Mappings
```
! → P, " → Q, # → R, $ → S, % → T, & → U, ' → V, ( → W, ) → X, * → Y, + → Z, , → [, - → \, . → ], / → ^
0 → O, 1 → P, 2 → Q, 3 → R, 4 → S, 5 → T, 6 → U, 7 → V, 8 → W, 9 → X
: → Y, ; → Z, < → [, = → \, > → ], ? → ^, @ → _, A → p, B → q, C → r, D → s, E → t, F → u, G → v, H → w, I → x, J → y, K → z, L → {, M → |, N → }, O → ~, P → , Q → !, R → ", S → #, T → $, U → %, V → &, W → ', X → (, Y → ), Z → *
[ → +, \ → ,, ] → -, ^ → ., _ → /, ` → 0, a → p, b → q, c → r, d → s, e → t, f → u, g → v, h → w, i → x, j → y, k → z, l → {, m → |, n → }, o → ~, p → , q → !, r → ", s → #, t → $, u → %, v → &, w → ', x → (, y → ), z → *
{ → +, | → ,, } → -, ~ → .
```

### ASCII Range Coverage
- **Start:** `!` (ASCII 33)
- **End:** `~` (ASCII 126)
- **Total Characters:** 94 printable ASCII characters
- **Shift:** 47 positions (half of the character set)

## Conclusion

The ROT47 cipher is an extended example of substitution ciphers that demonstrates:
- The concept of symmetric encryption with extended character sets
- The importance of key space in cryptography
- The relationship between simplicity and security
- The power of inheritance in cryptographic implementations
- The concept of fixed algorithms without variability
- The extension of classical ciphers to modern character sets

While not suitable for secure communication, ROT47 serves as an excellent educational tool for understanding extended substitution ciphers and the evolution of encryption methods from letter-based to character-based transformations. Its relationship to the Caesar cipher also demonstrates how complex ciphers can be built from simpler components and extended to work with larger character sets. 