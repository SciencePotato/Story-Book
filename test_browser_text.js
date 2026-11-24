const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const html = fs.readFileSync(path.join(__dirname, "templates/base.html"), "utf8");
const script = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)]
  .map(match => match[1]).join("\n");
const elements = new Map(), handlers = {};
function element() {
  return {
    style: {}, children: [], textContent: "", innerHTML: "",
    addEventListener() {}, appendChild(child) { this.children.push(child); },
  };
}
function get(id) {
  if (!elements.has(id)) elements.set(id, element());
  return elements.get(id);
}
vm.runInNewContext(script, {
  io: { connect() { return { on(name, fn) { handlers[name] = fn; }, emit() {} }; } },
  document: {
    domain: "example.test", getElementById: get, querySelector: get,
    createElement: element,
  },
  location: { port: "" }, window: {},
});
const literal = "<b>tacos & science</b>";
handlers["processing-finished"]({ content: literal, prompt: literal, image: "offline:image" });
assert.equal(get("content").children[0].textContent, "Prompt: " + literal);
assert.equal(get("content").children[1].textContent, literal);
handlers["end-finished"]({ title: literal, image: "offline:cover" });
assert.equal(get("story-Intro").children[0].textContent, literal);
assert.equal(get("content").children[2].children[0].src, "offline:image");
console.log("PASS literal prompt, narrative and title rendering with image preservation");
