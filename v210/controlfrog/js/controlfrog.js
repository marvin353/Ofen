// Colour settings
if(themeColour == 'white'){
	var metric = '#a9a9a9';
	var backColor = '#7d7d7d';
	var pointerColor = '#898989'; 	
	var pageBackgorund = '#fff';
	var pieTrack = metric;
	var pieBar = backColor;
	var gaugeTrackColor = metric;
	var gaugeBarColor = backColor;
	var gaugePointerColor = '#ccc';
	var pieSegColors = [metric,'#868686','#636363','#404040','#1d1d1d'];	
	var line= {
		line: '#7d7d7d',
		background: '#EFEFEF',
		pageBackgorund: '#fff',
		pointBackgroundColor: '#7d7d7d',
		pointBorderColor: '#7d7d7d',
	};
	var area = {
		line: '#363636',
		background: '#7d7d7d',
		pointBackgroundColor: '#363636',
		pointBorderColor: '#363636',
	};
	var pie = {
		pieSegColors: ['#7d7d7d','#868686','#636363','#404040','#1d1d1d'],
		border: '#fff'
	}
}
else {
	//default to black
	var backColor = '#4f4f4f';
	var metric = '#f2f2f2';	
	var pointerColor = '#898989'; 
	var pageBackgorund = '#2b2b2b';	
	var pieSegColors = [metric,'#c0c0c0','#8e8e8e','#5b5b5b','#292929'];
	var pieTrack = backColor;
	var pieBar = metric;
	var gaugeTrackColor = '#4f4f4f';
	var gaugeBarColor = '#898989';
	var gaugePointerColor = metric;
	var line = {
		line: '#ffffff',
		background: '#363636',
		pageBackgorund: '#25394d',
		pointBackgroundColor: '#ffffff',
		pointBorderColor: '#ffffff',
	};
	var area = {
		line: '#363636',
		background: '#232323',
		pointBackgroundColor: '#363636',
		pointBorderColor: '#363636',
	};
	var pie = {
		pieSegColors: ['#f2f2f2','#c0c0c0','#8e8e8e','#5b5b5b','#292929'],
		border: '#2b2b2b'
	}
}


// Stores
var cf_rSVPs = [];
var cf_rGs = [];
var cf_rZGs = [];
var cf_rLs = [];
var cf_rPs = [];
var cf_rRags = [];
var cf_rFunnels = [];

$(document).ready(function(){
	
	// Navigation 
	$('.cf-nav-toggle').click(function(e){

		if( $('.cf-nav').hasClass('cf-nav-state-min') ){
			$('.cf-nav').removeClass('cf-nav-state-min').addClass('cf-nav-state-max');
			$('.cf-container').addClass('cf-nav-state-max');
		}
		else{
			$('.cf-nav').removeClass('cf-nav-state-max').addClass('cf-nav-state-min');		
			$('.cf-container').removeClass('cf-nav-state-max');			
		}
		
		e.preventDefault();
	});
		
	// Time and date display 
	(function updateTime(){
		var now = moment();
		
		$('.cf-td').each(function(){
			if($(this).hasClass('cf-td-12')){
				$('.cf-td-time', $(this)).html(now.format('h:mm'));
				ampm = now.format('a');
				$('.cf-td-time', $(this)).append('<span>'+ampm+'</span>');
			}
			else{
				$('.cf-td-time', $(this)).html(now.format('HH:mm'));
			}

			$('.cf-td-day', $(this)).html(now.format('dddd'));   			
			$('.cf-td-date', $(this)).html(now.format('MMMM Do YYYY'));   
		});
	
		setTimeout(updateTime, 3000);
	})();
}); // end doc ready




