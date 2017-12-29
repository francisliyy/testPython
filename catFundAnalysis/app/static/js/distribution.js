

$(function(){

	$('.js-example-basic-single').select2({
	  placeholder: 'Select a type of building',
	  theme: "classic"
	});

	$('#heatmapBtn').click(function(event) {
		window.open($SCRIPT_ROOT+"/myview/showHeatChartCounty/"+tobSelectedType+"/2016/2017");
	});
});

