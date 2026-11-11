# Build and apply V6 (macOS)

From the **repository root** (`.../Agentic_AI_Book/etis-agentic-ai-book`):

```sh
tar -xzf ~/Downloads/etis-agentic-ai-book-v6-integrated-patch.tar.gz
python3 -m venv .venv
.venv/bin/python -m pip install python-docx
export PATH="$PWD/.venv/bin:$PATH"
make book-docx
make check
open dist/etis-agentic-ai-book.docx
```

If the virtual environment already exists, the `python3 -m venv .venv` step can be omitted. Run `make book-docx` **before** `make check` so built-output checks see the new manuscript.

The current Contents is a readable draft outline, not a final page-numbered TOC. Final numbering and recto parity must be verified in Word for Mac.
