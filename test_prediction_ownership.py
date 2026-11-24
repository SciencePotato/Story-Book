import ast
from pathlib import Path
import types
import unittest
from unittest.mock import MagicMock


def load_handlers():
    tree = ast.parse(Path(__file__).with_name("app.py").read_text())
    tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    for node in tree.body:
        node.decorator_list = []
    response = {"choices": [types.SimpleNamespace(text="A test story")]}
    namespace = {"time": MagicMock(), "openai": MagicMock(), "replicate": MagicMock(),
                 "emit": MagicMock(), "random": MagicMock(), "passage": "",
                 "passagePrompt": "", "passageList": [], "imageUrls": [],
                 "openAI_configuration": {"model": "test", "temperature": 0.7,
                                           "max_tokens": 10, "top_p": 1,
                                           "frequency_penalty": 0, "presence_penalty": 0}}
    namespace["openai"].Completion.create.return_value = response
    exec(compile(tree, "app.py", "exec"), namespace)
    return namespace


class PredictionOwnershipTests(unittest.TestCase):
    def test_handlers_emit_their_own_prediction_not_account_latest(self):
        for handler in ("generateContent", "endContent"):
            with self.subTest(handler=handler):
                module = load_handlers()
                version = module["replicate"].models.get.return_value.versions.get.return_value
                version.predict.return_value = ["https://example.invalid/own-result.png"]
                module["replicate"].predictions.list.return_value = [
                    types.SimpleNamespace(output=["https://example.invalid/another-request.png"])]
                module[handler]({"data": "test"})
                payload = module["emit"].call_args.args[1]
                self.assertEqual(payload["image"], "https://example.invalid/own-result.png")
                module["replicate"].predictions.list.assert_not_called()
                if handler == "generateContent":
                    self.assertEqual(module["imageUrls"], ["https://example.invalid/own-result.png"])


if __name__ == "__main__":
    unittest.main()
