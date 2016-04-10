var allZone

$( document ).ready(function() {
	getMaps().done(function() {
		setMap(0);
		getImageInfo();
		readAllZone();
	});
	$( "#floorMap" ).load(function() {
		imageOnlad();
	});
	readWatchs();
});


function readAllZone() {
	allZone = [];
	$.each( maps,function(key,val) {
		getZones(key,false,false).done(function() {
			allZone.push(zones);
		});
	});
}

function imageOnlad() {
	getZones(cur_map,true,false).done(function() {
		allZone[cur_map] = zones
	});
}

function readWatchs() {
	var r = $.Deferred();
	$.getJSON( api_url+"watch/list", function( data ) {
		watchs = data;

		con_icon = '<i class="dropdown icon"></i>';
		con_menu = '<div class="menu"><div class="item">設定</div><div class="item">更名</div><div class="item">刪除</div></div>'
		$.each( data, function( key, val ) {
			$( "<div/>", {
				"class": "ui left pointing dropdown link item watch",
				"id": "watch-"+key,
				html: con_icon+val.name+con_menu,
			}).insertBefore( "#settingArea" );
			r.resolve();
			$('#watch-'+key).dropdown();
		});
	});
	return r;
}

