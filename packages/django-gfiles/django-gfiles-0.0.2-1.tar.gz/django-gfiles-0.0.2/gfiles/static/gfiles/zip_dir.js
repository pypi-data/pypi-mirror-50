function show_dir() {
    if(document.getElementById('dir_button').style.display='table-row') {
        document.getElementById('dir_button').style.display='none';
        document.getElementById('zip_button').style.display='block';
        changeDisplay(document.getElementsByClassName('zip'), 'none');
        changeDisplay(document.getElementsByClassName('dir'), 'table-row');
        document.getElementById("id_use_directories").value = 'true';
    }
    return false;
}

function show_zip() {
    if(document.getElementById('dir_button').style.display=='none') {
        document.getElementById('dir_button').style.display='table-row';
        document.getElementById('zip_button').style.display='none';
        changeDisplay(document.getElementsByClassName('zip'), 'table-row');
        changeDisplay(document.getElementsByClassName('dir'), 'none');
        document.getElementById("id_use_directories").value = 'false';
        }
    return false;
}

function changeDisplay(obj, display){
    for(var i=0, len=obj.length; i<len; i++){
        obj[i].style.display = display;
    }
}