/*
*
* Pie charts (cf-pie)
*
*/
$(document).ready(function() {
	// Default Pie options
	window.cf_defaultPieOpts = {};		
	cf_defaultPieOpts.responsive = true;
	cf_defaultPieOpts.maintainAspectRatio = false;
	cf_defaultPieOpts.legend = {
		display: true,
		position: 'right'
	};
	
	/*
	*	Copy the each() function for each Pie chart
	* 	e.g. $('#cf-pie-1').each(function(){.....}
	*/	
	$('.cf-pie').each(function(){
		/*
		// Set custom options and merge with default
		customOptions = {};
		customOptions.legend.display = false;
		var pieOptions = $.extend({}, cf_defaultPieOpts, customOptions);
		*/
		
		// No custom options
		var pieOptions = cf_defaultPieOpts;

		// Get canvas
		var ctx = $('canvas', $(this));
		
		// Make bar chart
		var myBarChart = new Chart(ctx, {
				type: 'pie',
				data: {
					datasets: [
						{
							data: [10, 20, 30],
							backgroundColor: [
								pie.pieSegColors[0],
								pie.pieSegColors[1],
								pie.pieSegColors[2],
							],
							borderColor: pie.border,
						}
					],
					labels: [
							'Good',
							'Bad',
							'Ugly'
					]
				},
				options: pieOptions
		});
	});
});




/*
*
* Line chart (cf-line)
*
*/
$(document).ready(function() {
	// Default line options
	window.cf_defaultLineOpts = {};		
	cf_defaultLineOpts.responsive = true;
	cf_defaultLineOpts.maintainAspectRatio = false;
	cf_defaultLineOpts.legend = {
		display: false
	};
	cf_defaultLineOpts.scales = {
		xAxes: [{
				display: false
		}]
	};
	cf_defaultLineOpts.layout = {
		padding: {
			right: 4
		}
	};
	
	/*
	*	Copy the each() function for each doughnut chart you
	* 	e.g. $('#cf-line-1').each(function(){.....}
	*/	
	$('.cf-line').each(function(){
		/*
		// Set custom options and merge with default
		customOptions = {};
		customOptions.legend.display = false;
		var lineOptions = $.extend({}, cf_defaultLineOpts, customOptions);
		*/
		
		// No custom options
		var lineOptions = cf_defaultLineOpts;

		// Get canvas
		var ctx = $('canvas', $(this));
		
		// Make bar chart
		var myBarChart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          datasets: [
            {
              backgroundColor: line.background,
              borderColor: line.line,
              pointBackgroundColor: line.pointBackgroundColor,
              pointBorderColor: line.pointBorderColor,
              data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
            }
          ]
				},
				options: lineOptions
		});
	});
});



/*
*
* Doughnut
*
*/
$(document).ready(function() {
	// Default doughnutt options
	window.cf_defaultDoughnutOpts = {};		
	cf_defaultDoughnutOpts.responsive = true;
	cf_defaultDoughnutOpts.maintainAspectRatio = false;
	cf_defaultDoughnutOpts.legend = {
		display: true,
		position: 'right'
	};
	
	/*
	*	Copy the each() function for each doughnut chart you
	* 	e.g. $('#cf-doughnut-1').each(function(){.....}
	*/	
	$('.cf-doughnut').each(function(){
		/*
		// Set custom options and merge with default
		customOptions = {};
		customOptions.legend.display = false;
		var doughnutOptions = $.extend({}, cf_defaultDoughnutOpts, customOptions);
		*/
		
		// No custom options
		var doughnutOptions = cf_defaultDoughnutOpts;

		// Get canvas
		var ctx = $('canvas', $(this));
		
		// Make bar chart
		var myBarChart = new Chart(ctx, {
				type: 'doughnut',
				data: {
					datasets: [
						{
							data: [10, 20, 30],
							backgroundColor: [
								pie.pieSegColors[0],
								pie.pieSegColors[1],
								pie.pieSegColors[2],
							],
							borderColor: pie.border,
						}
					],
					labels: [
							'Good',
							'Bad',
							'Ugly'
					]
				},
				options: doughnutOptions
		});
	});
});




