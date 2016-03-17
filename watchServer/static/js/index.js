// Init vars
var api_url="api_web/"
var watchs;
var cur_watch = 0;
var areas;
var cur_area = 0;
var imgLocs;
var mapDotSize = {height: 0, width: 0};

//Webpage Init
$( document ).ready(function() {
	getWatchs().done(function() {
		setWatch(0);
	});
	getAreas().done(function () {
		setArea(0);
	});
	getDotSize();
});

$( window ).resize(function() {
	getImageInfo();
});

//function-about-watchs
function getWatchs() {
	var r = $.Deferred();
	$.getJSON( api_url+"watch/list/act", function( data ) {
		watchs = data;
		$.each( data, function( key, val ) {
			$( "<a/>", {
				"class": "item",
				"id": "watch-"+key,
				"href": "javascript: setWatch("+key+");",
				html: val.name
			}).appendTo( "#watchList" );
			r.resolve();
		});
	});
	return r;
}

function setWatch(watchID) {
	if ( cur_watch >= 0 ) {
		$("#watch-"+cur_watch).removeClass("active");
	}
	$("#watch-"+watchID).addClass("active");
	cur_watch = watchID;
}

//function-about-areas
function getAreas() {
	var r = $.Deferred();
	$.getJSON( api_url+"areas", function( data ) {
		areas = data;
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
	if ( cur_area >= 0 ) {
		$("#area-"+cur_area).removeClass("active");
	}
	$("#area-"+areaID).addClass("active");
	cur_area = areaID;
	$("#floorMap").attr("src",areas[cur_area].map)
}

function getImageInfo() {
	var pos = $("#floorMap").position();
	pos.height = $( "#floorMap" ).height();
	pos.width = $( "#floorMap" ).width();
	pos.pedding =  parseInt($('#floorMap').css('margin-left'));
	imgLocs = pos;
}

// functions for the moving DOT
function getDotSize() {
	mapDotSize.height=$("#map_position").height();
	mapDotSize.width=$("#map_position").width();
}

function movePos(x,y) {
	$("#map_position").css({"top": x+"px" , "left": y+"px"});
}

function movePosPrec(x,y) {
	movePos(
			imgLocs.top + imgLocs.height * x - mapDotSize.height / 2,
			imgLocs.left + imgLocs.pedding + imgLocs.width * y - mapDotSize.width / 2
			);
}
