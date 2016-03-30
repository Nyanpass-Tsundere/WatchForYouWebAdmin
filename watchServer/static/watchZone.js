// Init vars
var zones;

//Webpage Init
$( document ).ready(function() {
	getAreas().done(function () {
		setArea(0);
		getZones(cur_map);
	});
});

$( window ).resize(function() {
	$.each( zones, function( key, val ){
		scaleZone(key,val)
	});
})

function getZones(MapID) {
	var r = $.Deferred();
	$.getJSON( api_url+"zone/list/"+MapID, function( data ) {
		if ( data[0] == 0 ) {
			zones = data[1];
		}
		$.each( zones, function( key, val ){
			writeZone(key,val)
		});
		r.resolve();
	})
	return r;
}

function writeZone(key,val) {
	$( "<div/>", {
		"class": "zone",
		"id": "zone-"+key,
		html: "<div class=\"zoneText\">"+val[0]+"</div>"
	}).appendTo( "#map" );
	scaleZone(key,val);
}

function scaleZone(key,val) {
	getImageInfo();
	y = imgLocs['left'] + eval(val[3])[0] * imgLocs['prec'] + imgLocs['pedding'];
	x = imgLocs['top'] + eval(val[3])[1] * imgLocs['prec'];
	width = ( eval(val[4])[0] - eval(val[3])[0] ) * imgLocs['prec'] ;
	height = ( eval(val[4])[1] - eval(val[3])[1] ) * imgLocs['prec'] ;
	$("#zone-"+key).css({"top": x+"px" , "left": y+"px", "width": width+"px", "height": height+"px"});
}
