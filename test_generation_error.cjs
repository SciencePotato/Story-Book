const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const html = fs.readFileSync(path.join(__dirname, "templates/base.html"), "utf8");
const script = html.match(/<script type="text\/javascript" charset="utf-8" defer>([\s\S]*?)<\/script>/)[1];
const elements = new Map();
const handlers = {};
function element(id) {
  if (!elements.has(id)) elements.set(id, {
    style: {}, value: "synthetic prompt", textContent: "",
    addEventListener(event, fn) { this[event] = fn; }, appendChild() {}
  });
  return elements.get(id);
}
vm.runInNewContext(script, {
  document: {domain: "synthetic.invalid", getElementById: element, querySelector: element, createElement: element},
  location: {port: ""},
  io: {connect: () => ({emit() {}, on: (event, fn) => {handlers[event] = fn;}})},
  window: {}
});
assert.equal(typeof handlers["generation-error"], "function");
for (const action of ["generateStory", "end-story"]) {
  element(action).click();
  handlers["generation-error"]({message: "<synthetic error>"});
  assert.equal(element("loader").style.transform, "translateY(-100vh)");
  assert.equal(element("body").style.overflowY, "initial");
  assert.equal(element("generator").style.visibility, "initial");
  assert.equal(element("generator").style.display, "");
  assert.equal(element("end-story").style.visibility, "initial");
  assert.equal(element("printView").style.visibility, "hidden");
  assert.equal(element("promptTitle").textContent, "<synthetic error>");
}
