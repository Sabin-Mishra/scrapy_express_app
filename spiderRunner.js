const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

function runSpider() {
    return new Promise((resolve, reject) => {
        // Clear the log file before running the spider
        const logPath = path.join(__dirname, 'scrapy_log.txt');
        fs.writeFileSync(logPath, ''); // Clears the contents of the log file

        // Spawn the Scrapy process
        const pythonProcess = spawn('python', ['stmoritz.py']);

        pythonProcess.on('close', async (code) => {
            try {
                // After the spider closes, read the most recent data and the log file
                const data = await readMostRecentFile('scraped_data');
                const logs = await readFileContent('scrapy_log.txt');
                resolve({ data, logs });
            } catch (err) {
                reject(err);
            }
        });
    });
}

function readMostRecentFile(directory) {
    return new Promise((resolve, reject) => {
        const dirPath = path.join(__dirname, directory);
        fs.readdir(dirPath, (err, files) => {
            if (err) {
                reject(err);
                return;
            }
            const latestFile = files
                .map(filename => ({ filename, mtime: fs.statSync(path.join(dirPath, filename)).mtime }))
                .sort((a, b) => b.mtime - a.mtime)[0].filename;
            const filePath = path.join(dirPath, latestFile);
            fs.readFile(filePath, 'utf8', (err, data) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(data);
                }
            });
        });
    });
}

function readFileContent(filename) {
    return new Promise((resolve, reject) => {
        const filePath = path.join(__dirname, filename);
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                reject(err);
            } else {
                resolve(data);
            }
        });
    });
}

module.exports = runSpider;
