console.log('kassa4')

    
// текущий url в виде строки
var currentLocation = window.location.href;
// если в текущем url есть подстрока kassa-index то выполнить код
if (currentLocation.indexOf("kassa-index") >= 0) {
    
/* ######################################################################
    В input-ах modal окна kassa index при клике менять bg на оранжевый ##
    ######################################################################
*/

function onClickChangeBgAbonplata(){
    document.getElementById('abonplata_input_kassa').classList.add('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgSlr(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.add('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgKod(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.add('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgZakaz(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.add('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgProchee(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.add('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgAlem(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.add('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgInternet(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.add('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgDop_uslugi(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.add('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgKabel(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.add('my-bg-orange')
}
function onClickChangeAllModalInputBg(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}

/* ##########################################################################
    В input-ах modal окна kassa index при клике менять bg на оранжевый END ##
    ##########################################################################
*/

/* ############################################
kassa input on click change background color ##
    ############################################
*/


function onClickOnWkladKassa(){ 
    document.getElementById("wklad_input").classList.add('my-bg-orange');
    document.getElementById("search_number").classList.remove('my-bg-orange');
}

function onClickOnSerachKassa(){ 
    document.getElementById("wklad_input").classList.remove('my-bg-orange');
    document.getElementById("search_number").classList.add('my-bg-orange');
}
/* ################################################
kassa input on click change background color END ##
    ################################################
*/

/* ####################################
Печать квитанции (чека) после оплаты ##
    ####################################
*/
if (document.getElementById('printReceipt').innerHTML == 'yes') {
    var print_telefon = document.getElementById('print_telefon').innerHTML;
    var print_slr = document.getElementById('print_slr').innerHTML;
    var print_kod = document.getElementById('print_kod').innerHTML;
    var print_zakaz = document.getElementById('print_zakaz').innerHTML;
    var print_prochee = document.getElementById('print_prochee').innerHTML;
    var print_alem = document.getElementById('print_alem').innerHTML;
    var print_internet = document.getElementById('print_internet').innerHTML;
    var print_dop_uslugi = document.getElementById('print_dop_uslugi').innerHTML;
    var print_kabel = document.getElementById('print_kabel').innerHTML;

    var print_etrap = document.getElementById('print_etrap').innerHTML;
    var print_name_suname_telefon = document.getElementById('print_name_suname_telefon').innerHTML;
    var print_kw_date = document.getElementById('print_kw_date').innerHTML;
    var print_kassir = document.getElementById('print_kassir').innerHTML;
    var print_oplata_sum = document.getElementById('print_oplata_sum').innerHTML;

    var myWindow = window.open('', 'my div', 'height=300,width=400,font-size=9');
    myWindow.document.write('<div style=font-size:10px;>WEAK '+print_etrap+'</div>');
    myWindow.document.write('<div style=font-size:10px;>kwitansiya № '+ print_kw_date +'</div>');
    myWindow.document.write('<div style=font-size:10px;>'+print_name_suname_telefon+'</div>');
    myWindow.document.write('-----------------------------');
    myWindow.document.write('<div style=font-size:10px;padding-left:60px;>tolenen - galandy</div>');   
    myWindow.document.write('-----------------------------');
    if (print_telefon != '0,0' ){myWindow.document.write('<div style=font-size:10px;>Абонплата '+'<span style=font-size:10px;padding-left:20px>'+print_telefon+'</span>'+'</div>');}
    if (print_slr != '0,0'){myWindow.document.write('<div style=font-size:10px;>СЛР '+'<span style=font-size:10px;padding-left:47px>'+print_slr+'</span>'+'</div>');}    
    if (print_kod != '0,0'){myWindow.document.write('<div style=font-size:10px;>КОД '+'<span style=font-size:10px;padding-left:46px>'+print_kod+'</span>'+'</div>');}
    if (print_zakaz != '0,0'){myWindow.document.write('<div style=font-size:10px;>Заказ '+'<span style=font-size:10px;padding-left:43px>'+print_zakaz+'</span>'+'</div>');}
    if (print_prochee != '0,0'){myWindow.document.write('<div style=font-size:10px;>Прочее '+'<span style=font-size:10px;padding-left:35px>'+print_prochee+'</span>'+'</div>');}
    if (print_alem != '0,0'){myWindow.document.write('<div style=font-size:10px;>Alem TV '+'<span style=font-size:10px;padding-left:28px>'+print_alem+'</span>'+'</div>');}
    if (print_internet != '0,0'){myWindow.document.write('<div style=font-size:10px;>Интернет '+'<span style=font-size:10px;padding-left:25px>'+print_internet+'</span>'+'</div>');}
    if (print_dop_uslugi != '0,0'){myWindow.document.write('<div style=font-size:10px;>Доп.Услуги '+'<span style=font-size:10px;padding-left:17px>'+print_dop_uslugi+'</span>'+'</div>');}
    if (print_kabel != '0,0'){myWindow.document.write('<div style=font-size:10px;>Кабель '+'<span style=font-size:10px;padding-left:37px>'+print_kabel+'</span>'+'</div>');}
    myWindow.document.write('-----------------------------');
    myWindow.document.write('<div style=font-size:10px;>Jemi: <span style=font-size:10px;padding-left:45px>'+print_oplata_sum+'</span></div>');
    myWindow.document.write('<div style=font-size:10px;>Maglumat: '+print_kassir+'</div>');
    myWindow.document.write('<div style=font-size:10px;>Gaznachy __________________</div>');
    myWindow.focus(); // necessary for IE >= 10
    myWindow.print();
    myWindow.close();
    var form = document.getElementById('formForRefreshKassaWithNumber');
    form.submit();
}
/* ########################################
Печать квитанции (чека) после оплаты END ##
    ########################################
*/

/* ################################################################################
Запрет платежа при определенных условиях (например если в абонплате ввели букву) ##
    ################################################################################
*/
function stopSubmit() {

    // Если в абонплате есть буквы то запретить оплату
    // if (!Number(document.getElementById('abonplata_input_kassa').value) && document.getElementById('abonplata_input_kassa').value != ''|| parseFloat(document.getElementById('abonplata_input_kassa').value) < 0) {
    //     event.preventDefault()
    // }
    // if (!Number(document.getElementById('slr_input_kassa').value) && document.getElementById('slr_input_kassa').value != '' || parseFloat(document.getElementById('slr_input_kassa').value) < 0) {
    //     event.preventDefault()
    // }
    // if (!Number(document.getElementById('kod_input_kassa').value) && document.getElementById('kod_input_kassa').value != '' || parseFloat(document.getElementById('kod_input_kassa').value) < 0) {
    //     event.preventDefault()
    // }
    // if (!Number(document.getElementById('zakaz_input_kassa').value) && document.getElementById('zakaz_input_kassa').value != '' || parseFloat(document.getElementById('zakaz_input_kassa').value) < 0) {
    //     event.preventDefault()
    // }
    // if (!Number(document.getElementById('prochee_input_kassa').value) && document.getElementById('prochee_input_kassa').value != '' || parseFloat(document.getElementById('prochee_input_kassa').value) < 0) {
    //     event.preventDefault()
    // }
    // if (!Number(document.getElementById('alem_input_kassa').value) && document.getElementById('alem_input_kassa').value != '' || parseFloat(document.getElementById('alem_input_kassa').value) < 0) {
    //     event.preventDefault()
    // }
    // if (!Number(document.getElementById('internet_input_kassa').value) && document.getElementById('internet_input_kassa').value != '' || parseFloat(document.getElementById('internet_input_kassa').value) < 0) {
    //     event.preventDefault()
    // }
    // if (!Number(document.getElementById('dop_uslugi_input_kassa').value) && document.getElementById('dop_uslugi_input_kassa').value != '' || parseFloat(document.getElementById('dop_uslugi_input_kassa').value) < 0) {
    //     event.preventDefault()
    // }
    // if (!Number(document.getElementById('kabel_input_kassa').value) && document.getElementById('kabel_input_kassa').value != '' || parseFloat(document.getElementById('kabel_input_kassa').value) < 0) {
    //     event.preventDefault()
    // }

    // // Если в остаток платежа не 0 (т. е. если в кассу не попала вся сумма которую вложил абонент или если в кассу попала сумма больше чем вложил абонент то запретить оплату)
    // if (parseFloat(document.getElementById('ostatok_plateja').value) != 0 || parseFloat(document.getElementById('ostatok_plateja').value) < 0) {
    //     event.preventDefault()
    // }

    if (!Number(document.getElementById('abonplata_input_kassa').value) && document.getElementById('abonplata_input_kassa').value != ''|| parseFloat(document.getElementById('abonplata_input_kassa').value) < 0) {
        event.preventDefault()
    } else {
        if (!Number(document.getElementById('slr_input_kassa').value) && document.getElementById('slr_input_kassa').value != '' || parseFloat(document.getElementById('slr_input_kassa').value) < 0) {
            event.preventDefault()
        }else {
            if (!Number(document.getElementById('kod_input_kassa').value) && document.getElementById('kod_input_kassa').value != '' || parseFloat(document.getElementById('kod_input_kassa').value) < 0) {
                event.preventDefault()
            }else{
                if (!Number(document.getElementById('zakaz_input_kassa').value) && document.getElementById('zakaz_input_kassa').value != '' || parseFloat(document.getElementById('zakaz_input_kassa').value) < 0) {
                    event.preventDefault()
                }else{
                    if (!Number(document.getElementById('prochee_input_kassa').value) && document.getElementById('prochee_input_kassa').value != '' || parseFloat(document.getElementById('prochee_input_kassa').value) < 0) {
                        event.preventDefault()
                    }else{
                        if (!Number(document.getElementById('alem_input_kassa').value) && document.getElementById('alem_input_kassa').value != '' || parseFloat(document.getElementById('alem_input_kassa').value) < 0) {
                            event.preventDefault()
                        }else{
                            if (!Number(document.getElementById('internet_input_kassa').value) && document.getElementById('internet_input_kassa').value != '' || parseFloat(document.getElementById('internet_input_kassa').value) < 0) {
                                event.preventDefault()
                            }else{
                                if (!Number(document.getElementById('dop_uslugi_input_kassa').value) && document.getElementById('dop_uslugi_input_kassa').value != '' || parseFloat(document.getElementById('dop_uslugi_input_kassa').value) < 0) {
                                    event.preventDefault()
                                }else{}
                                    if (!Number(document.getElementById('kabel_input_kassa').value) && document.getElementById('kabel_input_kassa').value != '' || parseFloat(document.getElementById('kabel_input_kassa').value) < 0) {
                                        event.preventDefault()
                                    }else{

                                    // Если в остаток платежа не 0 (т. е. если в кассу не попала вся сумма которую вложил абонент или если в кассу попала сумма больше чем вложил абонент то запретить оплату)
                                    if (parseFloat(document.getElementById('ostatok_plateja').value) != 0 || parseFloat(document.getElementById('ostatok_plateja').value) < 0) {
                                        event.preventDefault()
                                    }else{
                                        document.getElementById('oplata_modal_form').submit();
                                        document.getElementById('oplata_modal_form_submit').disabled=true;
                                        // var myModalEl = document.getElementById('oplataModal');
                                        // var modal = bootstrap.Modal.getInstance(myModalEl)
                                        // modal.hide();
                                    }}}}}}}}}

        /* ####################################################################################
        Запрет платежа при определенных условиях (например если в абонплате ввели букву) END ##
        #######################################################################################
        */

    }


/* ########################################################
код для показа общего баланса в баланс в касса userTable ##
    ########################################################
*/
var abonplata_balance_kassa = parseFloat(document.getElementById('abonent_balance_in_kassa_table').innerHTML.replace(',', '.'))
var slr_balance_kassa = parseFloat(document.getElementById('slr_balance_in_kassa_table').innerHTML.replace(',', '.'))
var kod_balance_kassa = parseFloat(document.getElementById('kod_balance_in_kassa_table').innerHTML.replace(',', '.'))
var zakaz_balance_kassa = parseFloat(document.getElementById('zakaz_balance_in_kassa_table').innerHTML.replace(',', '.'))
var prochee_balance_kassa = parseFloat(document.getElementById('prochee_balance_in_kassa_table').innerHTML.replace(',', '.'))
var alem_balance_kassa = parseFloat(document.getElementById('alem_balance_in_kassa_table').innerHTML.replace(',', '.'))
var internet_balance_kassa = parseFloat(document.getElementById('internet_balance_in_kassa_table').innerHTML.replace(',', '.'))
var dop_uslugi_balance_kassa = parseFloat(document.getElementById('dop_uslugi_balance_in_kassa_table').innerHTML.replace(',', '.'))
var kabel_balance_kassa = parseFloat(document.getElementById('kabel_balance_in_kassa_table').innerHTML.replace(',', '.'))

// для Input Баланс в pay row Kassa index (сумма плюсов и минусов балансов)
balance_payRow = abonplata_balance_kassa + slr_balance_kassa + kod_balance_kassa + zakaz_balance_kassa + prochee_balance_kassa + alem_balance_kassa + internet_balance_kassa + dop_uslugi_balance_kassa + kabel_balance_kassa;
document.getElementById('kassa_balance_in_pay_row').value = balance_payRow.toFixed(2);
          
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!

// console.log('gg',mm)


// для Input Задолженность в pay row Kassa index (сумма всех минусов в балансе)
if (abonplata_balance_kassa < 0){var zadolAbonplata = abonplata_balance_kassa} else {var zadolAbonplata = 0}
if (slr_balance_kassa < 0){var zadolSlr = slr_balance_kassa} else {var zadolSlr = 0}
if (kod_balance_kassa < 0){var zadolKod = kod_balance_kassa} else {var zadolKod = 0}
if (zakaz_balance_kassa < 0){var zadolZakaz = zakaz_balance_kassa} else {var zadolZakaz = 0}
if (prochee_balance_kassa < 0){var zadolProchee = prochee_balance_kassa} else {var zadolProchee = 0}
if (alem_balance_kassa < 0){var zadolAlem = alem_balance_kassa} else {var zadolAlem = 0}
if (internet_balance_kassa < 0){var zadolinternet = internet_balance_kassa} else {var zadolinternet = 0}
if (dop_uslugi_balance_kassa < 0){var zadolDop_uslugi = dop_uslugi_balance_kassa} else {var zadolDop_uslugi = 0}
if (kabel_balance_kassa < 0){var zadolkabel = kabel_balance_kassa} else {var zadolkabel = 0};

var zadoljnennost = zadolAbonplata + zadolSlr + zadolKod + zadolZakaz + zadolProchee + zadolAlem + zadolinternet +  zadolDop_uslugi + zadolkabel;
document.getElementById('kassa__zadol_pay_row').value = zadoljnennost.toFixed(2);


// для Input Сумма к отключению в pay row Kassa index (это все суммы минусов в балансе но убрать минусы начисления текущего месяца)
// abonplataMonth01 = parseFloat(document.getElementById('abonplataMonth'+mm).innerHTML.replace(',', '.')
if (document.getElementById('abonplataMonth'+mm).innerHTML == '') {var abonplataCurrentMonth = 0} else {
    var abonplataCurrentMonth = parseFloat(document.getElementById('abonplataMonth'+mm).innerHTML.replace(',', '.'))
}

if (document.getElementById('slrMonth'+mm).innerHTML == '') {var slrCurrentMonth = 0} else {
    var slrCurrentMonth = parseFloat(document.getElementById('slrMonth'+mm).innerHTML.replace(',', '.'))
}

if (document.getElementById('kodMonth'+mm).innerHTML == '') {var kodCurrentMonth = 0} else {
    var kodCurrentMonth = parseFloat(document.getElementById('kodMonth'+mm).innerHTML.replace(',', '.'))
}


if (document.getElementById('zakazMonth'+mm).innerHTML == '') {var zakazCurrentMonth = 0} else {
    var zakazCurrentMonth = parseFloat(document.getElementById('zakazMonth'+mm).innerHTML.replace(',', '.'))
}

if (document.getElementById('procheeMonth'+mm).innerHTML == '') {var procheeCurrentMonth = 0} else {
    var procheeCurrentMonth = parseFloat(document.getElementById('procheeMonth'+mm).innerHTML.replace(',', '.'))
}
console.log(mm)
if (document.getElementById('dop_uslugiMonth'+mm).innerHTML == '') {var dop_uslugiCurrentMonth = 0} else {
    var dop_uslugiCurrentMonth = parseFloat(document.getElementById('dop_uslugiMonth'+mm).innerHTML.replace(',', '.'))
}

if (document.getElementById('internetMonth'+mm).innerHTML == '') {var internetCurrentMonth = 0} else {
    var internetCurrentMonth = parseFloat(document.getElementById('internetMonth'+mm).innerHTML.replace(',', '.'))
}

if (document.getElementById('kabelMonth'+mm).innerHTML == '') {var kabelCurrentMonth = 0} else {
    var kabelCurrentMonth = parseFloat(document.getElementById('kabelMonth'+mm).innerHTML.replace(',', '.'))
}

if (document.getElementById('alemMonth'+mm).innerHTML == '') {var alemCurrentMonth = 0} else {
    var alemCurrentMonth = parseFloat(document.getElementById('alemMonth'+mm).innerHTML.replace(',', '.'))
}

var summaKOtklucheniyu = zadoljnennost + abonplataCurrentMonth + slrCurrentMonth + kodCurrentMonth + zakazCurrentMonth + procheeCurrentMonth + dop_uslugiCurrentMonth + internetCurrentMonth + kabelCurrentMonth + alemCurrentMonth


document.getElementById('summa_k_otkl_payRow').value = summaKOtklucheniyu.toFixed(2);



/* ############################################################
код для показа общего баланса в баланс в касса userTable END ##
    ############################################################
*/


    /*фецис (цере) между цифрами телефона при вводе номера kassa-index*/
    (function () {
    document
        .getElementById("search_number")
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
    
    
    // // автофокус + автовыделения input номера после загрузки страницы kassa*/
    // document.addEventListener("DOMContentLoaded", function () {
    //     // document.getElementById("search_number").select();
    //     // console.log('rererererererer');
        
        
    //     // Если есть доступ к платежам, например если это кассир то выделять input pay
    //     if (document.getElementById('allow_to_pay_div') === 'True') {
    //         // Если найден номер свободный или ошибка то опять выделить search_number
    //         if (document.getElementById("kassa_surname_input").innerHTML == '' || document.getElementById("kassa_name_input").innerHTML == '') {
    //             document.getElementById("search_number").classList.add('my-bg-orange');
    //             document.getElementById("search_number").select();
    //         } else {
    //         //   Иначе если найден номер то выделить Input wklad
    //             document.getElementById("wklad_input").select();
    //             document.getElementById("search_number").classList.remove('my-bg-orange');
    //             document.getElementById('wklad_input').classList.add('my-bg-orange')
    //         }
    //     // иначе если нет доступа платежам то всегда выделят input number
    //     } else {
    //         document.getElementById("search_number").classList.add('my-bg-orange');
    //         document.getElementById("search_number").select();
    //     }
    // });
    // автофокус + автовыделения input номера после загрузки страницы kassa*/
    document.addEventListener("DOMContentLoaded", function () {

        if (document.getElementById('allow_to_pay_div').innerHTML === 'True') {
            document.getElementById("wklad_input").select();
            document.getElementById("search_number").classList.remove('my-bg-orange');
            document.getElementById('wklad_input').classList.add('my-bg-orange')
            // console.log('da allow', document.getElementById('allow_to_pay_div'));
            
            // // Если найден номер свободный или ошибка то опять выделить search_number
            // if (document.getElementById("kassa_surname_input").innerHTML == '' || document.getElementById("kassa_name_input").innerHTML == '') {
            //     document.getElementById("search_number").classList.add('my-bg-orange');
            //     document.getElementById("search_number").select();
            // } else {
            // //   Иначе если найден номер то выделить Input wklad
            //     document.getElementById("wklad_input").select();
            //     document.getElementById("search_number").classList.remove('my-bg-orange');
            //     document.getElementById('wklad_input').classList.add('my-bg-orange')
            // }
        // иначе если нет доступа платежам то всегда выделят input number
        } else {
            document.getElementById("search_number").classList.add('my-bg-orange');
            document.getElementById('wklad_input').classList.remove('my-bg-orange')
            document.getElementById("search_number").select();
            // console.log('net ne allow', document.getElementById('allow_to_pay_div').innerHTML);
        }

    // Если найден номер свободный или ошибка то опять выделить search_number
    // if (document.getElementById("kassa_surname_input").innerHTML == '' || document.getElementById("kassa_name_input").innerHTML == '') {
    //     document.getElementById("search_number").classList.add('my-bg-orange');
    //     document.getElementById("search_number").select();
    // } else {
    // //   Иначе если найден номер то выделить Input wklad
    //     document.getElementById("wklad_input").select();
    //     document.getElementById("search_number").classList.remove('my-bg-orange');
    //     document.getElementById('wklad_input').classList.add('my-bg-orange')
    // }
    });
    
    // функция для проверки есть ли в тексте пробел
    function hasWhiteSpace(str) {
    if (str.indexOf(' ') >= 0) {
        return true
    } else {
        return false
    }
    }
    
/* #################################################
код для запрета ввода пробела в касса модал input ##
    #################################################
*/
    var abonplata_taboo_space = document.getElementById('abonplata_input_kassa');
    var slr_taboo_space = document.getElementById('slr_input_kassa');
    var kod_taboo_space = document.getElementById('kod_input_kassa');
    var zakaz_taboo_space = document.getElementById('zakaz_input_kassa');
    var prochee_taboo_space = document.getElementById('prochee_input_kassa');
    var alem_taboo_space = document.getElementById('alem_input_kassa');
    var internet_taboo_space = document.getElementById('internet_input_kassa');
    var dop_uslugi_taboo_space = document.getElementById('dop_uslugi_input_kassa');
    var kabel_taboo_space = document.getElementById('kabel_input_kassa');
    
    // Запрет ввода пробела в abonplata Input в модалке кассы
    abonplata_taboo_space.oninput = () => {
    if(hasWhiteSpace(abonplata_taboo_space.value)) {
        document.getElementById('abonplata_input_kassa').value = abonplata_taboo_space.value.split(' ').join('')
    }
    
    }
    
    slr_taboo_space.oninput = () => {
    if(hasWhiteSpace(slr_taboo_space.value)) {
        document.getElementById('slr_input_kassa').value = slr_taboo_space.value.split(' ').join('')
    }
    }
    
    kod_taboo_space.oninput = () => {
    if(hasWhiteSpace(kod_taboo_space.value)) {
        document.getElementById('kod_input_kassa').value = kod_taboo_space.value.split(' ').join('')
    }
    }
    
    zakaz_taboo_space.oninput = () => {
    if(hasWhiteSpace(zakaz_taboo_space.value)) {
        document.getElementById('zakaz_input_kassa').value = zakaz_taboo_space.value.split(' ').join('')
    }
    }
    
    prochee_taboo_space.oninput = () => {
    if(hasWhiteSpace(prochee_taboo_space.value)) {
        document.getElementById('prochee_input_kassa').value = prochee_taboo_space.value.split(' ').join('')
    }
    }
    
    alem_taboo_space.oninput = () => {
    if(hasWhiteSpace(alem_taboo_space.value)) {
        document.getElementById('alem_input_kassa').value = alem_taboo_space.value.split(' ').join('')
    }
    }
    
    internet_taboo_space.oninput = () => {
    if(hasWhiteSpace(internet_taboo_space.value)) {
        document.getElementById('internet_input_kassa').value = internet_taboo_space.value.split(' ').join('')
    }
    }
    
    dop_uslugi_taboo_space.oninput = () => {
    if(hasWhiteSpace(dop_uslugi_taboo_space.value)) {
        document.getElementById('dop_uslugi_input_kassa').value = dop_uslugi_taboo_space.value.split(' ').join('')
    }
    }
    
    kabel_taboo_space.oninput = () => {
    if(hasWhiteSpace(kabel_taboo_space.value)) {
        document.getElementById('kabel_input_kassa').value = kabel_taboo_space.value.split(' ').join('')
    }
    }
/* #####################################################
код для запрета ввода пробела в касса модал input END ##
    #####################################################
*/
    
    
/* ######################
input-ы в касса индекс ##
    ######################
*/
    // Input поиска по номеру
    (function() {
        document.getElementById('search_number').addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {
            // Если поиска по номеру нажал вниз то переход в Input вклад
            var wklad_input = document.getElementById('wklad_input');
            document.getElementById('search_number').classList.remove('my-bg-orange')
            document.getElementById('wklad_input').classList.add('my-bg-orange')
            wklad_input.focus();
            }  
        if (e.keyCode === 46) {
            // Если нажал на delete то удалить все в inpute поиск по номеру
            var search_number = document.getElementById('search_number');
            search_number.value = '';
            search_number.focus();
            }         
        });
    })();
    
    // Input вклад
    (function() {
        document.getElementById('wklad_input').addEventListener('keydown', function(e) {
        if (e.keyCode === 38) {  
            // если с вклада нажал вверх то переход в Input поиска по номеру
            var search_number = document.getElementById('search_number');
            document.getElementById("wklad_input").classList.remove('my-bg-orange');
            document.getElementById("search_number").classList.add('my-bg-orange');
            e.preventDefault()
            document.getElementById('search_number').select();
            } 
        if (e.keyCode === 13) {  
            // Если нажал на enter то открыть oplataModal
            var oplata_input = document.getElementById('oplata_input');

            // Когда нажимеешь на enter в wklad_input то во время открития модального окна 
            // можно добавлять еще символы (если случайно нажать) (запрещием добавления нового символа после нажатия на enter)
            if (parseFloat(document.getElementById("wklad_input").value) > 0 ) {
            document.getElementById("wklad_input").readOnly = true
            }
            


            // проверка вклада input в касса (нет ли там буквы и больше ли 0 вклад) 
            if (Number(document.getElementById('wklad_input').value)) {
            if (parseFloat(document.getElementById('wklad_input').value) > 0) {
                oplata_input.click();
            } else {
                event.preventDefault()
            }
            } else {
            event.preventDefault()
            }
            } 

        });
    })();
    
    // Input оплатить
    (function() {
        document.getElementById('oplata_input').addEventListener('keydown', function(e) {
        if (e.keyCode === 38) {  
            // если с Input оплатить нажал вверх то переход в Input поиска по номеру
            var search_number = document.getElementById('search_number');
            search_number.focus();
            }
    
        if (e.keyCode === 39) {  
            // если с Input оплатить нажал на право то переход в Input вклад
            var wklad_input = document.getElementById('wklad_input');
            wklad_input.focus();
            }
        });
    })();
/* ##########################
input-ы в касса индекс END ##
    ##########################
*/
// var kassa_payRow = today.getFullYear();



    
/* #####################
input-ы в oplataModal ##
    #####################
*/
    // Input abonplata_input_kassa
    // (function() {
    //     document.getElementById('abonplata_input_kassa').addEventListener('keydown', function(e) {
    // if (e.keyCode === 1) {console.log('clicked')}
    //     if (e.keyCode === 40 || e.keyCode === 13) {  
    //         // если нажал вниз то переход к slr input
    //         var slr_input_kassa = document.getElementById('slr_input_kassa');
    //         document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    //         document.getElementById('slr_input_kassa').classList.add('my-bg-orange')
    //         slr_input_kassa.select();
    //         e.preventDefault();
    //         }
    
    //     if (e.keyCode === 32) {  
    //         // если нажал на пробел то вся сумма с остатка платежа должна переместиться этот input
    //         // Если ostatok plateja пусто, значит не ввели сумму в wklad (ничего не делаем)
    
    //         if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
    //         // иначе если wklad ввели
    //         } else {  
    //             // Если summa_w_kassu == '' или 0, то вводим то тупо все ostatok_plateja переводим в summa_w_kassu и в abonplata_input_kassa, а ostatok_plateja = 0
    //             if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
    //                 document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
    //                 document.getElementById('abonplata_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
    //                 document.getElementById('ostatok_plateja').value = 0
                
    //             // иначе если summa_w_kassu != '' или 0, то
    //             } else {
    //                 // если abonplata_input_kassa == 0 или == '', то тупо переводим все в абонплата
    //                 if (document.getElementById('abonplata_input_kassa').value == '' || document.getElementById('abonplata_input_kassa').value == 0) {
    //                     document.getElementById('abonplata_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);      
    //                 // иначе если abonplata_input_kassa != 0 и != '', то abonplata_input_kassa += ostatok_plateja
    //                 } else {
    //                     var abonplata = parseFloat(document.getElementById('abonplata_input_kassa').value)
    //                     document.getElementById('abonplata_input_kassa').value = (abonplata + parseFloat(document.getElementById('ostatok_plateja').value)).toFixed(2);
    //                 }
    //                 // и в конце в summa_w_kassu += ostatok_plateja, ostatok_plateja = 0
    //                 summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
    //                 document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
    //                 document.getElementById('ostatok_plateja').value = 0
    
    //             }
    //         }
    //         } 
            
    //     });
    // })();
    
    // Input slr_input_kassa
    // (function() {
    //     document.getElementById('slr_input_kassa').addEventListener('keydown', function(e) {
    
    //     if (e.keyCode === 40 || e.keyCode === 13) {  
    //         // вниз переход в kod input
    //         var kod_input_kassa = document.getElementById('kod_input_kassa');
    //         document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    //         document.getElementById('kod_input_kassa').classList.add('my-bg-orange')
    //         kod_input_kassa.select();
    //         e.preventDefault();
    //         }
        
    //     if (e.keyCode === 38) {  
    //         // вверх переход в abonplata input
    //         var abonplata_input_kassa = document.getElementById('abonplata_input_kassa');
    //         document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    //         document.getElementById('abonplata_input_kassa').classList.add('my-bg-orange')
    //         abonplata_input_kassa.select();
    //         e.preventDefault();
    //         }
            
    //     if (e.keyCode === 32) {  
    //         // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
    //         if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
    //         } else {
    //             if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
    //                 document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
    //                 document.getElementById('slr_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
    //                 document.getElementById('ostatok_plateja').value = 0
    //             } else {
    //                 if (document.getElementById('slr_input_kassa').value == '' || document.getElementById('slr_input_kassa').value == 0) {
    //                     document.getElementById('slr_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
    //                 } else {
    //                     var slr = parseFloat(document.getElementById('slr_input_kassa').value)
    //                     document.getElementById('slr_input_kassa').value = (slr + parseFloat(document.getElementById('ostatok_plateja').value)).toFixed(2);
    //                 }
    //                 summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
    //                 document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
    //                 document.getElementById('ostatok_plateja').value = 0
    //             }
    //         }
    //         }
    //     });
    // })();
    
    // Input kod_input_kassa
    // (function() {
    //     document.getElementById('kod_input_kassa').addEventListener('keydown', function(e) {
    
    //     if (e.keyCode === 40 || e.keyCode === 13) {  
    //         // вниз переход в zakaz_input_kassa input
    //         var zakaz_input_kassa = document.getElementById('zakaz_input_kassa');
    //         document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    //         document.getElementById('zakaz_input_kassa').classList.add('my-bg-orange')
    //         zakaz_input_kassa.select();
    //         e.preventDefault();
    //         }
        
    //     if (e.keyCode === 38) {  
    //         // вверх переход в slr_input_kassa input
    //         var slr_input_kassa = document.getElementById('slr_input_kassa');
    //         document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    //         document.getElementById('slr_input_kassa').classList.add('my-bg-orange')
    //         slr_input_kassa.select();
    //         e.preventDefault();
    //         }
    
    //     if (e.keyCode === 32) {  
    //         // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
    //         if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
    //         } else {
    //             if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
    //                 document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
    //                 document.getElementById('kod_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
    //                 document.getElementById('ostatok_plateja').value = 0
    //             } else {
    //                 if (document.getElementById('kod_input_kassa').value == '' || document.getElementById('kod_input_kassa').value == 0) {
    //                     document.getElementById('kod_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
    //                 } else {
    //                     var kod = parseFloat(document.getElementById('kod_input_kassa').value)
    //                     document.getElementById('kod_input_kassa').value = (kod + parseFloat(document.getElementById('ostatok_plateja').value)).toFixed(2)
    //                 }
    //                 summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
    //                 document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
    //                 document.getElementById('ostatok_plateja').value = 0
    //             }
    //         }
    //         }
    
    //     });
    // })();
    
    // Input zakaz_input_kassa
    // (function() {
    //     document.getElementById('zakaz_input_kassa').addEventListener('keydown', function(e) {
    //     if (e.keyCode === 40 || e.keyCode === 13) {  
    //         // вниз переход в prochee_input_kassa input
    //         var prochee_input_kassa = document.getElementById('prochee_input_kassa');
    //         document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    //         document.getElementById('prochee_input_kassa').classList.add('my-bg-orange')
    //         prochee_input_kassa.select();
    //         e.preventDefault();
    //         }
        
    //     if (e.keyCode === 38) {  
    //         // вверх переход в kod_input_kassa input
    //         var kod_input_kassa = document.getElementById('kod_input_kassa');
    //         document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    //         document.getElementById('kod_input_kassa').classList.add('my-bg-orange')
    //         kod_input_kassa.select();
    //         e.preventDefault();
    //         }
    
    //     if (e.keyCode === 32) {  
    //         // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
    //         if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
    //         } else {
    //             if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
    //                 document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
    //                 document.getElementById('zakaz_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
    //                 document.getElementById('ostatok_plateja').value = 0
    //             } else {
    //                 if (document.getElementById('zakaz_input_kassa').value == '' || document.getElementById('zakaz_input_kassa').value == 0) {
    //                     document.getElementById('zakaz_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
    //                 } else {
    //                     var zakaz = parseFloat(document.getElementById('zakaz_input_kassa').value)
    //                     document.getElementById('zakaz_input_kassa').value = (zakaz + parseFloat(document.getElementById('ostatok_plateja').value)).toFixed(2);
    //                 }
    //                 summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
    //                 document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
    //                 document.getElementById('ostatok_plateja').value = 0
    //             }
    //         }
    //         }
    
    //     });
    // })();
    
    // Input prochee_input_kassa
    (function() {
        document.getElementById('prochee_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40 || e.keyCode === 13) {
            // нет(вниз переход в dop_uslugi_input_kassa input) вниз переход в интернет
            var dop_uslugi_input_kassa = document.getElementById('dop_uslugi_input_kassa');
            document.getElementById('prochee_input_kassa').classList.remove('col6', 'my-bg-orange')
            document.getElementById('internet_input_kassa').classList.add('col8')
            internet_input_kassa.select();
            e.preventDefault();
            }
        // if (e.keyCode === 38) {  
        //     // нет(вверх переход в zakaz_input_kassa input) никуда
        //     var zakaz_input_kassa = document.getElementById('zakaz_input_kassa');
        //     document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
        //     document.getElementById('zakaz_input_kassa').classList.add('my-bg-orange')
        //     zakaz_input_kassa.select();
        //     e.preventDefault();
        //     }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('prochee_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('prochee_input_kassa').value == '' || document.getElementById('prochee_input_kassa').value == 0) {
                        document.getElementById('prochee_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
                    } else {
                        var prochee = parseFloat(document.getElementById('prochee_input_kassa').value)
                        document.getElementById('prochee_input_kassa').value = (prochee + parseFloat(document.getElementById('ostatok_plateja').value)).toFixed(2);
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
    
        });
    })();
    
    // Input dop_uslugi_input_kassa
    // (function() {
    //     document.getElementById('dop_uslugi_input_kassa').addEventListener('keydown', function(e) {
    //     if (e.keyCode === 40 || e.keyCode === 13) {  
    //         // вниз переход в internet_input_kassa input
    //         var internet_input_kassa = document.getElementById('internet_input_kassa');
    //         document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    //         document.getElementById('internet_input_kassa').classList.add('my-bg-orange')
    //         internet_input_kassa.select();
    //         e.preventDefault();
    //         }
    //     if (e.keyCode === 38) {  
    //         // вверх переход в prochee_input_kassa input
    //         var prochee_input_kassa = document.getElementById('prochee_input_kassa');
    //         document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    //         document.getElementById('prochee_input_kassa').classList.add('my-bg-orange')
    //         prochee_input_kassa.select();
    //         e.preventDefault();
    //         }
    
    //     if (e.keyCode === 32) {  
    //         // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
    //         if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
    //         } else {
    //             if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
    //                 document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
    //                 document.getElementById('dop_uslugi_input_kassa').value =parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
    //                 document.getElementById('ostatok_plateja').value = 0
    //             } else {
    //                 if (document.getElementById('dop_uslugi_input_kassa').value == '' || document.getElementById('dop_uslugi_input_kassa').value == 0) {
    //                     document.getElementById('dop_uslugi_input_kassa').value =parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
    //                 } else {
    //                     var dop_uslugi = parseFloat(document.getElementById('dop_uslugi_input_kassa').value)
    //                     document.getElementById('dop_uslugi_input_kassa').value = (dop_uslugi + parseFloat(document.getElementById('ostatok_plateja').value)).toFixed(2);
    //                 }
    //                 summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
    //                 document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
    //                 document.getElementById('ostatok_plateja').value = 0
    //             }
    //         }
    //         }
    
    //     });
    // })();
    
    // Input internet_input_kassa
    (function() {
        document.getElementById('internet_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40 || e.keyCode === 13) {  
            // вниз переход в kabel_input_kassa input
            var kabel_input_kassa = document.getElementById('kabel_input_kassa');
            document.getElementById('internet_input_kassa').classList.remove('col8')
            document.getElementById('kabel_input_kassa').classList.add('col9')
            kabel_input_kassa.select();
            e.preventDefault();
            }
        if (e.keyCode === 38) {  
            // нет(вверх переход в dop_uslugi_input_kassa input) вверх переход в prochee_input_kassa input
            var prochee_input_kassa = document.getElementById('prochee_input_kassa');
            document.getElementById('internet_input_kassa').classList.remove('col8')
            document.getElementById('prochee_input_kassa').classList.add('col6')
            prochee_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('internet_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('internet_input_kassa').value == '' || document.getElementById('internet_input_kassa').value == 0) {
                        document.getElementById('internet_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
                    } else {
                        var internet = parseFloat(document.getElementById('internet_input_kassa').value)
                        document.getElementById('internet_input_kassa').value = (internet + parseFloat(document.getElementById('ostatok_plateja').value)).toFixed(2);
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
    
        });
    })();
    
    // Input kabel_input_kassa
    (function() {
        document.getElementById('kabel_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40 || e.keyCode === 13) {  
            // вниз переход в kabel_input_kassa input
            var alem_input_kassa = document.getElementById('alem_input_kassa');
            document.getElementById('kabel_input_kassa').classList.remove('col9')
            document.getElementById('alem_input_kassa').classList.add('col10')
            alem_input_kassa.select();
            e.preventDefault();
            }
        if (e.keyCode === 38) {  
            // вверх переход в internet_input_kassa input
            var internet_input_kassa = document.getElementById('internet_input_kassa');
            document.getElementById('kabel_input_kassa').classList.remove('col9')
            document.getElementById('internet_input_kassa').classList.add('col8')
            internet_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('kabel_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('kabel_input_kassa').value == '' || document.getElementById('kabel_input_kassa').value == 0) {
                        document.getElementById('kabel_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
                    } else {
                        var kabel = parseFloat(document.getElementById('kabel_input_kassa').value)
                        document.getElementById('kabel_input_kassa').value = (kabel + parseFloat(document.getElementById('ostatok_plateja').value)).toFixed(2);
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
    
    
        });
    })();
    
    // Input alem_input_kassa
    (function() {
        document.getElementById('alem_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40 || e.keyCode === 13) {  
            // вниз переход в card_input_kassa input
            var card_input_kassa = document.getElementById('card_input_kassa');
            document.getElementById('alem_input_kassa').classList.remove('col10')
            card_input_kassa.focus();
            e.preventDefault();
            }
        if (e.keyCode === 38) {  
            // вверх переход в kabel_input_kassa input
            var kabel_input_kassa = document.getElementById('kabel_input_kassa');
            document.getElementById('alem_input_kassa').classList.remove('col10')
            document.getElementById('kabel_input_kassa').classList.add('col9')
            kabel_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('alem_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('alem_input_kassa').value == '' || document.getElementById('alem_input_kassa').value == 0) {
                        document.getElementById('alem_input_kassa').value = parseFloat(document.getElementById('ostatok_plateja').value).toFixed(2);
                    } else {
                        var alem = parseFloat(document.getElementById('alem_input_kassa').value)
                        document.getElementById('alem_input_kassa').value = (alem + parseFloat(document.getElementById('ostatok_plateja').value)).toFixed(2);
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
        });
    })();
    
    // Input card_input_kassa
    (function() {
        document.getElementById('card_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40 || e.keyCode === 13) {  
            // вниз переход в oplata_btm_modal input
            // var oplata_btm_modal = document.getElementById('oplata_btm_modal');
            var oplata_btm_modal = document.getElementById('oplata_modal_form_submit');
            oplata_btm_modal.focus()
            }
        if (e.keyCode === 38) {  
            // вверх переход в alem_input_kassa input
            var alem_input_kassa = document.getElementById('alem_input_kassa');
            document.getElementById('alem_input_kassa').classList.add('col10')
            alem_input_kassa.select();
            e.preventDefault();
            }
        });
    })();

// №№№
    // Input oplata_modal_form_submit
    (function() {
        document.getElementById('oplata_modal_form_submit').addEventListener('keydown', function(e) {
        if (e.keyCode === 38) {  
            // вверх переход в alem_input_kassa input
            var card_input_kassa = document.getElementById('card_input_kassa');
            document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
            card_input_kassa.focus();
            e.preventDefault();
            }
        });
    })();
// №№№
    
    // Input oplata_btm_modal
    (function() {
        document.getElementById('oplata_btm_modal').addEventListener('keydown', function(e) {
    
        if (e.keyCode === 38) {  
            // вверх переход в card_input_kassa input
            var card_input_kassa = document.getElementById('card_input_kassa');
            card_input_kassa.focus();
            }
        });
    })();
/* #########################
input-ы в oplataModal END ##
    #########################
*/

    
    
    
/* ###############################################
При активации модального окна касса oplataModal ##
    ###############################################
*/
    // Фокус input-a абонрлата (в oplataModal) после нажатия на оплатить (в касса)
    var myModal = document.getElementById('oplataModal')

    


    // Если модальное окно открылась
    myModal.addEventListener('shown.bs.modal', function () {

        var abonplata_input_kassa = document.getElementById('abonplata_input_kassa')
        var slr_input_kassa = document.getElementById('slr_input_kassa')
        var kod_input_kassa = document.getElementById('kod_input_kassa')
        var zakaz_input_kassa = document.getElementById('zakaz_input_kassa')
        var prochee_input_kassa = document.getElementById('prochee_input_kassa')
        var dop_uslugi_input_kassa = document.getElementById('dop_uslugi_input_kassa')
        var internet_input_kassa = document.getElementById('internet_input_kassa')
        var kabel_input_kassa = document.getElementById('kabel_input_kassa')
        var alem_input_kassa = document.getElementById('alem_input_kassa')

        var ostatok_plateja = document.getElementById('ostatok_plateja')
        var oplata_modal_balance_input = document.getElementById('oplata_modal_balance_input')
        var summa_k_otkl_payModal = document.getElementById('summa_k_otkl_payModal')
        var ostatok_zadol_payModal = document.getElementById('ostatok_zadol_payModal')
        var wklad_modal = document.getElementById('wklad_modal')

        var summa_w_kassu = document.getElementById('summa_w_kassu')
        // Сумма в кассу в modal
        if (summa_w_kassu.value == '') {
            var summa_w_kassu_ = 0
        } else {
            var summa_w_kassu_ = parseFloat(summa_w_kassu.value)
        }

        ostatok_plateja.classList.add('my-bg-red')
        summa_w_kassu.classList.add('my-bg-red')
        prochee_input_kassa.classList.add('my-bg-orange')

        oplata_modal_balance_input.value = document.getElementById('kassa_balance_in_pay_row').value
        summa_k_otkl_payModal.value = document.getElementById('summa_k_otkl_payRow').value
        ostatok_zadol_payModal.value = Math.abs(parseFloat(document.getElementById('kassa__zadol_pay_row').value.replace(',','.')))

        prochee_input_kassa.select()

        
        /* ########################################
        Все баланс минусы сделать 0 в modal окне ##
            ########################################
        */
        // Баланс в modal
        var balance_modal = parseFloat(oplata_modal_balance_input.value)
        // Вклад в modal
        var wklad_modal_ = parseFloat(wklad_modal.value)

        // Ост. задол. в modal
        if (ostatok_zadol_payModal.value == '' || ostatok_zadol_payModal.value == '0' || ostatok_zadol_payModal.value == 0) {
        var ostatok_zadol_payModal_ = 0
        } else {
        var ostatok_zadol_payModal_ = parseFloat(ostatok_zadol_payModal.value)
        }

        // Сумма к откл. modal
        if (summa_k_otkl_payModal.value == '') {
        var summa_k_otkl_payModal_ = 0
        } else {
        var summa_k_otkl_payModal_ = Math.abs(parseFloat(summa_k_otkl_payModal.value))
        }

        // if (kassa_payRow == '2024') {
        //     window.location.href = "http://127.0.0.1:8080/kassa-index";
        // }   

        // Балансы с кассы
        var abonplata_balance = parseFloat(document.getElementById('abonent_balance_in_kassa_table').innerHTML.replace(',', '.'))
        var slr_balance = parseFloat(document.getElementById('slr_balance_in_kassa_table').innerHTML.replace(',', '.'))
        var kod_balance = parseFloat(document.getElementById('kod_balance_in_kassa_table').innerHTML.replace(',', '.'))
        var zakaz_balance = parseFloat(document.getElementById('zakaz_balance_in_kassa_table').innerHTML.replace(',', '.'))
        var prochee_balance = parseFloat(document.getElementById('prochee_balance_in_kassa_table').innerHTML.replace(',', '.'))
        var alem_balance = parseFloat(document.getElementById('alem_balance_in_kassa_table').innerHTML.replace(',', '.'))
        var internet_balance = parseFloat(document.getElementById('internet_balance_in_kassa_table').innerHTML.replace(',', '.'))
        var dop_uslugi_balance= parseFloat(document.getElementById('dop_uslugi_balance_in_kassa_table').innerHTML.replace(',', '.'))
        var kabel_balance = parseFloat(document.getElementById('kabel_balance_in_kassa_table').innerHTML.replace(',', '.'))

        // Если есть отрицательные балансы в telefon, slr, kod, zakaz и dop_uslugi то показать их в modal окне (для информативности)
        var telefonReadonlyMinus = document.getElementById('telefonReadonlyMinus')
        var slrReadonlyMinus = document.getElementById('slrReadonlyMinus')
        var kodReadonlyMinus = document.getElementById('kodReadonlyMinus')
        var zakazReadonlyMinus = document.getElementById('zakazReadonlyMinus')
        var dop_uslugiReadonlyMinus = document.getElementById('dop_uslugiReadonlyMinus')
        if (abonplata_balance < 0) {telefonReadonlyMinus.innerHTML = Math.abs(abonplata_balance)}
        if (slr_balance < 0) {slrReadonlyMinus.innerHTML = Math.abs(slr_balance)}
        if (kod_balance < 0) {kodReadonlyMinus.innerHTML = Math.abs(kod_balance)}
        if (zakaz_balance < 0) {zakazReadonlyMinus.innerHTML = Math.abs(zakaz_balance)}
        if (dop_uslugi_balance < 0) {dop_uslugiReadonlyMinus.innerHTML = Math.abs(dop_uslugi_balance)}

        if (abonplata_balance < 0 && wklad_modal_ >= Math.abs(abonplata_balance)) {
            // абонплата в modal
            prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) +  Math.abs(abonplata_balance)
            // остаток платежа в modal
            ostatok_plateja.value = (wklad_modal_ - Math.abs(abonplata_balance)).toFixed(2);
            // сумма в кассу в modal
            summa_w_kassu.value = (summa_w_kassu_ + Math.abs(abonplata_balance)).toFixed(2);


            // если ост.задол. != 0 и ост. задол. - +(-abonplata_balance) >= 0
            if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(abonplata_balance) >= 0) {
                ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - Math.abs(abonplata_balance)).toFixed(2);
                    ostatok_zadol_payModal_ -= Math.abs(abonplata_balance);
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }   
        
            if (summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(abonplata_balance) >= 0){
                summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - Math.abs(abonplata_balance)).toFixed(2);
                    summa_k_otkl_payModal_ -= Math.abs(abonplata_balance);
                } else {
                    summa_k_otkl_payModal.value  = 0;
                    summa_k_otkl_payModal_ = 0;
                }
            
            // баланс в modal
            oplata_modal_balance_input.value = (balance_modal + Math.abs(abonplata_balance)).toFixed(2);
            balance_modal += Math.abs(abonplata_balance)
            wklad_modal_ -= Math.abs(abonplata_balance)
            summa_w_kassu_ += Math.abs(abonplata_balance)
        } else {
            // Иначе если абонплата баланс в минусе и вклад < abs(-abonplata_balance)
            if (abonplata_balance < 0 && wklad_modal_ < Math.abs(abonplata_balance)) {
                prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(wklad_modal_.toFixed(2));
                ostatok_plateja.value = 0;
                summa_w_kassu.value = (summa_w_kassu_ + Math.abs(wklad_modal_)).toFixed(2);

                if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(abonplata_balance) >= 0) {
                    ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - wklad_modal_).toFixed(2);
                    ostatok_zadol_payModal_ -= wklad_modal_;
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }
                
                if ((summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(abonplata_balance) >= 0)){
                    summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - wklad_modal_).toFixed(2);
                    summa_k_otkl_payModal_ -= wklad_modal_;
                } else {
                    summa_k_otkl_payModal.value  = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                // баланс в modal
                oplata_modal_balance_input.value = (balance_modal + wklad_modal_).toFixed(2);
                balance_modal += wklad_modal_;
                summa_w_kassu_ += wklad_modal_;
                wklad_modal_ = 0;
            }
        }
        if (slr_balance < 0 && wklad_modal_ >= Math.abs(slr_balance) && wklad_modal_ != 0) {
            prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(slr_balance)
            ostatok_plateja.value = (wklad_modal_ - Math.abs(slr_balance)).toFixed(2);
            summa_w_kassu.value = (summa_w_kassu_ + Math.abs(slr_balance)).toFixed(2);
            

            if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(slr_balance) >= 0) {
                ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - Math.abs(slr_balance)).toFixed(2);
                    ostatok_zadol_payModal_ -= Math.abs(slr_balance);
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

            if (summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(slr_balance) >= 0) {
                summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - Math.abs(slr_balance)).toFixed(2);
                    summa_k_otkl_payModal_ -= Math.abs(slr_balance)
                } else {
                    summa_k_otkl_payModal.value = 0;
                    summa_k_otkl_payModal_ = 0;
                } 

            oplata_modal_balance_input.value = (balance_modal + Math.abs(slr_balance)).toFixed(2);
            balance_modal += Math.abs(slr_balance);
            wklad_modal_ -= Math.abs(slr_balance);
            summa_w_kassu_ += Math.abs(slr_balance);
        } else {
            if (slr_balance < 0 && wklad_modal_ < Math.abs(slr_balance) && wklad_modal_ != 0) {
                prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(wklad_modal_.toFixed(2));
                ostatok_plateja.value = 0;
                summa_w_kassu.value = (summa_w_kassu_ + wklad_modal_).toFixed(2);

                if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(slr_balance) >= 0) {
                    ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - wklad_modal_).toFixed(2);
                    ostatok_zadol_payModal_ -= wklad_modal_;
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

                if ((summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(slr_balance) >= 0)){
                    summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - wklad_modal_).toFixed(2);
                    summa_k_otkl_payModal_ -= wklad_modal_;
                } else {
                    summa_k_otkl_payModal.value  = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                // баланс в modal
                oplata_modal_balance_input.value = (balance_modal + wklad_modal_).toFixed(2);
                balance_modal += wklad_modal_;
                summa_w_kassu_ += wklad_modal_;
                wklad_modal_ = 0;      
            }
        }

        if (kod_balance < 0 && wklad_modal_ >= Math.abs(kod_balance) && wklad_modal_ != 0) {
            prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(kod_balance);
            ostatok_plateja.value = (wklad_modal_ - Math.abs(kod_balance)).toFixed(2);
            summa_w_kassu.value = (summa_w_kassu_ + Math.abs(kod_balance)).toFixed(2);

            if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(kod_balance) >= 0) {
                ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - Math.abs(kod_balance)).toFixed(2);
                    ostatok_zadol_payModal_ -= Math.abs(kod_balance);
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

            if (summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(kod_balance) >= 0) {
                summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - Math.abs(kod_balance)).toFixed(2);
                    summa_k_otkl_payModal_ -= Math.abs(kod_balance);
                } else {
                    summa_k_otkl_payModal.value = 0;
                    summa_k_otkl_payModal_ = 0;
                }
            
                oplata_modal_balance_input.value = (balance_modal + Math.abs(kod_balance)).toFixed(2)
            balance_modal += Math.abs(kod_balance);
            wklad_modal_ -= Math.abs(kod_balance);
            summa_w_kassu_ += Math.abs(kod_balance);
        } else {
            if (kod_balance < 0 && wklad_modal_ < Math.abs(kod_balance) && wklad_modal_ != 0) {
                prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(wklad_modal_.toFixed(2));
                ostatok_plateja.value = 0;
                summa_w_kassu.value = (summa_w_kassu_ + wklad_modal_).toFixed(2);

                if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(kod_balance) >= 0) {
                    ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - wklad_modal_).toFixed(2);
                    ostatok_zadol_payModal_ -= wklad_modal_;
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

                if ((summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(kod_balance) >= 0)){
                    summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - wklad_modal_).toFixed(2);
                    summa_k_otkl_payModal_ -= wklad_modal_;
                } else {
                    summa_k_otkl_payModal.value  = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                // баланс в modal
                oplata_modal_balance_input.value = (balance_modal + wklad_modal_).toFixed(2);
                balance_modal += wklad_modal_;
                wklad_modal_ = 0;
                summa_w_kassu_ += wklad_modal_;
                
            }
        }

        if (zakaz_balance < 0 && wklad_modal_ >= Math.abs(zakaz_balance) && wklad_modal_ != 0) {
            prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(zakaz_balance);
            ostatok_plateja.value = (wklad_modal_ - Math.abs(zakaz_balance)).toFixed(2);
            summa_w_kassu.value = (summa_w_kassu_ + Math.abs(zakaz_balance)).toFixed(2);

            if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(zakaz_balance) >= 0) {
                ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - Math.abs(zakaz_balance)).toFixed(2);
                    ostatok_zadol_payModal_ -= Math.abs(zakaz_balance);
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }
            
            if (summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(zakaz_balance) >= 0) {
                summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - Math.abs(zakaz_balance)).toFixed(2);
                    summa_k_otkl_payModal_ -= Math.abs(zakaz_balance);
                } else {
                    summa_k_otkl_payModal.value = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                oplata_modal_balance_input.value = (balance_modal + Math.abs(zakaz_balance)).toFixed(2);
            balance_modal += Math.abs(zakaz_balance);
            wklad_modal_ -= Math.abs(zakaz_balance);
            summa_w_kassu_ += Math.abs(zakaz_balance);
        } else {
            if (zakaz_balance < 0 && wklad_modal_ < Math.abs(zakaz_balance) && wklad_modal_ != 0) {
                prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(wklad_modal_.toFixed(2));
                ostatok_plateja.value = 0;
                summa_w_kassu.value = (summa_w_kassu_ + wklad_modal_).toFixed(2);

                if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(zakaz_balance) >= 0) {
                    ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - wklad_modal_).toFixed(2);
                    ostatok_zadol_payModal_ -= wklad_modal_;
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

                if ((summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(zakaz_balance) >= 0)){
                    summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - wklad_modal_).toFixed(2);
                    summa_k_otkl_payModal_ -= wklad_modal_;
                } else {
                    summa_k_otkl_payModal.value  = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                // баланс в modal
                oplata_modal_balance_input.value = (balance_modal + wklad_modal_).toFixed(2);
                balance_modal += wklad_modal_;
                wklad_modal_ = 0;
                summa_w_kassu_ += wklad_modal_;
       
            }
        }

        if (prochee_balance < 0 && wklad_modal_ >= Math.abs(prochee_balance) && wklad_modal_ != 0) {
            prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(prochee_balance);
            ostatok_plateja.value = (wklad_modal_ - Math.abs(prochee_balance)).toFixed(2);
            summa_w_kassu.value = (summa_w_kassu_ + Math.abs(prochee_balance)).toFixed(2);

            if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(prochee_balance) >= 0) {
                ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - Math.abs(prochee_balance)).toFixed(2);
                    ostatok_zadol_payModal_ -= Math.abs(prochee_balance);
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }
                
            if (summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(prochee_balance) >= 0) {
                summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - Math.abs(prochee_balance)).toFixed(2);
                    summa_k_otkl_payModal_ -= Math.abs(prochee_balance);
                } else {
                    summa_k_otkl_payModal.value = 0;
                    summa_k_otkl_payModal_ = 0;
                }
                
                oplata_modal_balance_input.value = (balance_modal + Math.abs(prochee_balance)).toFixed(2);
            balance_modal += Math.abs(prochee_balance);
            wklad_modal_ -= Math.abs(prochee_balance);
            summa_w_kassu_ += Math.abs(prochee_balance);
        } else {
            if (prochee_balance < 0 && wklad_modal_ < Math.abs(prochee_balance) && wklad_modal_ != 0) {
                prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(wklad_modal_.toFixed(2));
                ostatok_plateja.value = 0;
                summa_w_kassu.value = (summa_w_kassu_ + wklad_modal_).toFixed(2);

                if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(prochee_balance) >= 0) {
                    ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - wklad_modal_).toFixed(2);
                    ostatok_zadol_payModal_ -= wklad_modal_;
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

                if ((summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(prochee_balance) >= 0)){
                    summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - wklad_modal_).toFixed(2);
                    summa_k_otkl_payModal_ -= wklad_modal_;
                } else {
                    summa_k_otkl_payModal.value  = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                // баланс в modal
                oplata_modal_balance_input.value = (balance_modal + wklad_modal_).toFixed(2);
                balance_modal += wklad_modal_;
                wklad_modal_ = 0;
                summa_w_kassu_ += wklad_modal_;

            }
        }

        if (dop_uslugi_balance < 0 && wklad_modal_ >= Math.abs(dop_uslugi_balance) && wklad_modal_ != 0) {
            prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(dop_uslugi_balance); 
            ostatok_plateja.value = (wklad_modal_ - Math.abs(dop_uslugi_balance)).toFixed(2);
            summa_w_kassu.value = (summa_w_kassu_ + Math.abs(dop_uslugi_balance)).toFixed(2);

            if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(dop_uslugi_balance) >= 0) {
                ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - Math.abs(dop_uslugi_balance)).toFixed(2);
                    ostatok_zadol_payModal_ -= Math.abs(dop_uslugi_balance);
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

            if (summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(dop_uslugi_balance) >= 0) {
                summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - Math.abs(dop_uslugi_balance)).toFixed(2);
                    summa_k_otkl_payModal_ -= Math.abs(dop_uslugi_balance);    
                } else {
                    summa_k_otkl_payModal.value = 0;
                    summa_k_otkl_payModal_ = 0;
                }
            
                oplata_modal_balance_input.value = (balance_modal + Math.abs(dop_uslugi_balance)).toFixed(2);
            balance_modal += Math.abs(dop_uslugi_balance);
            wklad_modal_ -= Math.abs(dop_uslugi_balance);
            summa_w_kassu_ += Math.abs(dop_uslugi_balance);
        } else {
            if (dop_uslugi_balance < 0 && wklad_modal_ < Math.abs(dop_uslugi_balance) && wklad_modal_ != 0) {
                prochee_input_kassa.value = Math.abs(prochee_input_kassa.value) + Math.abs(wklad_modal_.toFixed(2));
                ostatok_plateja.value = 0;
                summa_w_kassu.value = (summa_w_kassu_ + wklad_modal_).toFixed(2);

                if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(dop_uslugi_balance) >= 0) {
                    ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - wklad_modal_).toFixed(2);
                    ostatok_zadol_payModal_ -= wklad_modal_;
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

                if ((summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(dop_uslugi_balance) >= 0)){
                    summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - wklad_modal_).toFixed(2);
                    summa_k_otkl_payModal_ -= wklad_modal_;
                } else {
                    summa_k_otkl_payModal.value  = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                // баланс в modal
                oplata_modal_balance_input.value = (balance_modal + wklad_modal_).toFixed(2);
                balance_modal += wklad_modal_;
                wklad_modal_ = 0;
                summa_w_kassu_ += wklad_modal_;
            }
        }

        if (internet_balance < 0 && wklad_modal_ >= Math.abs(internet_balance) && wklad_modal_ != 0) {
            internet_input_kassa.value = Math.abs(internet_balance);
            ostatok_plateja.value = (wklad_modal_ - Math.abs(internet_balance)).toFixed(2);
            summa_w_kassu.value = (summa_w_kassu_ + Math.abs(internet_balance)).toFixed(2);

            if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(internet_balance) >= 0) {
                ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - Math.abs(internet_balance)).toFixed(2);
                    ostatok_zadol_payModal_ -= Math.abs(internet_balance);
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

            if (summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(internet_balance) >= 0) {
                summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - Math.abs(internet_balance)).toFixed(2);
                    summa_k_otkl_payModal_ -= Math.abs(internet_balance);    
                } else {
                    summa_k_otkl_payModal.value = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                oplata_modal_balance_input.value = (balance_modal + Math.abs(internet_balance)).toFixed(2);
            balance_modal += Math.abs(internet_balance);
            wklad_modal_ -= Math.abs(internet_balance);
            summa_w_kassu_ += Math.abs(internet_balance);
        } else {
            if (internet_balance < 0 && wklad_modal_ < Math.abs(internet_balance) && wklad_modal_ != 0) {
                internet_input_kassa.value = wklad_modal_.toFixed(2);
                ostatok_plateja.value = 0;
                summa_w_kassu.value = (summa_w_kassu_ + wklad_modal_).toFixed(2);

                if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(internet_balance) >= 0) {
                    ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - wklad_modal_).toFixed(2);
                    ostatok_zadol_payModal_ -= wklad_modal_;
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }

                if ((summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(internet_balance) >= 0)){
                    summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - wklad_modal_).toFixed(2);
                    summa_k_otkl_payModal_ -= wklad_modal_;
                } else {
                    summa_k_otkl_payModal.value  = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                // баланс в modal
                oplata_modal_balance_input.value = (balance_modal + wklad_modal_).toFixed(2);
                balance_modal += wklad_modal_;
                wklad_modal_ = 0;
                summa_w_kassu_ += wklad_modal_;
                
            }
        }

        // Теперь кабельное не платят в кассе для кабельного новая база поэтому нижние 30-40 строк кода в комментарии
        // if (kabel_balance < 0 && wklad_modal_ >= Math.abs(kabel_balance) && wklad_modal_ != 0) {
        //     kabel_input_kassa.value = Math.abs(kabel_balance); 
        //     ostatok_plateja.value = (wklad_modal_ - Math.abs(kabel_balance)).toFixed(2);
        //     summa_w_kassu.value = (summa_w_kassu_ + Math.abs(kabel_balance)).toFixed(2);

        //     if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(kabel_balance) >= 0) {
        //         ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - Math.abs(kabel_balance)).toFixed(2);
        //             ostatok_zadol_payModal_ -= Math.abs(kabel_balance);
        //         } else {
        //             ostatok_zadol_payModal.value = 0;
        //             ostatok_zadol_payModal_ = 0;
        //         }
            
        //     if (summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(kabel_balance) >= 0) {
        //         summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - Math.abs(kabel_balance)).toFixed(2);
        //             summa_k_otkl_payModal_ -= Math.abs(kabel_balance);    
        //         } else {
        //             summa_k_otkl_payModal.value = 0;
        //             summa_k_otkl_payModal_ = 0;
        //         }

        //         oplata_modal_balance_input.value = (balance_modal + Math.abs(kabel_balance)).toFixed(2);
        //     balance_modal += Math.abs(kabel_balance);
        //     wklad_modal_ -= Math.abs(kabel_balance);
        //     summa_w_kassu_ += Math.abs(kabel_balance);
        // } else {
        //     if (kabel_balance < 0 && wklad_modal_ < Math.abs(kabel_balance) && wklad_modal_ != 0) {
        //         kabel_input_kassa.value = wklad_modal_.toFixed(2); 
        //         ostatok_plateja.value = 0;
        //         summa_w_kassu.value = (summa_w_kassu_ + wklad_modal_).toFixed(2);

        //         if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(kabel_balance) >= 0) {
        //             ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - wklad_modal_).toFixed(2);
        //             ostatok_zadol_payModal_ -= wklad_modal_;
        //         } else {
        //             ostatok_zadol_payModal.value = 0;
        //             ostatok_zadol_payModal_ = 0;
        //         }
                
        //         if ((summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(kabel_balance) >= 0)){
        //             summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - wklad_modal_).toFixed(2);
        //             summa_k_otkl_payModal_ -= wklad_modal_;
        //         } else {
        //             summa_k_otkl_payModal.value  = 0;
        //             summa_k_otkl_payModal_ = 0;
        //         }

        //         // баланс в modal
        //         oplata_modal_balance_input.value = (balance_modal + wklad_modal_).toFixed(2);
        //         balance_modal += wklad_modal_;
        //         wklad_modal_ = 0;
        //         summa_w_kassu_ += wklad_modal_;
        //     }
        // }


        if (alem_balance < 0 && wklad_modal_ >= Math.abs(alem_balance) && wklad_modal_ != 0) {
            alem_input_kassa.value = Math.abs(alem_balance);
            ostatok_plateja.value = (wklad_modal_ - Math.abs(alem_balance)).toFixed(2);
            summa_w_kassu.value = (summa_w_kassu_ + Math.abs(alem_balance)).toFixed(2);
    
            if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(alem_balance) >= 0) {
                ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - Math.abs(alem_balance)).toFixed(2);
                    ostatok_zadol_payModal_ -= Math.abs(alem_balance);    
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0
                }

            if (summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(alem_balance) >= 0) {
                summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - Math.abs(alem_balance)).toFixed(2);
                    summa_k_otkl_payModal_ -= Math.abs(alem_balance);
                } else {
                    summa_k_otkl_payModal.value = 0;
                    summa_k_otkl_payModal_ = 0;
                }
    
                oplata_modal_balance_input.value = (balance_modal + Math.abs(alem_balance)).toFixed(2);
            balance_modal += Math.abs(alem_balance);
            wklad_modal_ -= Math.abs(alem_balance);
            summa_w_kassu_ += Math.abs(alem_balance);

        } else {
            if (alem_balance < 0 && wklad_modal_ < Math.abs(alem_balance) && wklad_modal_ > 0) {
                alem_input_kassa.value = wklad_modal_.toFixed(2); 
                ostatok_plateja.value = 0;
                summa_w_kassu.value = (summa_w_kassu_ + wklad_modal_).toFixed(2);

                if (ostatok_zadol_payModal_ != 0 && ostatok_zadol_payModal_ - Math.abs(alem_balance) >= 0) {
                    ostatok_zadol_payModal.value = (ostatok_zadol_payModal_ - wklad_modal_).toFixed(2);
                    ostatok_zadol_payModal_ -= wklad_modal_;
                } else {
                    ostatok_zadol_payModal.value = 0;
                    ostatok_zadol_payModal_ = 0;
                }
                
                if ((summa_k_otkl_payModal_ != 0 && summa_k_otkl_payModal_ - Math.abs(alem_balance) >= 0)){
                    summa_k_otkl_payModal.value = (summa_k_otkl_payModal_ - wklad_modal_).toFixed(2);
                    summa_k_otkl_payModal_ -= wklad_modal_;
                } else {
                    summa_k_otkl_payModal.value  = 0;
                    summa_k_otkl_payModal_ = 0;
                }

                // баланс в modal
                oplata_modal_balance_input.value = (balance_modal + wklad_modal_).toFixed(2);
                balance_modal += wklad_modal_;
                wklad_modal_ = 0;
                summa_w_kassu_ += wklad_modal_;               
            }
        }
    

        /* ############################################
        Все баланс минусы сделать 0 в modal окне END ##
            ############################################
        */
    })

    // Если модальное окно закрылась
    myModal.addEventListener('hidden.bs.modal', function () {
    document.getElementById("wklad_input").readOnly = false;

    // Отправка пост запроса с номеров по новой для обновления страницы и распределения денег с прочено на отрицательные балансы telefon, slr, kod, zakaz, dop_uslugi если есть
    var form = document.getElementById('formForRefreshKassaWithNumber');
    form.submit();
   

    // document.getElementById("wklad_input").value = 0;
    // var abonplata_balance = parseFloat(document.getElementById('abonent_balance_in_kassa_table').innerHTML.replace(',', '.'))
    // var slr_balance = parseFloat(document.getElementById('slr_balance_in_kassa_table').innerHTML.replace(',', '.'))
    // var kod_balance = parseFloat(document.getElementById('kod_balance_in_kassa_table').innerHTML.replace(',', '.'))
    // var zakaz_balance = parseFloat(document.getElementById('zakaz_balance_in_kassa_table').innerHTML.replace(',', '.'))
    // var prochee_balance = parseFloat(document.getElementById('prochee_balance_in_kassa_table').innerHTML.replace(',', '.'))
    // var alem_balance = parseFloat(document.getElementById('alem_balance_in_kassa_table').innerHTML.replace(',', '.'))
    // var internet_balance = parseFloat(document.getElementById('internet_balance_in_kassa_table').innerHTML.replace(',', '.'))
    // var dop_uslugi_balance= parseFloat(document.getElementById('dop_uslugi_balance_in_kassa_table').innerHTML.replace(',', '.'))
    // var kabel_balance = parseFloat(document.getElementById('kabel_balance_in_kassa_table').innerHTML.replace(',', '.'))
    // abonplata_balance.value = 0
    // slr_balance.value = 0
    // kod_balance.value = 0
    // zakaz_balance.value = 0
    // prochee_balance.value = 0
    // alem_balance.value = 0
    // internet_balance.value = 0
    // dop_uslugi_balance.value = 0
    // kabel_balance.value = 0

    document.getElementById('summa_w_kassu').value = ''
    // location.reload();


})
/* ###################################################
При активации модального окна касса oplataModal END ##
    ###################################################
*/
    
