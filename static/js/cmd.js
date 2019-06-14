var indextext = "Welcome to javafeng.com.\n" +
    "You can get help by input \"help\".\n\n" +
    "欢迎来到 javafeng.com。\n" +
    "输入\"help\"来获取帮助列表。\n\n"
var info =
    "*********************************\n\n" +
    "QQ:2210036996\nWechat:2210036996\nE-mail:blog@javafeng.com\n\n*********************************\n\n";
var help =
    "查看文章列表：article list\n" +
    "查看分类列表：category list\n" +
    "查看标签列表：tag list\n" +
    "查看文章归档：archive list\n" +
    "查看帮助：help\n" +
    "查看博主信息：info\n" +
    "查看百度：baidu\n" +
    "查看csdn：csdn\n" +
    "查看码云：gitee\n" +
    "支持TAB命令补全，但是仅支持article、category、archive和tag四个关键字，\n其他简单关键字暂不支持。"
var word = indextext
var index = 0;

function type() {
    document.getElementById("first").innerText = word.substring(0, index++);
    if (index == (word.length + 1)) {
        clearInterval(si)
    }
}

var si = setInterval(type, 10);

function onwithnewline() {
    $("#framehide").show()
    cmds = $("#shell-history").children("div")
    var allchildheight = 0
    for (let i = 0; i < cmds.length; i++) {
        allchildheight += cmds[i].clientHeight
    }
    if (allchildheight > ($("#shell-history").height() - 30)) {
        $("#shell-history").empty()
        $("#shell-history").append("<div id=\"first\"></div>")
        $("#shell-history").append("<div><span>> " + $("#shell-textarea").val() + "</span></div>")
    } else {
        $("#shell-history").append("<div><span>> " + $("#shell-textarea").val() + "</span></div>")
    }
    $("#shell-textarea").val("")
}

function onwithoutnewline() {
    $("#shell-textarea").val("")
}

$("#shell").click(function () {
    $("#shell-textarea").focus()
})
$("#shell-textarea").keydown(function (e) {
    var key = e.which;
    if (key == 13) {
        //*****************************/
        cmdtext = $("#shell-textarea").val()
        cmdtextold = $("#shell-textarea").val().replace(/\s+/g, "");
        cmdtext = cmdtext.toUpperCase().replace(/\s+/g, "");
        console.log(cmdtext)
        switch (cmdtext) {
            case "BAIDU":
                onwithnewline()
                $("#mainframe").attr("src", "https://www.baidu.com")
                $("#framehide").fadeOut(500)
                e.preventDefault();
                break;
            case "CSDN":
                onwithnewline()
                $("#mainframe").attr("src", "https://www.csdn.net")
                $("#framehide").fadeOut(500)
                e.preventDefault();
                break;
            case "GITEE":
                onwithnewline()
                $("#mainframe").attr("src", "https://www.gitee.com")
                $("#framehide").fadeOut(500)
                e.preventDefault();
                break;
            case "INFO":
                word = info
                si = setInterval(type, 12);
                index = 0
                onwithoutnewline()
                e.preventDefault();
                break;
            case "CLEAR":
                $("#shell-history").empty()
                $("#shell-history").append("<div id=\"first\"></div>")
                onwithoutnewline()
                e.preventDefault();
                break;
            case "HELP":
                word = help
                si = setInterval(type, 12);
                index = 0
                onwithoutnewline()
                e.preventDefault();
                break;
            case "ADMIN":
                onwithnewline()
                $("#mainframe").attr("src", "/adminindex")
                $("#framehide").fadeOut(500)
                e.preventDefault();
                break;
            case "INDEX":
                onwithnewline()
                $("#mainframe").attr("src", "/home")
                $("#framehide").fadeOut(500)
                e.preventDefault();
                break;
            case "-1":
                onwithnewline()
               window.history.go(-1);
                $("#framehide").fadeOut(500)
                e.preventDefault();
                break;
            case "1":
                onwithnewline()
               window.history.go(1);
                $("#framehide").fadeOut(500)
                e.preventDefault();
                break;
            case "":
                document.getElementById('mainframe').contentWindow.location.reload(true);
                $("#framehide").fadeOut(500)
                e.preventDefault();
                break;
            default:
                onwithnewline()
                e.preventDefault();
                if (cmdtext.indexOf("LOGIN") == 0) {
                    unstart = cmdtext.indexOf("-U") + 2
                    unstop = cmdtext.indexOf("-P")
                    pwdstart = unstop + 2
                    pwdstop = cmdtext.length
                    username = cmdtextold.substring(unstart, unstop)
                    password = cmdtextold.substring(pwdstart, pwdstop)
                    result = login(username, password)
                } else if (cmdtext.indexOf("ARTICLELIST") == 0) {
                    $("#mainframe").attr("src", "/articles")
                    $("#framehide").fadeOut(500)
                } else if (cmdtext.indexOf("CATEGORYLIST") == 0) {
                    $("#mainframe").attr("src", "/categories")
                    $("#framehide").fadeOut(500)
                }else{
                    $("#framehide").fadeOut(500)
                }
                break;
        }
        //*****************************/

    } else if (key == 9) {
        samedata = {
            samecount: 0,
            sameword: []
        }
        sv = $("#shell-textarea").val()
        console.log("article".indexOf(sv))
        console.log("category".indexOf(sv))
        console.log("archive".indexOf(sv))
        console.log("tag".indexOf(sv))
        if ("article".indexOf(sv) == 0) {
            samedata.samecount += 1
            samedata.sameword.push("article")
        }
        if ("category".indexOf(sv) == 0) {
            samedata.samecount += 1
            samedata.sameword.push("category")
        }
        if ("archive".indexOf(sv) == 0) {
            samedata.samecount += 1
            samedata.sameword.push("archive")
        }
        if ("tag".indexOf(sv) == 0) {
            samedata.samecount += 1
            samedata.sameword.push("tag")
        }
        if (samedata.samecount == 1) {
            $("#shell-textarea").val(samedata.sameword[0] + " ")
        }
        $("#shell-textarea").focus()
        e.preventDefault
        return false;
    }
})


function login(username, password) {
    var loginresult = {}
    $.post("/loginv", {username: username, password: password}, function (result) {
        result = eval("(" + result + ")")
        console.log(result)
        $("#framehide").fadeOut(500)
        if (result.state == 1) {
            $("#shell-history").append("<div><span style='color: deepskyblue !important;'>> " + result.msg + "</span></div>")
        } else {
            $("#shell-history").append("<div><span style='color: red !important;'>> " + result.msg + "</span></div>")
        }
    })
}