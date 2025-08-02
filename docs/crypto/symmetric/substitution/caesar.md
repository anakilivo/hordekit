# Caesar Cipher

The Caesar cipher is one of the oldest and simplest encryption methods, named after the Roman emperor Julius Caesar.

## History

### Origin
The Caesar cipher was invented by Julius Caesar (100-44 BC) to protect military correspondence. Caesar used a shift of 3 positions in the Latin alphabet.

### Historical Application
- **Military Communication**: Protecting messages from enemies
- **Diplomatic Correspondence**: Secret communication
- **Personal Correspondence**: Private messages

### Modern Significance
Although the Caesar cipher is not secure, it remains important for:
- Learning cryptography
- Understanding basic encryption principles
- Historical context

## Concept

### Mathematical Model
The Caesar cipher can be described by formulas:

**Encryption:**
```
C = (P + K) mod 26
```

**Decryption:**
```
P = (C - K) mod 26
```

Where:
- `C` - ciphertext character
- `P` - plaintext character  
- `K` - key (shift)
- `mod 26` - modulo operation with 26 (number of letters in alphabet)

### Visual Scheme

```
Alphabet: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Shift 3:  D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
```

### Working Example

| Position | Plaintext | Shift | Ciphertext |
|----------|-----------|-------|------------|
| 0        | H (7)     | +3    | K (10)     |
| 1        | E (4)     | +3    | H (7)      |
| 2        | L (11)    | +3    | O (14)     |
| 3        | L (11)    | +3    | O (14)     |
| 4        | O (14)    | +3    | R (17)     |

## Encoding

### Encryption Algorithm

1. **Preparation**: Convert text to uppercase
2. **Character Processing**: For each character:
   - If character is in alphabet → apply shift
   - If character is not in alphabet → leave unchanged
3. **Result**: Obtain ciphertext

### Examples

#### Example 1: Simple text
```
Plaintext: HELLO
Shift: 3
Ciphertext: KHOOR
```

#### Example 2: Text with spaces and punctuation
```
Plaintext: HELLO, WORLD!
Shift: 3
Ciphertext: KHOOR, ZRUOG!
```

#### Example 3: Different shifts

| Shift | HELLO → |
|-------|---------|
| 1     | IFMMP   |
| 3     | KHOOR   |
| 5     | MJQQT   |
| 10    | ROVVY   |
| 25    | GDKKN   |

## Decoding

### Decryption Algorithm

1. **Preparation**: Receive ciphertext
2. **Character Processing**: For each character:
   - If character is in alphabet → apply reverse shift
   - If character is not in alphabet → leave unchanged
3. **Result**: Obtain plaintext

### Decryption Examples

#### Example 1: Simple decryption
```
Ciphertext: KHOOR
Shift: 3
Plaintext: HELLO
```

#### Example 2: Verification
```
Ciphertext: MJQQT
Shift: 5
Plaintext: HELLO
```

## Attacks

### 1. Brute Force

**Principle**: Exhaustive search of all possible keys (1-25)

**Complexity**: O(n), where n = 25 (number of possible shifts)

**Example**:
```
Ciphertext: KHOOR
Possible decryptions:
Shift 1: JINNQ
Shift 2: HIMMP
Shift 3: HELLO ← correct
Shift 4: GDKKN
...
```

### 2. Frequency Analysis

**Principle**: Analysis of letter frequencies in ciphertext

**Basis**: Each language has characteristic letter frequencies

#### Letter Frequencies in English

| Letter | Frequency (%) | Letter | Frequency (%) |
|--------|---------------|--------|---------------|
| E      | 12.02        | M      | 2.61          |
| T      | 9.10         | F      | 2.30          |
| A      | 8.12         | Y      | 2.11          |
| O      | 7.68         | W      | 2.09          |
| I      | 7.31         | G      | 2.03          |
| N      | 6.95         | P      | 1.82          |
| S      | 6.28         | B      | 1.49          |
| R      | 6.02         | V      | 1.11          |
| H      | 5.92         | K      | 0.69          |
| D      | 4.32         | X      | 0.17          |
| L      | 3.98         | Q      | 0.11          |
| U      | 2.88         | J      | 0.10          |
| C      | 2.71         | Z      | 0.07          |

**Attack Algorithm**:
1. Count letter frequencies in ciphertext
2. Compare with known language frequencies
3. Find shift giving best match

**Example**:
```
Ciphertext: "KHOOR ZRUOG"
Frequencies: O=3, H=1, K=1, R=2, Z=1, U=1, G=1
Analysis: O appears most frequently → likely this is E
Shift: O(14) - E(4) = 10
Verification: KHOOR with shift 10 → HELLO ✓
```

### 3. Known Plaintext Attack

**Principle**: Using known plaintext ↔ ciphertext pairs

**Algorithm**:
1. Find corresponding characters
2. Calculate shift: `shift = cipher_char - plain_char`
3. Apply found shift to entire text

**Example**:
```
Known: "HELLO" → "KHOOR"
Analysis: H(7) → K(10), shift = 10 - 7 = 3
Result: shift = 3
```

### 4. Chosen Plaintext Attack

**Principle**: Ability to encrypt chosen texts

**Example**:
```
Chosen text: "AAAAA"
Encryption result: "DDDDD"
Conclusion: shift = 3 (D - A = 3)
```

## Security

### Vulnerabilities

1. **Small key space**: Only 25 possible keys
2. **Predictability**: Same shift for all characters
3. **Frequency analysis**: Easily susceptible to frequency analysis
4. **No diffusion**: Changing one character affects only one character

### Recommendations

- ❌ **Do not use** for protecting important information
- ✅ **Use** for learning cryptography
- ✅ **Use** for simple games and puzzles
- ✅ **Study** as foundation for more complex algorithms

## Implementation in Hordekit

### Creating an Instance

```python
from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher

# Create with specific shift
caesar = CaesarCipher(shift=3)

# Generate random key
caesar = CaesarCipher.generate_key()
```

### Encryption and Decryption

```python
# Encryption
encrypted = caesar.encode("HELLO WORLD")
print(encrypted)  # "KHOOR ZRUOG"

# Decryption
decrypted = caesar.decode(encrypted)
print(decrypted)  # "HELLO WORLD"
```

### Attacks

```python
from hordekit.crypto.utils import AttackMethod

# Brute force
results = caesar.attack(AttackMethod.BRUTE_FORCE, ciphertext="KHOOR")

# Frequency analysis
analysis = caesar.attack(AttackMethod.FREQUENCY_ANALYSIS, ciphertext="KHOOR ZRUOG")

# Known plaintext attack
shift = caesar.attack(
   AttackMethod.KNOWN_PLAINTEXT, plaintext="HELLO", ciphertext="KHOOR"
)
```



## Conclusion

The Caesar cipher is an excellent example for learning the basics of cryptography. Despite its simplicity and vulnerability, it demonstrates key concepts:

- **Substitution**: replacing characters according to a rule
- **Key**: parameter determining the shift
- **Symmetry**: one key for encryption and decryption
- **Attacks**: various methods of breaking

This algorithm serves as a foundation for understanding more complex cryptographic methods. 