/* ########################################################################
Матиматические вычисления в Input-ах oplataModal при введени в них чесел ##
    ########################################################################
*/
    function cloneWklad() {
        document.getElementById('wklad_modal').value = document.getElementById('wklad_input').value
        document.getElementById('ostatok_plateja').value = document.getElementById('wklad_input').value
    }
    
    function mathCalculate() {
    
        var wklad_input = parseFloat(document.getElementById('wklad_input').value)
    
        if (document.getElementById('abonplata_input_kassa').value == '') {var abonplata = 0} else {
            var abonplata = parseFloat(document.getElementById('abonplata_input_kassa').value)
        }
    
        if (document.getElementById('slr_input_kassa').value == '') {var slr = 0} else {
            var slr = parseFloat(document.getElementById('slr_input_kassa').value)
        }
    
        if (document.getElementById('kod_input_kassa').value == '') {var kod = 0} else {
            var kod = parseFloat(document.getElementById('kod_input_kassa').value)
        }
    
        if (document.getElementById('zakaz_input_kassa').value == '') {var zakaz = 0} else {
            var zakaz = parseFloat(document.getElementById('zakaz_input_kassa').value)
        }
    
        if (document.getElementById('prochee_input_kassa').value == '') {var prochee = 0} else {
            var prochee = parseFloat(document.getElementById('prochee_input_kassa').value)
        }
    
        if (document.getElementById('alem_input_kassa').value == '') {var alem = 0} else {
            var alem = parseFloat(document.getElementById('alem_input_kassa').value)
        }
    
        if (document.getElementById('internet_input_kassa').value == '') {var internet = 0} else {
            var internet = parseFloat(document.getElementById('internet_input_kassa').value)
        }
    
        if (document.getElementById('dop_uslugi_input_kassa').value == '') {var uslugi = 0} else {
            var uslugi = parseFloat(document.getElementById('dop_uslugi_input_kassa').value)
        }
    
        if (document.getElementById('kabel_input_kassa').value == '') {var kabel = 0} else {
            var kabel = parseFloat(document.getElementById('kabel_input_kassa').value)
        }
    
        // Код для изменения сумма в кассу в реальном времени
        document.getElementById('summa_w_kassu').value = (abonplata + slr + kod + zakaz + prochee + alem + internet + uslugi + kabel).toFixed(2);
        document.getElementById('ostatok_plateja').value = (wklad_input - parseFloat(document.getElementById('summa_w_kassu').value)).toFixed(2);

        // Код для изменения баланс в модалке в реальном времени
        var balance_total_var = parseFloat(document.getElementById('kassa_balance_in_pay_row').value.replace(',', '.'))
        document.getElementById('oplata_modal_balance_input').value = (balance_total_var + abonplata + slr + kod + zakaz + prochee + alem + internet + uslugi + kabel).toFixed(2);

        var ostatok_zadol_payRow_var = Math.abs(parseFloat(document.getElementById('kassa__zadol_pay_row').value))
        if ((ostatok_zadol_payRow_var - abonplata - slr - kod - zakaz - prochee - alem - internet - uslugi - kabel) > 0) {
            document.getElementById('ostatok_zadol_payModal').value = (ostatok_zadol_payRow_var - abonplata - slr - kod - zakaz - prochee - alem - internet - uslugi - kabel).toFixed(2);
        } else{
            document.getElementById('ostatok_zadol_payModal').value = 0
        }

        var summa_k_otkl_payRow_var = Math.abs(parseFloat(document.getElementById('summa_k_otkl_payRow').value))
        if ((summa_k_otkl_payRow_var - abonplata - slr - kod - zakaz - prochee - alem - internet - uslugi - kabel) > 0) {
            document.getElementById('summa_k_otkl_payModal').value = (summa_k_otkl_payRow_var - abonplata - slr - kod - zakaz - prochee - alem - internet - uslugi - kabel).toFixed(2);
        } else{
            document.getElementById('summa_k_otkl_payModal').value = 0
        }

        

        

        // изменения backgraund color в ostatok_plateja И summa_w_kassu в oplataModal
        if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == '0') {
            document.getElementById('ostatok_plateja').classList.add('my-bg-green')
            document.getElementById('summa_w_kassu').classList.add('my-bg-green')
    
            document.getElementById('ostatok_plateja').classList.remove('my-bg-red')
            document.getElementById('summa_w_kassu').classList.remove('my-bg-red')
        } else {
            document.getElementById('ostatok_plateja').classList.remove('my-bg-green')
            document.getElementById('summa_w_kassu').classList.remove('my-bg-green')
    
            document.getElementById('ostatok_plateja').classList.add('my-bg-red')
            document.getElementById('summa_w_kassu').classList.add('my-bg-red')
        }
    
    }
