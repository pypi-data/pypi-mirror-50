function show_filter_c(count) {
    if(document.getElementById('filters'+count).style.display=='none') {
        document.getElementById('filters'+count).style.display='block';
    }
    return false;
}

function hide_filter_c(count) {
    if(document.getElementById('filters'+count).style.display=='block') {
        document.getElementById('filters'+count).style.display='none';
    }
    return false;
}


function show_filters() {
    if(document.getElementById('filters').style.display=='none') {
        document.getElementById('filters').style.display='inline';
        document.getElementById('show_filter').style.display='none';
        document.getElementById('hide_filter').style.display='table-row';
    }
    return false;
}

function hide_filters() {
    if(document.getElementById('filters').style.display=='inline') {
        document.getElementById('filters').style.display='none';
        document.getElementById('hide_filter').style.display='none';
        document.getElementById('show_filter').style.display='table-row';
    }
    return false;
}