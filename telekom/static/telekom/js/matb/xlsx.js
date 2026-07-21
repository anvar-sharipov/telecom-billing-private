/*################
    import-xlsx ##
##################
*/
// текущий url в виде строки
var currentLocation = window.location.href;
// если в текущем url есть подстрока import-xlsx то выполнить код
if (currentLocation.indexOf("import-xlsx") >= 0) {

const file = document.querySelector('#file');
file.addEventListener('change', (e) => {
  // Get the selected file
  const [file] = e.target.files;
  // Get the file name and size
  const { name: fileName, size } = file;
  // Convert size in bytes to kilo bytes
  const fileSize = (size / 1000).toFixed(2);
  // Set the text content
  const fileNameAndSize = `${fileName} - ${fileSize}KB`;
  document.querySelector('.file-name').textContent = fileNameAndSize;
});

const file2 = document.querySelector('#file2');
file2.addEventListener('change', (e) => {
  // Get the selected file
  const [file2] = e.target.files;
  // Get the file name and size
  const { name: file2Name, size } = file2;
  // Convert size in bytes to kilo bytes
  const file2Size = (size / 1000).toFixed(2);
  // Set the text content
  const file2NameAndSize = `${file2Name} - ${file2Size}KB`;
  document.querySelector('.file2-name').textContent = file2NameAndSize;
});

const file3 = document.querySelector('#file3');
file3.addEventListener('change', (e) => {
  // Get the selected file
  const [file3] = e.target.files;
  // Get the file name and size
  const { name: file3Name, size } = file3;
  // Convert size in bytes to kilo bytes
  const file3Size = (size / 1000).toFixed(2);
  // Set the text content
  const file3NameAndSize = `${file3Name} - ${file3Size}KB`;
  document.querySelector('.file3-name').textContent = file3NameAndSize;
});


const file4 = document.querySelector('#file4');
file4.addEventListener('change', (e) => {
  // Get the selected file
  const [file4] = e.target.files;
  // Get the file name and size
  const { name: file4Name, size } = file4;
  // Convert size in bytes to kilo bytes
  const file4Size = (size / 1000).toFixed(2);
  // Set the text content
  const file4NameAndSize = `${file4Name} - ${file4Size}KB`;
  document.querySelector('.file4-name').textContent = file4NameAndSize;
});


function ChangeSubmitValue() {
  if (event.target.checked == true) {
    document.getElementById('internetPlatejiFormSubmit').innerHTML = 'Проверка'
    document.getElementById('internetPlatejiFormSubmit').classList.remove('btn-danger')
    document.getElementById('internetPlatejiFormSubmit').classList.add('btn-primary')
  } else {
    document.getElementById('internetPlatejiFormSubmit').innerHTML = 'Добавить'
    document.getElementById('internetPlatejiFormSubmit').classList.add('btn-danger')
    document.getElementById('internetPlatejiFormSubmit').classList.remove('btn-primary')
  }
}

function ChangeSubmitValue2() {
  if (event.target.checked == true) {
    document.getElementById('internetNachisleniyaFormSubmit').innerHTML = 'Проверка'
    document.getElementById('internetNachisleniyaFormSubmit').classList.remove('btn-danger')
    document.getElementById('internetNachisleniyaFormSubmit').classList.add('btn-primary')
  } else {
    document.getElementById('internetNachisleniyaFormSubmit').innerHTML = 'Добавить'
    document.getElementById('internetNachisleniyaFormSubmit').classList.add('btn-danger')
    document.getElementById('internetNachisleniyaFormSubmit').classList.remove('btn-primary')
  }
}

function ChangeSubmitValue3() {
  if (event.target.checked == true) {
    document.getElementById('alemNachisleniyaFormSubmit').innerHTML = 'Проверка'
    document.getElementById('alemNachisleniyaFormSubmit').classList.remove('btn-danger')
    document.getElementById('alemNachisleniyaFormSubmit').classList.add('btn-primary')
  } else {
    document.getElementById('alemNachisleniyaFormSubmit').innerHTML = 'Добавить'
    document.getElementById('alemNachisleniyaFormSubmit').classList.add('btn-danger')
    document.getElementById('alemNachisleniyaFormSubmit').classList.remove('btn-primary')
  }
}

function ChangeSubmitValue4() {
  if (event.target.checked == true) {
    document.getElementById('platejiSbillingaFormSubmit').innerHTML = 'Проверка'
    document.getElementById('platejiSbillingaFormSubmit').classList.remove('btn-danger')
    document.getElementById('platejiSbillingaFormSubmit').classList.add('btn-primary')
  } else {
    document.getElementById('platejiSbillingaFormSubmit').innerHTML = 'Добавить'
    document.getElementById('platejiSbillingaFormSubmit').classList.add('btn-danger')
    document.getElementById('platejiSbillingaFormSubmit').classList.remove('btn-primary')
  }
}

}
/*####################
    import-xlsx END ##
######################
*/



/*##############################
    internetPlatejiSearch END ##
################################
*/
    // текущий url в виде строки
    var currentLocation = window.location.href;
    // если в текущем url есть подстрока internet-plateji-search то выполнить код
    if (currentLocation.indexOf("internet-plateji-search") >= 0) {
        document.addEventListener("DOMContentLoaded", function () {
            document.getElementById("dogoworNomer").select();
    
        })
    }
/*##############################
    internetPlatejiSearch END ##
################################
*/
