# Flask Run

# pip install -r requirement.txt

# Api via .env file

Image responses are taken from the output of the handler's own
`version.predict(...)` call, not the latest prediction in the account. This
preserves image ownership when other requests finish concurrently.

Run `python3 -m unittest -v test_prediction_ownership` for offline mocked
handler tests. They do not invoke providers, load credentials, or use inference
credits. The app retains its legacy OpenAI Completion and Replicate
`version.predict` APIs; compatibility with current SDK releases is not claimed.