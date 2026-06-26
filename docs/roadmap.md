# hordekit — Roadmap

CTF-oriented toolkit. Modules are independent but share the same `HordeResult` interface and `.pipe()` chaining.

---

## crypto

### Classical ciphers

#### Substitution
- [x] Caesar
- [x] ROT13
- [x] ROT47
- [x] Atbash
- [x] Affine
- [x] Vigenere
- [ ] Playfair
- [ ] Beaufort
- [ ] Porta
- [ ] Four-square

#### Transposition
- [ ] Rail Fence
- [ ] Columnar transposition
- [ ] Route cipher

### Modern

- [ ] XOR (single-byte and multi-byte key)
- [ ] Base64 encoder/decoder (as a `BaseTool`, not a cipher)
- [ ] Base32, Base85
- [ ] RC4

### Attacks

#### Generic
- [x] Brute force (any cipher with enumerable `possible_keys()`)
- [ ] Dictionary attack

#### Substitution
- [x] Frequency analysis (monogram)
- [ ] Index of coincidence (detects polyalphabetic ciphers)
- [ ] Kasiski test (Vigenere key length)
- [ ] Bigram / trigram scoring

#### Transposition
- [ ] Anagram-based recovery

---

## web

Web vulnerability tools for CTF web challenges.

- [ ] SQLi — payload generator, error-based detection
- [ ] XSS — payload generator, filter bypass patterns
- [ ] Path traversal — payload wordlist + scanner
- [ ] SSTI — template injection detection (Jinja2, Twig, etc.)
- [ ] JWT — decode / forge / crack (weak secret)
- [ ] HTTP request smuggling — payload builder
- [ ] SSRF — payload generator with bypass techniques
- [ ] XXE — payload templates

---

## osint

- [ ] Username lookup across platforms
- [ ] Email → linked accounts
- [ ] Domain info (WHOIS, DNS records, subdomains)
- [ ] Google dork builder
- [ ] Shodan query builder
- [ ] Image metadata extractor (EXIF)
- [ ] Hash identifier + lookup (hashcat modes, online DBs)

---

## forensics *(future module)*

- [ ] File signature / magic bytes identifier
- [ ] Steganography — LSB extraction (PNG, BMP)
- [ ] PCAP parser helpers
- [ ] Strings extractor with entropy scoring

---

## misc *(utility tools)*

- [ ] Hex ↔ ASCII ↔ binary converters (as `BaseTool` for chaining)
- [ ] CRC / checksum tools
- [ ] Entropy calculator
- [ ] Pattern generator (cyclic patterns for buffer overflow)
