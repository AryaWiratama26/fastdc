/* FastDC Dashboard — Client-side Logic */

const API = {
    async get(url) {
        const res = await fetch(url);
        if (res.status === 401 || res.redirected) { window.location.href = '/login'; return null; }
        return res.json();
    },
    async post(url, data) {
        return (await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })).json();
    },
    async del(url) {
        return (await fetch(url, { method: 'DELETE' })).json();
    }
};

/* ── Status ─────────────────────────────────── */

async function loadStatus() {
    const d = await API.get('/api/status');
    if (!d) return;
    document.getElementById('botName').textContent = d.name || 'Offline';
    document.getElementById('statGuilds').textContent = d.guilds || '0';
    document.getElementById('statMembers').textContent = d.members?.toLocaleString() || '0';
    document.getElementById('statLatency').textContent = d.latency ? d.latency + 'ms' : '--';
    document.getElementById('statPrefix').textContent = d.prefix || '!';
    const dot = document.querySelector('.status-dot');
    d.online ? dot.classList.remove('offline') : dot.classList.add('offline');
}

/* ── Settings ───────────────────────────────── */

async function loadSettings() {
    const d = await API.get('/api/settings');
    if (!d) return;

    // Prefix
    document.getElementById('inputPrefix').value = d.prefix || '!';

    // AI
    const ai = d.ai || {};
    const sel = document.getElementById('inputAIProvider');
    sel.innerHTML = '';
    for (const [name] of Object.entries(ai.providers || {})) {
        const o = document.createElement('option');
        o.value = name; o.textContent = name;
        if (name === ai.active_provider) o.selected = true;
        sel.appendChild(o);
    }
    if (ai.active_provider && ai.providers?.[ai.active_provider])
        document.getElementById('inputAIModel').value = ai.providers[ai.active_provider].model || '';
    document.getElementById('inputAIContext').value = ai.context_file || '';
    setBadge('badgeAI', ai.active_provider ? ai.active_provider.toUpperCase() : 'OFF', !!ai.active_provider);

    // Anti-spam
    const as = d.anti_spam || {};
    document.getElementById('inputSpamMax').value = as.max_messages || 5;
    document.getElementById('inputSpamInterval').value = as.interval || 5;
    document.getElementById('inputSpamAction').value = as.action || 'warn';
    setBadge('badgeAntispam', as.enabled ? 'ON' : 'OFF', as.enabled);

    // Leveling
    document.getElementById('inputXP').value = d.leveling?.xp_per_message || 15;
    setBadge('badgeLeveling', d.leveling?.enabled ? 'ON' : 'OFF', d.leveling?.enabled);

    // Presence
    const p = d.presence || {};
    document.getElementById('inputPresenceStatus').value = p.status || 'online';
    document.getElementById('inputPresenceType').value = p.activity_type || 'playing';
    document.getElementById('inputPresenceName').value = p.activity_name || 'FastDC Bot';

    // Welcome / Leave
    document.getElementById('inputWelcomeMsg').value = d.welcome?.message || '';
    setBadge('badgeWelcome', d.welcome?.enabled ? 'ON' : 'OFF', d.welcome?.enabled);
    document.getElementById('inputLeaveMsg').value = d.leave?.message || '';
    setBadge('badgeLeave', d.leave?.enabled ? 'ON' : 'OFF', d.leave?.enabled);

    // Auto Role
    document.getElementById('inputAutoRole').value = d.auto_role?.role_id || '';

    // Starboard
    const sb = d.starboard || {};
    document.getElementById('inputStarChannel').value = sb.channel_id || '';
    document.getElementById('inputStarEmoji').value = sb.emoji || '\u2B50';
    document.getElementById('inputStarThreshold').value = sb.threshold || 3;
    setBadge('badgeStarboard', sb.enabled ? 'ON' : 'OFF', sb.enabled);

    // Temp Voice
    document.getElementById('inputTempVoice').value = d.temp_voice?.trigger_channel_id || '';
    setBadge('badgeTempVoice', d.temp_voice?.enabled ? 'ON' : 'OFF', d.temp_voice?.enabled);

    // Auto replies
    renderAutoReplies(d.auto_replies || []);
}

function setBadge(id, text, on) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = text;
    el.className = 'badge ' + (on ? 'badge-on' : 'badge-off');
}

/* ── Update Functions ───────────────────────── */

async function updatePrefix() {
    const v = document.getElementById('inputPrefix').value.trim();
    if (!v) return;
    await API.post('/api/settings', { prefix: v });
    document.getElementById('statPrefix').textContent = v;
    loadLogs();
}

async function updateAI() {
    await API.post('/api/settings', {
        ai: {
            active_provider: document.getElementById('inputAIProvider').value,
            model: document.getElementById('inputAIModel').value.trim() || 'default',
            context_file: document.getElementById('inputAIContext').value.trim()
        }
    });
    loadSettings(); loadLogs();
}

async function updateAntiSpam() {
    await API.post('/api/settings', {
        anti_spam: {
            max_messages: document.getElementById('inputSpamMax').value,
            interval: document.getElementById('inputSpamInterval').value,
            action: document.getElementById('inputSpamAction').value
        }
    });
    loadLogs();
}

async function updateLeveling() {
    await API.post('/api/settings', {
        leveling: {
            xp_per_message: document.getElementById('inputXP').value
        }
    });
    loadLogs();
}

async function updatePresence() {
    await API.post('/api/settings', {
        presence: {
            status: document.getElementById('inputPresenceStatus').value,
            activity_type: document.getElementById('inputPresenceType').value,
            activity_name: document.getElementById('inputPresenceName').value.trim()
        }
    });
    loadLogs();
}

