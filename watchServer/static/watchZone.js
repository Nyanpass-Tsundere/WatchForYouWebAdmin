// Init vars
var zones;
var rightClick;
var leftClick;
var resp;

//Webpage Init
$( document ).ready(function() {
	getMaps().done(function () {
		setMap(0);
		$( "#floorMap" ).load(function() {
			getZones(cur_map);
			getImageInfo();
		});
		startLoadImageInfo();
		startScaleZone();
	});
	makeClickEvent();
	prepareForm();
});

// form functions
function prepareForm() {
	$("#newZoneBTN").on("click", function(){
		//$('.ui.form').submit();
	});

	var formSettings = {
		fields: {
			leftClick: {
				identifier : 'leftClick',
				rules: [{
					type   : 'empty',
					prompt : '請選擇左鍵座標'
				}]
			},
			rightClick: {
				identifier : 'rightClick',
				rules: [{
					type   : 'empty',
					prompt : '請選擇右鍵座標'
				}]
			},
			name: {
				identifier : 'zoneName',
				rules: [{
					type   : 'empty',
					prompt : '請輸入區域名稱'
				}]
			},
		},
		onSuccess: formVal ,
	}

	$('#newZoneForm').form(formSettings);
}

function formVal() {
	resp = $.ajax({ 
		url: api_url + 'zone/new',
		method: 'POST', 
		data: {
			MapID: cur_map,
			Name: $( "#zoneName" ).val(),
			LT: '[' + leftClick.toString() + ']',
			RB: '[' + rightClick.toString() + ']',
		},
	}).
	done( formSuc ).
	fail( formFail );
}

function formSuc() {
	alert(resp.responseText)
	getZones(cur_map)
}

function formFail() {
	alert(resp.responseText)
}

function makeClickEvent() {
	$('#floorMap').mousedown(function(e) {
		var offset = $(this).offset();
		var pos = [e.pageX - offset.left , e.pageY - offset.top] 
		updateClick(e.which,pos)
	});	
	$('#floorMap').bind('contextmenu', function(e) {
		return false;
	}); 
}

function updateClick(click,pos) {
	roundPos = [ Math.round(pos[0] / imgLocs['ratio']),Math.round(pos[1] / imgLocs['ratio']) ]
	switch (click) {
		case 1:
			leftClick = pos
			$('#leftClick').val(roundPos);
			break;
		case 3:
			rightClick = pos
			$('#rightClick').val(roundPos);
			break;
	}
}

function writeZoneToMenu(key,val) {
	if (val[5] === 0) {
		stat = "";
		setting = "<a href=\"javascript: changeZoneAlert("+val[0]+",1);\" class=\"item\">變更警示模式</a>"
	}
	else {
		stat = "<span class=\"AlertArea\">(強制警示)</span>";
		setting = "<a href=\"javascript: changeZoneAlert("+val[0]+",0);\" class=\"item\">變更警示模式</a>"
	}
	setting+="<a href=\"javascript: renameZone(\'"+val[0]+"\');\" class=\"renameZone item\">改名</a>"
	setting+="<a href=\"javascript: delZone(\'"+val[0]+"\');\" class=\"delZone item\">刪除</a>"
	menu = "<div class=\"menu\">"+setting+"</div>";

	icon = "<i class=\"dropdown icon\"></i>";
	$( "<div/>",{
		//"class": "item zone cfgableZone",
		"class": "ui left pointing dropdown link item  zone cfgableZone",
		"id": "cfgableZone-"+key,
		html: icon + val[0]+stat+menu
	}).appendTo( "#zoneMenu" );
	//$('ui.dropdown').dropdown();
	$('#cfgableZone-'+key).dropdown();
}

function changeZoneAlert(zone,target) {
	resp = $.ajax({ 
		url: api_url + 'zone/setAlert',
		method: 'POST', 
		data: {
			MapID: cur_map,
			Name: zone,
			Alert: target,
		},
	}).
	done( formSuc ).
	fail( formFail );
}

function renameZone(zone) {
	if ( $( "#zoneName" ).val() === "" ) {
		alert("「新區域名稱」輸入要更改後的名稱！");
	}
	else {
		resp = $.ajax({ 
			url: api_url + 'zone/rename',
			method: 'POST', 
			data: {
				MapID: cur_map,
				Name: zone,
				NewName: $( "#zoneName" ).val(),
			},
		}).
		done( formSuc ).
		fail( formFail );
	}
}

function delZone(zone) {
	resp = $.ajax({ 
		url: api_url + 'zone/del',
		method: 'POST', 
		data: {
			MapID: cur_map,
			Name: zone,
		},
	}).
	done( formSuc ).
	fail( formFail );
	//alert(cur_map+","+zone);
}
