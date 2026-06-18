const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'templates', 'index.html');
const lines = fs.readFileSync(htmlPath, 'utf8').split('\n');

lines.forEach((line, idx) => {
  if (line.includes('progressHud') || line.includes('progress-hud')) {
    console.log(`Line ${idx + 1}: ${line.trim()}`);
  }
});