/*
*
* Single Metric & Change & Bars (cf-svmc-chart)
*
*/
$(document).ready(function() {
	// Default bar chart options
	window.cf_defaultSMBarOpts = {};		
	cf_defaultSMBarOpts.responsive = true;
	cf_defaultSMBarOpts.maintainAspectRatio = false;
	cf_defaultSMBarOpts.legend = {
		display: false
	};
	cf_defaultSMBarOpts.scales = {
		xAxes: [{
				display: false,
				barPercentage: 0.7,
				categoryPercentage: 1
		}],
		yAxes: [{
				display: false,
		}]
	};
	cf_defaultSMBarOpts.barPercentage = 1;
	cf_defaultSMBarOpts.categoryPercentage = 1;	

	/*
	*	Copy the each() function for each bar chart you
	* 	e.g. $('#cf-svmc-bars-1').each(function(){.....}
	*/	
	$('.cf-svmc-bars').each(function(){
		/*
		// Set custom options and merge with default
		customBarOptions = {};
		customBarOptions.barPercentage = 2;
		var smBarOptions = $.extend({}, cf_defaultSMBarOpts, smBarOptions);
		*/
		
		// No custom options
		var smBarOptions = cf_defaultSMBarOpts;

		// Get canvas
		var ctx = $('canvas', $(this));
		
		// Make bar chart
		var myBarChart = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'],
					datasets: [
						{
							backgroundColor: metric,
							data: [100, 200, 500, 900, 500, 100, 300, 500, 200, 100, 100, 80, 200, 900, 450, 300]
						}
					],
				},
				options: smBarOptions
		});
	});
});




/*
*
* Single Metric & Change & Area chart (cf-svmc-area)
*
*/
$(document).ready(function() {
	// Default bar chart options
	window.cf_defaultSMAreaOpts = {};		
	cf_defaultSMAreaOpts.responsive = true;
	cf_defaultSMAreaOpts.maintainAspectRatio = false;
	cf_defaultSMAreaOpts.legend = {
		display: false
	};
	cf_defaultSMAreaOpts.scales = {
		xAxes: [{
				display: false,
		}],
		yAxes: [{
				display: false,
		}]
	};
	cf_defaultSMAreaOpts.barPercentage = 1;
	cf_defaultSMAreaOpts.categoryPercentage = 1;


	/*
	*	Copy the each() function for each bar chart you
	* 	e.g. $('#cf-svmc-area-1').each(function(){.....}
	*/	
	$('.cf-svmc-area').each(function(){
		/*
		// Set custom options and merge with default
		customBarOptions = {};
		customBarOptions.barPercentage = 2;
		var smBarOptions = $.extend({}, cf_defaultSMAreaOpts, smBarOptions);
		*/
		
		// No custom options
		var smAreaOptions = cf_defaultSMAreaOpts;

		// Get canvas
		var ctx = $('canvas', $(this));
		
		// Make bar chart
		var myBarChart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'],
					datasets: [
						{
							backgroundColor: area.background,
							borderColor: area.line,
							pointBackgroundColor: area.pointBackgroundColor,
							pointBorderColor: area.pointBorderColor,
							pointRadius: 1,
							data: [100, 200, 500, 900, 500, 100, 300, 500, 50, 150, 100, 80, 200, 900, 450]
						}
					],
				},
				options: smAreaOptions
		});
	});
});




/*
*
* Single Metric & Change & trend chart (cf-svmc-area)
*
*/
$(document).ready(function() {
	// Default line chart options
	window.cf_defaultSMTreaOpts = {};		
	cf_defaultSMTreaOpts.responsive = true;
	cf_defaultSMTreaOpts.maintainAspectRatio = false;
	cf_defaultSMTreaOpts.legend = {
		display: false
	};
	cf_defaultSMTreaOpts.scales = {
		xAxes: [{
				display: false,
		}],
		yAxes: [{
				display: false,
		}]
	};
	cf_defaultSMTreaOpts.barPercentage = 1;
	cf_defaultSMTreaOpts.categoryPercentage = 1;


	/*
	*	Copy the each() function for each line/trend chart you
	* 	e.g. $('#cf-svmc-trend-1').each(function(){.....}
	*/	
	$('.cf-svmc-trend').each(function(){
		/*
		// Set custom options and merge with default
		customOptions = {};
		customOptions.barPercentage = 2;
		var smTrendOptions = $.extend({}, cf_defaultSMTreaOpts, customOptions);
		*/
		
		// No custom options
		var smTrendOptions = cf_defaultSMTreaOpts;

		// Get canvas
		var ctx = $('canvas', $(this));
		
		// Make bar chart
		var myBarChart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'],
					datasets: [
						{
							backgroundColor: pageBackgorund,
							borderColor: line.line,
							pointBackgroundColor: line.pointBackgroundColor,
							pointBorderColor: line.pointBorderColor,
							lineTension: 0,
							pointRadius: 1,
							data: [100, 200, 500, 900, 500, 100, 300, 500, 50, 150, 100, 80, 200, 900, 450]
						}
					],
				},
				options: smTrendOptions
		});
	});
});



