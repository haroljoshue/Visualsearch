const { JSDOM } = require("jsdom");
const fs = require("fs");
const path = require("path");

const html = fs.readFileSync(path.join(__dirname, "templates", "index.html"), "utf8");

const dom = new JSDOM(html, {
  runScripts: "dangerously",
  resources: "usable"
});

dom.window.addEventListener("error", (e) => {
  console.error("LOAD ERROR:", e.error ? e.error.stack : e.message);
});

console.log("JSDOM Loaded. Waiting for errors...");
setTimeout(() => {
  console.log("Checking if functions exist in window:");
  console.log("window.startTest:", typeof dom.window.startTest);
  console.log("window.confirmStartTest:", typeof dom.window.confirmStartTest);
  process.exit(0);
}, 1000);
