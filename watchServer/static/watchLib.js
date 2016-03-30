var api_url="api_web/"
var imgLocs;
var maps;
var cur_map = 0;

$( window ).resize(function() {
	getImageInfo();
});

//function-about-watchs
function setWatch(watchID) {
	if ( cur_watch >= 0 ) {
		$("#watch-"+cur_watch).removeClass("active");
		stopMoving()
	}
	$("#watch-"+watchID).addClass("active");
	cur_watch = watchID;
	startMoving(watchs[watchID]['ID'],1)
}

//function-about-maps
function getAreas() {
	var r = $.Deferred();
	$.getJSON( api_url+"maps", function( data ) {
		maps = data;
		var items = [];
		$.each( data, function( key, val ) {
			$( "<a/>", {
				"class": "item",
				"id": "area-"+key,
				"href": "javascript: setArea("+key+");",
				html: val.name
			}).appendTo( "#floorList" );
			r.resolve();
		});
	});
	return r;
};

function setArea(areaID) {
	if ( cur_map >= 0 ) {
		$("#area-"+cur_map).removeClass("active");
	}
	$("#area-"+areaID).addClass("active");
	cur_map = areaID;
	$("#floorMap").attr("src",maps[cur_map].map)
}

function getImageInfo() {
	var pos = $("#floorMap").position();
	pos.height = $( "#floorMap" ).height();
	pos.width = $( "#floorMap" ).width();
	pos.pedding =  parseInt($('#floorMap').css('margin-left'));
	pos.prec =  $( "#floorMap" ).width() / maps[cur_map]['size'][0] 
	imgLocs = pos;
}

