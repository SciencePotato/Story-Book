import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock


def load():
    tree = ast.parse(Path(__file__).with_name("app.py").read_text())
    tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    for node in tree.body:
        node.decorator_list = []
    ns = {"request": SimpleNamespace(sid="A"), "_stories": {},
          "openai": MagicMock(), "replicate": MagicMock(), "time": MagicMock(),
          "random": MagicMock(), "emit": MagicMock(),
          "openAI_configuration": dict(model="mock", prompt="", temperature=0.7,
              max_tokens=512, top_p=1, frequency_penalty=0.5, presence_penalty=1.5),
          "passage": "", "passageList": [], "passagePrompt": "", "imageUrls": []}
    exec(compile(tree, "app.py", "exec"), ns)
    return ns


def response(text):
    return {"choices": [SimpleNamespace(text=text)]}


class StorySessionTests(unittest.TestCase):
    def test_bad_payload_never_reaches_a_provider(self):
        for value in [None, {}, {"data": 3}, {"data": "   "}, []]:
            with self.subTest(payload=value):
                ns = load()
                ns["generateContent"](value)
                ns["openai"].Completion.create.assert_not_called()
                ns["replicate"].models.get.assert_not_called()
                self.assertEqual(ns["emit"].call_args.args[0], "generation-error")
                self.assertNotIn("broadcast", ns["emit"].call_args.kwargs)

    def test_continuations_are_isolated_by_connection(self):
        ns = load()
        ns["openai"].Completion.create.side_effect = [
            response("A secret story"), response("summary A"),
            response("B private story"), response("summary B"),
            response("A continuation"), response("summary C")]
        ns["generateContent"]({"data": "first A"})
        ns["request"].sid = "B"
        ns["generateContent"]({"data": "first B"})
        ns["request"].sid = "A"
        ns["generateContent"]({"data": "continue A"})
        calls = ns["openai"].Completion.create.call_args_list
        self.assertNotIn("A secret story", calls[2].kwargs["prompt"])
        self.assertIn("A secret story", calls[4].kwargs["prompt"])
        self.assertNotIn("B private story", calls[4].kwargs["prompt"])

    def test_title_uses_only_requesting_connections_story(self):
        ns = load()
        ns["openai"].Completion.create.side_effect = [
            response("A secret story"), response("summary A"),
            response("B private story"), response("summary B"),
            response("B title")]
        ns["generateContent"]({"data": "first A"})
        ns["request"].sid = "B"
        ns["generateContent"]({"data": "first B"})
        ns["endContent"]({})
        prompt = ns["openai"].Completion.create.call_args.kwargs["prompt"]
        self.assertIn("B private story", prompt)
        self.assertNotIn("A secret story", prompt)
        self.assertEqual(ns["emit"].call_args.args[0], "end-finished")
        self.assertFalse(ns["emit"].call_args.kwargs.get("broadcast", False))

    def test_end_without_story_and_disconnect_cleanup(self):
        ns = load()
        ns["endContent"]({})
        ns["openai"].Completion.create.assert_not_called()
        ns["_stories"]["A"] = {"passage": "story", "parts": ["story"]}
        ns["disconnect"]()
        self.assertNotIn("A", ns["_stories"])


if __name__ == "__main__":
    unittest.main()
