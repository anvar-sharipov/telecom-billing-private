console.log('kassaReestr.js')



/* #######################################
для инкремента нумераций в kassa-reestr ##
   #######################################
*/

// для Dashoguz реестр (наличными)
var dashoguzFalsecount = 1
var dashoguzFalseincrement = document.getElementsByClassName('dashoguzFalseincrement');
for (var i = 0; i < dashoguzFalseincrement.length; i++) {
    dashoguzFalseincrement[i].innerHTML = dashoguzFalsecount
    dashoguzFalsecount++
}
if (document.getElementById('dashoguzFalseWkladCount')) {
    document.getElementById('dashoguzFalseWkladCount').innerHTML = dashoguzFalsecount - 1
}

// для Dashoguz реестр (карточкой)
var dashoguzTruecount = 1
var dashoguzTrueincrement = document.getElementsByClassName('dashoguzTrueincrement');
for (var i = 0; i < dashoguzTrueincrement.length; i++) {
    dashoguzTrueincrement[i].innerHTML = dashoguzTruecount
    dashoguzTruecount++
}
if (document.getElementById('dashoguzTrueWkladCount')) {
    document.getElementById('dashoguzTrueWkladCount').innerHTML = dashoguzTruecount - 1
}

// для Akdepe реестр (наличными)
var AkdepeFalsecount = 1
var AkdepeFalseincrement = document.getElementsByClassName('AkdepeFalseincrement');
for (var i = 0; i < AkdepeFalseincrement.length; i++) {
    AkdepeFalseincrement[i].innerHTML = AkdepeFalsecount
    AkdepeFalsecount++
}
if (document.getElementById('AkdepeFalseWkladCount')) {
    document.getElementById('AkdepeFalseWkladCount').innerHTML = AkdepeFalsecount - 1
}

// для Akdepe реестр (картой)
var AkdepeTruecount = 1
var AkdepeTrueincrement = document.getElementsByClassName('AkdepeTrueincrement');
for (var i = 0; i < AkdepeTrueincrement.length; i++) {
    AkdepeTrueincrement[i].innerHTML = AkdepeTruecount
    AkdepeTruecount++
}
if (document.getElementById('AkdepeTrueWkladCount')) {
    document.getElementById('AkdepeTrueWkladCount').innerHTML = AkdepeTruecount - 1
}

// для Gorogly реестр (наличными)
var GoroglyFalsecount = 1
var GoroglyFalseincrement = document.getElementsByClassName('GoroglyFalseincrement');
for (var i = 0; i < GoroglyFalseincrement.length; i++) {
    GoroglyFalseincrement[i].innerHTML = GoroglyFalsecount
    GoroglyFalsecount++
}
if (document.getElementById('GoroglyFalseWkladCount')) {
    document.getElementById('GoroglyFalseWkladCount').innerHTML = GoroglyFalsecount - 1
}

// для Gorogly реестр (картой)
var GoroglyTruecount = 1
var GoroglyTrueincrement = document.getElementsByClassName('GoroglyTrueincrement');
for (var i = 0; i < GoroglyTrueincrement.length; i++) {
    GoroglyTrueincrement[i].innerHTML = GoroglyTruecount
    GoroglyTruecount++
}
if (document.getElementById('GoroglyTrueWkladCount')) {
    document.getElementById('GoroglyTrueWkladCount').innerHTML = GoroglyTruecount - 1
}

// для Ruhubelent реестр (наличными)
var RuhubelentFalsecount = 1
var RuhubelentFalseincrement = document.getElementsByClassName('RuhubelentFalseincrement');
for (var i = 0; i < RuhubelentFalseincrement.length; i++) {
    RuhubelentFalseincrement[i].innerHTML = RuhubelentFalsecount
    RuhubelentFalsecount++
}
if (document.getElementById('RuhubelentFalseWkladCount')) {
    document.getElementById('RuhubelentFalseWkladCount').innerHTML = RuhubelentFalsecount - 1
}

// для Ruhubelent реестр (картой)
var RuhubelentTruecount = 1
var RuhubelentTrueincrement = document.getElementsByClassName('RuhubelentTrueincrement');
for (var i = 0; i < RuhubelentTrueincrement.length; i++) {
    RuhubelentTrueincrement[i].innerHTML = RuhubelentTruecount
    RuhubelentTruecount++
}
if (document.getElementById('RuhubelentTrueWkladCount')) {
    document.getElementById('RuhubelentTrueWkladCount').innerHTML = RuhubelentTruecount - 1
}

