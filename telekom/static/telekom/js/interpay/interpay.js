console.log('interpay1')

/* #################################################
для изменения BG строки в таблице InterpayBilling ##
   #################################################
*/
function interpayChangeBg(pk) {
    var interpay_pks = document.getElementsByClassName(pk);

    var all_rows = document.getElementsByTagName('td');
    for (var i = 0; i < all_rows.length; i++) {
        if (all_rows[i].classList.contains('my-bg-orange')) { all_rows[i].classList.remove('my-bg-orange'); }
    }
    
    for (let i = 0; i < interpay_pks.length; i++) {
        if (interpay_pks[i].tagName != 'INPUT') {
            interpay_pks[i].classList.add('my-bg-orange')
        }
    }
}
/* #####################################################
для изменения BG строки в таблице InterpayBilling END ##
   #####################################################
*/

// После загрузки страницы Intepay.html проверяем есть ли checked в input-ах имен кассиров
// если есть то bg делаем orange
document.addEventListener("DOMContentLoaded", function () {
    var interpayCheckBoxes = document.getElementsByClassName('kassirsInput')
    for (var i = 0; i < interpayCheckBoxes.length; i++) {
        if (interpayCheckBoxes[i].childNodes[3].checked == true) {
            interpayCheckBoxes[i].classList.add('my-bg-orange')
        }
    }
});

// при клике на input-ы где имена кассиров, вкл-откл bg orange 
function InterpayKassirsChangeBG(id) {    
    var inrterpayKassirClass = document.getElementsByClassName(id);
    if (inrterpayKassirClass[0].classList.contains('my-bg-orange')) {
        inrterpayKassirClass[0].classList.remove('my-bg-orange')
    }
    else {
        inrterpayKassirClass[0].classList.add('my-bg-orange')
    }
}
 