const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'templates', 'index.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf8');

const scriptMatch = htmlContent.match(/<script>([\s\S]*?)<\/script>/);

if (scriptMatch) {
  const jsCode = scriptMatch[1];
  const tempFile = path.join(__dirname, 'temp_check.js');
  fs.writeFileSync(tempFile, jsCode, 'utf8');
  console.log("JavaScript code extracted successfully to temp_check.js. Running syntax check...");
  
  const { execSync } = require('child_process');
  try {
    execSync(`node --check "${tempFile}"`, { stdio: 'inherit' });
    console.log("Syntax check passed: No syntax errors found in JavaScript!");
    fs.unlinkSync(tempFile);
  } catch (err) {
    console.error("Syntax error detected in JavaScript!");
    // Keep the temp file for debugging
  }
} else {
  console.error("No script tag found!");
}