// для Nyyazow реестр (наличными)
var NyyazowFalsecount = 1
var NyyazowFalseincrement = document.getElementsByClassName('NyyazowFalseincrement');
for (var i = 0; i < NyyazowFalseincrement.length; i++) {
    NyyazowFalseincrement[i].innerHTML = NyyazowFalsecount
    NyyazowFalsecount++
}
if (document.getElementById('NyyazowFalseWkladCount')) {
    document.getElementById('NyyazowFalseWkladCount').innerHTML = NyyazowFalsecount - 1
}

// для Nyyazow реестр (картой)
var NyyazowTruecount = 1
var NyyazowTrueincrement = document.getElementsByClassName('NyyazowTrueincrement');
for (var i = 0; i < NyyazowTrueincrement.length; i++) {
    NyyazowTrueincrement[i].innerHTML = NyyazowTruecount
    NyyazowTruecount++
}
if (document.getElementById('NyyazowTrueWkladCount')) {
    document.getElementById('NyyazowTrueWkladCount').innerHTML = NyyazowTruecount - 1
}

// для Turkmenbashy реестр (наличными)
var TurkmenbashyFalsecount = 1
var TurkmenbashyFalseincrement = document.getElementsByClassName('TurkmenbashyFalseincrement');
for (var i = 0; i < TurkmenbashyFalseincrement.length; i++) {
    TurkmenbashyFalseincrement[i].innerHTML = TurkmenbashyFalsecount
    TurkmenbashyFalsecount++
}
if (document.getElementById('TurkmenbashyFalseWkladCount')) {
    document.getElementById('TurkmenbashyFalseWkladCount').innerHTML = TurkmenbashyFalsecount - 1
}

// для Turkmenbashy реестр (картой)
var TurkmenbashyTruecount = 1
var TurkmenbashyTrueincrement = document.getElementsByClassName('TurkmenbashyTrueincrement');
for (var i = 0; i < TurkmenbashyTrueincrement.length; i++) {
    TurkmenbashyTrueincrement[i].innerHTML = TurkmenbashyTruecount
    TurkmenbashyTruecount++
}
if (document.getElementById('TurkmenbashyTrueWkladCount')) {
    document.getElementById('TurkmenbashyTrueWkladCount').innerHTML = TurkmenbashyTruecount - 1
}

// для Boldumsaz реестр (наличными)
var BoldumsazFalsecount = 1
var BoldumsazFalseincrement = document.getElementsByClassName('BoldumsazFalseincrement');
for (var i = 0; i < BoldumsazFalseincrement.length; i++) {
    BoldumsazFalseincrement[i].innerHTML = BoldumsazFalsecount
    BoldumsazFalsecount++
}
if (document.getElementById('BoldumsazFalseWkladCount')) {
    document.getElementById('BoldumsazFalseWkladCount').innerHTML = BoldumsazFalsecount - 1
}

// для Boldumsaz реестр (картой)
var BoldumsazTruecount = 1
var BoldumsazTrueincrement = document.getElementsByClassName('BoldumsazTrueincrement');
for (var i = 0; i < BoldumsazTrueincrement.length; i++) {
    BoldumsazTrueincrement[i].innerHTML = BoldumsazTruecount
    BoldumsazTruecount++
}
if (document.getElementById('BoldumsazTrueWkladCount')) {
    document.getElementById('BoldumsazTrueWkladCount').innerHTML = BoldumsazTruecount - 1
}

// для Koneurgench реестр (наличными)
var KoneurgenchFalsecount = 1
var KoneurgenchFalseincrement = document.getElementsByClassName('KoneurgenchFalseincrement');
for (var i = 0; i < KoneurgenchFalseincrement.length; i++) {
    KoneurgenchFalseincrement[i].innerHTML = KoneurgenchFalsecount
    KoneurgenchFalsecount++
}
if (document.getElementById('KoneurgenchFalseWkladCount')) {
    document.getElementById('KoneurgenchFalseWkladCount').innerHTML = KoneurgenchFalsecount - 1
}

// для Koneurgench реестр (картой)
var KoneurgenchTruecount = 1
var KoneurgenchTrueincrement = document.getElementsByClassName('KoneurgenchTrueincrement');
for (var i = 0; i < KoneurgenchTrueincrement.length; i++) {
    KoneurgenchTrueincrement[i].innerHTML = KoneurgenchTruecount
    KoneurgenchTruecount++
}
if (document.getElementById('KoneurgenchTrueWkladCount')) {
    document.getElementById('KoneurgenchTrueWkladCount').innerHTML = KoneurgenchTruecount - 1
}

/* ###########################################
для инкремента нумераций в kassa-reestr END ##
   ###########################################
*/