# hordekit — Roadmap

CTF-oriented toolkit. Modules are independent but share the same `HordeResult` interface and `.pipe()` chaining.

Legend: `[x]` done · `[ ]` planned · `[~]` in progress · `[?]` under consideration

---

## crypto

### Classical ciphers

#### Substitution
- [x] Caesar — code + tests + docs
- [x] ROT13 — code + tests + docs
- [x] ROT47 — code + tests + docs
- [x] Atbash — code + tests + docs
- [x] Affine — code + tests + docs
- [x] Vigenère — code + tests + docs
- [x] Autokey — like Vigenère but key is extended with plaintext (harder to crack)
- [x] Beaufort — reciprocal variant of Vigenère (encrypt == decrypt)
- [x] Playfair — digraph substitution, 5×5 key square
- [x] Hill — matrix-based substitution; vulnerable to known-plaintext attack
- [ ] Polybius square — letter → 2-digit coordinate pair
- [ ] Four-square — double Playfair variant
- [ ] Porta — polyalphabetic, 13-row tableau
- [ ] Baconian — 5-bit binary encoding of letters (A=AAAAA … Z=BBBBB)

#### Transposition
- [ ] Rail Fence — zigzag pattern; key is number of rails
- [ ] Columnar transposition — write in rows, read in column order; key is column permutation
- [ ] Double columnar — columnar applied twice
- [ ] Scytale — ancient Greek cylinder cipher (strip wound around rod)
- [ ] Route cipher — spiral/vertical/horizontal read patterns

#### Polygraphic / other
- [ ] Nihilist — Polybius + numeric Vigenère
- [ ] Bifid — Polybius coordinates split and recombined
- [ ] Trifid — 3D variant of Bifid

### Modern encodings & stream ciphers

- [ ] XOR — single-byte key (brute-forceable), multi-byte key (keystream recovery via crib-drag)
- [ ] RC4 — key scheduling + PRNG stream; known biases exploitable
- [ ] ChaCha20 / Salsa20 — reference implementation for CTF challenges involving nonce reuse
- [ ] LFSR — linear feedback shift register; Berlekamp–Massey attack
- [ ] MT19937 (Mersenne Twister) — predict next outputs from 624 observed 32-bit values

### Block ciphers (AES-based)