/*
*
* Bar charts (cf-bar)
*
*/
$(document).ready(function() {
	// Default bar chart options
	window.cf_defaultBarOpts = {};		
	cf_defaultBarOpts.responsive = true;
	cf_defaultBarOpts.maintainAspectRatio = false;
	cf_defaultBarOpts.legend = {
		display: false
	};
	cf_defaultBarOpts.scales = {
		xAxes: [{
				display: false,
				barPercentage: 0.7,
				categoryPercentage: 1
		}]
	};
	cf_defaultBarOpts.barPercentage = 1;
	cf_defaultBarOpts.categoryPercentage = 1;


	/*
	*	Copy the each() function for each bar chart you
	* 	e.g. $('#cf-bar-1').each(function(){.....}
	*/	
	$('.cf-bar').each(function(){
		/*
		// Set custom options and merge with default
		customBarOptions = {};
		customBarOptions.barPercentage = 2;
		var barOptions = $.extend({}, cf_defaultBarOpts, customBarOptions);
		*/
		
		// No custom options
		var barOptions = cf_defaultBarOpts;

		// Get canvas
		var ctx = $('canvas', $(this));
		
		// Make bar chart
		var myBarChart = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          datasets: [
            {
              backgroundColor: metric,
              data: [40, 20, 28, 39, 20, 40, 39, 80, 40, 30, 19, 26]
            }
          ],
				},
				options: barOptions
		});
	});
});




/*
*
*	Gauge (cf-gauge)
*
*/
$(document).ready(function(){
	//Initialise gauges to default 
	$('.cf-gauge').each(function(){

		// Gather IDs 
		var gId = $(this).prop('id');					// Gauge container id e.g. cf-gauge-1
		var gcId = $('canvas', $(this)).prop('id');		// Gauge canvas id e.g. cf-gauge-1-g
		var gmId = $('.metric', $(this)).prop('id');  	// Gauge metric id e.g. cf-gauge-1-m

		//Create a canvas
		var ratio = 2.1;
		var width = $('.canvas',$(this)).width();
		var height = Math.round(width/ratio);
		$('canvas', $(this)).prop('width', width).prop('height', height);

		// Set options  	
		rGopts = {};
		rGopts.lineWidth = 0.30;
		rGopts.strokeColor = gaugeTrackColor;
		rGopts.limitMax = true;
		rGopts.colorStart = gaugeBarColor;
		rGopts.percentColors = void 0;	
		rGopts.pointer = {
			length: 0.7,
			strokeWidth: 0.035,
			color: gaugePointerColor
		};

		// Create gauge
		cf_rGs[gId] = new Gauge(document.getElementById(gcId)).setOptions(rGopts);
		cf_rGs[gId].setTextField(document.getElementById(gmId));

		// Set up values for gauge (in reality it'll likely be done one by one calling the function, not from here)
		updateOpts = {'minVal':'0','maxVal':'1000','newVal':'500'};
		gaugeUpdate(gId, updateOpts);


		// Responsiveness	
		$(window).resize(function(){
		
			//Get canvas measurements
			var ratio = 2.1;
			var width = $('.canvas', $('#'+gId)).width();
			var height = Math.round(width/ratio);

			cf_rGs[gId].ctx.clearRect(0, 0, width, height);
			$('canvas', $('#'+gId)).width(width).height(height);
			cf_rGs[gId].render();
		});

	});
});

/*
*	Set or update a Gauge
*	@param gauge 	string 		ID of gauge container
*	@param opts 	object		JSON object of options
*/
function gaugeUpdate(gauge, opts){
	if(opts.minVal){
		$('.val-min .metric-small', $('#'+gauge)).html(opts.minVal);		
		cf_rGs[gauge].minValue = opts.minVal;
	}
	if(opts.maxVal){
		cf_rGs[gauge].maxValue = opts.maxVal;
		$('.val-max .metric-small', $('#'+gauge)).html(opts.maxVal);
	}
	if(opts.newVal){
		cf_rGs[gauge].set(parseInt(opts.newVal));
	}
}






