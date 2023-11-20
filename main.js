const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const runSpider = require('./spiderRunner');

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  win.loadFile('index.html');

  ipcMain.handle('run-spider', async () => {
    console.log("IPC 'run-spider' event received");
    const logs = await runSpider();
    console.log("Sending back logs");
    return logs;
});
}

app.whenReady().then(createWindow);

function clearLogFile() {
    const logPath = path.join(__dirname, 'scrapy_log.txt');
    // Clear the log file
    if (fs.existsSync(logPath)) {
        fs.unlinkSync(logPath);
    }
}

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    clearLogFile(); // Clear the log file before quitting the app
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
