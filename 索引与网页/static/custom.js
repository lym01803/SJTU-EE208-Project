var p_class = -1;
var c_class = -1;

function submitt() {
    $("#subb").click();
}

function rearrange(){
    $("div").remove(".temp");
    if (p_class == -1 && c_class == -1){
        for (j=0;j<7;++j)
            $(".p-"+(j)).css("display", "block");
        return;
    }
    var str = "";
    if (p_class != -1)
        str += ".p-"+p_class;
    if (c_class != -1)
        str += ".c-"+c_class;
    var tmp;
    var x = 0;
    var tgs = $(str);
    for (j=0;j<7;++j)
        $(".p-"+(j)).css("display", "none");
    for (j=0;j<tgs.length;++j)
    {
        tmp = tgs[j].cloneNode(true);
        tmp.setAttribute("class", "temp");
        tmp.setAttribute("style", "padding:20px 5px;height:570px;border:5px solid #bac;border-radius:30px;display:block;");
        document.getElementById("col-"+(((x++)%3))).appendChild(tmp);
    }
}

function select_price(i){
    $("#p-"+p_class).removeClass("activeLi");
    p_class = i;
    $("#p-"+i).addClass("activeLi");
    rearrange();
    return;
}

function select_class(i){
    $("#c-"+c_class).removeClass("activeLi");
    c_class = i;
    $("#c-"+i).addClass("activeLi");
    rearrange();
    return;
}

$(function () {
    $("#back-top").hide();
    $(window).scroll(function () {
        if ($(this).scrollTop() > 500) {
            $('#back-top').fadeIn();
        } else {
            $('#back-top').fadeOut();
        }
    });
        $('body,html').animate({
            scrollTop: 0
        }, 800);
        return false;
    });


$(document).ready(function(){
	$('ul.dropdown').superfish({
		autoArrows: true,
		animation: {height:'show'}
	});
});


