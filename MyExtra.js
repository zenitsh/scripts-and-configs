
//
//Class: MyExtra
//
//

function MyExtra()
{
    this.initialize.apply(this,arguments);
}

MyExtra.prototype.initialize = function(){
    //alert("MyExtra.prototype.initialize");
    this.bHasPressed = false;
    this.bF = true;
    this.Pi = 3.14;
};

MyExtra.countDistance = function(a,b)
{
    var dx=a.x+a.width/2-b.x-b.width/2;
    var dy=a.y+a.height/2-b.y-b.height/2;
    return dx*dx+dy*dy;
};

var myextra = new MyExtra();

//
//Class: Scene_Danmaku
//
//

function Scene_Danmaku()
{
    //alert("Scene_Danmaku");
    this.initialize.apply(this,arguments);
}

Scene_Danmaku.prototype = Object.create(Scene_Base.prototype);
Scene_Danmaku.prototype.constructor = Scene_Danmaku;

Scene_Danmaku.prototype.initialize = function(){
    //alert("Scene_Danmaku.prototype.initialize");
    this._bossSprite = null;
    this._enemySprite = [];
    this._playerSprite = null;
    this._sign = 1;
    this._todo = 'none';
    this._t = 0;
    Scene_Base.prototype.initialize.call(this);
};

Scene_Danmaku.prototype.create = function()
{
    //alert("Scene_Danmaku.prototype.create");
    Scene_Base.prototype.create.call(this);
    this.createDisplayObjects();
};

Scene_Danmaku.prototype.start = function()
{
    //alert("Scene_Danmaku.prototype.start");
    Scene_Base.prototype.start.call(this);
    this._remainingTime=60;
};

Scene_Danmaku.prototype.update = function()
{
    var active = this.isActive();
    $gameTimer.update(active);
    $gameScreen.update();
    if(active && !this.isBusy())
    {
        this.updateProcess();
    }
    Scene_Base.prototype.update.call(this);
    if(this._todo=='die')
    {
        SceneManager.pop();
        SceneManager.goto(Scene_Gameover);
    }
    else if(this._todo=='win')
    {
        SceneManager.pop();
    }
};

Scene_Danmaku.prototype.stop = function()
{
    this._active = false;
};

Scene_Danmaku.prototype.isBusy = function()
{
    return Scene_Base.prototype.isBusy();
};

Scene_Danmaku.prototype.terminate = function()
{
    this.removeChild(this._bossSprite);
    this.removeChild(this._playerSprite);
    for(i in this._enemySprite)
    {
        delete this._enemySprite[i];
    }
}

Scene_Danmaku.prototype.createDisplayObjects = function()
{
    this._bossSprite = new Sprite(ImageManager.loadFace("t"));
    this.addChild(this._bossSprite);
    this._playerSprite = new Sprite(ImageManager.loadFace("m"));
    this.addChild(this._playerSprite);
    this._playerSprite.x=500;
    this._playerSprite.y=500;
    var rightWindowBitmap = new Bitmap(300,600);
    rightWindowBitmap.fillRect(0,0,300,600,"#ff6666");
    this._rightWindowSprite = new Sprite(rightWindowBitmap);
    this._rightWindowSprite.x=650;
    this.addChild(this._rightWindowSprite);
};

Scene_Danmaku.prototype.updateProcess = function()
{
    this._rightWindowSprite.bitmap.fillRect(0,0,300,600,"#ff6666");
    this._rightWindowSprite.bitmap.drawText("Time:%1".format(this._remainingTime),0,0,300,30,'left');
    this._bossSprite.x+=13*this._sign;
    if(this._t%75==0)
    {
        this._remainingTime--;
    }
    if(this._remainingTime==0)
    {
        this._todo='win';
    }
    if(this._bossSprite.x>600)
    {
        this._sign=-1;
    }
    else if(this._bossSprite.x<0)
    {
        this._sign=1;
    }
    for(var i in this._enemySprite)
    {
        var en=this._enemySprite[i];
        en.y+=2+Math.random()*3;
        en.x+=Math.random()*2*(2*(i%2)-1)*(2*(en.y>300)-1);
        if(MyExtra.countDistance(en,this._playerSprite) < (en.width/2 + this._playerSprite.width/2)*(en.width/2 + this._playerSprite.width/2))
        {
            this._todo = 'die';
        }
    }
    this._t++;
    if(this._t%(Math.floor(this._remainingTime/5)+5)==0)
    {
        var enemy = new Sprite(ImageManager.loadFace("t"));
        enemy.x=this._bossSprite.x;
        this.addChild(enemy);
        this._enemySprite.push(enemy);
    }
    if(Input.isPressed('left'))
    {
        if(this._playerSprite.x>5)
            this._playerSprite.x-=5;
    }
    if(Input.isPressed('right'))
    {
        if(this._playerSprite.x<595)
            this._playerSprite.x+=5;
    }
    if(Input.isPressed('up'))
    {
        if(this._playerSprite.y>5)
            this._playerSprite.y-=5;
    }
    if(Input.isPressed('down'))
    {
        if(this._playerSprite.y<600)
            this._playerSprite.y+=5;
    }
};

