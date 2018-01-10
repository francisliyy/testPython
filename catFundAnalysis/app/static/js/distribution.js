

$(function(){

	$('.js-example-basic-single').select2({
	  placeholder: 'Select a type of building',
	  theme: "classic"
	});

	$('#heatmapBtn').click(function(event) {
		window.open($SCRIPT_ROOT+"/myview/showHeatChart"+maptype+"/exp/"+maptype+"/"+tob+"/"+lastyear+"/"+thisyear);
	});

	$('#aalheatmapBtn').click(function(event) {
		window.open($SCRIPT_ROOT+"/myview/showHeatChart"+maptype+"/aal/"+maptype+"/"+tob+"/"+lastyear+"/"+thisyear);
	});

	$('#lcostsheatmapBtn').click(function(event) {
		window.open($SCRIPT_ROOT+"/myview/showHeatChart"+maptype+"/lcosts/"+maptype+"/"+tob+"/"+lastyear+"/"+thisyear);
	});
});

