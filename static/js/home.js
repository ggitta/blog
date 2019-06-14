 function addrss() {
        $("#rsstip").hide()
        email = $("#rssinp").val()
        var regEmail = /^[a-zA-Z\d]+([-_\.][a-zA-Z\d]+)*@[a-zA-Z\d]+\.[a-zA-Z\d]{2,4}$/;
        if (regEmail.test(email)) {
            $.post("/addrss", {email: email}, function (result) {
                result = eval("(" + result + ")")
                $("#rssinp").val("")
                $("#rsstip").html(result.msg)
                $("#rsstip").show()
                autohide = window.setTimeout(function () {
                    $("#rsstip").hide()
                }, 3000);
            })
        } else {
            $("#rssinp").val("")
            $("#rsstip").html("邮箱格式不正确")
            $("#rsstip").show()
            autohide = window.setTimeout(function () {
                $("#rsstip").hide()
            }, 3000);
        }

    }

    function getips() {
        $.post("/getips", null, function (result) {
                result = eval("(" + result + ")")
                console.log("---以下为IP↓---")
                console.log(result)
                console.log("---以上为IP↑---")
                $("#msgmodal").modal()
            })
    }
    
    var verifyCode = new GVerify("v_container");
    document.getElementById("my_button").onclick = function () {
        var res = verifyCode.validate(document.getElementById("code_input").value);
        if (res) {
            c4_base = 200 + 58 + 326 + 360 + 320 + 38 + 2
            c4 = c4_base + 847
            $("#vfcodetip").hide()
            $("#code_input").val("****" + c4 + "****")
        } else {
            $("#vfcodetip").show()
            $("#code_input").val("")
        }
    }

    function getphone() {
        $("#vfcode").modal()
    }

    console.log("SHELL模式尝个鲜")
    console.log("请访问：http://javafeng.com/shellindex")

    function toggleSea() {
        $("#rssp").fadeOut(0)
        $("#seap").fadeToggle(100)
    }

    function toggleRss() {
        $("#seap").fadeOut(0)
        $("#rssp").fadeToggle(100)
    }

    window.onload = function () {
        changeDivHeight();
    }
    window.onresize = function () {
        changeDivHeight();
    }

    function changeDivHeight() {
        var h = document.documentElement.clientHeight;//获取页面可见高度
        document.getElementById("content-main").style.minHeight = h + "px";//掐头去尾，减去100px
    }