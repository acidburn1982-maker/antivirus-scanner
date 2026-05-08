const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  startScan: (scanType) => ipcRenderer.invoke('start-scan', scanType),
  getScanProgress: () => ipcRenderer.invoke('get-scan-progress'),
  stopScan: () => ipcRenderer.invoke('stop-scan')
});
