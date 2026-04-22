const express = require('express');
const mongoose = require('mongoose');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const axios = require('axios');

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.json());

// Datenbank Verbindung (Variable wird in Render gesetzt)
mongoose.connect(process.env.MONGODB_URI);

// User Modell mit ID Logik
const userSchema = new mongoose.Schema({
    username: String,
    customId: { type: Number, default: 1001 },
    bio: String
});
const User = mongoose.model('User', userSchema);

// HS-Code Modell (Erweiterbar)
const hsSchema = new mongoose.Schema({ code: String, name: String });
const HSCode = mongoose.model('HSCode', hsSchema);

// Routen
app.get('/', async (req, res) => {
    try {
        // News-Simulation (Aktuelle Zoll-News)
        const news = [
            { t: "Neue Einfuhrumsatzsteuer-Regeln 2026", d: "22.04.2026" },
            { t: "Zollauktion: Fahrzeuge in München", d: "21.04.2026" },
            { t: "Strengere Kontrollen für Textilimporte", d: "20.04.2026" }
        ];
        res.render('index', { news });
    } catch (e) { res.send("Fehler beim Laden"); }
});

// API für Währungsumrechnung (Nutzt kostenlose API)
app.get('/api/cur', async (req, res) => {
    const r = await axios.get('https://api.exchangerate-api.com/v4/latest/EUR');
    res.json(r.data.rates);
});

// Chat Logik
io.on('connection', (socket) => {
    socket.on('chatMsg', (data) => io.emit('chatMsg', data));
});

const PORT = process.env.PORT || 3000;
http.listen(PORT, () => console.log('System aktiv auf Port ' + PORT));
