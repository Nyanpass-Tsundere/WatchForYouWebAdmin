var allZone

$( document ).ready(function() {
	getMaps().done(function() {
		setMap(0);
		getImageInfo();
	});
	$('.ui.dropdown')
		.dropdown()
	;
});

function readAllZone() {
	allZone = [];
	$.each( maps,function(key,val) {
		getZones(key,false,false);
		allZone.push(zones);
	});
}
