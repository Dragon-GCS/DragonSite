$(function(){
    //返回上一级
    $("#back-button").click(function () {
        location.href = $("#goback").text()
    })
    // 新建文件夹
    $("#create").click(function () {
        $("#folder_input").show();
        $("#folder_name").focus()
    })
    $("#cancel-create").click(function () {
        $("#folder_input").hide();
    })

    $("#create-button").click(function () {
        if($("#folder_name").val()){
            $("#create-form").submit();
        }
        else {
            alert("请输入文件名")
        }
    })

    // 文件上传
    $("#upload").click(function(){
        $("#file_upload").click();
    })
     $("#file_upload").change(function(){
        $("#upload_form").submit();
    })
    // 文件与文件夹选项
    $('.folder-detail').mouseenter(function(){
        $(this).find(".hidden-option").show();
    });
    $(".folder-detail").mouseleave(function(){
        $(this).find(".hidden-option").hide();
    });
    // 重命名
    $(".rename-button").click(function(){
        $(this).parent().siblings(".rename-form").show();
        $(this).parent().siblings(".rename-form").find(":text").focus();
        $(this).parent().hide();
        $(this).parent().siblings("a").children(".name").hide()
    });

    $(".rename-form :button").click(function(){
        $(this).parent().siblings(".name").show();
        $(this).parent().siblings(".hidden-option").show();
        $(this).parent().hide();
    });

     $(".rename-form").mouseleave(function () {
        $(this).find(":button").click();
        $(this).siblings("a").children(".name").show()
     })
    // 文件删除确认
    $(".del-button").click(function(){
    var url = $(this).siblings(".del-url").text();
    if (confirm("确定要删除吗？")){
        location.href = url;
        }
    })
    /* 可以从服务器读取字节流
    $(function () {
        var img = $(".image-icon")
        var url = img.attr('src')
        var xmlhttp = new XMLHttpRequest()
            xmlhttp.open("GET",url,true);
            xmlhttp.responseType = "blob";
            xmlhttp.onload = function(){
                if (this.status == 200) {
                    var blob = this.response;
                    //var img = document.createElement("img");
                    img.onload = function(e) {
                        window.URL.revokeObjectURL(img.attr("src"));
                    };
                    img.attr("src", window.URL.createObjectURL(blob));
                }
            }
    })*/

})