/* ############################################################################
Матиматические вычисления в Input-ах oplataModal при введени в них чесел END ##
    ############################################################################
*/
}


// текущий url в виде строки
var currentLocation = window.location.href;
// если в текущем url есть подстрока receipts то выполнить код
if (currentLocation.indexOf("receipts") >= 0) {

/* #########################################
rePrint повторная печать квитанции (чека) ##
    #########################################
*/
function rePrint(id) {  
var y = document.getElementsByClassName(id);

var print_etrap = y[0].innerHTML

var print_kw_nomer = y[1].innerHTML
var print_kw_date = y[2].innerHTML
var print_name_suname_telefon = y[3].innerHTML

var print_telefon = y[4].innerHTML
var print_slr = y[5].innerHTML
var print_kod = y[6].innerHTML
var print_zakaz = y[7].innerHTML
var print_prochee = y[8].innerHTML
var print_alem = y[9].innerHTML
var print_internet = y[10].innerHTML
var print_dop_uslugi = y[11].innerHTML
var print_kabel = y[12].innerHTML
var print_oplata_sum = y[13].innerHTML
var print_kassir = y[14].innerHTML

var myWindow = window.open('', 'my div', 'height=300,width=400,font-size=9');
myWindow.document.write('<div style=font-size:10px;>'+print_etrap+' WEAK</div>');
myWindow.document.write('<div style=font-size:10px;>'+ print_kw_nomer +'</div>');
myWindow.document.write('<div style=font-size:10px;>'+ print_kw_date +'</div>');
myWindow.document.write('<div style=font-size:10px;>'+print_name_suname_telefon+'</div>');
myWindow.document.write('-----------------------------');
myWindow.document.write('<div style=font-size:10px;padding-left:60px;>tolenen - galany</div>');   
myWindow.document.write('-----------------------------');
if (print_telefon != '0,0' ){myWindow.document.write('<div style=font-size:10px;>Абонплата '+'<span style=font-size:10px;padding-left:20px>'+print_telefon+'</span>'+'</div>');}
if (print_slr != '0,0'){myWindow.document.write('<div style=font-size:10px;>СЛР '+'<span style=font-size:10px;padding-left:47px>'+print_slr+'</span>'+'</div>');}    
if (print_kod != '0,0'){myWindow.document.write('<div style=font-size:10px;>КОД '+'<span style=font-size:10px;padding-left:46px>'+print_kod+'</span>'+'</div>');}
if (print_zakaz != '0,0'){myWindow.document.write('<div style=font-size:10px;>Заказ '+'<span style=font-size:10px;padding-left:43px>'+print_zakaz+'</span>'+'</div>');}
if (print_prochee != '0,0'){myWindow.document.write('<div style=font-size:10px;>Прочее '+'<span style=font-size:10px;padding-left:35px>'+print_prochee+'</span>'+'</div>');}
if (print_alem != '0,0'){myWindow.document.write('<div style=font-size:10px;>Alem TV '+'<span style=font-size:10px;padding-left:28px>'+print_alem+'</span>'+'</div>');}
if (print_internet != '0,0'){myWindow.document.write('<div style=font-size:10px;>Интернет '+'<span style=font-size:10px;padding-left:25px>'+print_internet+'</span>'+'</div>');}
if (print_dop_uslugi != '0,0'){myWindow.document.write('<div style=font-size:10px;>Доп.Услуги '+'<span style=font-size:10px;padding-left:17px>'+print_dop_uslugi+'</span>'+'</div>');}
if (print_kabel != '0,0'){myWindow.document.write('<div style=font-size:10px;>Кабель '+'<span style=font-size:10px;padding-left:37px>'+print_kabel+'</span>'+'</div>');}
myWindow.document.write('-----------------------------');
myWindow.document.write('<div style=font-size:10px;>Jemi: <span style=font-size:10px;padding-left:45px>'+print_oplata_sum+'</span></div>');
myWindow.document.write('<div style=font-size:10px;>'+print_kassir+'</div>');
myWindow.document.write('<br>');
myWindow.document.write('<div style=font-size:10px;>Gaznachy __________________</div>');
myWindow.focus(); // necessary for IE >= 10
myWindow.print();
myWindow.close();
}

/* #############################################
rePrint повторная печать квитанции (чека) END ##
################################################
*/

/*дефис (цере) между цифрами телефона при вводе номера kassa-receipt*/
(function () {
document
    .getElementById("search_number_receipt")
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











/*
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################
*/

/*############################################
Kassa rezerw
##############################################*/


   
// текущий url в виде строки
var currentLocation = window.location.href;
// если в текущем url есть подстрока kassa-rezerw-index то выполнить код
if (currentLocation.indexOf("kassa-rezerw-index") >= 0) {

/* ######################################################################
    В input-ах modal окна kassa index при клике менять bg на оранжевый ##
    ######################################################################
*/

function onClickChangeBgAbonplata(){
    document.getElementById('abonplata_input_kassa').classList.add('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgSlr(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.add('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgKod(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.add('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgZakaz(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.add('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgProchee(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.add('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgAlem(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.add('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgInternet(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.add('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgDop_uslugi(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.add('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}
function onClickChangeBgKabel(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.add('my-bg-orange')
}
function onClickChangeAllModalInputBg(){
    document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
    document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
}

/* ##########################################################################
    В input-ах modal окна kassa index при клике менять bg на оранжевый END ##
    ##########################################################################
*/

/* ############################################
kassa input on click change background color ##
    ############################################
*/
function onClickOnWkladKassa(){ 
    document.getElementById("wklad_input").classList.add('my-bg-orange');
    document.getElementById("search_number").classList.remove('my-bg-orange');
}

function onClickOnSerachKassa(){ 
    document.getElementById("wklad_input").classList.remove('my-bg-orange');
    document.getElementById("search_number").classList.add('my-bg-orange');
}
/* ################################################
kassa input on click change background color END ##
    ################################################
*/

/* ####################################
Печать квитанции (чека) после оплаты ##
    ####################################
*/
if (document.getElementById('printReceipt').innerHTML == 'yes') {
    var print_telefon = document.getElementById('print_telefon').innerHTML;
    var print_slr = document.getElementById('print_slr').innerHTML;
    var print_kod = document.getElementById('print_kod').innerHTML;
    var print_zakaz = document.getElementById('print_zakaz').innerHTML;
    var print_prochee = document.getElementById('print_prochee').innerHTML;
    var print_alem = document.getElementById('print_alem').innerHTML;
    var print_internet = document.getElementById('print_internet').innerHTML;
    var print_dop_uslugi = document.getElementById('print_dop_uslugi').innerHTML;
    var print_kabel = document.getElementById('print_kabel').innerHTML;

    var print_etrap = document.getElementById('print_etrap').innerHTML;
    var print_name_suname_telefon = document.getElementById('print_name_suname_telefon').innerHTML;
    var print_kw_date = document.getElementById('print_kw_date').innerHTML;
    var print_kassir = document.getElementById('print_kassir').innerHTML;
    var print_oplata_sum = document.getElementById('print_oplata_sum').innerHTML;
    var PC_name = document.getElementById('PC_name').innerHTML;

    var myWindow = window.open('', 'my div', 'height=300,width=400,font-size=9');
    myWindow.document.write('<div style=font-size:10px;>WEAK '+print_etrap+' ' + PC_name + '</div>');
    myWindow.document.write('<div style=font-size:10px;>kwitansiya № '+ print_kw_date +'</div>');
    myWindow.document.write('<div style=font-size:10px;>'+print_name_suname_telefon+'</div>');
    myWindow.document.write('-----------------------------');
    myWindow.document.write('<div style=font-size:10px;padding-left:60px;>tolenen - galandy</div>');   
    myWindow.document.write('-----------------------------');
    if (print_telefon != '0,0' ){myWindow.document.write('<div style=font-size:10px;>Абонплата '+'<span style=font-size:10px;padding-left:20px>'+print_telefon+'</span>'+'</div>');}
    if (print_slr != '0,0'){myWindow.document.write('<div style=font-size:10px;>СЛР '+'<span style=font-size:10px;padding-left:47px>'+print_slr+'</span>'+'</div>');}    
    if (print_kod != '0,0'){myWindow.document.write('<div style=font-size:10px;>КОД '+'<span style=font-size:10px;padding-left:46px>'+print_kod+'</span>'+'</div>');}
    if (print_zakaz != '0,0'){myWindow.document.write('<div style=font-size:10px;>Заказ '+'<span style=font-size:10px;padding-left:43px>'+print_zakaz+'</span>'+'</div>');}
    if (print_prochee != '0,0'){myWindow.document.write('<div style=font-size:10px;>Прочее '+'<span style=font-size:10px;padding-left:35px>'+print_prochee+'</span>'+'</div>');}
    if (print_alem != '0,0'){myWindow.document.write('<div style=font-size:10px;>Alem TV '+'<span style=font-size:10px;padding-left:28px>'+print_alem+'</span>'+'</div>');}
    if (print_internet != '0,0'){myWindow.document.write('<div style=font-size:10px;>Интернет '+'<span style=font-size:10px;padding-left:25px>'+print_internet+'</span>'+'</div>');}
    if (print_dop_uslugi != '0,0'){myWindow.document.write('<div style=font-size:10px;>Доп.Услуги '+'<span style=font-size:10px;padding-left:17px>'+print_dop_uslugi+'</span>'+'</div>');}
    if (print_kabel != '0,0'){myWindow.document.write('<div style=font-size:10px;>Кабель '+'<span style=font-size:10px;padding-left:37px>'+print_kabel+'</span>'+'</div>');}
    myWindow.document.write('-----------------------------');
    myWindow.document.write('<div style=font-size:10px;>Jemi: <span style=font-size:10px;padding-left:45px>'+print_oplata_sum+'</span></div>');
    myWindow.document.write('<div style=font-size:10px;>Maglumat: '+print_kassir+'</div>');
    myWindow.document.write('<div style=font-size:10px;>Gaznachy __________________</div>');
    myWindow.focus(); // necessary for IE >= 10
    myWindow.print();
    myWindow.close();
}
/* ########################################
Печать квитанции (чека) после оплаты END ##
    ########################################
*/

/* ################################################################################
Запрет платежа при определенных условиях (например если в абонплате ввели букву) ##
    ################################################################################
*/
function stopSubmit() {
    // Если в абонплате есть буквы то запретить оплату
    if (!Number(document.getElementById('abonplata_input_kassa').value) && document.getElementById('abonplata_input_kassa').value != ''|| parseFloat(document.getElementById('abonplata_input_kassa').value) < 0) {
        event.preventDefault()
    }
    if (!Number(document.getElementById('slr_input_kassa').value) && document.getElementById('slr_input_kassa').value != '' || parseFloat(document.getElementById('slr_input_kassa').value) < 0) {
        event.preventDefault()
    }
    if (!Number(document.getElementById('kod_input_kassa').value) && document.getElementById('kod_input_kassa').value != '' || parseFloat(document.getElementById('kod_input_kassa').value) < 0) {
        event.preventDefault()
    }
    if (!Number(document.getElementById('zakaz_input_kassa').value) && document.getElementById('zakaz_input_kassa').value != '' || parseFloat(document.getElementById('zakaz_input_kassa').value) < 0) {
        event.preventDefault()
    }
    if (!Number(document.getElementById('prochee_input_kassa').value) && document.getElementById('prochee_input_kassa').value != '' || parseFloat(document.getElementById('prochee_input_kassa').value) < 0) {
        event.preventDefault()
    }
    if (!Number(document.getElementById('alem_input_kassa').value) && document.getElementById('alem_input_kassa').value != '' || parseFloat(document.getElementById('alem_input_kassa').value) < 0) {
        event.preventDefault()
    }
    if (!Number(document.getElementById('internet_input_kassa').value) && document.getElementById('internet_input_kassa').value != '' || parseFloat(document.getElementById('internet_input_kassa').value) < 0) {
        event.preventDefault()
    }
    if (!Number(document.getElementById('dop_uslugi_input_kassa').value) && document.getElementById('dop_uslugi_input_kassa').value != '' || parseFloat(document.getElementById('dop_uslugi_input_kassa').value) < 0) {
        event.preventDefault()
    }
    if (!Number(document.getElementById('kabel_input_kassa').value) && document.getElementById('kabel_input_kassa').value != '' || parseFloat(document.getElementById('kabel_input_kassa').value) < 0) {
        event.preventDefault()
    }

    // Если в остаток платежа не 0 (т. е. если в кассу не попала вся сумма которую вложил абонент или если в кассу попала сумма больше чем вложил абонент то запретить оплату)
    if (parseFloat(document.getElementById('ostatok_plateja').value) != 0 || parseFloat(document.getElementById('ostatok_plateja').value) < 0) {
        event.preventDefault()
    }

        /* ####################################################################################
        Запрет платежа при определенных условиях (например если в абонплате ввели букву) END ##
        #######################################################################################
        */

    }


/* ########################################################
код для показа общего баланса в баланс в касса userTable ##
    ########################################################
*/
var abonplata_balance_kassa = parseFloat(document.getElementById('abonent_balance_in_kassa_table').innerHTML.replace(',', '.'))
var slr_balance_kassa = parseFloat(document.getElementById('slr_balance_in_kassa_table').innerHTML.replace(',', '.'))
var kod_balance_kassa = parseFloat(document.getElementById('kod_balance_in_kassa_table').innerHTML.replace(',', '.'))
var zakaz_balance_kassa = parseFloat(document.getElementById('zakaz_balance_in_kassa_table').innerHTML.replace(',', '.'))
var prochee_balance_kassa = parseFloat(document.getElementById('prochee_balance_in_kassa_table').innerHTML.replace(',', '.'))
var alem_balance_kassa = parseFloat(document.getElementById('alem_balance_in_kassa_table').innerHTML.replace(',', '.'))
var internet_balance_kassa = parseFloat(document.getElementById('internet_balance_in_kassa_table').innerHTML.replace(',', '.'))
var dop_uslugi_balance_kassa = parseFloat(document.getElementById('dop_uslugi_balance_in_kassa_table').innerHTML.replace(',', '.'))
var kabel_balance_kassa = parseFloat(document.getElementById('kabel_balance_in_kassa_table').innerHTML.replace(',', '.'))

// для Input Баланс в pay row Kassa index
document.getElementById('kassa_balance_in_pay_row').value 
            = 
            abonplata_balance_kassa
            +
            slr_balance_kassa
            +
            kod_balance_kassa
            +
            zakaz_balance_kassa
            +
            prochee_balance_kassa
            +
            alem_balance_kassa
            +
            internet_balance_kassa
            +
            dop_uslugi_balance_kassa
            +
            kabel_balance_kassa;

// для Input Задолженность в pay row Kassa index
if (abonplata_balance_kassa < 0){var zadolAbonplata = abonplata_balance_kassa} else {var zadolAbonplata = 0}
if (slr_balance_kassa < 0){var zadolSlr = slr_balance_kassa} else {var zadolSlr = 0}
if (kod_balance_kassa < 0){var zadolKod = kod_balance_kassa} else {var zadolKod = 0}
if (zakaz_balance_kassa < 0){var zadolZakaz = zakaz_balance_kassa} else {var zadolZakaz = 0}
if (prochee_balance_kassa < 0){var zadolProchee = prochee_balance_kassa} else {var zadolProchee = 0}
if (alem_balance_kassa < 0){var zadolAlem = alem_balance_kassa} else {var zadolAlem = 0}
if (internet_balance_kassa < 0){var zadolinternet = internet_balance_kassa} else {var zadolinternet = 0}
if (dop_uslugi_balance_kassa < 0){var zadolDop_uslugi = dop_uslugi_balance_kassa} else {var zadolDop_uslugi = 0}
if (kabel_balance_kassa < 0){var zadolkabel = kabel_balance_kassa} else {var zadolkabel = 0};

document.getElementById('kassa__zadol_pay_row').value = zadolAbonplata + zadolSlr + zadolKod + zadolZakaz + zadolProchee + zadolAlem + zadolinternet +  zadolDop_uslugi + zadolkabel;

            




/* ############################################################
код для показа общего баланса в баланс в касса userTable END ##
    ############################################################
*/


    /*фецис (цере) между цифрами телефона при вводе номера kassa-index*/
    (function () {
    document
        .getElementById("search_number")
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
        // document.getElementById("search_number").select();

        

    // // Если найден номер свободный или ошибка то опять выделить search_number
    // if (document.getElementById("kassa_surname_input").innerHTML == '' || document.getElementById("kassa_name_input").innerHTML == '') {
    //     document.getElementById("search_number").classList.add('my-bg-orange');
    //     document.getElementById("search_number").select();
    // } else {
    // //   Иначе если найден номер то выделить Input wklad
    //     document.getElementById("wklad_input").select();
    //     document.getElementById("search_number").classList.remove('my-bg-orange');
    //     document.getElementById('wklad_input').classList.add('my-bg-orange')
    // }
    });
    
    // функция для проверки есть ли в тексте пробел
    function hasWhiteSpace(str) {
    if (str.indexOf(' ') >= 0) {
        return true
    } else {
        return false
    }
    }
    
/* #################################################
код для запрета ввода пробела в касса модал input ##
    #################################################
*/
    var abonplata_taboo_space = document.getElementById('abonplata_input_kassa');
    var slr_taboo_space = document.getElementById('slr_input_kassa');
    var kod_taboo_space = document.getElementById('kod_input_kassa');
    var zakaz_taboo_space = document.getElementById('zakaz_input_kassa');
    var prochee_taboo_space = document.getElementById('prochee_input_kassa');
    var alem_taboo_space = document.getElementById('alem_input_kassa');
    var internet_taboo_space = document.getElementById('internet_input_kassa');
    var dop_uslugi_taboo_space = document.getElementById('dop_uslugi_input_kassa');
    var kabel_taboo_space = document.getElementById('kabel_input_kassa');
    
    // Запрет ввода пробела в abonplata Input в модалке кассы
    abonplata_taboo_space.oninput = () => {
    if(hasWhiteSpace(abonplata_taboo_space.value)) {
        document.getElementById('abonplata_input_kassa').value = abonplata_taboo_space.value.split(' ').join('')
    }

    
    }
    
    slr_taboo_space.oninput = () => {
    if(hasWhiteSpace(slr_taboo_space.value)) {
        document.getElementById('slr_input_kassa').value = slr_taboo_space.value.split(' ').join('')
    }
    }
    
    kod_taboo_space.oninput = () => {
    if(hasWhiteSpace(kod_taboo_space.value)) {
        document.getElementById('kod_input_kassa').value = kod_taboo_space.value.split(' ').join('')
    }
    }
    
    zakaz_taboo_space.oninput = () => {
    if(hasWhiteSpace(zakaz_taboo_space.value)) {
        document.getElementById('zakaz_input_kassa').value = zakaz_taboo_space.value.split(' ').join('')
    }
    }
    
    prochee_taboo_space.oninput = () => {
    if(hasWhiteSpace(prochee_taboo_space.value)) {
        document.getElementById('prochee_input_kassa').value = prochee_taboo_space.value.split(' ').join('')
    }
    }
    
    alem_taboo_space.oninput = () => {
    if(hasWhiteSpace(alem_taboo_space.value)) {
        document.getElementById('alem_input_kassa').value = alem_taboo_space.value.split(' ').join('')
    }
    }
    
    internet_taboo_space.oninput = () => {
    if(hasWhiteSpace(internet_taboo_space.value)) {
        document.getElementById('internet_input_kassa').value = internet_taboo_space.value.split(' ').join('')
    }
    }
    
    dop_uslugi_taboo_space.oninput = () => {
    if(hasWhiteSpace(dop_uslugi_taboo_space.value)) {
        document.getElementById('dop_uslugi_input_kassa').value = dop_uslugi_taboo_space.value.split(' ').join('')
    }
    }
    
    kabel_taboo_space.oninput = () => {
    if(hasWhiteSpace(kabel_taboo_space.value)) {
        document.getElementById('kabel_input_kassa').value = kabel_taboo_space.value.split(' ').join('')
    }
    }
/* #####################################################
код для запрета ввода пробела в касса модал input END ##
    #####################################################
*/
    
    
/* ######################
input-ы в касса индекс ##
    ######################
*/
    // Input поиска по номеру
    (function() {
        document.getElementById('search_number').addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {
            // Если поиска по номеру нажал вниз то переход в Input вклад
            var wklad_input = document.getElementById('wklad_input');
            document.getElementById('search_number').classList.remove('my-bg-orange')
            document.getElementById('wklad_input').classList.add('my-bg-orange')
            wklad_input.focus();
            }  
        if (e.keyCode === 46) {
            // Если нажал на delete то удалить все в inpute поиск по номеру
            var search_number = document.getElementById('search_number');
            search_number.value = '';
            search_number.focus();
            }         
        });
    })();
    
    // Input вклад
    (function() {
        document.getElementById('wklad_input').addEventListener('keydown', function(e) {
        if (e.keyCode === 38) {  
            // если с вклада нажал вверх то переход в Input поиска по номеру
            var search_number = document.getElementById('search_number');
            document.getElementById("wklad_input").classList.remove('my-bg-orange');
            document.getElementById("search_number").classList.add('my-bg-orange');
            e.preventDefault()
            document.getElementById('search_number').select();
            } 
        if (e.keyCode === 13) {  
            // Если нажал на enter то открыть oplataModal
            var oplata_input = document.getElementById('oplata_input');

            // Когда нажимеешь на enter в wklad_input то во время открития модального окна 
            // можно добавлять еще символы (если случайно нажать) (запрещием добавления нового символа после нажатия на enter)
            if (parseFloat(document.getElementById("wklad_input").value) > 0 ) {
            document.getElementById("wklad_input").readOnly = true
            }
            


            // проверка вклада input в касса (нет ли там буквы и больше ли 0 вклад) 
            if (Number(document.getElementById('wklad_input').value)) {
            if (parseFloat(document.getElementById('wklad_input').value) > 0) {
                oplata_input.click();
            } else {
                event.preventDefault()
            }
            } else {
            event.preventDefault()
            }
            } 

        });
    })();
    
    // Input оплатить
    (function() {
        document.getElementById('oplata_input').addEventListener('keydown', function(e) {
        if (e.keyCode === 38) {  
            // если с Input оплатить нажал вверх то переход в Input поиска по номеру
            var search_number = document.getElementById('search_number');
            search_number.focus();
            }
    
        if (e.keyCode === 39) {  
            // если с Input оплатить нажал на право то переход в Input вклад
            var wklad_input = document.getElementById('wklad_input');
            wklad_input.focus();
            }
        });
    })();
/* ##########################
input-ы в касса индекс END ##
    ##########################
*/
    
    
/* #####################
input-ы в oplataModal ##
    #####################
*/
    // Input abonplata_input_kassa
    (function() {
        document.getElementById('abonplata_input_kassa').addEventListener('keydown', function(e) {
    if (e.keyCode === 1) {console.log('clicked')}
        if (e.keyCode === 40) {  
            // если нажал вниз то переход к slr input
            var slr_input_kassa = document.getElementById('slr_input_kassa');
            document.getElementById('abonplata_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('slr_input_kassa').classList.add('my-bg-orange')
            slr_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться этот input
            // Если ostatok plateja пусто, значит не ввели сумму в wklad (ничего не делаем)
    
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            // иначе если wklad ввели
            } else {  
                // Если summa_w_kassu == '' или 0, то вводим то тупо все ostatok_plateja переводим в summa_w_kassu и в abonplata_input_kassa, а ostatok_plateja = 0
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
    
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('abonplata_input_kassa').value = document.getElementById('ostatok_plateja').value
    
                    document.getElementById('ostatok_plateja').value = 0
                
                // иначе если summa_w_kassu != '' или 0, то
                } else {
                    // если abonplata_input_kassa == 0 или == '', то тупо переводим все в абонплата
                    if (document.getElementById('abonplata_input_kassa').value == '' || document.getElementById('abonplata_input_kassa').value == 0) {
    
                        document.getElementById('abonplata_input_kassa').value = document.getElementById('ostatok_plateja').value
                        
                    // иначе если abonplata_input_kassa != 0 и != '', то abonplata_input_kassa += ostatok_plateja
                    } else {
    
                        var abonplata = parseFloat(document.getElementById('abonplata_input_kassa').value)
                        document.getElementById('abonplata_input_kassa').value = abonplata + parseFloat(document.getElementById('ostatok_plateja').value)
                    }
                    // и в конце в summa_w_kassu += ostatok_plateja, ostatok_plateja = 0
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
    
                }
            }
            } 
            
        });
    })();
    
    // Input slr_input_kassa
    (function() {
        document.getElementById('slr_input_kassa').addEventListener('keydown', function(e) {
    
        if (e.keyCode === 40) {  
            // вниз переход в kod input
            var kod_input_kassa = document.getElementById('kod_input_kassa');
            document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('kod_input_kassa').classList.add('my-bg-orange')
            kod_input_kassa.select();
            e.preventDefault();
            }
        
        if (e.keyCode === 38) {  
            // вверх переход в abonplata input
            var abonplata_input_kassa = document.getElementById('abonplata_input_kassa');
            document.getElementById('slr_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('abonplata_input_kassa').classList.add('my-bg-orange')
            abonplata_input_kassa.select();
            e.preventDefault();
            }
            
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('slr_input_kassa').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('slr_input_kassa').value == '' || document.getElementById('slr_input_kassa').value == 0) {
                        document.getElementById('slr_input_kassa').value = document.getElementById('ostatok_plateja').value
                    } else {
                        var slr = parseFloat(document.getElementById('slr_input_kassa').value)
                        document.getElementById('slr_input_kassa').value = slr + parseFloat(document.getElementById('ostatok_plateja').value)
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
        });
    })();
    
    // Input kod_input_kassa
    (function() {
        document.getElementById('kod_input_kassa').addEventListener('keydown', function(e) {
    
        if (e.keyCode === 40) {  
            // вниз переход в zakaz_input_kassa input
            var zakaz_input_kassa = document.getElementById('zakaz_input_kassa');
            document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('zakaz_input_kassa').classList.add('my-bg-orange')
            zakaz_input_kassa.select();
            e.preventDefault();
            }
        
        if (e.keyCode === 38) {  
            // вверх переход в slr_input_kassa input
            var slr_input_kassa = document.getElementById('slr_input_kassa');
            document.getElementById('kod_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('slr_input_kassa').classList.add('my-bg-orange')
            slr_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('kod_input_kassa').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('kod_input_kassa').value == '' || document.getElementById('kod_input_kassa').value == 0) {
                        document.getElementById('kod_input_kassa').value = document.getElementById('ostatok_plateja').value
                    } else {
                        var kod = parseFloat(document.getElementById('kod_input_kassa').value)
                        document.getElementById('kod_input_kassa').value = kod + parseFloat(document.getElementById('ostatok_plateja').value)
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
    
        });
    })();
    
    // Input zakaz_input_kassa
    (function() {
        document.getElementById('zakaz_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {  
            // вниз переход в zakaz_input_kassa input
            var prochee_input_kassa = document.getElementById('prochee_input_kassa');
            document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('prochee_input_kassa').classList.add('my-bg-orange')
            prochee_input_kassa.select();
            e.preventDefault();
            }
        
        if (e.keyCode === 38) {  
            // вверх переход в slr_input_kassa input
            var kod_input_kassa = document.getElementById('kod_input_kassa');
            document.getElementById('zakaz_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('kod_input_kassa').classList.add('my-bg-orange')
            kod_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('zakaz_input_kassa').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('zakaz_input_kassa').value == '' || document.getElementById('zakaz_input_kassa').value == 0) {
                        document.getElementById('zakaz_input_kassa').value = document.getElementById('ostatok_plateja').value
                    } else {
                        var zakaz = parseFloat(document.getElementById('zakaz_input_kassa').value)
                        document.getElementById('zakaz_input_kassa').value = zakaz + parseFloat(document.getElementById('ostatok_plateja').value)
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
    
        });
    })();
    
    // Input prochee_input_kassa
    (function() {
        document.getElementById('prochee_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {  
            // вниз переход в alem_input_kassa input
            var alem_input_kassa = document.getElementById('alem_input_kassa');
            document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('alem_input_kassa').classList.add('my-bg-orange')
            alem_input_kassa.select();
            e.preventDefault();
            }
        if (e.keyCode === 38) {  
            // вверх переход в slr_input_kassa input
            var zakaz_input_kassa = document.getElementById('zakaz_input_kassa');
            document.getElementById('prochee_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('zakaz_input_kassa').classList.add('my-bg-orange')
            zakaz_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('prochee_input_kassa').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('prochee_input_kassa').value == '' || document.getElementById('prochee_input_kassa').value == 0) {
                        document.getElementById('prochee_input_kassa').value = document.getElementById('ostatok_plateja').value
                    } else {
                        var prochee = parseFloat(document.getElementById('prochee_input_kassa').value)
                        document.getElementById('prochee_input_kassa').value = prochee + parseFloat(document.getElementById('ostatok_plateja').value)
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
    
        });
    })();
    
    // Input alem_input_kassa
    (function() {
        document.getElementById('alem_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {  
            // вниз переход в internet_input_kassa input
            var internet_input_kassa = document.getElementById('internet_input_kassa');
            document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('internet_input_kassa').classList.add('my-bg-orange')
            internet_input_kassa.select();
            e.preventDefault();
            }
        if (e.keyCode === 38) {  
            // вверх переход в prochee_input_kassa input
            var prochee_input_kassa = document.getElementById('prochee_input_kassa');
            document.getElementById('alem_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('prochee_input_kassa').classList.add('my-bg-orange')
            prochee_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('alem_input_kassa').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('alem_input_kassa').value == '' || document.getElementById('alem_input_kassa').value == 0) {
                        document.getElementById('alem_input_kassa').value = document.getElementById('ostatok_plateja').value
                    } else {
                        var alem = parseFloat(document.getElementById('alem_input_kassa').value)
                        document.getElementById('alem_input_kassa').value = alem + parseFloat(document.getElementById('ostatok_plateja').value)
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
    
        });
    })();
    
    // Input internet_input_kassa
    (function() {
        document.getElementById('internet_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {  
            // вниз переход в dop_uslugi_input_kassa input
            var dop_uslugi_input_kassa = document.getElementById('dop_uslugi_input_kassa');
            document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('dop_uslugi_input_kassa').classList.add('my-bg-orange')
            dop_uslugi_input_kassa.select();
            e.preventDefault();
            }
        if (e.keyCode === 38) {  
            // вверх переход в alem_input_kassa input
            var alem_input_kassa = document.getElementById('alem_input_kassa');
            document.getElementById('internet_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('alem_input_kassa').classList.add('my-bg-orange')
            alem_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('internet_input_kassa').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('internet_input_kassa').value == '' || document.getElementById('internet_input_kassa').value == 0) {
                        document.getElementById('internet_input_kassa').value = document.getElementById('ostatok_plateja').value
                    } else {
                        var internet = parseFloat(document.getElementById('internet_input_kassa').value)
                        document.getElementById('internet_input_kassa').value = internet + parseFloat(document.getElementById('ostatok_plateja').value)
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
    
        });
    })();
    
    // Input dop_uslugi_input_kassa
    (function() {
        document.getElementById('dop_uslugi_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {  
            // вниз переход в kabel_input_kassa input
            var kabel_input_kassa = document.getElementById('kabel_input_kassa');
            document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('kabel_input_kassa').classList.add('my-bg-orange')
            kabel_input_kassa.select();
            e.preventDefault();
            }
        if (e.keyCode === 38) {  
            // вверх переход в internet_input_kassa input
            var internet_input_kassa = document.getElementById('internet_input_kassa');
            document.getElementById('dop_uslugi_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('internet_input_kassa').classList.add('my-bg-orange')
            internet_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('dop_uslugi_input_kassa').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('dop_uslugi_input_kassa').value == '' || document.getElementById('dop_uslugi_input_kassa').value == 0) {
                        document.getElementById('dop_uslugi_input_kassa').value = document.getElementById('ostatok_plateja').value
                    } else {
                        var dop_uslugi = parseFloat(document.getElementById('dop_uslugi_input_kassa').value)
                        document.getElementById('dop_uslugi_input_kassa').value = dop_uslugi + parseFloat(document.getElementById('ostatok_plateja').value)
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
    
    
        });
    })();
    
    // Input kabel_input_kassa
    (function() {
        document.getElementById('kabel_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {  
            // вниз переход в card_input_kassa input
            var card_input_kassa = document.getElementById('card_input_kassa');
            document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
            card_input_kassa.select();
            e.preventDefault();
            }
        if (e.keyCode === 38) {  
            // вверх переход в dop_uslugi_input_kassa input
            var dop_uslugi_input_kassa = document.getElementById('dop_uslugi_input_kassa');
            document.getElementById('kabel_input_kassa').classList.remove('my-bg-orange')
            document.getElementById('dop_uslugi_input_kassa').classList.add('my-bg-orange')
            dop_uslugi_input_kassa.select();
            e.preventDefault();
            }
    
        if (e.keyCode === 32) {  
            // если нажал на пробел то вся сумма с остатка платежа должна переместиться в этот input
            if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == 0) {
    
            } else {
                if (document.getElementById('summa_w_kassu').value == '' || document.getElementById('summa_w_kassu').value == 0) {
                    document.getElementById('summa_w_kassu').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('kabel_input_kassa').value = document.getElementById('ostatok_plateja').value
                    document.getElementById('ostatok_plateja').value = 0
                } else {
                    if (document.getElementById('kabel_input_kassa').value == '' || document.getElementById('kabel_input_kassa').value == 0) {
                        document.getElementById('kabel_input_kassa').value = document.getElementById('ostatok_plateja').value
                    } else {
                        var kabel = parseFloat(document.getElementById('kabel_input_kassa').value)
                        document.getElementById('kabel_input_kassa').value = kabel + parseFloat(document.getElementById('ostatok_plateja').value)
                    }
                    summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
                    document.getElementById('summa_w_kassu').value = summa_w_kassu + parseFloat(document.getElementById('ostatok_plateja').value)
                    document.getElementById('ostatok_plateja').value = 0
                }
            }
            }
        });
    })();
    
    // Input card_input_kassa
    (function() {
        document.getElementById('card_input_kassa').addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {  
            // вниз переход в oplata_btm_modal input
            var oplata_btm_modal = document.getElementById('oplata_btm_modal');
            oplata_btm_modal.focus()
            }
        if (e.keyCode === 38) {  
            // вверх переход в kabel_input_kassa input
            var kabel_input_kassa = document.getElementById('kabel_input_kassa');
            document.getElementById('kabel_input_kassa').classList.add('my-bg-orange')
            kabel_input_kassa.select();
            e.preventDefault();
            }
        });
    })();
    
    // Input oplata_btm_modal
    (function() {
        document.getElementById('oplata_btm_modal').addEventListener('keydown', function(e) {
    
        if (e.keyCode === 38) {  
            // вверх переход в card_input_kassa input
            var card_input_kassa = document.getElementById('card_input_kassa');
            card_input_kassa.focus();
            }
        });
    })();
/* #########################
input-ы в oplataModal END ##
    #########################
*/

    
    
    
/* ###############################################
При активации модального окна касса oplataModal ##
    ###############################################
*/
    // Фокус input-a абонрлата (в oplataModal) после нажатия на оплатить (в касса)
    var myModal = document.getElementById('oplataModal')
    var myInput = document.getElementById('abonplata_input_kassa')
    // Если модальное окно открылась
    myModal.addEventListener('shown.bs.modal', function () {

        document.getElementById('ostatok_plateja').classList.add('my-bg-red')
        document.getElementById('summa_w_kassu').classList.add('my-bg-red')
        document.getElementById('abonplata_input_kassa').classList.add('my-bg-orange')

        document.getElementById('oplata_modal_balance_input').value = document.getElementById('kassa_balance_in_pay_row').value
        myInput.select()
    
        /* ########################################
        Все баланс минусы сделать 0 в modal окне ##
            ########################################
        */
        var balance_modal = parseFloat(document.getElementById('oplata_modal_balance_input').value)
        var wklad_modal = parseFloat(document.getElementById('wklad_modal').value)

        if (document.getElementById('summa_w_kassu').value == '') {
        var summa_w_kassu = 0
        } else {
        var summa_w_kassu = parseFloat(document.getElementById('summa_w_kassu').value)
        }

        var abonplata_balance = parseFloat(document.getElementById('abonent_balance_in_kassa_table').innerHTML)
        var slr_balance = parseFloat(document.getElementById('slr_balance_in_kassa_table').innerHTML)
        var kod_balance = parseFloat(document.getElementById('kod_balance_in_kassa_table').innerHTML)
        var zakaz_balance = parseFloat(document.getElementById('zakaz_balance_in_kassa_table').innerHTML)
        var prochee_balance = parseFloat(document.getElementById('prochee_balance_in_kassa_table').innerHTML)
        var alem_balance = parseFloat(document.getElementById('alem_balance_in_kassa_table').innerHTML)
        var internet_balance = parseFloat(document.getElementById('internet_balance_in_kassa_table').innerHTML)
        var dop_uslugi_balance= parseFloat(document.getElementById('dop_uslugi_balance_in_kassa_table').innerHTML)
        var kabel_balance = parseFloat(document.getElementById('kabel_balance_in_kassa_table').innerHTML)

        if (abonplata_balance < 0 && wklad_modal > Math.abs(abonplata_balance)) {
        document.getElementById('abonplata_input_kassa').value = Math.abs(abonplata_balance)
        document.getElementById('ostatok_plateja').value = wklad_modal - Math.abs(abonplata_balance)
        document.getElementById('summa_w_kassu').value = summa_w_kassu + Math.abs(abonplata_balance)
        document.getElementById('oplata_modal_balance_input').value = balance_modal + Math.abs(abonplata_balance)
        balance_modal += Math.abs(abonplata_balance)
        wklad_modal -= Math.abs(abonplata_balance)
        summa_w_kassu += Math.abs(abonplata_balance)
        }

        if (slr_balance < 0 && wklad_modal > Math.abs(slr_balance)) {
        document.getElementById('slr_input_kassa').value = Math.abs(slr_balance)
        document.getElementById('ostatok_plateja').value = wklad_modal - Math.abs(slr_balance)
        document.getElementById('summa_w_kassu').value = summa_w_kassu + Math.abs(slr_balance)
        document.getElementById('oplata_modal_balance_input').value = balance_modal + Math.abs(slr_balance)
        balance_modal += Math.abs(slr_balance)
        wklad_modal -= Math.abs(slr_balance)
        summa_w_kassu += Math.abs(slr_balance)
        }

        if (kod_balance < 0 && wklad_modal > Math.abs(kod_balance)) {
        document.getElementById('kod_input_kassa').value = Math.abs(kod_balance)
        document.getElementById('ostatok_plateja').value = wklad_modal - Math.abs(kod_balance)
        document.getElementById('summa_w_kassu').value = summa_w_kassu + Math.abs(kod_balance)
        document.getElementById('oplata_modal_balance_input').value = balance_modal + Math.abs(kod_balance)
        balance_modal += Math.abs(kod_balance)
        wklad_modal -= Math.abs(kod_balance)
        summa_w_kassu += Math.abs(kod_balance)
        }

        if (zakaz_balance < 0 && wklad_modal > Math.abs(zakaz_balance)) {
        document.getElementById('zakaz_input_kassa').value = Math.abs(zakaz_balance)
        document.getElementById('ostatok_plateja').value = wklad_modal - Math.abs(zakaz_balance)
        document.getElementById('summa_w_kassu').value = summa_w_kassu + Math.abs(zakaz_balance)
        document.getElementById('oplata_modal_balance_input').value = balance_modal + Math.abs(zakaz_balance)
        balance_modal += Math.abs(zakaz_balance)
        wklad_modal -= Math.abs(zakaz_balance)
        summa_w_kassu += Math.abs(zakaz_balance)
        }

        if (prochee_balance < 0 && wklad_modal > Math.abs(prochee_balance)) {
        document.getElementById('prochee_input_kassa').value = Math.abs(prochee_balance)
        document.getElementById('ostatok_plateja').value = wklad_modal - Math.abs(prochee_balance)
        document.getElementById('summa_w_kassu').value = summa_w_kassu + Math.abs(prochee_balance)
        document.getElementById('oplata_modal_balance_input').value = balance_modal + Math.abs(prochee_balance)
        balance_modal += Math.abs(prochee_balance)
        wklad_modal -= Math.abs(prochee_balance)
        summa_w_kassu += Math.abs(prochee_balance)
        }

        if (alem_balance < 0 && wklad_modal > Math.abs(alem_balance)) {
        document.getElementById('alem_input_kassa').value = Math.abs(alem_balance)
        document.getElementById('ostatok_plateja').value = wklad_modal - Math.abs(alem_balance)
        document.getElementById('summa_w_kassu').value = summa_w_kassu + Math.abs(alem_balance)
        document.getElementById('oplata_modal_balance_input').value = balance_modal + Math.abs(alem_balance)
        balance_modal += Math.abs(alem_balance)
        wklad_modal -= Math.abs(alem_balance)
        summa_w_kassu += Math.abs(alem_balance)
        }

        if (internet_balance < 0 && wklad_modal > Math.abs(internet_balance)) {
        document.getElementById('internet_input_kassa').value = Math.abs(internet_balance)
        document.getElementById('ostatok_plateja').value = wklad_modal - Math.abs(internet_balance)
        document.getElementById('summa_w_kassu').value = summa_w_kassu + Math.abs(internet_balance)
        document.getElementById('oplata_modal_balance_input').value = balance_modal + Math.abs(internet_balance)
        balance_modal += Math.abs(internet_balance)
        wklad_modal -= Math.abs(internet_balance)
        summa_w_kassu += Math.abs(internet_balance)
        }

        if (dop_uslugi_balance < 0 && wklad_modal > Math.abs(dop_uslugi_balance)) {
        document.getElementById('dop_uslugi_input_kassa').value = Math.abs(dop_uslugi_balance) 
        document.getElementById('ostatok_plateja').value = wklad_modal - Math.abs(dop_uslugi_balance)
        document.getElementById('summa_w_kassu').value = summa_w_kassu + Math.abs(dop_uslugi_balance)
        document.getElementById('oplata_modal_balance_input').value = balance_modal + Math.abs(dop_uslugi_balance)
        balance_modal += Math.abs(dop_uslugi_balance)
        wklad_modal -= Math.abs(dop_uslugi_balance)
        summa_w_kassu += Math.abs(dop_uslugi_balance)
        }

        if (kabel_balance < 0 && wklad_modal > Math.abs(kabel_balance)) {
        document.getElementById('kabel_input_kassa').value = Math.abs(kabel_balance) 
        document.getElementById('ostatok_plateja').value = wklad_modal - Math.abs(kabel_balance)
        document.getElementById('summa_w_kassu').value = summa_w_kassu + Math.abs(kabel_balance)
        document.getElementById('oplata_modal_balance_input').value = balance_modal + Math.abs(kabel_balance)
        balance_modal += Math.abs(kabel_balance)
        wklad_modal -= Math.abs(kabel_balance)
        summa_w_kassu += Math.abs(kabel_balance)
        }
        /* ############################################
        Все баланс минусы сделать 0 в modal окне END ##
            ############################################
        */
    })

    // Если модальное окно закрылась
    myModal.addEventListener('hidden.bs.modal', function () {
    document.getElementById("wklad_input").readOnly = false


})
/* ###################################################
При активации модального окна касса oplataModal END ##
    ###################################################
*/
    
/* ########################################################################
Матиматические вычисления в Input-ах oplataModal при введени в них чесел ##
    ########################################################################
*/
    function cloneWklad() {
        document.getElementById('wklad_modal').value = document.getElementById('wklad_input').value
        document.getElementById('ostatok_plateja').value = document.getElementById('wklad_input').value
    }
    
    function mathCalculate() {
    
        var wklad_input = parseFloat(document.getElementById('wklad_input').value)
    
        if (document.getElementById('abonplata_input_kassa').value == '') {var abonplata = 0} else {
            var abonplata = parseFloat(document.getElementById('abonplata_input_kassa').value)
        }
    
        if (document.getElementById('slr_input_kassa').value == '') {var slr = 0} else {
            var slr = parseFloat(document.getElementById('slr_input_kassa').value)
        }
    
        if (document.getElementById('kod_input_kassa').value == '') {var kod = 0} else {
            var kod = parseFloat(document.getElementById('kod_input_kassa').value)
        }
    
        if (document.getElementById('zakaz_input_kassa').value == '') {var zakaz = 0} else {
            var zakaz = parseFloat(document.getElementById('zakaz_input_kassa').value)
        }
    
        if (document.getElementById('prochee_input_kassa').value == '') {var prochee = 0} else {
            var prochee = parseFloat(document.getElementById('prochee_input_kassa').value)
        }
    
        if (document.getElementById('alem_input_kassa').value == '') {var alem = 0} else {
            var alem = parseFloat(document.getElementById('alem_input_kassa').value)
        }
    
        if (document.getElementById('internet_input_kassa').value == '') {var internet = 0} else {
            var internet = parseFloat(document.getElementById('internet_input_kassa').value)
        }
    
        if (document.getElementById('dop_uslugi_input_kassa').value == '') {var uslugi = 0} else {
            var uslugi = parseFloat(document.getElementById('dop_uslugi_input_kassa').value)
        }
    
        if (document.getElementById('kabel_input_kassa').value == '') {var kabel = 0} else {
            var kabel = parseFloat(document.getElementById('kabel_input_kassa').value)
        }
    
        // Код для изменения сумма в кассу в реальном времени
        document.getElementById('summa_w_kassu').value = abonplata + slr + kod + zakaz + prochee + alem + internet + uslugi + kabel
        document.getElementById('ostatok_plateja').value = wklad_input - parseFloat(document.getElementById('summa_w_kassu').value)

        // Код для изменения баланс в модалке в реальном времени
        var balance_total_var = parseFloat(document.getElementById('kassa_balance_in_pay_row').value.replace(',', '.'))
        document.getElementById('oplata_modal_balance_input').value = balance_total_var + abonplata + slr + kod + zakaz + prochee + alem + internet + uslugi + kabel

        // изменения backgraund color в ostatok_plateja И summa_w_kassu в oplataModal
        if (document.getElementById('ostatok_plateja').value == '' || document.getElementById('ostatok_plateja').value == '0') {
            document.getElementById('ostatok_plateja').classList.add('my-bg-green')
            document.getElementById('summa_w_kassu').classList.add('my-bg-green')
    
            document.getElementById('ostatok_plateja').classList.remove('my-bg-red')
            document.getElementById('summa_w_kassu').classList.remove('my-bg-red')
        } else {
            document.getElementById('ostatok_plateja').classList.remove('my-bg-green')
            document.getElementById('summa_w_kassu').classList.remove('my-bg-green')
    
            document.getElementById('ostatok_plateja').classList.add('my-bg-red')
            document.getElementById('summa_w_kassu').classList.add('my-bg-red')
        }
    
    }
/* ############################################################################
Матиматические вычисления в Input-ах oplataModal при введени в них чесел END ##
    ############################################################################
*/
}


// текущий url в виде строки
var currentLocation = window.location.href;
// если в текущем url есть подстрока receipts то выполнить код
if (currentLocation.indexOf("receipts") >= 0) {

/* #########################################
rePrint повторная печать квитанции (чека) ##
    #########################################
*/
function rePrint(id) {  
var y = document.getElementsByClassName(id);

var print_etrap = y[0].innerHTML

var print_kw_nomer = y[1].innerHTML
var print_kw_date = y[2].innerHTML
var print_name_suname_telefon = y[3].innerHTML

var print_telefon = y[4].innerHTML
var print_slr = y[5].innerHTML
var print_kod = y[6].innerHTML
var print_zakaz = y[7].innerHTML
var print_prochee = y[8].innerHTML
var print_alem = y[9].innerHTML
var print_internet = y[10].innerHTML
var print_dop_uslugi = y[11].innerHTML
var print_kabel = y[12].innerHTML
var print_oplata_sum = y[13].innerHTML
var print_kassir = y[14].innerHTML

var myWindow = window.open('', 'my div', 'height=300,width=400,font-size=9');
myWindow.document.write('<div style=font-size:10px;>'+print_etrap+' WEAK</div>');
myWindow.document.write('<div style=font-size:10px;>'+ print_kw_nomer +'</div>');
myWindow.document.write('<div style=font-size:10px;>'+ print_kw_date +'</div>');
myWindow.document.write('<div style=font-size:10px;>'+print_name_suname_telefon+'</div>');
myWindow.document.write('-----------------------------');
myWindow.document.write('<div style=font-size:10px;padding-left:60px;>tolenen - galany</div>');   
myWindow.document.write('-----------------------------');
if (print_telefon != '0,0' ){myWindow.document.write('<div style=font-size:10px;>Абонплата '+'<span style=font-size:10px;padding-left:20px>'+print_telefon+'</span>'+'</div>');}
if (print_slr != '0,0'){myWindow.document.write('<div style=font-size:10px;>СЛР '+'<span style=font-size:10px;padding-left:47px>'+print_slr+'</span>'+'</div>');}    
if (print_kod != '0,0'){myWindow.document.write('<div style=font-size:10px;>КОД '+'<span style=font-size:10px;padding-left:46px>'+print_kod+'</span>'+'</div>');}
if (print_zakaz != '0,0'){myWindow.document.write('<div style=font-size:10px;>Заказ '+'<span style=font-size:10px;padding-left:43px>'+print_zakaz+'</span>'+'</div>');}
if (print_prochee != '0,0'){myWindow.document.write('<div style=font-size:10px;>Прочее '+'<span style=font-size:10px;padding-left:35px>'+print_prochee+'</span>'+'</div>');}
if (print_alem != '0,0'){myWindow.document.write('<div style=font-size:10px;>Alem TV '+'<span style=font-size:10px;padding-left:28px>'+print_alem+'</span>'+'</div>');}
if (print_internet != '0,0'){myWindow.document.write('<div style=font-size:10px;>Интернет '+'<span style=font-size:10px;padding-left:25px>'+print_internet+'</span>'+'</div>');}
if (print_dop_uslugi != '0,0'){myWindow.document.write('<div style=font-size:10px;>Доп.Услуги '+'<span style=font-size:10px;padding-left:17px>'+print_dop_uslugi+'</span>'+'</div>');}
if (print_kabel != '0,0'){myWindow.document.write('<div style=font-size:10px;>Кабель '+'<span style=font-size:10px;padding-left:37px>'+print_kabel+'</span>'+'</div>');}
myWindow.document.write('-----------------------------');
myWindow.document.write('<div style=font-size:10px;>Jemi: <span style=font-size:10px;padding-left:45px>'+print_oplata_sum+'</span></div>');
myWindow.document.write('<div style=font-size:10px;>'+print_kassir+'</div>');
myWindow.document.write('<br>');
myWindow.document.write('<div style=font-size:10px;>Gaznachy __________________</div>');
myWindow.focus(); // necessary for IE >= 10
myWindow.print();
myWindow.close();
}

/* #############################################
rePrint повторная печать квитанции (чека) END ##
################################################
*/

/*дефис (цере) между цифрами телефона при вводе номера kassa-receipt*/
(function () {
document
    .getElementById("search_number_receipt")
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


/*#########################
kassa rezerw End ##########
##########################*/
