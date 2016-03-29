// Init vars
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