/*
*
*	Zoned Gauge (cf-zoned-gauge)
*
*/
$(document).ready(function(){
	//Initialise gauges to default 
	$('.cf-zoned-gauge').each(function(){

		// Gather IDs 
		var gId = $(this).prop('id');					// Gauge container id e.g. cf-zoned-gauge-1
		var gcId = $('canvas', $(this)).prop('id');		// Gauge canvas id e.g. cf-zoned-gauge-1-g
		var gmId = $('.metric', $(this)).prop('id');  	// Gauge metric id e.g. cf-zoned-gauge-1-m

		//Create a canvas
		var ratio = 2.1;
		var width = $('.canvas',$(this)).width();
		var height = Math.round(width/ratio);
		$('canvas', $(this)).prop('width', width).prop('height', height);

		// Set options  	
		rZGopts = {};
		rZGopts.lineWidth = 0.30;
		rZGopts.strokeColor = gaugeTrackColor;
		rZGopts.limitMax = true;
		rZGopts.colorStart = gaugeBarColor;
		rZGopts.percentColors = void 0;	
		rZGopts.pointer = {
			length: 0.7,
			strokeWidth: 0.035,
			color: gaugePointerColor
		};
		rZGopts.gradientZoneDirection = 'left';
		rZGopts.zoneColors = [
			"#66ce39", 
			"#e89640",
			"#f23c25"
		];
		rZGopts.zoneValues = [
			{min: 0, max: 333},
			{min: 333, max: 666},
			{min: 666, max: 1000},
		];
		let zones = [];
		let colors = rZGopts.zoneColors;
		if(rZGopts.gradientZoneDirection === 'left'){
			zones = colors.map((color, i) => Object.assign({}, rZGopts.zoneValues[i], { strokeStyle: color }))
		}
		if(rZGopts.gradientZoneDirection === 'right'){
			colors = colors.reverse();
			zones = colors.map((color, i) => Object.assign({}, rZGopts.zoneValues[i], { strokeStyle: color }))
		}
		rZGopts.staticZones = zones;
		

		// Create gauge
		cf_rZGs[gId] = new Gauge(document.getElementById(gcId)).setOptions(rZGopts);
		cf_rZGs[gId].setTextField(document.getElementById(gmId));

		// Set up values for gauge (in reality it'll likely be done one by one calling the function, not from here)
		updateOpts = {'minVal':'0','maxVal':'1000','newVal':'500'};
		zonedGaugeUpdate(gId, updateOpts);


		// Responsiveness	
		$(window).resize(function(){
		
			//Get canvas measurements
			var ratio = 2.1;
			var width = $('.canvas', $('#'+gId)).width();
			var height = Math.round(width/ratio);

			cf_rZGs[gId].ctx.clearRect(0, 0, width, height);
			$('canvas', $('#'+gId)).width(width).height(height);
			cf_rZGs[gId].render();
		});

	});
});

/*
*	Set or update a Zoned Gauge
*	@param gauge 	string 		ID of zoned gauge container
*	@param opts 	object		JSON object of options
*/
function zonedGaugeUpdate(gauge, opts){
	if(opts.minVal){
		$('.val-min .metric-small', $('#'+gauge)).html(opts.minVal);		
		cf_rZGs[gauge].minValue = opts.minVal;
	}
	if(opts.maxVal){
		cf_rZGs[gauge].maxValue = opts.maxVal;
		$('.val-max .metric-small', $('#'+gauge)).html(opts.maxVal);
	}
	if(opts.newVal){
		cf_rZGs[gauge].set(parseInt(opts.newVal));
	}
}




/*
*
* R.A.G
*
*/
$(document).ready(function(){
	/*
	*	Copy the each() function for each R.A.G chart you have
	* 	e.g. $('#cf-rag-1').each(function(){.....}
	*/								
	$('.cf-rag').each(function(){
		// Dummy data for RAG
		ragData = [40,50,10];
		ragLabels = ['Red','Amber','Green'];
		ragOpts = {postfix:'%'}

		cf_rRags[$(this).prop('id')] = new RagChart($(this).prop('id'), ragData, ragLabels, ragOpts);
	});
}); // end doc ready




