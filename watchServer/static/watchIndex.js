// Init vars
var watchs;
var cur_watch = 0;
var mapDotSize = {height: 0, width: 0};
var alertData=[];
var resp;

//Webpage Init
$( document ).ready(function() {
	getWatchs().done(function() {
		setWatch(0);
	});
	getMaps().done(function () {
		setMap(0);
		$( "#floorMap" ).load(function() {
			getImageInfo();
			aMove(watchs[cur_watch]['ID'],false)
		});
	});
	startFetchAlert();
	getDotSize();
	startLoadImageInfo();
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
				"href": "javascript: setWatchClick("+key+");",
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

function setWatchClick(watchID) {
	if ( cur_watch >= 0 ) {
		$("#watch-"+cur_watch).removeClass("active");
		stopMoving()
	}
	$("#watch-"+watchID).addClass("active");
	cur_watch = watchID;
	startMoving(watchs[watchID]['ID'],1)
	movePos(maps[cur_map].size[0],maps[cur_map].size[1]+50)
}

// functions for the moving DOT
function getDotSize() {
	mapDotSize.height=$("#map_position").height();
	mapDotSize.width=$("#map_position").width();
}

function movePos(x,y) {
	x = imgLocs['left'] + eval(x * imgLocs['ratio'])  - mapDotSize.width / 2; 
	y = imgLocs['top'] + eval(y * imgLocs['ratio'])  - mapDotSize.height / 2;
	$("#map_position").css({"top": y+"px" , "left": x+"px"});
}

function startMoving(watchID,follow) {
	refreshcon = setInterval(function() {
		aMove(watchID,follow);
		//$('#postcontainer').load('new/posts.php', function(){  });
	}, 3000);
}

function aMove(watchID,follow) {
		$.getJSON( api_url+"watch/loc/"+watchID, function( data ) {
			if ( data[0][1][2] == cur_map ) {
				movePos(data[0][1][0],data[0][1][1])
			}
			else if ( data[0][1][2] != cur_map && follow ) {
				setMap(data[0][1][2])
				movePos(data[0][1][0],data[0][1][1])
			}
			else {
				movePos(maps[cur_map].size[0],maps[cur_map].size[1]+50)
			}
		})
}

function stopMoving() {
	try{
		clearInterval(refreshcon);
	}catch(err){}
}

function startFetchAlert() {
	refreshAlert = setInterval(function() {
		$.getJSON( api_url+"alert/new", function( data ) {
			if ( JSON.stringify(alertData) != JSON.stringify(data) ){
				alertData = data;
				showAlert(data);
			}
		});
	}, 3000);
}

function showAlert(data) {
	$( "#irruptWarning > .content , .actions" ).remove();
	$.each(data, function(key,val) {
		console.log(val);
		if ( val[1]==0 ) {
			warnLevel = 'Error';
			Title = '入侵警告';
		}
		else {
			warnLevel = 'Info';
			Title = '一般通知';
		}
		$( "<div/>", {
			"id": "warn-"+key,
			"class": "content warn "+warnLevel,
		}).appendTo( "#irruptWarning" );
		$( "<h2/>", {
			html: Title,
		}).appendTo( "#warn-"+key );
		
		if (val[3][1] == 1) {
			areaNotice = '(強制警示區)';
		}
		else {
			areaNotice = '';
		}
		$( "<p/>", {
			"class": "warnTime",
			html: "時間："+val[0]+"<br>"+"手錶："+val[2]+"<br>"+"入侵區域："+val[3][0]+areaNotice,
		}).appendTo( "#warn-"+key );

	});
	$( "<div/>", {
		"class": "actions",
		html: '<div class="ui approve button">確認警報</div>',
	}).appendTo( "#irruptWarning" );
	$("#irruptWarning").modal('show');
	
}

