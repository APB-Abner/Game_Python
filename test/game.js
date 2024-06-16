const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

let player;
let slowObstacles;
let gameOverObstacles;
let boosts;
let cursors;
let boostActive = false;
let boostTimer = 0;
let score = 0;
let scoreText;
let initialObstacleVelocity = 3; // Velocidade inicial dos obstáculos
let velocityIncrease = 1.15
let boostBar;
let padsCollected = 0;

function preload() {
    this.load.spritesheet('background', 'img/sprit_road-0.png', {
        frameWidth: 600,
        frameHeight: 700
        
    });
    this.load.image('player', 'img/car.png'); // Substitua pelo caminho da imagem do carro
    this.load.image('slow_obstacle', 'img/slow_pad.png'); // Substitua pelo caminho da imagem do obstáculo que lentifica
    this.load.image('boost', 'img/pad.png'); // Substitua pelo caminho da imagem do boost

    // Carregando diferentes imagens para obstáculos de game over
    this.load.image('game_over_obstacle1', 'img/obstacle.png');
    this.load.image('game_over_obstacle2', 'img/obstacle1.png');
    this.load.image('game_over_obstacle3', 'img/obstacle2.png');
    this.load.image('game_over_obstacle4', 'img/obstacle3.png');
}

function create() {
    // Adicionando a animação de fundo
    this.anims.create({
        key: 'background_anim',
        frames: this.anims.generateFrameNumbers('background', { start: 1, end: 64 }),
        frameRate: 10,
        repeat: -1
    });

    this.background = this.add.sprite(400, 450, 'background');
    this.background.play('background_anim');

    // Adicionando HUD para pontuação
    scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '32px', fill: '#fff' });

    // Adicionando a barra de boost
    boostBar = this.add.graphics();
    updateBoostBar();

    player = this.physics.add.sprite(400, 500, 'player');
    player.setCollideWorldBounds(true);

    slowObstacles = this.physics.add.group({
        key: 'slow_obstacle',
        repeat: 2,
        setXY: { x: 300, y: -100 }
    });

    boosts = this.physics.add.group({
        key: 'boost',
        repeat: 2,
        setXY: { x: 300, y: -100 }
    });

    gameOverObstacles = this.physics.add.group();

    cursors = this.input.keyboard.createCursorKeys();

    this.physics.add.overlap(player, slowObstacles, hitSlowObstacle, null, this);
    this.physics.add.overlap(player, boosts, collectBoost, null, this);
    this.physics.add.overlap(player, gameOverObstacles, hitGameOverObstacle, null, this);

    slowObstacles.children.iterate(function (child) {
        child.setVelocityY(3);
    });

    boosts.children.iterate(function (child) {
        child.setVelocityY(5);
    });

    this.time.addEvent({
        delay: 2000,
        callback: createGameOverObstacle,
        callbackScope: this,
        loop: true
    });

    this.time.addEvent({
        delay: 20000,
        callback: increaseVelocity,
        callbackScope: this,
        loop: true
    });

    this.input.keyboard.on('keydown_ESC', function (event) {
        pauseMenu(this);
    }, this);
}

function updateBoostBar() {
    boostBar.clear();
    boostBar.fillStyle(0x000000);
    boostBar.fillRect(10, 100, 200, 20);

    const progress = Phaser.Math.Clamp(padsCollected / 3, 0, 1);
    boostBar.fillStyle(0x00ff00);
    boostBar.fillRect(10, 100, 200 * progress, 20);

    boostBar.lineStyle(2, 0xffffff);
    boostBar.strokeRect(10, 100, 200, 20);
}

function update() {
    if (cursors.left.isDown) {
        player.setVelocityX(boostActive ? -400 : -160);
    } else if (cursors.right.isDown) {
        player.setVelocityX(boostActive ? 400 : 160);
    } else {
        player.setVelocityX(0);
    }

    Phaser.Actions.IncY(slowObstacles.getChildren(), 5);
    Phaser.Actions.IncY(boosts.getChildren(), 7);
    Phaser.Actions.IncY(gameOverObstacles.getChildren(), 10);

    slowObstacles.children.iterate(function (child) {
        if (child.y > 700) {
            child.y = 0;
            child.x = Phaser.Math.Between(50, 550);
        }
    });

    boosts.children.iterate(function (child) {
        if (child.y > 700) {
            child.y = 0;
            child.x = Phaser.Math.Between(50, 550);
        }
    });

    gameOverObstacles.children.iterate(function (child) {
        if (child.y > 700) {
            child.destroy(); // Destroi o obstáculo quando ele sai da tela
        }
    });

    // Atualizando a pontuação
    score += 1;
    scoreText.setText('Score: ' + score);
}

