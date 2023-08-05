var url = document.getElementById("django_update_url").value;

function update() {
    // =======================================================================
    // Update for updating progress bars and table
    // =======================================================================
    // https://stackoverflow.com/questions/1879872/django-update-div-with-ajax

    // get the hidden 'selected_items' object

    $.getJSON(url, function(data){
        // Enumerate JSON
        var table_data = data.table_data;
        var wtable = document.getElementById("status_table");
        document.getElementById("updating").innerHTML = 'Initial updating complete (updates will occur in the background now periodically). Refresh the page ' +
                                                         'if entries are not updating as expected';
        document.getElementById("update_spinner").style.display = "none";

        $("tbody").find("tr").each(function(i) { //get all rows in table
            var new_row = table_data[i];
            for (var key in new_row) {
                    var value = new_row[key];
                    if (key === 'estimated_progress'){
                        perc = Math.round(value);
                        var text_for_div = perc+"%";
                        var style_width = "width:"+perc+"%";
                        $(this).find('.progress-bar').text(text_for_div);
                        $(this).find('.progress-bar').attr("style", style_width);
                        $(this).find('.progress-bar').attr("aria-valuenow", perc);
                    }else if (key === 'history_data_bioblend_list'){
                        $(this).find('.history_data_bioblend_list a').attr('href', value);
                    }else{
                        $(this).find('td.'+key).text(value);
                    }
            }
        });
        setTimeout('update()', 1000)
        });
}
// update();






$(document).ready(function() {
    update();

});
