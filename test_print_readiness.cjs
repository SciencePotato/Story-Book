const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");
const assert = require("node:assert/strict");

const page = fs.readFileSync(path.join(__dirname, "templates/base.html"), "utf8");
const script = [...page.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)]
  .map(match => match[1]).find(text => text.includes("var socket"));
function element() {
  return {
    style: {}, children: [], listeners: {},
    addEventListener(name, callback) { this.listeners[name] = callback; },
    appendChild(child) { this.children.push(child); },
  };
}
const nodes = new Map();
for (const id of ["loader", "generateStory", "prompt", "content", "promptTitle",
                   "end-story", "generator", "printView", "story-Intro"]) {
  nodes.set(id, element());
}
nodes.get("printView").style.visibility = "hidden";
const socket = { callbacks: {}, on(name, callback) { this.callbacks[name] = callback; }, emit() {} };
vm.runInNewContext(script, {
  document: {
    domain: "synthetic.invalid",
    getElementById: id => nodes.get(id),
    querySelector: element,
    createElement: element,
  },
  window: {}, location: { port: "" }, io: { connect: () => socket },
});
nodes.get("end-story").listeners.click();
assert.equal(nodes.get("printView").style.visibility, "hidden",
             "an unfinished cover must not be printable");
assert.equal(nodes.get("story-Intro").children.length, 0);
socket.callbacks["end-finished"]({ title: "Synthetic title", image: "synthetic-image" });
assert.equal(nodes.get("story-Intro").children.length, 2);
assert.equal(nodes.get("printView").style.visibility, "initial",
             "the completed cover must enable printing");
console.log("PASS: Print is enabled only after completed cover insertion");