- [ ] AES-ECB — encrypt/decrypt; detect ECB mode (duplicate block detector)
- [ ] AES-CBC — encrypt/decrypt; bit-flipping attack, padding oracle (PKCS#7)
- [ ] AES-CTR — encrypt/decrypt; nonce-reuse XOR keystream recovery
- [ ] AES-GCM — nonce-reuse (forbidden attack)
- [ ] PKCS#7 padding — pad/unpad utility used by CBC tools

### RSA

This is the most common CTF crypto category. Each attack is a separate module under `hordekit/crypto/rsa/attacks/`.

#### Implementation
- [ ] RSA core — key generation, textbook encrypt/decrypt (`pow(m, e, n)`)
- [ ] Key parser — parse PEM / DER keys; extract n, e, d, p, q
- [ ] Number theory utilities — `gcd`, `lcm`, `mod_inverse`, `CRT`, `iroot`, `is_prime`, `next_prime`

#### RSA attacks
- [ ] Small public exponent (e=3) — cube-root when `m^e < n`
- [ ] Coppersmith / Håstad broadcast — same message encrypted with different moduli, small e
- [ ] Common modulus — two ciphertexts of same message with same n but different e
- [ ] Wiener's attack — small private exponent d via continued fractions
- [ ] Fermat factoring — when p and q are close together
- [ ] Pollard p−1 — smooth p−1 factor
- [ ] Pollard rho — general-purpose factorization (wraps gmpy2/sympy)
- [ ] Known partial key — recover d from partial knowledge (Boneh–Durfee lite)
- [ ] Franklin–Reiter related message — two related messages, same key
- [ ] Parity oracle — decrypt bit-by-bit using even/odd oracle
- [ ] CRT fault attack — broken signature leaks prime factor

### Hash functions

- [ ] Hash identifier — detect MD5 / SHA-1 / SHA-256 / SHA-512 / bcrypt / etc. from length + prefix
- [ ] MD5 / SHA-1 length extension attack — appends to a hashed message without knowing the secret
- [ ] Hash cracker — wrapper around hashcat / john wordlist modes
- [ ] HMAC oracle — timing-safe comparison bypass simulator (for CTF logic challenges)

### Attacks (generic)

#### Generic
- [x] Brute force (any cipher with enumerable `possible_keys()`)
- [x] Dictionary attack (user-supplied wordlist)
- [ ] Auto-cracker — detect cipher type and chain attacks automatically

#### Substitution
- [x] Frequency analysis (monogram)
- [x] Index of Coincidence — mono vs. poly detection + key length estimate
- [x] Kasiski test — Vigenère key length from repeated trigrams
- [x] Quadgram scoring — default scorer for brute_force and dictionary_attack
- [ ] Chi-squared test — alternative to IoC; better for short texts
- [ ] Automated Vigenère full crack — Kasiski → IoC confirm → per-column Caesar brute force, returns plaintext
- [x] Hill cipher known-plaintext attack — recover key matrix from plaintext/ciphertext pairs

#### Transposition
- [ ] Period detection — IC-based detection of rail fence / columnar period
- [ ] Columnar key recovery — anagram scoring over column permutations
- [ ] Rail fence brute force — try all rail counts

#### XOR
- [ ] Single-byte XOR — brute force all 256 keys
- [ ] Multi-byte XOR key length — Hamming distance / Kasiski adapted for XOR
- [ ] Crib dragging — recover XOR keystream from two ciphertexts encrypted with same key
- [ ] Known-plaintext keystream recovery — XOR ciphertext with known plaintext fragment

#### Modern / probabilistic
- [ ] Berlekamp–Massey — recover LFSR polynomial from output stream
- [ ] MT19937 untemper — recover full state from 624 outputs; predict future values
- [ ] Padding oracle (PKCS#7 / AES-CBC) — decrypt arbitrary ciphertext block-by-block

---

## encoding

Standalone encode/decode tools that fit the `BaseTool` interface and chain via `.pipe()`.

- [ ] Base16 (hex) — encode/decode
- [ ] Base32 — encode/decode
- [ ] Base58 — Bitcoin-style alphabet; common in CTF wallet challenges
- [ ] Base62 — URL-safe alphanumeric
- [ ] Base64 — encode/decode (standard + URL-safe + no-padding variants)
- [ ] Base85 / ASCII85 — encode/decode
- [ ] URL encode/decode — `%xx` escaping
- [ ] HTML entity encode/decode — `&amp;`, `&#x41;`, `&#65;`
- [ ] Unicode normalizer — NFC / NFD / NFKC / NFKD; detect homoglyph substitution
- [ ] Morse code — encode/decode
- [ ] Braille — encode/decode (6-dot + 8-dot)
- [ ] Baudot/ITA2 — early teleprinter encoding
- [ ] Multi-encoding detector — given bytes, try all known encodings, score, return best chain

---

## web

Web vulnerability tools for CTF challenges. No HTTP client built in — tools produce payloads / analysers only; use `requests` or `httpx` externally.

### Input injection

- [ ] SQL injection — payload generator (error-based, blind boolean, time-based, UNION); DB detection heuristics
- [ ] XSS — payload generator, filter bypass patterns (tag/attribute/event, SVG, polyglots)
- [ ] SSTI — probe payloads for Jinja2 / Twig / FreeMarker / Velocity; RCE escalation chains
- [ ] XXE — payload templates (basic read, error-based exfil, blind OOB)
- [ ] LDAP injection — payload fragments
- [ ] NoSQL injection — MongoDB operator injection patterns

### Auth & session

- [ ] JWT — decode (header + payload), verify/skip signature, forge (alg:none, weak HMAC secret brute force, RS256→HS256 confusion)
- [ ] Cookie decoder/forger — Flask session, Django signed cookie, Rails HMAC cookie
- [ ] OAuth misconfig — open redirect chain, state parameter bypass payloads
- [ ] Insecure deserialization — PHP object injection gadget templates; Java ysoserial payload wrappers

### Access & traversal

- [ ] Path traversal — wordlist generator (`../../../etc/passwd` variants, encoding bypass)
- [ ] SSRF — payload generator with bypass techniques (DNS rebinding hints, IPv6, decimal IP, redirects)
- [ ] Open redirect — payload list + filter bypass patterns
- [ ] IDOR — sequential ID fuzzer helper

### Infrastructure

- [ ] HTTP request smuggling — CL.TE / TE.CL / TE.TE payload builder
- [ ] CORS misconfiguration checker — analyse `Access-Control-Allow-Origin` logic
- [ ] Cache poisoning — header injection payload builder
- [ ] CSP analyser — parse policy, identify bypasses (unsafe-inline, wildcard, JSONP endpoints)
- [ ] GraphQL — introspection query builder, batch query DoS patterns, type enumeration

### Prototype pollution / client-side

- [ ] Prototype pollution — JS gadget payloads, `__proto__` / `constructor.prototype` chains
- [ ] DOM XSS sources/sinks — pattern list for manual review

---

## osint

Tools produce structured data; network calls are the caller's responsibility (no implicit HTTP in the module itself — wrap externally).

### Passive reconnaissance

- [ ] Domain analyser — parse WHOIS data, extract registrant info
- [ ] DNS enumerator — A, AAAA, MX, TXT, NS, SOA record helpers; zone transfer attempt
- [ ] Subdomain wordlist generator — permutation + common prefix/suffix combinations
- [ ] Certificate transparency — query crt.sh for subdomains; parse SAN fields
- [ ] Wayback Machine helper — construct snapshot queries, diff two snapshots
- [ ] Google dork builder — structured dork generator (site:, filetype:, inurl:, intitle: combos)
- [ ] Shodan query builder — structured filter builder for Shodan syntax
- [ ] Email header analyser — parse Received chain, extract IPs, detect spoofing indicators

### Identity & accounts

- [ ] Username permutator — generate variations for cross-platform search
- [ ] Email → breach lookup helper — structure queries for HaveIBeenPwned API
- [ ] Phone number analyser — parse E.164, extract carrier/region hints
- [ ] Social media profile builder — aggregate public data from usernames

### Code & data leaks

- [ ] Git exposure checker — detect `.git/` exposure; reconstruct repo from index
- [ ] Sensitive file wordlist — common backup/config paths (`/.env`, `/config.php.bak`, etc.)
- [ ] Paste site monitor — structure queries for Pastebin / GitHub Gist / PrivateBin search
- [ ] GitHub dorking — `filename:`, `extension:`, `org:` query builder for code search

### Crypto / blockchain

- [ ] Bitcoin address analyser — extract info from address (type: P2PKH / P2SH / Bech32)
- [ ] Ethereum address tools — checksum validation, ENS name hints
- [ ] Transaction graph helper — structure blockchain explorer queries

---

## forensics

### File analysis

- [ ] Magic bytes identifier — match file header against a table of 200+ signatures; suggest `file` equivalent
- [ ] File carver — extract embedded files by magic byte scanning (ZIP inside JPEG, etc.)
- [ ] Strings extractor with entropy scoring — find high-entropy blobs, flag as potentially encrypted/compressed
- [ ] Archive handler — nested/password-protected ZIP/7z/RAR unwrapper
- [ ] Metadata extractor — EXIF (images), PDF metadata, Office document properties

### Image forensics

- [ ] LSB steganography — extract hidden data from low bits of PNG/BMP channels
- [ ] Alpha channel dump — extract RGBA alpha layer as raw bytes
- [ ] Pixel histogram — plot per-channel frequency; detect unusual distributions
- [ ] Stego detector — run detection heuristics (chi-square pixel pairs test)
- [ ] QR code / barcode decoder — decode from image file
- [ ] Hidden layer detector — check for multiple frames in GIF / APNG

### Audio forensics

- [ ] Spectrogram generator — dump spectrogram as data (common CTF: hidden text in spectrogram)
- [ ] DTMF decoder — detect and decode phone keypad tones from WAV
- [ ] LSB audio steganography — extract hidden data from WAV sample LSBs
- [ ] MP3 / FLAC metadata extractor — ID3 tags, comment fields
- [ ] Audio speed/pitch analyser — detect reversed/slowed audio (reversing is common CTF trick)

### Network

- [ ] PCAP parser — extract TCP streams, HTTP sessions, credentials in clear text
- [ ] DNS query extractor — reconstruct data exfiltrated via DNS TXT/subdomain tunneling
- [ ] HTTP session reconstructor — rebuild request/response pairs from PCAP

### Memory forensics

- [ ] Volatility wrapper — common plugin shortcuts (`pslist`, `dlllist`, `filescan`, `dumpfiles`)
- [ ] String searcher — grep memory dump for flags / credentials / URLs
- [ ] Process memory extractor — dump a process address space section

---

## misc

Utility tools that implement `BaseTool` and participate in `.pipe()` chains.

### Data transformation

- [ ] Hex ↔ ASCII ↔ binary converters
- [ ] Integer ↔ bytes (big-endian / little-endian)
- [ ] Bit reversal / byte reversal
- [ ] Null-byte stripper / inserter
- [ ] Byte frequency counter — returns `dict[int, int]` in metadata
- [ ] Entropy calculator — Shannon entropy; flag > 7.0 as likely encrypted/compressed
- [ ] CRC calculator — CRC8, CRC16, CRC32, CRC64

### String utilities

- [ ] Reverse string/bytes
- [ ] Rotate bytes (ROT-N for arbitrary N, works on any byte range)
- [ ] String interleaver / deinterleaver — split/merge even/odd bytes
- [ ] Padding stripper — PKCS#7, zero-padding, space-padding

### Pattern & wordlist tools

- [ ] Cyclic pattern generator — De Bruijn sequence for buffer overflow offset finding
- [ ] Cyclic pattern finder — given 4 bytes, return offset in the pattern
- [ ] Wordlist mutator — apply leet-speak, case combos, append numbers/symbols

### Number theory

- [ ] GCD / LCM — Euclidean
- [ ] Extended GCD — returns Bézout coefficients (needed for modular inverse)
- [ ] Modular inverse — `pow(a, -1, m)`
- [ ] Chinese Remainder Theorem (CRT) — solve simultaneous congruences
- [ ] Integer square root — exact `iroot(n, k)` with remainder
- [ ] Primality test — Miller–Rabin
- [ ] Next prime — deterministic search from a starting value
- [ ] Factorization — trial division + Pollard rho for moderate-size integers
- [ ] Discrete logarithm — baby-step giant-step (BSGS) for small-group DLP

### Auto-detect & pipelines

- [ ] Cipher / encoding detector — given bytes, score against known formats (base64, hex, caesar, XOR, JWT header, etc.) and return ranked candidates
- [ ] CTF flag extractor — scan bytes for common flag patterns (`HTB{...}`, `CTF{...}`, `flag{...}`, etc.)
- [ ] Pipeline presets — common CTF decode chains (e.g. base64 → XOR → caesar)

---

## infrastructure *(meta)*

- [ ] CLI — `hordekit <module> <tool> [args]` for quick terminal use without writing Python
- [ ] Interactive REPL mode — `hordekit shell` with tab-complete and piped history
- [ ] Plugin system — drop a `.py` file in `~/.hordekit/plugins/` to register custom tools
- [ ] Result serializer — save / load `HordeResult` + metadata to JSON for session persistence
- [ ] Challenge notes format — attach problem statement to a HordeResult session for reference
