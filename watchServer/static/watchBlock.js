// Init vars
var blockInfo

//Webpage Init
$( document ).ready(function() {
	getMaps().done(function () {
		setMap(0);
		$( "#floorMap" ).load(function() {
			getImageInfo();
			genBlocks();
		});
		startScaleBlock()
	});
});

function startScaleBlock() {
	$( window ).resize(function() {
		scaleBlockDiv(maps[cur_map].block[0],maps[cur_map].block[1]);
	})
}

function genBlocks() {
	$(".block").remove();
	if ( maps[cur_map].block === undefined ) {
		alert('這張圖沒有設定block！')
	}
	else {
		maps[cur_map].block[0];
		maps[cur_map].block[1];
		$.getJSON( api_url + "block/" + cur_map , function( data ) {
			blockInfo = data;
			writeBlockDiv(maps[cur_map].block[0],maps[cur_map].block[1]);
			scaleBlockDiv(maps[cur_map].block[0],maps[cur_map].block[1]);
		})
		
	}
}

function initBlockInfo(x_num,y_num) {
	for (var x=0; x<x_num; x++) {
		var line = [];
		for (var y=0; y<y_num; y++) {
			line.push(0);
		}
		blockInfo.push(line);
	}
}

function writeBlockDiv(x,y) {
	if (blockInfo[x] === undefined) {
		initBlockInfo(x,y)
	}
	a = function(x,y) {
		if (blockInfo[y][x]==1) {
			divClass = 'road'
		}
		else {
			divClass = ''
		}
		$( "<div/>", {
			"class": "zone block "+divClass,
			"id": "block-"+x+"-"+y,
			html: "<div class=\"zoneAreaText blockAreaText\">"+x+","+y+"</div>"
		}).appendTo( "#map" );
		$( "#block-"+x+"-"+y ).click(function() {
			setBlock(x,y);
		});
	}
	blockFor(x,y,a)
}

function setBlock(x,y) {
	if (blockInfo[x][y] == 0) {
		blockInfo[x][y] = 1;
		$( "#block-"+x+"-"+y ).addClass("road");
	}
	else {
		blockInfo[x][y] = 0;
		$( "#block-"+x+"-"+y ).removeClass("road");
	}
}

function genCurBlockSetting() {
	console.log(JSON.stringify(blockInfo));
}

function scaleBlockDiv(x,y) {
	getImageInfo();
	blockSize = [imgLocs.width / (x)  , imgLocs.height / (y)  ];

	a=function(x,y) {
		loc_x = blockSize[0] * x + imgLocs['left'];
		loc_y = blockSize[1] * y + imgLocs['top'];
		width = blockSize[0];
		height = blockSize[1];

		$("#block-"+x+"-"+y).css({
			"left": loc_x+"px", 
			"top": loc_y+"px" ,
			"width": blockSize[0]+"px", 
			"height": blockSize[1]+"px"
		});

	}
	blockFor(x,y,a)
}

function blockFor(x_num,y_num,func) {
	for (var x=0; x<x_num; x++) {
		for (var y=0; y<y_num; y++) {
			func(x,y)
		}
	}
}
