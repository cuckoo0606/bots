/*
 * fileupload
 * Copyright (c) 2013 lixingtie
 * date: 2013-08-04
 * 美化bootstrap的fileupload控件样式
 */
(function($){
    $.fn.fileupload = function(options){
        var defaults = {
            text : "选择",
            value : ""
        }
        var options = $.extend(defaults, options);
        this.each(function(){
            var fileupload = $(this);
            var fileupload_display = fileupload.next()
            if(fileupload_display.hasClass("fileupload-display"))
                fileupload_display.remove()

            fileupload.addClass("hide");
            
            var cls = fileupload.attr("class");
            cls = cls.replace("fileupload", "");
            cls = cls.replace("hide", "");
            
            var style = fileupload.attr("style");
            
            var display = "<div class='input-group fileupload-display " + cls + "' style='" + style + "'>";
            display += "       <input type='text' class='form-control' style='background-color:white;color:black;' disabled />";
            display += "       <span class='input-group-btn'>";
            display += "           <a href='#' class='btn btn-default'>" + options.text + "</a>";
            display += "       </span>";
            display += "   </div>";
            
            fileupload.after(display);
            
            var input = $("input", fileupload.next());
            input.val(options.value);
            fileupload.on("change", function(e){
                var file = e.target.files !== undefined ? e.target.files[0] : (e.target.value ? { name: e.target.value.replace(/^.+\\/, '') } : null)
                input.val(file.name);
            });
            
            var a = $("a", fileupload.next());
            a.on("click", function(){
                fileupload.click();
            });
        });
    };
})(jQuery);
