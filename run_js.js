const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'templates', 'index.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf8');

const scriptMatch = htmlContent.match(/<script>([\s\S]*?)<\/script>/);

if (scriptMatch) {
  const jsCode = scriptMatch[1];
  console.log("Extracted JS code. Compiling and running in Node context...");
  
  // Create a mock window/document environment
  const mockDOM = `
    const document = {
      getElementById: (id) => ({
        value: 'test',
        style: {},
        classList: { add: () => {}, remove: () => {} },
        addEventListener: () => {}
      }),
      querySelector: () => ({ style: {} }),
      addEventListener: () => {}
    };
    const window = {
      addEventListener: () => {},
      location: { protocol: 'http:' }
    };
    let Chart = function() { return { destroy: () => {} }; };
    let bootstrap = { Modal: function() { return { show: () => {}, hide: () => {} }; } };
  `;
  
  try {
    const fn = new Function(mockDOM + jsCode);
    fn();
    console.log("Script executed successfully without syntax or initialization errors!");
  } catch (err) {
    console.error("INITIALIZATION ERROR DETECTED:", err.stack);
  }
} else {
  console.error("No script tag found!");
}
