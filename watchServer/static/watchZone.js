// Init vars
var zones;
var rightClick;
var leftClick;

//Webpage Init
$( document ).ready(function() {
	getMaps().done(function () {
		setMap(0);
		$( "#floorMap" ).load(function() {
			getZones(cur_map);
		});
		startLoadImageInfo();
		startScaleZone();
	});
	makeClickEvent();
	prepareForm();
});

function startScaleZone() {
	$( window ).resize(function() {
		ScaleZone()
	})
}

function ScaleZone() {
	$.each( zones, function( key, val ){
		scaleZone(key,val)
	});
}

// form functions
function prepareForm() {
	$("#newZoneBTN").on("click", function(){
		$('.ui.form').submit();
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
		onSuccess: formSuc ,
	}

	$('#newZoneForm').form(formSettings);
}

function formSuc() {
  alert("Valid Submission, modal will close.");
}

function makeClickEvent() {
	$('#floorMap').mousedown(function(e) {
		var offset = $(this).offset();
		var pos = [e.pageX - offset.left , e.pageY - offset.top] 
		updateClick(e.which,pos)
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

function getZones(MapID) {
	var r = $.Deferred();
	$.getJSON( api_url+"zone/list/"+MapID, function( data ) {
		$( ".zone" ).remove();
		if ( data[0] == 0 ) {
			zones = data[1];
			$.each( zones, function( key, val ){
				writeZone(key,val)
			});
		}
		r.resolve();
	})
	return r;
}

function writeZone(key,val) {
	$( "<div/>", {
		"class": "zone zoneArea",
		"id": "zone-"+key,
		html: "<div class=\"zoneAreaText\">"+val[0]+"</div>"
	}).appendTo( "#map" );
	scaleZone(key,val);
	$( "<div/>",{
		"class": "item zone cfgableZone",
		"id": "cfgableZone-"+key,
		html: val[0]+"<br>"+val[5]
	
	}).appendTo( "#zoneMenu" );
}

function scaleZone(key,val) {
	getImageInfo();
	y = imgLocs['left'] + eval(val[3])[0] * imgLocs['ratio'];
	x = imgLocs['top'] + eval(val[3])[1] * imgLocs['ratio'];
	width = ( eval(val[4])[0] - eval(val[3])[0] ) * imgLocs['ratio'] ;
	height = ( eval(val[4])[1] - eval(val[3])[1] ) * imgLocs['ratio'] ;
	$("#zone-"+key).css({"top": x+"px" , "left": y+"px", "width": width+"px", "height": height+"px"});
}
