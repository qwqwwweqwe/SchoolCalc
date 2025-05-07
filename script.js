const canvas = document.getElementById("game_canvas_sunrise");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();

const particles = [];
const mouse = { x: null, y: null };

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 5 + 2;
        this.speedX = Math.random() * 2 - 1;
        this.speedY = Math.random() * 2 - 1;
        this.baseSize = this.size;
        this.baseColor = "rgba(139, 0, 0, 0.6)";
    }

    update() {
        let dx = mouse.x - this.x;
        let dy = mouse.y - this.y;
        let distance = Math.sqrt(dx * dx + dy * dy);
        let attraction = distance < 100 ? (100 - distance) / 100 : 0;

        this.x += this.speedX + dx / distance * attraction * 2;
        this.y += this.speedY + dy / distance * attraction * 2;

        if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
        if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;

        this.size = distance < 50 ? this.baseSize * 1.3 : this.baseSize;
        this.color = distance < 50 ? "rgba(255, 64, 64, 0.8)" : this.baseColor;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

function init() {
    for (let i = 0; i < 75; i++) {
        particles.push(new Particle());
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });
    requestAnimationFrame(animate);
}

window.addEventListener("mousemove", e => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

window.addEventListener("mouseout", () => {
    mouse.x = null;
    mouse.y = null;
});

const featureItems = document.querySelectorAll(".features-item");
featureItems.forEach(item => {
    item.addEventListener("mouseenter", () => {
        let glow = document.createElement("div");
        glow.className = "features-item-glow";
        item.appendChild(glow);
        setTimeout(() => glow.remove(), 1200);
    });
});


init();
animate();