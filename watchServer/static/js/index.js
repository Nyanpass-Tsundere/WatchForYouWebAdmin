var api_url="api_web/"

var watchs;
var cur_watch = 0;
var areas;
var cur_area = 0;
var imgLocs;

$( '#floorMap' ).ready(function() {
	//setTimeout(5000);
	//getImageInfo();
	//alert("fuck World");
});  

$( document ).ready(function() {
	getWatchs();
	getAreas();
});

$( window ).resize(function() {
	getImageInfo();
});

function getWatchs() {
	$.getJSON( api_url+"watchs", function( data ) {
		watchs = data;
		var items = [];
		var first = " active";
		$.each( data, function( key, val ) {
			$( "<a/>", {
				"class": "item"+first,
				"id": "watch-"+key,
				"href": "javascript: setWatch("+key+");",
				html: val
			}).appendTo( "#watchList" );
			first = "";
		});
	});
}

function setWatch(watchID) {
	if ( cur_watch >= 0 ) {
		$("#watch-"+cur_watch).removeClass("active");
	}
	$("#watch-"+watchID).addClass("active");
	cur_watch = watchID;
}

//好不容易成功可是覺得很髒的語法
function getWatchs_fullDiv() {
	$.getJSON( api_url+"watchs", function( data ) {
		var items = [];
		$.each( data, function( key, val ) {
			items.push( "<a id='watch" + key + "' class='item'>" + val + "</a>" );
		});
	
	$( "<div/>", {
		"id": "watchList",
		"class": "ui vertical pointing menu",
		html: items.join( "" )
		}).appendTo( "#sidebar" );
	});
}

function getAreas() {
	$.getJSON( api_url+"areas", function( data ) {
		areas = data;
		var items = [];
		var first = " active";
		$.each( data, function( key, val ) {
			$( "<a/>", {
				"class": "item"+first,
				"id": "area-"+key,
				"href": "javascript: setArea("+key+");",
				html: val
			}).appendTo( "#floorList" );
			first = "";
		});
	});
}

function setArea(areaID) {
	if ( cur_area >= 0 ) {
		$("#area-"+cur_area).removeClass("active");
	}
	$("#area-"+areaID).addClass("active");
	cur_area = areaID;
}

function getImageInfo() {
	var pos = $("#floorMap").position();
	pos.height = $( "#floorMap" ).height();
	pos.width = $( "#floorMap" ).width();
	imgLocs = pos;
}
