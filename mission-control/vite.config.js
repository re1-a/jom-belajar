import { defineConfig } from 'vite';
import fs from 'fs';
import path from 'path';

function inboxApiPlugin() {
  return {
    name: 'inbox-api-plugin',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url === '/api/inbox' && req.method === 'POST') {
          let body = '';
          req.on('data', chunk => { body += chunk.toString(); });
          req.on('end', () => {
            try {
              const data = JSON.parse(body);
              const inboxPath = path.resolve(__dirname, '../inbox.md');
              
              if (data.text && data.text.trim() !== '') {
                fs.appendFileSync(inboxPath, `\n${data.text.trim()}\n`);
              }
              
              res.statusCode = 200;
              res.setHeader('Content-Type', 'application/json');
              res.end(JSON.stringify({ success: true }));
            } catch (error) {
              console.error(error);
              res.statusCode = 500;
              res.end(JSON.stringify({ error: 'Failed to write inbox' }));
            }
          });
        } else {
          next();
        }
      });
    }
  };
}

export default defineConfig({
  plugins: [inboxApiPlugin()],
  server: {
    fs: {
      allow: [
        '..', // Allow access to parent folder (Pembantu_AI)
        '/Users/re1/.gemini/antigravity/brain/c0e5d5d4-f531-48fe-8750-6c9bcc5de92a' // Allow access to specific plan folder
      ]
    }
  }
});
