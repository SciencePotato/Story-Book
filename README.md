# Flask Run

## Socket story ownership

Story continuations and title prompts are isolated by Socket.IO connection ID.
State is in-memory, single-process, and removed on disconnect; reconnecting starts
a new story. Invalid/blank `generateContent` prompts and `endContent` before a
story emit `generation-error` to the requesting connection without provider calls.
Successful event names are unchanged.

Run `python3 -m unittest -v test_story_sessions` for offline handler checks with
all provider calls mocked. This does not verify live provider/model availability
or replace the separate prediction-result ownership PR.

# pip install -r requirement.txt

# Api via .env file