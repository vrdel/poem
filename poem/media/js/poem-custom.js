
function poem_metric_instance_defaults() {
    $('input[id*=id_metric_instances][id$=atp_service_type_flavour]:not([value])').change(function() {
    	
        var $tr = $(this).parents('tr');
        $tr.find('input[id$=vo]').val($('input[id=id_atp_vo]').val());
    });
    
    $('input[id*=id_metric_instances][id$=metric]:not([value])').change(function() {
    	
        var $tr = $(this).parents('tr');
        $tr.find('input[id$=vo]').val($('input[id=id_atp_vo]').val());
    });
}

$(document).ready(function() {
	poem_metric_instance_defaults();
});
