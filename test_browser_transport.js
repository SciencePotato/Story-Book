const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const html = fs.readFileSync(path.join(__dirname, "templates/base.html"), "utf8");
const script = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)]
  .map(match => match[1]).join("\n");
for (const protocol of ["https:", "http:"]) {
  let connectArgs;
  const socket = { on() {}, emit() {} };
  const element = { addEventListener() {} };
  vm.runInNewContext(script, {
    io: { connect(...args) { connectArgs = args; return socket; } },
    document: { domain: "example.test", getElementById() { return element; } },
    location: { protocol, port: "" }, window: {},
  });
  assert.deepEqual(connectArgs, [], "Socket.IO must derive transport from the page origin");
}
console.log("PASS same-origin Socket.IO setup for HTTP and HTTPS");
