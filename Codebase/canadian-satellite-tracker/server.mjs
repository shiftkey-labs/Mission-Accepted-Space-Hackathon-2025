// server.mjs (recommend renaming to .mjs for clarity)

import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';

const app = express();
app.use(cors());
const PORT = 5000;

// Use process.env for your credentials
const USERNAME = process.env.SPACETRACK_USERNAME;
const PASSWORD = process.env.SPACETRACK_PASSWORD;

app.get('/api/tle', async (req, res) => {
  const noradList = req.query.norad;
  if (!noradList) return res.status(400).json({ error: 'NORAD list required' });

  const ids = noradList.split(',').map(id => id.trim()).filter(Boolean).join(',');
  const auth = Buffer.from(`${USERNAME}:${PASSWORD}`).toString('base64');
  const url = `https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/${ids}/ORDINAL/1/format/json`;

  try {
    const resp = await fetch(url, {
      headers: { Authorization: `Basic ${auth}` }
    });
    if (!resp.ok) return res.status(resp.status).json({ error: 'Space-Track fetch failed' });
    const data = await resp.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: 'Proxy error', details: err.message });
  }
});

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  next();
});


app.listen(PORT, () => console.log(`Space-Track proxy running at http://localhost:${PORT}`));
