// Script để tải các file assets cần thiết
const https = require('https');
const fs = require('fs');
const path = require('path');

const assets = [
  // Bootstrap
  {
    url: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    path: 'js/bootstrap.bundle.min.js'
  },
  {
    url: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    path: 'css/bootstrap.min.css'
  },
  // jQuery
  {
    url: 'https://code.jquery.com/jquery-3.7.1.min.js',
    path: 'js/jquery.min.js'
  },
  // SimpleBar
  {
    url: 'https://cdn.jsdelivr.net/npm/simplebar@6.2.5/dist/simplebar.min.js',
    path: 'plugins/simplebar/js/simplebar.min.js'
  },
  {
    url: 'https://cdn.jsdelivr.net/npm/simplebar@6.2.5/dist/simplebar.min.css',
    path: 'plugins/simplebar/css/simplebar.css'
  },
  // MetisMenu
  {
    url: 'https://cdn.jsdelivr.net/npm/metismenu@3.0.7/dist/metisMenu.min.js',
    path: 'plugins/metismenu/js/metisMenu.min.js'
  },
  {
    url: 'https://cdn.jsdelivr.net/npm/metismenu@3.0.7/dist/metisMenu.min.css',
    path: 'plugins/metismenu/css/metisMenu.min.css'
  },
  // Perfect Scrollbar
  {
    url: 'https://cdn.jsdelivr.net/npm/perfect-scrollbar@1.5.5/dist/perfect-scrollbar.min.js',
    path: 'plugins/perfect-scrollbar/js/perfect-scrollbar.js'
  },
  {
    url: 'https://cdn.jsdelivr.net/npm/perfect-scrollbar@1.5.5/css/perfect-scrollbar.css',
    path: 'plugins/perfect-scrollbar/css/perfect-scrollbar.css'
  },
  // Pace.js
  {
    url: 'https://cdn.jsdelivr.net/npm/pace-js@1.2.4/pace.min.js',
    path: 'js/pace.min.js'
  },
  {
    url: 'https://cdn.jsdelivr.net/npm/pace-js@1.2.4/themes/blue/pace-theme-minimal.css',
    path: 'css/pace.min.css'
  }
];

function downloadFile(url, filePath) {
  return new Promise((resolve, reject) => {
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    const file = fs.createWriteStream(filePath);
    https.get(url, (response) => {
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        console.log(`Downloaded: ${filePath}`);
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(filePath, () => {}); // Delete the file async
      reject(err);
    });
  });
}

async function downloadAll() {
  console.log('Starting download of assets...');
  for (const asset of assets) {
    try {
      await downloadFile(asset.url, path.join(__dirname, asset.path));
    } catch (error) {
      console.error(`Failed to download ${asset.path}:`, error.message);
    }
  }
  console.log('Download completed!');
}

downloadAll(); 