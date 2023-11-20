const { ipcRenderer } = require('electron');

document.getElementById('runSpider').addEventListener('click', async () => {
  try {
      const { data, logs } = await ipcRenderer.invoke('run-spider');
      document.getElementById('dataOutput').innerText = data;  // Assuming you have an element with ID 'dataOutput'
      document.getElementById('logOutput').innerText = logs;   // Your existing log output element
  } catch (error) {
      console.error('Error:', error);
      // Handle error
  }
});

