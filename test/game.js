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
let collectedBoosts = 0;

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
        frameRate: 60,
        repeat: -1
    });

    this.background = this.add.sprite(400, 450, 'background');
    this.background.play('background_anim');

    // Adicionando HUD para pontuação
    scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '32px', fill: '#fff' });

    player = this.physics.add.sprite(300, 100, 'player');
    player.setCollideWorldBounds(true);
  
    slowObstacles = this.physics.add.group({
        key: 'slow_obstacle',
        repeat: 2, // Reduzindo o número de obstáculos
        setXY: { x: 300, y: -100 }, // Começando no centro do topo
    });
    
    boosts = this.physics.add.group({
        key: 'boost',
        repeat: 2,
        setXY: { x: 300, y: -100 },
    });

    gameOverObstacles = this.physics.add.group();

    cursors = this.input.keyboard.createCursorKeys();

    this.physics.add.overlap(player, slowObstacles, hitSlowObstacle, null, this);
    this.physics.add.overlap(player, boosts, collectBoost, null, this);
    this.physics.add.overlap(player, gameOverObstacles, hitGameOverObstacle, null, this);

    // Diminuindo a velocidade inicial
slowObstacles.children.iterate(function (child) {
    child.setVelocityY(3); // Ajuste a velocidade conforme necessário
});

boosts.children.iterate(function (child) {
    child.setVelocityY(5); // Ajuste a velocidade conforme necessário
});

    // Criar novos obstáculos de game over em intervalos regulares
    this.time.addEvent({
        delay: 2000,
        callback: createGameOverObstacle,
        callbackScope: this,
        loop: true
    });

        // Temporizador para aumentar a velocidade a cada 20 segundos
        this.time.addEvent({
            delay: 20000, // 20 segundos
            callback: increaseVelocity,
            callbackScope: this,
            loop: true
        });
}

function update() {
    if (cursors.left.isDown) {
        if (boostActive) {
            player.setVelocityX(-400); // Velocidade aumentada quando o boost está ativo
        } else {
            player.setVelocityX(-160); // Velocidade normal
        }
    } else if (cursors.right.isDown) {
        if (boostActive) {
            player.setVelocityX(400); // Velocidade aumentada quando o boost está ativo
        } else {
            player.setVelocityX(160); // Velocidade normal
        }
    } else {
        player.setVelocityX(0); // Quando nenhuma tecla de movimento é pressionada
    }



    Phaser.Actions.IncY(slowObstacles.getChildren(), 5);
    Phaser.Actions.IncY(boosts.getChildren(), 7);
    Phaser.Actions.IncY(gameOverObstacles.getChildren(), 10);

    slowObstacles.children.iterate(function (child) {
        if (child.y > 700) {
            child.y = 0;
            child.x = Phaser.Math.Between(50, 550);
        }
        child.setScale(0.1); // Ajuste a escala inicial conforme necessário
        child.setVelocityY(3); // Ajuste a velocidade conforme necessário
        child.setDisplaySize(100, 100); // Ajuste o tamanho inicial do sprite
        // Lógica para aumentar gradualmente o tamanho
        this.tweens.add({
            targets: child,
            scaleX: 1, // Escala final
            scaleY: 1, // Escala final
            duration: 1000, // Tempo para alcançar a escala final
        });
    }, this);

    boosts.children.iterate(function (child) {
        if (child.y > 700) {
            child.y = 0;
            child.x = Phaser.Math.Between(50, 550);
        }
        child.setScale(0.1); // Ajuste a escala inicial conforme necessário
        child.setVelocityY(3); // Ajuste a velocidade conforme necessário
        child.setDisplaySize(100, 100); // Ajuste o tamanho inicial do sprite
        // Lógica para aumentar gradualmente o tamanho
        this.tweens.add({
            targets: child,
            scaleX: 1, // Escala final
            scaleY: 1, // Escala final
            duration: 1000, // Tempo para alcançar a escala final
        });
    }, this);

    gameOverObstacles.children.iterate(function (child) {
        if (child.y > 700) {
            child.y = 0;
            child.x = Phaser.Math.Between(50, 550);
        }
        child.setScale(0.1); // Ajuste a escala inicial conforme necessário
        child.setVelocityY(3); // Ajuste a velocidade conforme necessário
        child.setDisplaySize(100, 100); // Ajuste o tamanho inicial do sprite
        // Lógica para aumentar gradualmente o tamanho
        this.tweens.add({
            targets: child,
            scaleX: 1, // Escala final
            scaleY: 1, // Escala final
            duration: 1000, // Tempo para alcançar a escala final
        });
    }, this);

    // Atualizando a pontuação
    score += 1;
    scoreText.setText('Score: ' + score);
}

function hitSlowObstacle(player, obstacle) {
    obstacle.disableBody(true, true);
    console.log("Colidiu com obstáculo de lentificação! Diminuindo velocidade.");
    player.setVelocityY(100);
    this.time.delayedCall(2000, () => {
        player.setVelocityY(0);
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

function createGameOverObstacle() {
    if (gameOverObstacles.countActive(true) < 3) {
        const xPosition = Phaser.Math.Between(50, 550);
        const obstacleTypes = ['game_over_obstacle1', 'game_over_obstacle2', 'game_over_obstacle3', 'game_over_obstacle4'];
        const selectedObstacle = Phaser.Utils.Array.GetRandom(obstacleTypes);

        const obstacle = gameOverObstacles.create(xPosition, -100, selectedObstacle);
        obstacle.setVelocityY(200);
    }
}

function increaseVelocity() {
    // Aumentar a velocidade de todos os grupos de obstáculos
    slowObstacles.children.iterate(function (child) {
        child.setVelocityY(child.body.velocity.y * velocityIncrease);
    });

    boosts.children.iterate(function (child) {
        child.setVelocityY(child.body.velocity.y * velocityIncrease);
    });

    gameOverObstacles.children.iterate(function (child) {
        child.setVelocityY(child.body.velocity.y * velocityIncrease);
    });

    // Ajustar a velocidade inicial para os próximos obstáculos gerados
    initialObstacleVelocity *= velocityIncrease;
}