async function updateWelcome() {
    await API.post('/api/settings', {
        welcome: {
            message: document.getElementById('inputWelcomeMsg').value.trim()
        }
    });
    loadLogs();
}

async function updateLeave() {
    await API.post('/api/settings', {
        leave: {
            message: document.getElementById('inputLeaveMsg').value.trim()
        }
    });
    loadLogs();
}

async function updateAutoRole() {
    await API.post('/api/settings', {
        auto_role: {
            role_id: document.getElementById('inputAutoRole').value.trim()
        }
    });
    loadLogs();
}

async function updateStarboard() {
    await API.post('/api/settings', {
        starboard: {
            channel_id: document.getElementById('inputStarChannel').value.trim(),
            emoji: document.getElementById('inputStarEmoji').value.trim(),
            threshold: document.getElementById('inputStarThreshold').value
        }
    });
    loadLogs();
}

async function updateTempVoice() {
    await API.post('/api/settings', {
        temp_voice: {
            trigger_channel_id: document.getElementById('inputTempVoice').value.trim()
        }
    });
    loadLogs();
}

async function saveData() {
    await API.post('/api/save', {});
    loadLogs();
}

/* ── Custom Commands ────────────────────────── */

function toggleAddCmd() {
    const f = document.getElementById('addCmdForm');
    f.style.display = f.style.display === 'none' ? 'block' : 'none';
}

async function loadCommands() {
    const d = await API.get('/api/commands');
    if (!d) return;
    const list = document.getElementById('commandsList');
    if (!d.length) { list.innerHTML = '<div class="empty-state">No custom commands yet.</div>'; return; }
    list.innerHTML = d.map(c => `
        <div class="list-item">
            <span class="list-item-name">!${c.name}</span>
            <span class="list-item-detail">${esc(c.response)}</span>
            <div class="list-item-right">
                <button class="btn btn-danger btn-sm" onclick="deleteCommand('${c.name}')">Delete</button>
            </div>
        </div>
    `).join('');
}

async function addCommand() {
    const n = document.getElementById('cmdName').value.trim();
    const r = document.getElementById('cmdResponse').value.trim();
    if (!n || !r) return;
    await API.post('/api/commands', { name: n, response: r });
    document.getElementById('cmdName').value = '';
    document.getElementById('cmdResponse').value = '';
    document.getElementById('addCmdForm').style.display = 'none';
    loadCommands(); loadLogs();
}

async function deleteCommand(name) {
    await API.del('/api/commands/' + name);
    loadCommands(); loadLogs();
}

/* ── Auto Replies ───────────────────────────── */

function toggleAddReply() {
    const f = document.getElementById('addReplyForm');
    f.style.display = f.style.display === 'none' ? 'block' : 'none';
}

function renderAutoReplies(replies) {
    const list = document.getElementById('repliesList');
    if (!replies.length) { list.innerHTML = '<div class="empty-state">No auto replies configured.</div>'; return; }
    list.innerHTML = replies.map((r, i) => `
        <div class="list-item">
            <span class="list-item-name">"${esc(r.trigger)}"</span>
            <span class="list-item-detail">${esc(r.response)}</span>
            <div class="list-item-right">
                <button class="btn btn-danger btn-sm" onclick="deleteAutoReply(${i})">Delete</button>
            </div>
        </div>
    `).join('');
}

async function addAutoReply() {
    const t = document.getElementById('replyTrigger').value.trim();
    const r = document.getElementById('replyResponse').value.trim();
    if (!t || !r) return;
    await API.post('/api/autoreplies', { trigger: t, response: r });
    document.getElementById('replyTrigger').value = '';
    document.getElementById('replyResponse').value = '';
    document.getElementById('addReplyForm').style.display = 'none';
    loadSettings(); loadLogs();
}

async function deleteAutoReply(index) {
    await API.del('/api/autoreplies/' + index);
    loadSettings(); loadLogs();
}

/* ── Leaderboard ────────────────────────────── */

async function loadLeaderboard() {
    const d = await API.get('/api/leaderboard');
    if (!d) return;
    const list = document.getElementById('leaderboardList');
    if (!d.length) { list.innerHTML = '<div class="empty-state">No activity yet.</div>'; return; }
    list.innerHTML = d.map((u, i) => `
        <div class="list-item">
            <span class="lb-rank">${i + 1}</span>
            <span class="list-item-name">${esc(u.name)}</span>
            <span class="list-item-detail"></span>
            <div class="list-item-right">
                <span class="lb-level">Lv. ${u.level}</span>
                <span class="lb-xp">${u.xp.toLocaleString()} XP</span>
            </div>
        </div>
    `).join('');
}

/* ── Logs ───────────────────────────────────── */

async function loadLogs() {
    const d = await API.get('/api/logs');
    if (!d) return;
    const list = document.getElementById('logsList');
    if (!d.length) { list.innerHTML = '<div class="empty-state">No logs yet.</div>'; return; }
    list.innerHTML = d.map(l => `
        <div class="log-item">
            <span class="log-time">${l.time}</span>
            <span class="log-action">${esc(l.action)}</span>
            <span class="log-detail">${esc(l.detail)}</span>
        </div>
    `).join('');
}

/* ── Helpers ────────────────────────────────── */

function esc(s) {
    if (!s) return '';
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/* ── Init ───────────────────────────────────── */

async function init() {
    await Promise.all([loadStatus(), loadSettings(), loadCommands(), loadLeaderboard(), loadLogs()]);
    setInterval(() => { loadStatus(); loadLeaderboard(); loadLogs(); }, 15000);
}

init();