/*
*
* Funnel charts
*
*/
$(document).ready(function(){
	/*
	*	Copy the each() function for each Funnel chart you have
	* 	e.g. $('#cf-funnel-1').each(function(){.....}
	*/								

	$('.cf-funnel').each(function(){
	
		// Dummy data for Funnel chart
		funData = [3000,1500,500,250,10];
		funLabels = ['Visits','Cart','Checkout','Purchase','Refund'];
		funOptions = {barOpacity:true};
		
		cf_rFunnels[$(this).prop('id')] = new FunnelChart($(this).prop('id'), funData, funLabels, funOptions);
	});
	
}); // end doc ready





/*
*
* Single Value Pie Charts (cf-svp)
*
*/
$(document).ready(function(){

	// Initialise single value pie charts
	$('.cf-svp').each(function(){
		cf_rSVPs[$(this).prop('id')] = {};
		rSVP($(this));
	});
	
	// Update a single value pie chart
	// -- Example of how to update a chart, can be used in other cases than from a button click
	$('.svp-update').click( function(){
		var element = $(this).data('update');
		
		// Call EasyPieChart update function
		cf_rSVPs[element].chart.update(12);
		// Update the data-percent so it redraws on resize properly
		$('#svp-1 .chart').data('percent', 12);
		// Update the UI metric
		$('.metric', $('#'+element)).html('12');
	});
});





/*
*	Create single value pie charts
*/
function rSVP(element, options){
	// Call the chart generation on window resize
	$(window).resize(generateChart);
	
	var container = $(element);
	var chart = '#'+$(element).attr('id')+' .chart';

	// Create the chart
	function generateChart(){
		
		// Remove any existing canvas                
		if($('canvas', $(container)).length){
			$.when($('canvas', $(container)).remove()).then(addChart());
		}
		else{
			addChart();
		}
		
		function addChart(){
			
			var minOfWidthAndHeight = Math.min(container[0].offsetHeight, container[0].offsetWidth);
			var calcLineWidth = minOfWidthAndHeight < 200 ? 10 : 25;
			
			//Setup options
			var rsvpOpt = {
				barColor: pieBar,
				trackColor: pieTrack,
				scaleColor: false,
				lineWidth: calcLineWidth,			
				lineCap: 'butt',
				size: Math.min(container[0].offsetHeight, container[0].offsetWidth)-30
			};
			
			// Create and store the chart
			cf_rSVPs[$(element).attr('id')].chart = new EasyPieChart(document.querySelector(chart), rsvpOpt);
		}
	};

	// Run once on first load
	generateChart();
}





/*
*	Shorten large numbers
*/
function prettyNumber (number) {
    var prettyNumberSuffixes = ["", "K", "M", "bn", "tr"];
	var addCommas = function (nStr){
		var x = '';
		var rgx = /(\d+)(\d{3})/;
		while (rgx.test(x)) {
			x = x.replace(rgx, '$1' + ',' + '$2');
		}
		return x;
	}
	var prettyNumber_rec = function (number, i) {
		if (i == prettyNumberSuffixes.length) {
			return addCommas(Math.round(number*1000)) + prettyNumberSuffixes[i-1];
		}
		if (number / 1000 >= 1) { // 1000+
			return prettyNumber_rec(number / 1000, ++i);
		}
		else {
			var decimals = number - Math.floor(number);
			if (decimals != 0) {
				if (number >= 10) { // 10 - 100
					number = Math.floor(number) + Math.round(decimals*10) / 10 + '';
					number = number.replace(/(.*\..).*$/, '$1');
				}
				else { // 0 - 10
					number = Math.floor(number) + Math.round(decimals*100) / 100 + '';
					number = number.replace(/(.*\...).*$/, '$1');
				}
				return number + prettyNumberSuffixes[i];
			}
			else {
				return Math.floor(number) + prettyNumberSuffixes[i];
			}
		}
	}
	return prettyNumber_rec(number, 0);
}