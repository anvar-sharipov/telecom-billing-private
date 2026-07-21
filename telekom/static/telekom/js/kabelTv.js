// текущий url в виде строки
var currentLocation = window.location.href;
// если в текущем url есть подстрока kabel-tv-add-user то выполнить код
if (currentLocation.indexOf("kabel-tv-add-user") >= 0) {

    document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("kabelTv_AddUser_search_number").select();
    })

function KabelIsEnterprisesButton (id) {
    if (document.getElementById(id).childNodes[1].checked == false) {
        document.getElementById(id).childNodes[1].checked = true
    } else {
        document.getElementById(id).childNodes[1].checked = false
    }
}

function KabelIsOnButton (id) {
    if (document.getElementById(id).childNodes[1].checked == false) {
        document.getElementById(id).childNodes[1].checked = true
    } else {
        document.getElementById(id).childNodes[1].checked = false
    }
}

/*фецис (цере) между цифрами телефона при вводе номера*/
(function () {
    document
        .getElementById("kabelTv_AddUser_search_number")
        .addEventListener("keydown", function (e) {
        if (e.keyCode !== 8 && e.keyCode !== 46) {
            if (document.activeElement.value.length == 1) {
            document.activeElement.value += "-";
            }
            if (document.activeElement.value.length == 4) {
            document.activeElement.value += "-";
            }
        }
        });
    })();

}

// текущий url в виде строки
var currentLocation = window.location.href;
// если в текущем url есть подстрока kabel-tv-info то выполнить код
if (currentLocation.indexOf("kabel-tv-info") >= 0) {

/*дефис (цере) между цифрами телефона при вводе номера*/
(function () {
document
    .getElementById("kabelNumberSearch")
    .addEventListener("keydown", function (e) {
    if (e.keyCode !== 8 && e.keyCode !== 46) {
        if (document.activeElement.value.length == 1) {
        document.activeElement.value += "-";
        }
        if (document.activeElement.value.length == 4) {
        document.activeElement.value += "-";
        }
    }
    });
})();

}
