const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'templates', 'index.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf8');

const hasProgressHud = htmlContent.includes('id="progress-hud"') || htmlContent.includes("id='progress-hud'");
console.log("Does HTML contain 'progress-hud'?", hasProgressHud);

const matches = htmlContent.match(/id=['"]progress-hud['"]/g);
console.log("Matches found:", matches);
