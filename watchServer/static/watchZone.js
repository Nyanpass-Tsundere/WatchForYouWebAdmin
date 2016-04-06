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

