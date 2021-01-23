var intervalID ;
var url = "http://ofenwatch.woller.pizza/php/ofenwatch/get_data.php";

var i = 0;
var local = true; //Set this value depending on the running environment of this script 

function init() {
	if (!local) {
		loadData();
		startPeriodicallyLoading();
		main();
	} else {
		//main();
	}
}

function startPeriodicallyLoading() {
	intervalID = setInterval(function(){loadData();}, 5000);

}

function stopPeriodicallyLoading() {
	clearInterval(intervalID);
}

function loadDataAndDraw() {
	xhttp.open("POST", "demo_post.asp", true);
	xhttp.send();
}

function loadData() {
	
	console.log("loadData");
	
	var xhttp;
	xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			//cFunction(this);
			parseJSONData(this.responseText);
			//console.log(this.responseText);
		}
	};

	xhttp.open("POST", url, true);
	xhttp.send();

} 

//Use this on local Ofen-client, get data directly from PI source, don't access remote DB
eel.expose(loadData_Interrupt);
function loadData_Interrupt(data) {
	console.log("loadData_Interrupt Data:");
	console.log(data);
	parseJSONData(data);
}

eel.expose(loadData_Interrupt_Settings);
function loadData_Interrupt_Settings(drosselklappe, air, automode, fastheatup, temp2hold, fan ,errors) {
	console.log("loadData_Interrupt_Settings");
	updateCurrentSettingValues(drosselklappe, air, automode, fastheatup, temp2hold, errors);
}


function parseJSONData(jsonText) {
	
	obj = JSON.parse(jsonText);
	
	//console.log(obj[1].timestamp);
	//console.log(obj[10].timestamp);
	
	var latestEntry = obj[obj.length-1];
	//console.log(latestEntry.timestamp);
	
	//trigger redrawing
	update(latestEntry);
	
	//trigger chart updates
	updateChartofenwatch(obj);
}


function myFunction(xhttp) {
 // document.getElementById("demo").innerHTML =
  //xhttp.responseText;
}