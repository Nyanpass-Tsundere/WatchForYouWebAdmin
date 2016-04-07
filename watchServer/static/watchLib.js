var api_url="api_web/"
var imgLocs;
var maps;
var cur_map = 0;

function startLoadImageInfo() {
	$( window ).resize(function() {
		getImageInfo();
	});
}

//function-about-map-image
function getMaps() {
	var r = $.Deferred();
	$.getJSON( api_url+"maps", function( data ) {
		maps = data;
		var items = [];
		$.each( data, function( key, val ) {
			$( "<a/>", {
				"class": "item",
				"id": "area-"+key,
				"href": "javascript: setMap("+key+");",
				html: val.name
			}).appendTo( "#floorList" );
			r.resolve();
		});
	});
	return r;
};

function setMap(areaID) {
	if ( cur_map >= 0 ) {
		$("#area-"+cur_map).removeClass("active");
	}
	$("#area-"+areaID).addClass("active");
	cur_map = areaID;
	$("#floorMap").attr("src",maps[cur_map]['map'])
}

function getImageInfo() {
	//image location on Page
	var pos = $("#floorMap").position();
	//when image too small, semantic-ui will add auto margin make image place in center
	pos['left'] = pos['left'] + parseInt($('#floorMap').css('margin-left'));
	//image size on page
	pos.height = $( "#floorMap" ).height();
	pos.width = $( "#floorMap" ).width();
	//ratio for convert real-Location to display-Location
	pos.ratio =  $( "#floorMap" ).width() / maps[cur_map]['size'][0] 
	imgLocs = pos;
}

//Function about Zones
function startScaleZone() {
	$( window ).resize(function() {
		ScaleZone()
	})
}

function ScaleZone() {
	$.each( zones, function( key, val ){
		scaleZone(key,val)
	});
}

function getZones(MapID,writeToMap = true,writeToMenu = true) {
	var r = $.Deferred();
	$.getJSON( api_url+"zone/list/"+MapID, function( data ) {
		$( ".zone" ).remove();
		if ( data[0] == 0 ) {
			zones = data[1];
			if ( writeToMap ) 
				$.each( zones, function( key, val ) 
					writeZoneToMap(key,val) );
			
			if ( writeToMenu ) 
				$.each( zones, function( key, val )
					writeZoneToMenu(key,val) );
		}
		r.resolve();
	})
	return r;
}

function writeZoneToMap(key,val) {
	$( "<div/>", {
		"class": "zone zoneArea",
		"id": "zone-"+key,
		html: "<div class=\"zoneAreaText\">"+val[0]+"</div>"
	}).appendTo( "#map" );
	scaleZone(key,val);
}

function scaleZone(key,val) {
	getImageInfo();
	y = imgLocs['left'] + eval(val[3])[0] * imgLocs['ratio'];
	x = imgLocs['top'] + eval(val[3])[1] * imgLocs['ratio'];
	width = ( eval(val[4])[0] - eval(val[3])[0] ) * imgLocs['ratio'] ;
	height = ( eval(val[4])[1] - eval(val[3])[1] ) * imgLocs['ratio'] ;
	$("#zone-"+key).css({"top": x+"px" , "left": y+"px", "width": width+"px", "height": height+"px"});
}
