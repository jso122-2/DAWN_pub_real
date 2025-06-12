const { ipcMain } = require('electron');
const pty = require('node-pty');
const os = require('os');

const shells = new Map();

function setupShellHandlers() {
  ipcMain.handle('shell:spawn', (event, shell = '/bin/bash') => {
    const ptyProcess = pty.spawn(shell, [], {
      name: 'xterm-color',
      cols: 80,
      rows: 30,
      cwd: process.env.HOME,
      env: process.env
    });

    const pid = ptyProcess.pid;
    shells.set(pid, ptyProcess);

    ptyProcess.on('data', (data) => {
      event.sender.send(`shell:data:${pid}`, data);
    });

    ptyProcess.on('exit', (code) => {
      event.sender.send(`shell:exit:${pid}`, code);
      shells.delete(pid);
    });

    return pid;
  });

  ipcMain.on('shell:write', (event, pid, data) => {
    const ptyProcess = shells.get(pid);
    if (ptyProcess) {
      ptyProcess.write(data);
    }
  });

  ipcMain.on('shell:resize', (event, pid, cols, rows) => {
    const ptyProcess = shells.get(pid);
    if (ptyProcess) {
      ptyProcess.resize(cols, rows);
    }
  });

  ipcMain.on('shell:kill', (event, pid) => {
    const ptyProcess = shells.get(pid);
    if (ptyProcess) {
      ptyProcess.kill();
      shells.delete(pid);
    }
  });
}

module.exports = { setupShellHandlers }; 