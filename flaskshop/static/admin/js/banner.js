var time;
var num = $('#banner li').length;
var b_num = 1;

//初始设置显示第一张轮播图
$('#banner li').eq(0).show();
//轮播图自动切换
function bannerMove() {
    time = setInterval(function () {
        //轮播图淡入淡出
        $('#banner li').eq(b_num % num).fadeIn(500).siblings('li').fadeOut(200);
        b_num++;
    }, 3000)
};
bannerMove();//开始自动轮播

//鼠标移入图片和左右按钮时停止自动播放
$('#banner li,#banner .right,#banner .left').mouseover(function () {
    clearInterval(time)
});

//鼠标移出图片和左右按钮时开始自动播放
$('#banner li,#banner .right,#banner .left').mouseout(function () {
    bannerMove()
});

//点击右键切换图片
$('#banner .right').click(function () {
    $('#banner li').eq(b_num % num).fadeIn(500).siblings('li').fadeOut(200);
    b_num++;
})
//点击左键切换图片
$('#banner .left').click(function () {
    if (b_num % num == 0) {
        b_num = 3;
    }
    $('#banner li').eq(b_num - 2 % num).fadeIn(500).siblings('li').fadeOut(200);
    b_num--;
});