function collectedBoosts(player, boost) {
    boost.disableBody(true, true);
    padsCollected += 1;
    updateBoostBar();
    console.log("Pegou um boost! Boosts coletados: " + padsCollected);

    if (padsCollected >= 3 && !boostActive) {
        boostActive = true;
        boostTimer = this.time.now;
        padsCollected = 0; // Reinicia a contagem de boosts coletados
    }
}

function hitSlowObstacle(player, obstacle) {
    obstacle.disableBody(true, true);
    console.log("Colidiu com obstáculo de lentificação! Diminuindo velocidade.");
    player.setVelocityX(player.body.velocity.x / 2); // Diminui a velocidade na horizontal
    this.time.delayedCall(2000, () => {
        player.setVelocityX(0); // Para o movimento após o efeito de lentificação
    });
}

function createGameOverObstacle() {
    if (gameOverObstacles.countActive(true) < 5) {
        const xPosition = Phaser.Math.Between(50, 550);
        const obstacleTypes = ['game_over_obstacle1', 'game_over_obstacle2', 'game_over_obstacle3', 'game_over_obstacle4'];
        const selectedObstacle = Phaser.Utils.Array.GetRandom(obstacleTypes);

        const obstacle = gameOverObstacles.create(xPosition, 0, selectedObstacle);
        obstacle.setVelocityY(3);
    }
}

function increaseVelocity() {
    slowObstacles.children.iterate(function (child) {
        child.setVelocityY(child.body.velocity.y * 1.15);
    });

    boosts.children.iterate(function (child) {
        child.setVelocityY(child.body.velocity.y * 1.15);
    });

    gameOverObstacles.children.iterate(function (child) {
        child.setVelocityY(child.body.velocity.y * 1.15);
    });
}

function hitGameOverObstacle(player, obstacle) {
    console.log("Colidiu com obstáculo de game over! Fim de jogo.");
    this.physics.pause();
    player.setTint(0xff0000);
    // Adicionar uma tela de game over ou reiniciar o jogo aqui
}

function collectBoost(player, boost) {
    boost.disableBody(true, true);
    console.log("Pegou um boost! Aumentando velocidade.");
    collectedBoosts++;

    if (collectedBoosts >= 3) {
        boostActive = true;
        boostTimer = this.time.now;
        collectedBoosts = 0; // Reinicia o contador de boosts após ativar o boost
    }
}

function displayText(scene, text, fontSize, color, x, y) {
    const style = { fontSize: fontSize + 'px', fill: color };
    scene.add.text(x, y, text, style);
}

function drawButton(scene, text, x, y, width, height, color, textColor, action) {
    const button = scene.add.rectangle(x, y, width, height, color).setInteractive();
    const buttonText = scene.add.text(x, y, text, { fontSize: '32px', fill: textColor }).setOrigin(0.5);

    button.on('pointerdown', action);
    button.on('pointerover', () => {
        button.setFillStyle(0x888888); // Cor quando o mouse passa por cima
    });
    button.on('pointerout', () => {
        button.setFillStyle(color); // Cor normal
    });

    return button;
}

function pauseMenu(scene) {
    scene.physics.pause(); // Pausa a física do jogo

    const resumeButton = drawButton(scene, 'Continuar', scene.cameras.main.centerX, scene.cameras.main.centerY - 60, 250, 50, 0x000000, '#ffffff', () => {
        scene.physics.resume();
        resumeButton.destroy();
        optionsButton.destroy();
        quitButton.destroy();
    });

    const optionsButton = drawButton(scene, 'Opções', scene.cameras.main.centerX, scene.cameras.main.centerY, 250, 50, 0x000000, '#ffffff', () => {
        // Implementar a lógica do menu de opções
    });

    const quitButton = drawButton(scene, 'Sair', scene.cameras.main.centerX, scene.cameras.main.centerY + 60, 250, 50, 0x000000, '#ffffff', () => {
        scene.game.destroy(true); // Fecha o jogo
    });
}