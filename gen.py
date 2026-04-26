import json, pathlib

assets = json.loads(pathlib.Path("json_folder/assets_base64.json").read_text())
bg   = assets.get("Background","")
bCas = assets.get("Blue Castle","")
rCas = assets.get("Red Castle","")
p1   = assets.get("Projectile_1","")
p2   = assets.get("Projectile_2","")
w1   = assets.get("Weapon_1","")
w2   = assets.get("Weapon_2","")

STORE = "https://play.google.com/store/apps/details?id=com.epicoro.castleclashers"

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>Castle Clasher</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;user-select:none;-webkit-user-select:none;}
body{width:100%;height:100%;overflow:hidden;background:#1a1a2e;font-family:'Segoe UI',sans-serif;}
html{width:100%;height:100%;}
#GameDiv{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0d0d1a;}
#GameContainer{position:relative;overflow:hidden;}
#GameCanvas{display:block;touch-action:none;}
/* UI layer sits on top of canvas */
#ui-layer{position:absolute;inset:0;pointer-events:none;}
/* HP bars */
.hp-wrap{position:absolute;top:12px;width:140px;}
#hp-player{left:10px;}
#hp-enemy{right:10px;text-align:right;}
.hp-label{font-size:11px;color:#fff;font-weight:700;text-shadow:0 1px 3px #000;margin-bottom:3px;}
.hp-bar-bg{height:14px;border-radius:7px;background:rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.2);}
.hp-bar-fill{height:100%;border-radius:7px;transition:width .3s;box-shadow:0 0 8px currentColor;}
#hp-player .hp-bar-fill{background:linear-gradient(90deg,#27ae60,#2ecc71);color:#2ecc71;}
#hp-enemy .hp-bar-fill{background:linear-gradient(90deg,#e74c3c,#c0392b);color:#e74c3c;margin-left:auto;}
/* Level indicator */
#level-badge{position:absolute;top:10px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,.6);color:#f1c40f;font-size:13px;font-weight:700;padding:4px 14px;border-radius:20px;border:1px solid #f1c40f44;}
/* Character cards */
#char-cards{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:8px;pointer-events:auto;}
.char-card{width:58px;height:68px;border-radius:10px;background:rgba(0,0,0,.55);border:2px solid rgba(255,255,255,.2);display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:border-color .15s,transform .15s;}
.char-card.selected{border-color:#f1c40f;transform:scale(1.08);}
.char-card.used{opacity:.4;pointer-events:none;}
.char-card canvas{border-radius:50%;}
.char-card .char-label{font-size:9px;color:#fff;margin-top:3px;font-weight:600;}
/* Tutorial */
#tutorial{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.55);pointer-events:auto;}
#tutorial-inner{text-align:center;color:#fff;}
#tutorial-inner h2{font-size:26px;font-weight:800;text-shadow:0 2px 8px #000;margin-bottom:8px;}
#tutorial-inner p{font-size:15px;opacity:.85;}
.tap-hint{margin-top:18px;font-size:13px;opacity:.6;animation:pulse 1.4s infinite;}
@keyframes pulse{0%,100%{opacity:.6}50%{opacity:1}}
/* Level 2 transition screen */
#lvl2-screen{position:absolute;inset:0;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.82);pointer-events:auto;}
#lvl2-screen.show{display:flex;}
#lvl2-inner{text-align:center;color:#fff;}
#lvl2-inner h2{font-size:36px;font-weight:900;color:#f1c40f;text-shadow:0 0 30px #f1c40f88;}
#lvl2-inner p{font-size:16px;color:#e0e0e0;margin-top:8px;}
/* End screen */
#end-screen{position:absolute;inset:0;display:none;flex-direction:column;align-items:center;justify-content:center;background:rgba(0,0,0,.78);pointer-events:auto;}
#end-screen.show{display:flex;}
#end-title{font-size:38px;font-weight:900;color:#f1c40f;text-shadow:0 0 30px #f1c40f;}
#end-message{font-size:16px;color:#fff;margin:10px 0 24px;}
#cta-button{padding:16px 40px;font-size:18px;font-weight:800;color:#fff;background:linear-gradient(135deg,#6C5CE7,#a855f7);border:none;border-radius:30px;cursor:pointer;box-shadow:0 4px 20px #6C5CE788;animation:ctapulse 1.2s infinite;pointer-events:auto;}
@keyframes ctapulse{0%,100%{transform:scale(1);box-shadow:0 4px 20px #6C5CE788}50%{transform:scale(1.05);box-shadow:0 6px 28px #6C5CE7bb}}
</style>
</head>
<body>
<div id="GameDiv">
  <div id="GameContainer">
    <!-- main canvas -->
    <canvas id="GameCanvas"></canvas>
    <!-- ui overlay -->
    <div id="ui-layer">
      <!-- hp bars -->
      <div class="hp-wrap" id="hp-player">
        <div class="hp-label">&#x1F3F0; You</div>
        <div class="hp-bar-bg"><div class="hp-bar-fill" id="hp-player-fill" style="width:100%"></div></div>
      </div>
      <div class="hp-wrap" id="hp-enemy">
        <div class="hp-label">Enemy &#x1F3F0;</div>
        <div class="hp-bar-bg"><div class="hp-bar-fill" id="hp-enemy-fill" style="width:100%"></div></div>
      </div>
      <!-- level badge -->
      <div id="level-badge">Level 1</div>
      <!-- character selector -->
      <div id="char-cards">
        <div class="char-card selected" id="card-0" data-idx="0">
          <canvas width="38" height="38" id="card-canvas-0"></canvas>
          <span class="char-label">Cyclops</span>
        </div>
        <div class="char-card" id="card-1" data-idx="1">
          <canvas width="38" height="38" id="card-canvas-1"></canvas>
          <span class="char-label">Skeleton</span>
        </div>
        <div class="char-card" id="card-2" data-idx="2">
          <canvas width="38" height="38" id="card-canvas-2"></canvas>
          <span class="char-label">Goblin</span>
        </div>
      </div>
      <!-- level 2 transition screen -->
      <div id="lvl2-screen">
        <div id="lvl2-inner">
          <h2>&#x26A1; Level 2 &#x26A1;</h2>
          <p>The enemy fights back harder...</p>
        </div>
      </div>
      <!-- end screen -->
      <div id="end-screen">
        <div id="end-title">Victory!</div>
        <div id="end-message">The castle has fallen!</div>
        <button id="cta-button">Play Now</button>
      </div>
      <!-- tutorial -->
      <div id="tutorial">
        <div id="tutorial-inner">
          <h2>Castle Clasher</h2>
          <p>Drag to aim, release to fire!</p>
          <p class="tap-hint">Tap to Start</p>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
'use strict';
/* =====================================================================
   CONFIG
   ===================================================================== */
const config = {
  parameters: {
    gameTitle:              { value: "Castle Clasher" },
    tutorialText:           { value: "Drag to aim, release to fire!" },
    winText:                { value: "Victory!" },
    loseText:               { value: "Defeated!" },
    ctaText:                { value: "Play Now" },
    primaryColor:           { value: "#6C5CE7" },
    secondaryColor:         { value: "#00D2D3" },
    difficulty:             { value: 1 },
    autoRedirectAfterClicks:{ value: 0 },
    autoRedirectAfterSeconds:{ value: 0 }
  },
  storeLinks: [
    { store:"APP_STORE",  url:"STORE_URL", platform:"IOS" },
    { store:"PLAY_STORE", url:"STORE_URL", platform:"ANDROID" }
  ]
};

const GAME_CONFIG = {
  physics: { gravity: 0.3, projectileSpeed: 12, maxDragRadius: 80 },
  player:  { hp: 100, castleX: 0.18 },
  enemy:   { hp: 100, castleX: 0.72, aimVariance: 0.2, turnDelay: 1200 },
  characters: [
    { id:"red_cyclops",  label:"Cyclops",  bodyColor:"#c0392b", eyeColor:"#f1948a", projectileType:"cannonball", damage:30, trailColor:"orange" },
    { id:"skeleton",     label:"Skeleton", bodyColor:"#d5d8dc", eyeColor:"#2e86c1", projectileType:"rocket",     damage:22, trailColor:"grey"   },
    { id:"green_goblin", label:"Goblin",   bodyColor:"#27ae60", eyeColor:"#e74c3c", projectileType:"bomb",       damage:26, trailColor:"orange" }
  ],
  enemyChar: { id:"crow", bodyColor:"#2c3e50", projectileType:"bomb", damage:22, trailColor:"black" },
  difficulty: {
    easy:   { enemyHp:150, aimVariance:0.4,  enemyDmgMult:0.7 },
    medium: { enemyHp:100, aimVariance:0.2,  enemyDmgMult:1.0 },
    hard:   { enemyHp:70,  aimVariance:0.05, enemyDmgMult:1.5 }
  }
};

/* =====================================================================
   ASSETS
   ===================================================================== */
const ASSETS = {};
const ASSET_SRCS = {
  bg:     'BG_SRC',
  castle_player: 'BCASTLE_SRC',
  castle_enemy:  'RCASTLE_SRC',
  proj1:  'P1_SRC',
  proj2:  'P2_SRC',
  weap1:  'W1_SRC',
  weap2:  'W2_SRC'
};
function loadAssets() {
  return Promise.all(Object.entries(ASSET_SRCS).map(([k, src]) => new Promise(res => {
    if (!src) { res(); return; }
    const img = new Image();
    img.onload = () => { ASSETS[k] = img; res(); };
    img.onerror = () => res();
    img.src = src;
  })));
}

/* =====================================================================
   EVENT EMITTER
   ===================================================================== */
class EventEmitter {
  constructor() { this._h = {}; }
  on(ev, fn) { (this._h[ev] = this._h[ev]||[]).push(fn); return this; }
  emit(ev, d) { (this._h[ev]||[]).forEach(fn => fn(d)); }
}

/* =====================================================================
   MINI VSDK RUNTIME
   ===================================================================== */
class MiniVSDKRuntime extends EventEmitter {
  constructor(cfg) {
    super();
    this._cfg = cfg;
    this._redirected = false;
    this._audio = { volume:1, muted:false };
    this._game = null;
  }
  init({ playableFactory }) {
    this.emit('PRELOAD');
    loadAssets().then(() => {
      this._game = playableFactory({ vsdk: this });
      this._game.init();
      this._game.create();
      this.emit('READY');
      window.addEventListener('resize', () => {
        this._game.onResize();
        this.emit('SCREEN_RESIZED');
      });
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) { this.pause(); } else { this.resume(); }
      });
    });
  }
  startPlayable() { this._game && this._game.start(); this.emit('START'); }
  pause()  { this._game && this._game.pause();  this.emit('PAUSE'); }
  resume() { this._game && this._game.resume(); this.emit('RESUME'); }
  winGame()  { this.endGame('win'); }
  loseGame() { this.endGame('lose'); }
  endGame(status) {
    this.emit('END', { status });
    const t = document.getElementById('end-title');
    const m = document.getElementById('end-message');
    if (t) t.textContent = status === 'win' ?
      this.getParameterValue('winText') : this.getParameterValue('loseText');
    if (m) m.textContent = status === 'win' ? 'The castle has fallen!' : 'Your castle was destroyed!';
    const es = document.getElementById('end-screen');
    if (es) es.classList.add('show');
    this.emit(status === 'win' ? 'WIN' : 'LOSE');
  }
  redirectToInstallPage() {
    if (this._redirected) return;
    this._redirected = true;
    const url = this.getStoreLink();
    window.open(url, '_blank');
  }
  getStoreLink() {
    const ua = navigator.userAgent;
    const links = this._cfg.storeLinks || [];
    if (/iPhone|iPad|iPod/.test(ua)) {
      const ios = links.find(l => l.platform === 'IOS');
      if (ios) return ios.url;
    }
    const and = links.find(l => l.platform === 'ANDROID');
    return and ? and.url : (links[0] ? links[0].url : '#');
  }
  getParameterValue(key) {
    const p = this._cfg.parameters[key];
    return p ? p.value : undefined;
  }
  getScreenSize() { return { width: window.innerWidth, height: window.innerHeight }; }
  getAudioVolume() { return this._audio.volume; }
  setVolume(v) { this._audio.volume = v; this.emit('VOLUME_CHANGED', v); }
  muteAudio()   { this._audio.muted = true;  this.emit('VOLUME_CHANGED', 0); }
  unmuteAudio() { this._audio.muted = false; this.emit('VOLUME_CHANGED', this._audio.volume); }
}

/* =====================================================================
   PLAYABLE GAME
   ===================================================================== */
class PlayableGame {
  constructor({ vsdk }) {
    this.vsdk = vsdk;
    this.canvas = document.getElementById('GameCanvas');
    this.ctx    = this.canvas.getContext('2d');
    this.W = 0; this.H = 0;
    this.raf = null;
    this.running = false;
    // game state
    this.state = 'idle'; // idle|playing|aiming|flying|enemy_turn|ended
    this.level = 1;
    this.playerHp = GAME_CONFIG.player.hp;
    this.playerHpMax = GAME_CONFIG.player.hp;
    this.enemyHp  = GAME_CONFIG.enemy.hp;
    this.enemyHpMax = GAME_CONFIG.enemy.hp;
    this._aimVariance   = GAME_CONFIG.enemy.aimVariance;
    this._enemyDmgMult  = 1.0;
    this.gameEnded = false;
    this.transitioning = false;
    this.shotCount = 0;
    this.redirectOnImpact = false;
    // projectile
    this.proj = null;
    this.trail = [];
    // drag
    this.dragging = false;
    this.dragX = 0; this.dragY = 0;
    // particles
    this.particles = [];
    this.dmgNumbers = [];
    // shake
    this.shakeAmt = 0;
    // character
    this.selectedIdx = 0;
    this.charUsed = [false,false,false];
    // castle damage states
    this.playerDmgState = 0; // 0-4
    this.enemyDmgState  = 0;
    this.playerTilt = 0;
    this.enemyTilt  = 0;
    // layout
    this.groundY = 0; this.castleW = 0; this.castleH = 0;
    this.pCX = 0; this.pCY = 0; this.eCX = 0; this.eCY = 0;
    this.slingshotX = 0; this.slingshotY = 0;
  }

  init() {
    this._resize();
  }

  create() {
    this._drawCharCards();
    const cta = document.getElementById('cta-button');
    if (cta) cta.addEventListener('click', () => this.vsdk.redirectToInstallPage());
    // bind events
    this.canvas.addEventListener('pointerdown',  e => this._onDown(e));
    this.canvas.addEventListener('pointermove',  e => this._onMove(e));
    this.canvas.addEventListener('pointerup',    e => this._onUp(e));
    this.canvas.addEventListener('pointercancel',e => this._onUp(e));
    // character card clicks
    document.querySelectorAll('.char-card').forEach(el => {
      el.addEventListener('click', () => {
        const idx = parseInt(el.dataset.idx);
        if (!this.charUsed[idx]) this._selectChar(idx);
      });
    });
    // tutorial click starts game
    const tut = document.getElementById('tutorial');
    if (tut) tut.addEventListener('pointerdown', () => {
      tut.style.display = 'none';
      this.vsdk.startPlayable();
    });
    // start render loop
    this.running = true;
    this._loop();
  }

  start() {
    this.state = 'playing';
  }

  pause()  { this.running = false; cancelAnimationFrame(this.raf); }
  resume() { if (!this.running) { this.running = true; this._loop(); } }

  onResize() { this._resize(); }
  onAudioVolumeChanged() {}
  onParameterUpdated() {}

  /* ---- layout ---- */
  _resize() {
    const cont = document.getElementById('GameContainer');
    const div  = document.getElementById('GameDiv');
    const vw = div.clientWidth, vh = div.clientHeight;
    const aspect = 16/9;
    let W, H;
    if (vw / vh > aspect) { H = vh; W = H * aspect; }
    else { W = vw; H = W / aspect; }
    this.W = W; this.H = H;
    this.canvas.width  = W; this.canvas.height = H;
    cont.style.width  = W + 'px';
    cont.style.height = H + 'px';
    this._layout();
  }

  _layout() {
    const W = this.W, H = this.H;
    this.groundY  = H * 0.72;
    this.castleW  = Math.min(Math.max(W * 0.26, 80), 200);
    this.castleH  = this.castleW * (958 / 731);
    this.pCX      = W * GAME_CONFIG.player.castleX + this.castleW * 0.35;
    this.pCY      = this.groundY;
    this.eCX      = W * GAME_CONFIG.enemy.castleX  - this.castleW * 0.35;
    this.eCY      = this.groundY;
    this.slingshotX = this.pCX;
    this.slingshotY = this.pCY - this.castleH * 0.82;
  }

  /* ---- game loop ---- */
  _loop() {
    if (!this.running) return;
    this.raf = requestAnimationFrame(() => this._loop());
    this._update();
    this._draw();
  }

  _update() {
    // update projectile
    if (this.proj) {
      this.proj.vx *= 0.999;
      this.proj.vy += GAME_CONFIG.physics.gravity;
      this.proj.x  += this.proj.vx;
      this.proj.y  += this.proj.vy;
      this.proj.age++;
      // trail
      this.trail.push({ x: this.proj.x, y: this.proj.y, age: 0 });
      if (this.trail.length > 22) this.trail.shift();
      this.trail.forEach(t => t.age++);
      // hit detection
      const ex = this.eCX, ey = this.eCY - this.castleH * 0.5;
      const px = this.pCX, py = this.pCY - this.castleH * 0.5;
      if (this.proj.owner === 'player') {
        if (Math.abs(this.proj.x - ex) < this.castleW * 0.55 &&
            Math.abs(this.proj.y - ey) < this.castleH * 0.6) {
          this._onPlayerHit(this.proj);
        }
      } else {
        if (Math.abs(this.proj.x - px) < this.castleW * 0.55 &&
            Math.abs(this.proj.y - py) < this.castleH * 0.6) {
          this._onEnemyHit(this.proj);
        }
      }
      // out of bounds
      if (this.proj && (this.proj.x < -50 || this.proj.x > this.W + 50 ||
          this.proj.y > this.H + 50 || this.proj.age > 400)) {
        this.proj = null; this.trail = [];
        if (this.state === 'flying') this._afterPlayerMiss();
      }
    }
    // particles
    this.particles = this.particles.filter(p => {
      p.x += p.vx; p.y += p.vy; p.vy += 0.15; p.life--;
      p.vx *= 0.97; return p.life > 0;
    });
    this.dmgNumbers = this.dmgNumbers.filter(d => {
      d.y -= 1.2; d.life--; return d.life > 0;
    });
    // shake decay
    if (this.shakeAmt > 0) this.shakeAmt = Math.max(0, this.shakeAmt - 0.6);
    // castle tilt decay
    this.playerTilt *= 0.88;
    this.enemyTilt  *= 0.88;
  }

  /* ---- drawing ---- */
  _draw() {
    const ctx = this.ctx, W = this.W, H = this.H;
    ctx.save();
    // screen shake
    if (this.shakeAmt > 0) {
      ctx.translate(
        (Math.random() - 0.5) * this.shakeAmt * 2,
        (Math.random() - 0.5) * this.shakeAmt * 2
      );
    }
    // background
    this._drawBackground(ctx, W, H);
    // ground
    this._drawGround(ctx, W, H);
    // castles
    this._drawCastle(ctx, 'player');
    this._drawCastle(ctx, 'enemy');
    // slingshot
    if (this.state !== 'idle') this._drawSlingshot(ctx);
    // arc preview
    if (this.state === 'aiming' && this.dragging) this._drawArcPreview(ctx);
    // trail
    this._drawTrail(ctx);
    // projectile
    if (this.proj) this._drawProjectile(ctx, this.proj);
    // particles
    this._drawParticles(ctx);
    // damage numbers
    this._drawDmgNumbers(ctx);
    ctx.restore();
  }

  _drawBackground(ctx, W, H) {
    if (ASSETS.bg) {
      ctx.drawImage(ASSETS.bg, 0, 0, W, H);
    } else {
      // gradient sky fallback
      const sky = ctx.createLinearGradient(0,0,0,H*0.7);
      sky.addColorStop(0,'#1a1a4e'); sky.addColorStop(1,'#4a6fa5');
      ctx.fillStyle = sky; ctx.fillRect(0,0,W,H);
    }
  }

  _drawGround(ctx, W, H) {
    const gy = this.groundY;
    const g = ctx.createLinearGradient(0, gy, 0, H);
    g.addColorStop(0, '#2d5a1b'); g.addColorStop(0.3, '#1a3a0d'); g.addColorStop(1,'#0d1f07');
    ctx.fillStyle = g; ctx.fillRect(0, gy, W, H - gy);
    // snow line
    ctx.beginPath(); ctx.moveTo(0, gy);
    for (let x = 0; x <= W; x += 8) {
      ctx.lineTo(x, gy + Math.sin(x * 0.05) * 3);
    }
    ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.closePath();
    ctx.fillStyle = 'rgba(255,255,255,0.15)'; ctx.fill();
  }

  _drawCastle(ctx, side) {
    const isPlayer = side === 'player';
    const cx = isPlayer ? this.pCX : this.eCX;
    const cy = isPlayer ? this.pCY : this.eCY;
    const img = isPlayer ? ASSETS.castle_player : ASSETS.castle_enemy;
    const cw = this.castleW, ch = this.castleH;
    const dmg = isPlayer ? this.playerDmgState : this.enemyDmgState;
    const tilt = isPlayer ? this.playerTilt : this.enemyTilt;
    ctx.save();
    ctx.translate(cx, cy);
    if (tilt) ctx.rotate(tilt * Math.PI / 180);
    const x = -cw * 0.5, y = -ch;
    if (img) {
      ctx.drawImage(img, x, y, cw, ch);
    } else {
      // fallback castle
      const col = isPlayer ? '#3498db' : '#e74c3c';
      ctx.fillStyle = col;
      ctx.fillRect(x, y, cw, ch);
      ctx.fillStyle = '#2c3e50';
      for (let i = 0; i < 3; i++) {
        ctx.fillRect(x + cw*0.1 + i*cw*0.3, y + ch*0.1, cw*0.18, ch*0.2);
      }
    }
    // damage overlay
    if (dmg > 0) {
      ctx.globalAlpha = dmg * 0.18;
      ctx.fillStyle = '#1a0000';
      ctx.fillRect(x, y, cw, ch);
      ctx.globalAlpha = 1;
      // crack lines
      ctx.strokeStyle = `rgba(0,0,0,${dmg*0.25})`;
      ctx.lineWidth = 1.5;
      for (let i = 0; i < dmg * 2; i++) {
        const rx = x + (i*47+13) % cw;
        const ry = y + (i*31+7)  % ch;
        ctx.beginPath();
        ctx.moveTo(rx, ry);
        ctx.lineTo(rx + (i%2?8:-6), ry + 12);
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  _drawSlingshot(ctx) {
    const sx = this.slingshotX, sy = this.slingshotY;
    const cw = this.castleW, ch = this.castleH;
    // fork — thin Y arms
    const forkH = 22, forkW = 14;
    ctx.strokeStyle = '#5d3a1a'; ctx.lineWidth = 4; ctx.lineCap = 'round';
    // center post
    ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx, sy + forkH * 1.4); ctx.stroke();
    // left arm
    ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx - forkW, sy - forkH); ctx.stroke();
    // right arm
    ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx + forkW, sy - forkH); ctx.stroke();
    const lx = sx - forkW, ly = sy - forkH;
    const rx = sx + forkW, ry = sy - forkH;
    // elastic bands — clipped to castle bounds
    let cx = sx, cy2 = sy;
    if (this.dragging) { cx = this.dragX; cy2 = this.dragY; }
    ctx.save();
    ctx.beginPath();
    ctx.rect(this.pCX - cw * 0.5, this.pCY - ch, cw, ch);
    ctx.clip();
    const tension = this.dragging ?
      Math.min(1, Math.hypot(cx - sx, cy2 - sy) / GAME_CONFIG.physics.maxDragRadius) : 0;
    const bandColor = tension > 0.8 ? '#e74c3c' : '#8B4513';
    ctx.strokeStyle = bandColor; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(cx, cy2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(rx, ry); ctx.lineTo(cx, cy2); ctx.stroke();
    ctx.restore();
    // character in slingshot
    const charId = GAME_CONFIG.characters[this.selectedIdx].id;
    this._drawCharFace(ctx, cx, cy2, 13, charId);
  }

  _drawArcPreview(ctx) {
    const sx = this.slingshotX, sy = this.slingshotY;
    const dx = this.dragX - sx, dy = this.dragY - sy;
    const speed = GAME_CONFIG.physics.projectileSpeed;
    const maxDrag = GAME_CONFIG.physics.maxDragRadius;
    const dist = Math.min(Math.hypot(dx, dy), maxDrag);
    if (dist < 5) return;
    const vx = -dx / maxDrag * speed;
    const vy = -dy / maxDrag * speed;
    const g  = GAME_CONFIG.physics.gravity;
    const nodes = 12;
    const dt = 5;
    ctx.save();
    for (let i = 1; i <= nodes; i++) {
      const t = i * dt;
      const nx = sx + vx * t;
      const ny = sy + vy * t + 0.5 * g * t * t;
      if (nx < 0 || nx > this.W || ny > this.H) break;
      const alpha = 1 - i / (nodes + 1);
      ctx.globalAlpha = alpha * 0.7;
      ctx.fillStyle = '#fff';
      const r = 4 - i * 0.2;
      ctx.beginPath();
      ctx.arc(nx, ny, Math.max(r, 1.5), 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  _drawTrail(ctx) {
    if (!this.trail.length) return;
    const char = GAME_CONFIG.characters[this.selectedIdx];
    const col = this.proj && this.proj.owner === 'enemy' ?
      GAME_CONFIG.enemyChar.trailColor : (char ? char.trailColor : 'orange');
    this.trail.forEach((t, i) => {
      const alpha = (i / this.trail.length) * 0.5;
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.fillStyle = col;
      const r = 4 * (i / this.trail.length);
      ctx.beginPath(); ctx.arc(t.x, t.y, r, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    });
  }

  _drawProjectile(ctx, p) {
    if (p.owner === 'player') {
      this._drawCharFace(ctx, p.x, p.y, 12, GAME_CONFIG.characters[this.selectedIdx].id);
    } else {
      this._drawCharFace(ctx, p.x, p.y, 12, GAME_CONFIG.enemyChar.id);
    }
  }

  _drawParticles(ctx) {
    this.particles.forEach(p => {
      ctx.save();
      ctx.globalAlpha = p.life / p.maxLife;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });
  }

  _drawDmgNumbers(ctx) {
    this.dmgNumbers.forEach(d => {
      ctx.save();
      ctx.globalAlpha = d.life / d.maxLife;
      ctx.fillStyle = d.color;
      ctx.font = `bold ${d.size}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.strokeStyle = 'rgba(0,0,0,0.6)';
      ctx.lineWidth = 3;
      ctx.strokeText(d.text, d.x, d.y);
      ctx.fillText(d.text, d.x, d.y);
      ctx.restore();
    });
  }

  /* ---- character face drawing ---- */
  _drawCharFace(ctx, x, y, r, charId) {
    ctx.save();
    if (charId === 'red_cyclops') {
      // red body
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2);
      ctx.fillStyle = '#c0392b'; ctx.fill();
      ctx.strokeStyle = '#922b21'; ctx.lineWidth = 1.5; ctx.stroke();
      // single big white eye
      const er = r * 0.52;
      ctx.beginPath(); ctx.arc(x, y - r*0.05, er, 0, Math.PI*2);
      ctx.fillStyle = '#fff'; ctx.fill();
      // iris
      ctx.beginPath(); ctx.arc(x, y - r*0.05, er*0.55, 0, Math.PI*2);
      ctx.fillStyle = '#2980b9'; ctx.fill();
      // pupil
      ctx.beginPath(); ctx.arc(x, y - r*0.05, er*0.28, 0, Math.PI*2);
      ctx.fillStyle = '#000'; ctx.fill();
      // highlight
      ctx.beginPath(); ctx.arc(x + er*0.2, y - r*0.05 - er*0.2, er*0.14, 0, Math.PI*2);
      ctx.fillStyle = '#fff'; ctx.fill();
    } else if (charId === 'skeleton') {
      // grey body
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2);
      ctx.fillStyle = '#d5d8dc'; ctx.fill();
      ctx.strokeStyle = '#aab7b8'; ctx.lineWidth = 1.5; ctx.stroke();
      // eye sockets (dark ellipses)
      const ew = r*0.28, eh = r*0.22;
      ctx.fillStyle = '#2c3e50';
      ctx.beginPath(); ctx.ellipse(x - r*0.3, y - r*0.15, ew, eh, 0, 0, Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.ellipse(x + r*0.3, y - r*0.15, ew, eh, 0, 0, Math.PI*2); ctx.fill();
      // nose cavity
      ctx.beginPath(); ctx.ellipse(x, y + r*0.08, r*0.1, r*0.12, 0, 0, Math.PI*2);
      ctx.fillStyle = '#2c3e50'; ctx.fill();
      // teeth
      ctx.fillStyle = '#fff';
      const tw = r*0.14, th = r*0.17;
      for (let i = -1; i <= 1; i++) {
        ctx.fillRect(x + i*tw*1.1 - tw*0.5, y + r*0.32, tw*0.9, th);
      }
    } else if (charId === 'green_goblin') {
      // pointy ears behind head
      ctx.fillStyle = '#1e8449';
      ctx.beginPath(); ctx.moveTo(x - r*0.85, y);
      ctx.lineTo(x - r*1.3, y - r*0.7); ctx.lineTo(x - r*0.5, y - r*0.3); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.moveTo(x + r*0.85, y);
      ctx.lineTo(x + r*1.3, y - r*0.7); ctx.lineTo(x + r*0.5, y - r*0.3); ctx.closePath(); ctx.fill();
      // green body
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2);
      ctx.fillStyle = '#27ae60'; ctx.fill();
      ctx.strokeStyle = '#1e8449'; ctx.lineWidth = 1.5; ctx.stroke();
      // red eyes
      const er2 = r * 0.2;
      [-1,1].forEach(side => {
        ctx.beginPath(); ctx.arc(x + side*r*0.32, y - r*0.18, er2, 0, Math.PI*2);
        ctx.fillStyle = '#e74c3c'; ctx.fill();
        ctx.beginPath(); ctx.arc(x + side*r*0.32, y - r*0.18, er2*0.5, 0, Math.PI*2);
        ctx.fillStyle = '#000'; ctx.fill();
      });
      // grin
      ctx.beginPath();
      ctx.arc(x, y + r*0.2, r*0.35, 0.1, Math.PI - 0.1);
      ctx.strokeStyle = '#145a32'; ctx.lineWidth = 2; ctx.stroke();
      // teeth
      ctx.fillStyle = '#fff';
      for (let i = -1; i <= 1; i++) {
        ctx.fillRect(x + i*r*0.22 - r*0.09, y + r*0.2, r*0.17, r*0.2);
      }
    } else if (charId === 'crow') {
      // dark crow
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2);
      ctx.fillStyle = '#2c3e50'; ctx.fill();
      // beak
      ctx.beginPath(); ctx.moveTo(x + r*0.7, y);
      ctx.lineTo(x + r, y - r*0.15); ctx.lineTo(x + r, y + r*0.15); ctx.closePath();
      ctx.fillStyle = '#f39c12'; ctx.fill();
      // eye
      ctx.beginPath(); ctx.arc(x + r*0.3, y - r*0.2, r*0.2, 0, Math.PI*2);
      ctx.fillStyle = '#fff'; ctx.fill();
      ctx.beginPath(); ctx.arc(x + r*0.3, y - r*0.2, r*0.1, 0, Math.PI*2);
      ctx.fillStyle = '#000'; ctx.fill();
    } else {
      // generic fallback
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2);
      ctx.fillStyle = '#7f8c8d'; ctx.fill();
    }
    ctx.restore();
  }

  _drawCharCards() {
    GAME_CONFIG.characters.forEach((ch, i) => {
      const cv = document.getElementById('card-canvas-' + i);
      if (!cv) return;
      const ctx = cv.getContext('2d');
      ctx.clearRect(0,0,38,38);
      this._drawCharFace(ctx, 19, 19, 15, ch.id);
    });
  }

  /* ---- input ---- */
  _canvasPos(e) {
    const r = this.canvas.getBoundingClientRect();
    const clientX = e.clientX !== undefined ? e.clientX : e.touches[0].clientX;
    const clientY = e.clientY !== undefined ? e.clientY : e.touches[0].clientY;
    return {
      x: (clientX - r.left) * (this.W / r.width),
      y: (clientY - r.top)  * (this.H / r.height)
    };
  }

  _onDown(e) {
    if (this.gameEnded || this.transitioning) return;
    const pos = this._canvasPos(e);
    const dx = pos.x - this.slingshotX, dy = pos.y - this.slingshotY;
    const inDragZone = Math.hypot(dx, dy) < 110 || pos.x < this.W * 0.55;
    if (this.level === 2 && !inDragZone) {
      this.vsdk.redirectToInstallPage(); return;
    }
    if (this.state !== 'playing') return;
    if (inDragZone) {
      this.dragging = true;
      this.canvas.setPointerCapture(e.pointerId);
      this.dragX = this.slingshotX; this.dragY = this.slingshotY;
      this.state = 'aiming';
    }
  }

  _onMove(e) {
    if (!this.dragging) return;
    const pos = this._canvasPos(e);
    const sx = this.slingshotX, sy = this.slingshotY;
    const dx = pos.x - sx, dy = pos.y - sy;
    const dist = Math.hypot(dx, dy);
    const maxR = GAME_CONFIG.physics.maxDragRadius;
    if (dist > maxR) {
      this.dragX = sx + dx / dist * maxR;
      this.dragY = sy + dy / dist * maxR;
    } else {
      this.dragX = pos.x; this.dragY = pos.y;
    }
  }

  _onUp(e) {
    if (!this.dragging) return;
    this.dragging = false;
    if (this.state !== 'aiming') return;
    const sx = this.slingshotX, sy = this.slingshotY;
    const dx = this.dragX - sx, dy = this.dragY - sy;
    const dist = Math.hypot(dx, dy);
    if (dist < 10) { this.state = 'playing'; return; }
    const speed = GAME_CONFIG.physics.projectileSpeed;
    const maxR  = GAME_CONFIG.physics.maxDragRadius;
    const vx = -dx / maxR * speed;
    const vy = -dy / maxR * speed;
    this._launch(vx, vy);
  }

  _launch(vx, vy) {
    this.shotCount++;
    if (this.shotCount >= 6) this.redirectOnImpact = true;
    this.proj = {
      x: this.slingshotX, y: this.slingshotY,
      vx, vy, owner: 'player', age: 0
    };
    this.trail = [];
    this.state = 'flying';
    this.charUsed[this.selectedIdx] = true;
    this._updateCards();
    // pick next unused char
    const next = this.charUsed.findIndex(u => !u);
    if (next >= 0) this.selectedIdx = next;
  }

  /* ---- hit handling ---- */
  _onPlayerHit(p) {
    const char = GAME_CONFIG.characters[this.selectedIdx >= 0 ? this.selectedIdx : 0];
    const dmg = char ? char.damage : 25;
    this.enemyHp -= dmg;
    if (this.enemyHp < 0) this.enemyHp = 0;
    this.enemyDmgState = Math.floor((1 - this.enemyHp / this.enemyHpMax) * 4);
    this.enemyTilt = (Math.random()-0.5) * 6;
    this._spawnImpact(p.x, p.y, char ? char.trailColor : 'orange');
    this._spawnDmgNum(p.x, p.y, '-' + dmg, '#e74c3c');
    this.shakeAmt = 6;
    this.proj = null; this.trail = [];
    this._updateHPBars();
    if (this.redirectOnImpact) {
      setTimeout(() => this.vsdk.redirectToInstallPage(), 300); return;
    }
    if (this.enemyHp <= 0) {
      this.gameEnded = true;
      if (this.level === 1) {
        setTimeout(() => this._loadLevel2(), 550);
      } else {
        setTimeout(() => this.vsdk.winGame(), 550);
      }
    } else {
      setTimeout(() => this._startEnemyTurn(), 450);
    }
  }

  _onEnemyHit(p) {
    const baseDmg = GAME_CONFIG.enemyChar.damage;
    const dmg = Math.round(baseDmg * this._enemyDmgMult);
    this.playerHp -= dmg;
    if (this.playerHp < 0) this.playerHp = 0;
    this.playerDmgState = Math.floor((1 - this.playerHp / this.playerHpMax) * 4);
    this.playerTilt = (Math.random()-0.5) * 6;
    this._spawnImpact(p.x, p.y, GAME_CONFIG.enemyChar.trailColor);
    this._spawnDmgNum(p.x, p.y, '-' + dmg, '#e67e22');
    this.shakeAmt = 5;
    this.proj = null; this.trail = [];
    this._updateHPBars();
    if (this.playerHp <= 0) {
      this.gameEnded = true;
      setTimeout(() => this.vsdk.loseGame(), 550);
    } else {
      setTimeout(() => this._returnToPlayer(), 450);
    }
  }

  _afterPlayerMiss() {
    setTimeout(() => this._startEnemyTurn(), 300);
  }

  _startEnemyTurn() {
    if (this.gameEnded) return;
    this.state = 'enemy_turn';
    setTimeout(() => this._fireEnemy(), GAME_CONFIG.enemy.turnDelay);
  }

  _fireEnemy() {
    if (this.gameEnded) return;
    const sx = this.eCX, sy = this.eCY - this.castleH * 0.7;
    const targetX = this.pCX, targetY = this.pCY - this.castleH * 0.5;
    const dx = targetX - sx, dy = targetY - sy;
    const dist = Math.hypot(dx, dy);
    const speed = GAME_CONFIG.physics.projectileSpeed * 0.9;
    // simple trajectory aim
    const t = dist / speed * 1.2;
    const vxIdeal = dx / t;
    const vyIdeal = (dy - 0.5 * GAME_CONFIG.physics.gravity * t * t) / t;
    const variance = this._aimVariance;
    const vx = vxIdeal + (Math.random()-0.5) * speed * variance;
    const vy = vyIdeal + (Math.random()-0.5) * speed * variance;
    this.proj = { x: sx, y: sy, vx, vy, owner: 'enemy', age: 0 };
    this.trail = [];
    this.state = 'flying';
  }

  _returnToPlayer() {
    if (this.gameEnded) return;
    this.state = 'playing';
  }

  /* ---- level 2 ---- */
  _loadLevel2() {
    if (this.transitioning) return;
    this.transitioning = true;
    this.gameEnded = false;
    this.shotCount = 0; this.redirectOnImpact = false; this.level = 2;
    const hd = GAME_CONFIG.difficulty.hard;
    this.enemyHp = hd.enemyHp; this.enemyHpMax = hd.enemyHp;
    this._aimVariance = hd.aimVariance; this._enemyDmgMult = hd.enemyDmgMult;
    this.enemyDmgState = 0; this.enemyTilt = 0;
    this.particles = []; this.dmgNumbers = [];
    this.charUsed = [false,false,false]; this.selectedIdx = 0;
    this._showLevel2Screen();
    setTimeout(() => {
      this._hideLevel2Screen();
      const badge = document.getElementById('level-badge');
      if (badge) badge.textContent = 'Level 2  ★';
      this._updateHPBars(); this._updateCards();
      this.transitioning = false; this.state = 'playing';
    }, 1500);
  }

  _showLevel2Screen() {
    const s = document.getElementById('lvl2-screen');
    if (s) s.classList.add('show');
  }
  _hideLevel2Screen() {
    const s = document.getElementById('lvl2-screen');
    if (s) s.classList.remove('show');
  }

  /* ---- particles ---- */
  _spawnImpact(x, y, color) {
    const count = 18;
    for (let i = 0; i < count; i++) {
      const angle = (Math.PI * 2 * i) / count + Math.random() * 0.4;
      const speed = 2 + Math.random() * 5;
      this.particles.push({
        x, y,
        vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed - 2,
        color, r: 2 + Math.random() * 3,
        life: 30 + Math.random() * 20, maxLife: 50
      });
    }
    // flash
    this.particles.push({ x, y, vx:0, vy:0, color:'#fff', r:18, life:6, maxLife:6 });
  }

  _spawnDmgNum(x, y, text, color) {
    this.dmgNumbers.push({
      x, y, text, color, life: 50, maxLife: 50, size: 18 + Math.random() * 6
    });
  }

  /* ---- UI updates ---- */
  _updateHPBars() {
    const pf = document.getElementById('hp-player-fill');
    const ef = document.getElementById('hp-enemy-fill');
    if (pf) pf.style.width = Math.max(0, this.playerHp / this.playerHpMax * 100) + '%';
    if (ef) ef.style.width = Math.max(0, this.enemyHp  / this.enemyHpMax * 100) + '%';
  }

  _selectChar(idx) {
    this.selectedIdx = idx;
    document.querySelectorAll('.char-card').forEach((el, i) => {
      el.classList.toggle('selected', i === idx);
    });
  }

  _updateCards() {
    document.querySelectorAll('.char-card').forEach((el, i) => {
      el.classList.toggle('used', this.charUsed[i]);
      el.classList.toggle('selected', i === this.selectedIdx && !this.charUsed[i]);
    });
  }
}

/* =====================================================================
   ENTRY POINT
   ===================================================================== */
const playable = {
  default: ({ vsdk }) => new PlayableGame({ vsdk })
};

window.addEventListener('load', () => {
  const runtime = new MiniVSDKRuntime(config);
  runtime.init({ playableFactory: playable.default });
});
</script>
</body>
</html>
"""

# Inject store URLs
html = html.replace('STORE_URL', STORE)

# Inject assets
html = html.replace("'BG_SRC'",      f"'{bg}'"   if bg   else "''")
html = html.replace("'BCASTLE_SRC'", f"'{bCas}'" if bCas else "''")
html = html.replace("'RCASTLE_SRC'", f"'{rCas}'" if rCas else "''")
html = html.replace("'P1_SRC'",      f"'{p1}'"   if p1   else "''")
html = html.replace("'P2_SRC'",      f"'{p2}'"   if p2   else "''")
html = html.replace("'W1_SRC'",      f"'{w1}'"   if w1   else "''")
html = html.replace("'W2_SRC'",      f"'{w2}'"   if w2   else "''")

pathlib.Path("generated-playable.html").write_text(html, encoding='utf-8')
print("Done ->", pathlib.Path("generated-playable.html").stat().st_size, "bytes")
