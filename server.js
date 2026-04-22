const express = require('express');
const { createClient } = require('@supabase/supabase-js');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const axios = require('axios');

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.json());

// Verbindung zu Supabase (Kostenlos)
const supabase = createClient(process.env.SUPA_URL, process.env.SUPA_KEY);

// Hauptseite mit Zoll-News
app.get('/', async (req, res) => {
    const news = [
        { t: "Kostenlose Datenbank aktiv", d: "22.04.2026" },
        { t: "Zoll-News: Neue Freigrenzen", d: "21.04.2026" }
    ];
    res.render('index', { news });
});

// Währungsumrechner API
app.get('/api/cur', async (req, res) => {
    const r = await axios.get('https://api.exchangerate-api.com/v4/latest/EUR');
    res.json(r.data.rates);
});

// Chat-Logik
io.on('connection', (socket) => {
    socket.on('chatMsg', (data) => io.emit('chatMsg', data));
});

const PORT = process.env.PORT || 3000;
http.listen(PORT, () => console.log('System läuft auf Port ' + PORT));
