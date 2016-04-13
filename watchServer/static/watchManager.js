var allZone
var formBoxs
var cur_watch
var resp

$( document ).ready(function() {
	getMaps().done(function() {
		setMap(0);
		getImageInfo();
		readAllZone();
		$( "#floorMap" ).load(function() {
			imageOnlad();
		});
	});
	prepareCNameForm();
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
		$.each( data, function( key, val ) {
			con_menu = '<div class="menu">'+
				'<a class="item" href=\"javascript: launchActForm('+key+');\">啟用</a>'+
				'<a class="item" href=\"javascript: launchCName('+key+');\">更名</a>'+
				'</div>';
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

function launchActForm(watchNum) {
	cur_watch = watchNum;

	title = "<h4>"+watchs[watchNum]['name']+"("+watchs[watchNum]['ID']+")"+"</h4>";
	menu = $( "<div/>", {
		"class": "item ui form",
		"id": "settingArea",
		html: title+'<div id="settingAreaZones" />'+
			'<div id="settingAreaTime" />'+
			'<div id="settingAreaButtons" />',

	});
	$( "#settingArea" ).replaceWith(menu);

	Zones = $( "<div/>",{ 
		"class": "field form",
		"id": "settingAreaZones",
		html: "<p>許可區域：</p>",
	});
	$( "#settingAreaZones" ).replaceWith(Zones);

	formBoxs = []
	$.each( allZone, function( mapID, mapZones ) {
		$.each( mapZones , function( key,Zone) {
			var mapName = maps[mapID]['name'];
			var zoneName = Zone[0];
			var name = JSON.stringify( [mapID,Zone[0]] );

			num = formBoxs.push(name) -1;
			$( "<div/>", {
				"class": 'ui checkbox',
				html: '<input type="checkbox" class="zoneBox" id="formBox-'+num+'"><label>'+mapName+'-'+Zone[0]+'</label>'
			}).appendTo( "#settingAreaZones" );
			$( "#formBox-"+num ).click(function() {
				if (cur_map != mapID){
					setMap(mapID);
				}
			});
		});
	});

	time = $( "<div/>", {
		"class": "field",
		"id": "settingAreaTime",
		html: '<label>許可時間</label><input type="number" value="2" id="allowHours">',
	});
	$( "#settingAreaTime" ).replaceWith(time);

	buttons = $( "<div/>", {
		"class": "field",
		"id": "settingAreaButtons",
		html: '<button class="ui primary button submit" style="width: 70%;" id="settingActBtn">啟動手錶</button>'+
			'<button class="ui button" style="width: calc(30%-7px);" id="settingCanBtn">取消</button>',
	});
	$( "#settingAreaButtons" ).replaceWith(buttons);

	$( "#settingActBtn" ).click(function() {
		submitForm();
	})
	
	$( "#settingCanBtn" ).click(function() {
		reloadForm();
	}); 
}

function submitForm() {
	allowArea = readCheckedBox();
	allowHour = $( "#allowHours" ).val()
	if ( allowArea.length == 0 ) {
		alert("尚未選取可以進入的區域")
	}
	else if ( allowHour == "" ) {
		alert("請輸入許可時間")
	}
   	else{
		allowAreaStr = JSON.stringify(allowArea);
		resp = $.ajax({
			url: api_url + 'watch/Act',
			method: 'POST',
			data: {
				ID: watchs[cur_watch]['ID'],
				hour: allowHour,
				zone: allowAreaStr,
			},
		})
		.done(formSuc)
		.fail(formFail)
		.always(function() {
		});

		//console.log(watchs[cur_watch]['ID']);
		//console.log(string);
	}
}

function readCheckedBox() {
	checked = []
	$.each(formBoxs,function(key,val) {
		if ( $( "#formBox-"+key ).prop("checked") ) {
			checked.push(val);
		}
	});
	return checked;
}

function reloadForm() {
	sideBar = $( "<div/>", {
		"class": "column ui vertical menu sideMenu",
		"id": "zoneMenu",
		html: '<h3 class="ui top attached inverted header">手錶設定</h3>'+
			'<div id="settingArea"></div>',
	});
	$( "#zoneMenu" ).replaceWith(sideBar);
	readWatchs();
}

function formSuc() {
	alert(resp.responseText)
	reloadForm();
}

function formFail() {
	alert(resp.responseText)
}

function launchCName(watchNum) {
	cur_watch = watchNum;

	//Resets form input fields
	$('#changeWatchNameForm').trigger("reset");
	//Resets form error messages
	$('#changeWatchNameForm .field.error').removeClass( "error" );
	$('#changeWatchNameForm.error').removeClass( "error" );
	$('#modalChangeName').modal('show');
}

function prepareCNameForm() {
	var formSettings = {
		fields: {
			name: {
				identifier : 'name',
				rules: [{
					type   : 'empty',
					prompt : '請輸新的手錶名稱'
				}]
			},
		},
		onSuccess: formVal ,
	}

	$('#changeWatchNameForm').form(formSettings);
}

function formVal() {
	$('.modal').modal('hide');
	resp = $.ajax({ 
		url: api_url + 'watch/Name',
		method: 'POST', 
		data: {
			"ID": watchs[cur_watch]['ID'],
			"Name": $( "#name" ).val(),
		},
	}).
	done( formSuc ).
	fail( formFail ).
	always(function() {
	});
}

