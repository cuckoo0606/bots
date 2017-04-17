$(function(){
    $(".tab-pane ul div a li").mouseover(function(){
        $(this).css("background-color","#ddd");
    });
    $(".tab-pane ul div a li").mouseout(function(){
        $(this).css("background-color","#fff");
    });
    $(".tab-pane ul div a li").click(function(){
        var val = $(this).css("border");
        if("val == 1px solid rgb(221, 221, 221)"){
            $(".tab-pane ul div a li").css({ "border":"1px solid #ddd" });
            $(this).css({ "border":"1px solid #f63" });
            $("button").removeClass("disabled" )
        }
    });
})

