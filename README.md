# security-final-project

This project uses a variety of encryption techniques in combination to provide encryption and decryption of files.

Flowchart Diagram

```mermaid
flowchart TB
A[Start] --> B{Mode}
B -->|Encrypt| C[Read Key]
B -->|Decrypt| C
C --> D[Process Input File]
D --> E[Apply Encryption / Decryption Algorithms]
E --> F[Generate Output File]
```