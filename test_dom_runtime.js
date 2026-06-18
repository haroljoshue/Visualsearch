const { JSDOM } = require("jsdom");
const fs = require("fs");
const path = require("path");

const htmlPath = path.join(__dirname, "templates", "index.html");
const html = fs.readFileSync(htmlPath, "utf8");

const dom = new JSDOM(html, {
  runScripts: "dangerously",
  resources: "usable",
  url: "http://localhost/"
});

const { window } = dom;
const { document } = window;

window.addEventListener("error", (e) => {
  console.error("RUNTIME EXCEPTION DETECTED:", e.message, "at", e.filename, "line", e.lineno);
});

console.log("JSDOM initialized.");

try {
  const idInput = document.getElementById("subject-id");
  const ageInput = document.getElementById("subject-age");
  
  if (idInput && ageInput) {
    idInput.value = "TEST-SUBJECT";
    ageInput.value = "25";
    
    const form = document.querySelector("form");
    if (form) {
      console.log("Submitting form...");
      
      // Override fetch to avoid network calls failing
      window.fetch = () => Promise.resolve({
        json: () => Promise.resolve({ status: "success", message: "cleared" })
      });
      
      const submitEvent = new window.Event("submit", { bubbles: true, cancelable: true });
      form.dispatchEvent(submitEvent);
      
      console.log("Form submitted. Active screen is now:", document.querySelector(".screen.active").id);
      
      // Find the instructions confirm button
      const confirmBtn = document.querySelector("#screen-instructions button");
      if (confirmBtn) {
        console.log("Clicking confirm button...");
        confirmBtn.click();
        console.log("Confirm button clicked. Active screen is now:", document.querySelector(".screen.active").id);
      } else {
        console.log("Confirm button not found on instructions screen!");
      }
    } else {
      console.log("Form not found.");
    }
  } else {
    console.log("Inputs not found:", !!idInput, !!ageInput);
  }
} catch (err) {
  console.error("Execution error:", err);
}
