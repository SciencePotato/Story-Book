# Flask Run

The browser handles the `generation-error` event emitted by the server's
pending prompt-validation change (PR #3). It exits loading, restores editing
controls for a retry, and displays the error as text without discarding pages.
Offline DOM/event regression: `node test_generation_error.cjs`.

# pip install -r requirement.txt

# Api via .env file