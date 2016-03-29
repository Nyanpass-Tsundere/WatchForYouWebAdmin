// Init vars
var api_url="api_web/"
var watchs;
var cur_watch = 0;
var maps;
var cur_map = 0;
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

function startMoving(watchID,follow) {
	refreshcon = setInterval(function() {
			$.getJSON( api_url+"watch/loc/"+watchID, function( data ) {
				if ( data[0][1][2] != cur_map && follow ) {
					setArea(data[0][1][2])
				}
				movePosPrec(data[0][1][0],data[0][1][1])

			})
		//$('#postcontainer').load('new/posts.php', function(){  });
	}, 3000);
}

function stopMoving() {
	try{
		clearInterval(refreshcon);
	}catch(err){}
}
