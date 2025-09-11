const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the current directory
app.use(express.static(__dirname));

// Route for the main application
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Route for health check
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    message: 'Interactive Organigram is running',
    timestamp: new Date().toISOString(),
  });
});

// Catch-all route to serve the main app for any path
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`🚀 Interactive Organigram server running on port ${PORT}`);
  console.log(`📱 Access the app at: http://localhost:${PORT}`);
});
