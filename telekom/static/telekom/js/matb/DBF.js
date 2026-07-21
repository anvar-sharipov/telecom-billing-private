/* ###############
    local-calls ##
   ###############
*/
var currentLocation = window.location.href;
if (currentLocation.indexOf("/local-calls") >= 0) {
    (function () {
    document
        .getElementById("localCallsSerachNumber")
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

    // автофокус + автовыделения input номера после загрузки страницы kassa*/
    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("localCallsSerachNumber").select();
    });
}
/* ###################
    local-calls END ##
   ###################
*/
/* ####################
    none-local-calls ##
   ####################
*/
var currentLocation = window.location.href;
if (currentLocation.indexOf("/none-local-calls") >= 0) {  
    (function () {
    document
        .getElementById("nonLocalCallsSerachNumber")
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

    // автофокус + автовыделения input номера после загрузки страницы kassa*/
    document.addEventListener("DOMContentLoaded", function () {  
        document.getElementById("nonLocalCallsSerachNumber").select();
    });  
}
/* ########################
    none-local-calls END ##
   ########################
*/
