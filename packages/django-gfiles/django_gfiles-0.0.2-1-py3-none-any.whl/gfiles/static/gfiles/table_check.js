////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Standard AJAX setup for django
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Table check session store
////////////////////////////////////////////////////////////////////////////////////////////////////////////////


function toggle(source) {
    var check_name = 'check';
    var table_id = source.parentElement.parentElement.parentElement.parentElement.id;

    checkboxes = document.getElementsByName('check'+table_id);
    for(var i=0; i < checkboxes.length; i++) {
        checkboxes[i].checked = +source.checked;
    }
}

function addfile(source) {
	// Try to grab any from storage and append/push them to the newly created 'selected_items' array

}

function clearSelection(source) {
    var selected_items = clear();
    postSelectedItems(selected_items);
}

function clear(){
    var tnum = $('.table-container').length;

    for(var i=0; i < tnum; i++) {
        // get all the check boxes
        if (tnum==1){
            var checkboxes = document.getElementsByName('check');
        }else{
            var checkboxes = document.getElementsByName('check'+i);
        }
        for(var j=0; j < checkboxes.length; j++) {
            checkboxes[j].checked = false;
        }
    }

    var selected_items_str = document.getElementById("selected_items").value;
    var selected_items = JSON.parse(selected_items_str);
    for (var k in selected_items) {
        if (selected_items.hasOwnProperty(k)) {
            selected_items[k] = 0;
        }
    }

    return selected_items;

}



var lots_of_stuff_already_done = false;

// $(document).ready(function() will run at on the start of page load
$(document).ready(function() {
    // =======================================================================
    // Update the checkbox with any previous checks from the django session whenever page is opened
    // =======================================================================
    // get the hidden 'selected_items' object
    var s = document.getElementById("selected_items").value;

    if (s){
        var selected_items = JSON.parse(s);
        var tnum = $('.table-container').length;


        for(var i=0; i < tnum; i++) {
            // get all the check boxes
            if (tnum==1){
                var checkboxes = document.getElementsByName('check');
            }else{
                var checkboxes = document.getElementsByName('check'+i);
            }
            // loop through all the checkboxes and see if we have an equivalent saved selected item
            // if we do, then add if it is true (1) or false (0)
            for(var j=0; j < checkboxes.length; j++) {
                // combined key of the table_id and
                var cv = i+'_'+checkboxes[j].value;
                if (cv in selected_items){
                    checkboxes[j].checked = selected_items[cv];
                }

            }
        }
    }


    $('ul.pager li').mouseover(function(e) { saveSelectedItems(e);  });
    // $('form').mouseover(function(e) { saveSelectedItems(e);  });
    // $('ul.pager li').unbind('click').bind('click', function(e) { saveSelectedItems(e, 'c');  });
    $("button").mouseover(function(e) { saveSelectedItems(e);  });

});

function saveSelectedItems(e){
    // if (lots_of_stuff_already_done) {
    //     lots_of_stuff_already_done = false; // reset flag
    //
    //     return; // let the event bubble away
    // }

    var tnum = $('.table-container').length;

    e.preventDefault();
    // e.stopPropagation();

    var selected_items_to_save = {};

    for(var i=0; i < tnum; i++) {
        // get all the check boxes from each table
        if (tnum==1){
            var checkboxes = document.getElementsByName('check');
        }else{
            var checkboxes = document.getElementsByName('check'+i);
        }
        // loop through all the check box from a particular and save the results (using a combined key to track)
        for (var j = 0; j < checkboxes.length; j++) {
            var cv = i+'_'+checkboxes[j].value;
            selected_items_to_save[cv] = +checkboxes[j].checked;
        }
    }



    postSelectedItems(selected_items_to_save);

    // lots_of_stuff_already_done = true; // set flag
    // if (op !== 'c') {
    //     $('this').trigger("submit");
    // } else {
    //     $('this').trigger("click");
    // }
    // location.reload();

}

function postSelectedItems(selected_items_to_save){
    var url = document.getElementsByName('django_url')[0].value;
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    $.ajax({
            url: url,
            type: 'POST',

            // contentType: 'application/json',
            csrfmiddlewaretoken: csrftoken,
            async:   true,
            data: JSON.stringify({'selected_items':selected_items_to_save}),
            success: function() {
                console.log('SUCCESS');
            },
            error: function (data, e) {
                sc = data.statusCode();
                console.log('Sorry, there was an error. ('+data.statusText+ ' ' + ' ' + data.status + ' ' + e);
            }
        });
}
