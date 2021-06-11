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
    // 文件夹名称验证
    $("#create-button").click(function () {
        var folder_name = $("#folder_name").val()
        if (folder_name === ""){
            alert("请输入文件名")
        }
        else {
             if(! space_detect(folder_name)){
                $("#create-form").submit();
                }
            else {
                alert("文件夹名称不能包含空格，请重新输入。")
            }
        }
    })
    // 文件上传
    $("#upload").click(function(){
        $("#file_upload").click();
    })
     $("#file_upload").change(function(){
         var submit = true;
         var files = document.getElementById("file_upload").files;
         for(i=0,len=files.length;i<len;i++){
             var name = files[i].name
                 if(space_detect(name)){
                 alert(name+" 文件名中包含空格，无法提交。");
                 return false
                 }
            }
         $("#upload_form").submit();
     })
    // 文件与文件夹选项
    $('.folder-detail').mouseenter(function(){
        $(this).find(".hidden-option").show();
    });
    $(".folder-detail").mouseleave(function(){
        $(this).find(".hidden-option").hide();
    });
    // 点击重命名按钮
    $(".rename-button").click(function(){
        var input_form = $(this).parent().siblings(".rename-form");
        var item_name = $(this).parent().siblings("a.name").children(".item-name");
        input_form.show();
        input_form.children(":text").attr("placeholder",item_name.text())
        input_form.children(":text").focus();
        $(this).parent().hide();
    });
    // 重命名提交确认
    $(".rename-form :submit").click(function () {
        var new_name = $(this).siblings("input[name='new_name']").val()
        var name = $(this).parent().siblings("a.name").children(".item-name").text()
        console.log(name)
        if(space_detect(new_name)){
            alert("名称中不能含有空格");
            return false;
        }
        if(new_name===get_prefix(name)){
            alert("请输入新的文件名");
            return false;
        }
    })
    // 取消重命名
    $(".rename-form :button").click(function(){
        $(this).parent().hide();
        $(this).parent().siblings(".name").children(".item-name").show();
        $(this).parent().siblings(".hidden-option").show();
    });
    // 鼠标移出取消重命名
     $(".rename-form").mouseleave(function () {
        $(this).find(":button").click();
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

function space_detect(text,target=" ") {
    if(text.indexOf(target) !== -1){
        return true
    }
}

function get_prefix(filename) {
    var prefix = filename;
    if(space_detect(filename,".")){
        prefix = filename.substring(0, filename.lastIndexOf("."));
    }
    return prefix
}