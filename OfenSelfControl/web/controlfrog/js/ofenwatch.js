//Temperature Values
		var tempDach = -1000;  //Is the same as inside temp in backing room
		var tempFront = -1000;
		var tempLeft = -1000;
		var tempRight = -1000;
		var tempLowerLeft = -1000;
		var tempLowerRight = -1000;
		var tempSteamOutput = -1000;
		
		var tempBack = -1000;
		var tempLowerFront = -1000;
		var tempStone = -1000;
		
		var tempLowerFrontInside = -1000;
		var tempSteamInside = -1000;
		var tempSteamCooler = -1000;
		
		//var windowWidth = 350;
		//var windowHeight = 300;
				
		var error = [0,0,0,0,0,0,0,0,0,0];
		
		
		
		function main() {
			
			//----------ZEUG---------
			
			console.log("main called");
		
			var slider = document.getElementById("myRange");
			var output = document.getElementById("demo");
			var sliderDach = document.getElementById("dachRange");
			var outputDach = document.getElementById("dachDemo");
			
			//var canvas = document.getElementById('theCanvas');
			//if (canvas.getContext){
				//var windowWidth = canvas.width;
				//var windowHeight = canvas.height;
				//zeichne(0);
			//}
			
			output.innerHTML = slider.value;
			slider.oninput = function() {
				output.innerHTML = this.value;
				tempFront = this.value;
				tempBack = this.value;
				//zeichne(this.value);
				updateTest();
			}
			
			outputDach.innerHTML = sliderDach.value;
			sliderDach.oninput = function() {
				outputDach.innerHTML = this.value;
				tempDach = this.value;
				//zeichne(this.value);
				updateTest();
			}
			//update(null);
		
			zeichne(0);
			//-----------------------
			
		}
		
		function update(obj) {
			//if (obj != null) {
				tempDach = checkForErrors(obj.temp1,1);
				tempFront = checkForErrors(obj.temp2,2);
				tempLeft = checkForErrors(obj.temp3,3);
				tempRight = checkForErrors(obj.temp4,4);
				tempLowerLeft = checkForErrors(obj.temp5,5);
				tempLowerRight = checkForErrors(obj.temp6,6);
				tempSteamOutput = checkForErrors(obj.temp7,7);
				
				tempBack = checkForErrors(obj.temp8,8);
				tempLowerFront = checkForErrors(obj.temp9,9);
				tempStone = checkForErrors(obj.temp10,10);
				
				tempLowerFrontInside = checkForErrors(obj.temp6,6);
				tempSteamInside = checkForErrors(obj.temp7,7);
				tempSteamCooler = checkForErrors(obj.temp8,8);
				
	
				
				var drosselklappe = obj.drosselklappe * 100 + "%";
				var fastheatup = "---";
				if (obj.fastHeatupActive == 1) {
					fastheatup = "AN";
				} else {
					fastheatup = "AUS";
				}
				var air = obj.airInput * 100 + "%";
				var automode = "---";
				if (obj.automode == 1) {
					automode = "AN";
				} else {
					automode = "AUS";
				}
				var temp2hold = obj.temp2hold + "°C";
				var fan = obj.fan * 100 + "%";
				var errors = "NULL";
				
			//}
			
			updateCurrentSettingValues(drosselklappe, air, automode, fastheatup, temp2hold, fan, errors);
			
			//Draw ofen thermogram
			zeichne(0);
			
			//Update gauges and charts
			
			//Dach (Backraum)
			var opts5 = JSON.parse('{"maxVal":"' + calcMaxVal(tempDach) + '", "newVal":' + tempDach + '}'); 
			zonedGaugeUpdate("cf-zoned-gauge-5", opts5);
			
			//Abgas innen
			var opts4 = JSON.parse('{"maxVal":"' + calcMaxVal(tempSteamInside) + '", "newVal":' + tempSteamInside + '}'); 
			zonedGaugeUpdate("cf-zoned-gauge-4", opts4);
			
			//Stein
			var opts2 = JSON.parse('{"maxVal":"' + calcMaxVal(tempStone) + '", "newVal":' + tempStone + '}'); 
			zonedGaugeUpdate("cf-zoned-gauge-2", opts2);
			
			//Kamin
			var opts1 = JSON.parse('{"maxVal":"' + calcMaxVal(tempSteamOutput) + '", "newVal":' + tempSteamOutput + '}'); 
			zonedGaugeUpdate("cf-zoned-gauge-1", opts1);
			
			
			console.log("update finished");
			
		}
		
		function updateCurrentSettingValues(drosselklappe, air, automode, fastheatup, temp2hold, fan, errors) {
			var drosselklappeVar = document.getElementById("drosselklappe");
			var airVar = document.getElementById("lufteinlass");
			var automodeVar = document.getElementById("automode");
			var fastheatupVar = document.getElementById("fastheatup");
			var temp2holdVar = document.getElementById("temp2hold");
			var fanVar = document.getElementById("fan");
			
			drosselklappeVar.innerHTML = drosselklappe;
			airVar.innerHTML = air;
			automodeVar.innerHTML = automode;
			fastheatupVar.innerHTML = fastheatup;
			temp2holdVar.innerHTML = temp2hold;
			fanVar.innerHTML = fan;
			
			
		}
		
		
		function updateChartofenwatch(dataset) {
			console.log("updateChart");
			var data = [];
			var labels = [];
			for (var i = 0; i < dataset.length; i++) {
				if (dataset[i].temp1 > -50) {
					data.push(dataset[i].temp1);
					labels.push(dataset[i].timestamp);
				} else {
					data.push("0");
					labels.push(dataset[i].timestamp);
				}
				
			}
			//console.log(data);
			//console.log(labels);
			
			var labelsNew = labels.map(x => x.substring(11, 17));
			updateDataset("cf-line-1",labelsNew, data);
			
		}
		
		function updateTest() {
			//Draw ofen thermogram
			zeichne(0);
			
			//Update gauges and charts
			
			
			//Dach (Backraum)
			var opts5 = JSON.parse('{"maxVal":"' + calcMaxVal(tempDach) + '", "newVal":' + tempDach + '}'); 
			zonedGaugeUpdate("cf-zoned-gauge-5", opts5);
			
			//Abgas innen
			var opts4 = JSON.parse('{"maxVal":"' + calcMaxVal(tempSteamInside) + '", "newVal":' + tempSteamInside + '}'); 
			zonedGaugeUpdate("cf-zoned-gauge-4", opts4);
			
			//Stein
			var opts2 = JSON.parse('{"maxVal":"' + calcMaxVal(tempStone) + '", "newVal":' + tempStone + '}'); 
			zonedGaugeUpdate("cf-zoned-gauge-2", opts2);
			
			//Kamin
			var opts1 = JSON.parse('{"maxVal":"' + calcMaxVal(tempSteamOutput) + '", "newVal":' + tempSteamOutput + '}'); 
			zonedGaugeUpdate("cf-zoned-gauge-1", opts1);
			
			
			console.log("updateTest finished");
		}
		
		function calcMaxVal(temp) {
			newMaxVal = 500;
			if (temp > 500) {
				newMaxVal = 1000;
				if (temp > 1000) {
					newMaxVal = 1200
					if (temp > 1200) {
						newMaxVal = 1400
						if (temp > 1400) {
							newMaxVal = 2000
						}
					}
				}
			} 
			
			return newMaxVal;
		}
		
		function checkForErrors(temp, id) {
			console.log("checkErrors id:" + id)
			if (temp < -100) {
				error[id-1] = 1;
				return 0;
			} else {
				error[id-1] = 0;
				return temp;
			}
			
			return 0;
		}
		
		
		
		//function zeichne(tempDach,tempFront, tempBack, tempLowerLeft, tempLowerFront, tempLowerFrontInside, tempSteamInside, tempSteamCooler, tempSteamOutput, tempStone){
		function zeichne(temp){
			
			
			var canvas = document.getElementById('theCanvas');
			if (canvas.getContext){
				var bild = canvas.getContext('2d');
				
				//bild.clearRect(0, 0, 1000, 1000);
				
				//var windowWidth = canvas.width;//window.innerWidth;//canvas.width = window.innerWidth;
				//var windowHeight = canvas.height;//window.innerHeight;//canvas.height = window.innerHeight;
				
				var windowWidth = canvas.width = window.innerWidth;
				var windowHeight = canvas.height = window.innerHeight;
				
				
				var isMobileDevice = 0;
				if (windowWidth < windowHeight) {
					isMobileDevice = 1;
					windowHeight = canvas.height = window.innerWidth;
				}
				
				var scale = 0.7;
				var width =  1850 * scale;
				var height =  1080 * scale;
				
				console.log("Hallo");
				
				//Calculate canvas scale
				var canvasScale = (windowWidth / width);
				var canvasScaleH = (windowHeight / height);
				
				if (isMobileDevice == 0) {
					canvasScale = canvasScale * 1.0;
				} else {
					canvasScale = canvasScale * 1;
					canvasScaleH = 0.5;
				}
				
				var blurval = 0;
				
				var background = new Image();
				background.src = "../../img/Ofen/OfenPic3.png";
				// Make sure the image is loaded first otherwise nothing will draw.
				background.onload = function() {
					bild.fillStyle = "rgba(0,0,0,1)";
					bild.fillRect(0,0,width,height);
					bild.drawImage(background,0,0,width,height);   
					//makeText(bild,width,height);
					
					//---------Draw Ofen Thermogram--------
				
					//Front
					//var colorFront = "rgb(250,90,200)";
					//var colorFront = "rgba(0,90,200,0.5)";
					var colorFront = colorCode(tempFront);
					bild.fillStyle = colorFront;
					//bild.globalAlpha=0.2;
					bild.shadowBlur = blurval;
					bild.shadowColor = colorFront;
					bild.beginPath();
					bild.moveTo( 725, 530);
					bild.lineTo( 1080, 445);
					bild.lineTo( 1080, 335);
					bild.lineTo( 1050, 230);
					bild.lineTo( 995, 175);
					bild.lineTo( 835, 200);
					bild.lineTo( 768, 275);
					bild.lineTo( 725, 400);
					bild.fill();
					
					
					//Back
					//var colorBack = "rgb(0,90,200)";
					var colorBack = colorCode(tempBack);
					bild.fillStyle = colorBack;
					//bild.globalAlpha=0.2;
					bild.shadowBlur = blurval;
					bild.shadowColor = colorBack;
					bild.beginPath();
					bild.moveTo( 225, 450);
					bild.lineTo( 260, 445);
					bild.lineTo( 260, 430);
					bild.lineTo( 300, 440);
					bild.lineTo( 315, 435);
					bild.lineTo( 315, 417);
					
					bild.lineTo( 605, 365);
					bild.lineTo( 605, 285);
					bild.lineTo( 570, 185);
					bild.lineTo( 510, 135);
					bild.lineTo( 336, 157);
					bild.lineTo( 268, 225);
					bild.lineTo( 225, 340);
					bild.fill();
					
					
					//Stone
					var colorStone = colorCode(tempStone);
					bild.fillStyle = colorStone;
					//bild.globalAlpha=0.2;
					bild.shadowBlur = blurval;
					bild.shadowColor = colorStone;
					bild.beginPath();
					bild.moveTo( 310, 439);
					bild.lineTo( 720, 498);
					bild.lineTo( 722, 400);
					bild.lineTo( 729, 382);
					bild.lineTo( 655, 373);
					bild.fill();
					
					bild.beginPath();
					bild.moveTo( 785, 490);
					bild.lineTo( 1027, 430);
					bild.lineTo( 1027, 420);
					bild.lineTo( 785, 390);
					bild.fill();
					
					
					//Lower Left Side
					var colorLLSide = colorCode(tempLowerLeft);
					bild.fillStyle = colorLLSide;
					//bild.globalAlpha=0.2;
					bild.shadowBlur = blurval;
					bild.shadowColor = colorLLSide;
					bild.beginPath();
					bild.moveTo( 222, 460);
					bild.lineTo( 222, 622);
					bild.lineTo( 722, 714);
					bild.lineTo( 722, 535);
					bild.fill();
					
					
					//Lower Inside
					/*var colorLInside = colorCode(tempLowerFrontInside);
					bild.fillStyle = colorLInside;
					//bild.globalAlpha=0.2;
					bild.shadowBlur = blurval;
					bild.shadowColor = colorLInside;
					bild.beginPath();
					bild.moveTo( 784, 543);
					bild.lineTo( 782, 668);
					bild.lineTo( 887, 637);
					bild.lineTo( 890, 515);
					bild.fill();
					
					bild.beginPath();
					bild.moveTo( 931, 506);
					bild.lineTo( 927, 624);
					bild.lineTo( 1022, 595);
					bild.lineTo( 1025, 481);
					bild.fill();*/
					
					
					//Lower Front
					var colorLFront = colorCode(tempLowerFront);
					bild.fillStyle = colorLFront;
					//bild.globalAlpha=0.2;
					bild.shadowBlur = blurval;
					bild.shadowColor = colorLFront;
					bild.beginPath();
					bild.moveTo( 724, 533);
					bild.lineTo( 724, 713);
					bild.lineTo( 1080, 605);
					bild.lineTo( 1082, 447);
					bild.fill();
					
					
					//Chimney
					var colorChimney= colorCode(tempSteamOutput);
					bild.fillStyle = colorChimney;
					//bild.globalAlpha=0.2;
					bild.shadowBlur = blurval;
					bild.shadowColor = colorChimney;
					bild.beginPath();
					bild.moveTo( 775, 15);
					
					bild.lineTo( 772, 160);
					bild.lineTo( 772, 169);
					bild.lineTo( 768, 176);
					bild.lineTo( 780, 182);
					bild.lineTo( 830, 185);
					bild.lineTo( 850, 180);
					bild.lineTo( 848, 177);
					bild.lineTo( 850, 16);
					
					
					bild.fill();
					
					
					
					//Dach
					var colorDach= colorCode(tempDach);
					bild.fillStyle = colorDach;
					bild.globalAlpha=0.5;
					bild.shadowBlur = blurval;
					bild.shadowColor = colorDach;
					bild.beginPath();
					bild.moveTo( 225, 455);
					bild.lineTo( 225, 337);
					bild.lineTo( 265, 225);
					bild.lineTo( 335, 158);
					bild.lineTo( 512, 137);
					
					bild.lineTo( 769, 160);
					bild.lineTo( 767, 169);
					bild.lineTo( 768, 176);
					bild.lineTo( 780, 182);
					bild.lineTo( 830, 185);
					bild.lineTo( 850, 180);
					bild.lineTo( 855, 177);
					bild.lineTo( 850, 165);
					
					bild.lineTo( 996, 176);
					bild.lineTo( 830, 200);
					bild.lineTo( 762, 280);
										
					bild.lineTo( 722, 400);
					bild.lineTo( 720, 532);
					bild.fill();
					

					//Text and lines
					bild.font = "30px Comic Sans MS";
					bild.globalAlpha = 1;
					bild.shadowBlur = 0;
					bild.fillStyle = "white";
					bild.textAlign = "center";
					bild.strokeStyle = "grey";
					
					//Links
					bild.fillText(tempLeft + "°C", 150, 210); 
					bild.strokeStyle = "lightgrey";
					bild.beginPath();
					bild.moveTo( 108, 220);
					bild.lineTo( 190, 220);
					bild.lineTo( 330, 300);
					bild.lineWidth = 3;
					bild.stroke();
					
					//Dach
					bild.fillText(tempDach + "°C", 430, 60); 
					bild.strokeStyle = "lightgrey";
					bild.beginPath();
					bild.moveTo( 388, 70);
					bild.lineTo( 470, 70);
					bild.lineTo( 600, 160);
					bild.lineWidth = 3;
					bild.stroke();
					
					//Seite unten links
					bild.fillText(tempLowerLeft + "°C", 160, 690); 
					bild.strokeStyle = "lightgrey";
					bild.beginPath();
					bild.moveTo( 118, 700);
					bild.lineTo( 200, 700);
					bild.lineTo( 430, 610);
					bild.lineWidth = 3;
					bild.stroke();
					
					//Vorderwand
					bild.fillText(tempFront + "°C", 1145, 180);
					bild.beginPath();
					bild.moveTo( 1190, 190);
					bild.lineTo( 1070, 190);
					bild.lineTo( 980, 230);
					bild.lineWidth = 3;
					bild.stroke();
					
					//Kamin
					bild.fillText(tempSteamOutput + "°C", 950, 70);
					bild.beginPath();
					bild.moveTo( 990, 80);
					bild.lineTo( 900, 80);
					bild.lineTo( 850, 100);
					bild.lineWidth = 3;
					bild.stroke();
					
					//Vorderwand unten
					/*bild.fillText(tempLowerFront + "°C", 1145, 670);
					bild.beginPath();
					bild.moveTo( 1190, 680);
					bild.lineTo( 1070, 680);
					bild.lineTo( 910, 590);
					bild.lineWidth = 3;
					bild.stroke();*/
					
					//Rechts oben
					bild.fillText(tempRight + "°C", 1200, 410);
					bild.beginPath();
					bild.moveTo( 1250, 420);
					bild.lineTo( 1120, 420);
					bild.lineTo( 930, 360);
					bild.lineWidth = 3;
					bild.stroke();
					
					//Rechts unten
					bild.fillText(tempLowerRight + "°C", 1145, 670);
					bild.beginPath();
					bild.moveTo( 1190, 680);
					bild.lineTo( 1070, 680);
					bild.lineTo( 950, 520);
					bild.lineWidth = 3;
					bild.stroke();
					
					//-------Draw Ofen Thermogram END------
					
				}
				


			/*	bild.fillStyle = "rgb(200,0,0)";
				bild.fillRect (10, 10, 60, 50);

				bild.strokeStyle= "rgb(0,200,0)";
				bild.beginPath();
				bild.moveTo( 100, 50);
				bild.lineTo( 200, 0);
				bild.lineTo( 150, 200);
				bild.lineTo( 100, 50);
				bild.stroke();

				bild.fillStyle = "rgb(0,0,200)";
				bild.beginPath();
				bild.moveTo( 50, 100);
				bild.lineTo( 100, 50);
				bild.lineTo( 100, 150);
				bild.fill();

				bild.strokeStyle= "rgb(0,0,0)";
				bild.beginPath();
				bild.arc(75,210,50,0,Math.PI*2,true); // Outer circle
				bild.moveTo(110,210);
				bild.arc(75,210,35,0,Math.PI,false);   // Mouth (clockwise)
				bild.moveTo(65,200);
				bild.arc(60,200,5,0,Math.PI*2,true);  // Left eye
				bild.moveTo(95,200);
				bild.arc(90,200,5,0,Math.PI*2,true);  // Right eye
				bild.stroke();*/
				
				
				
				
				
				// Rescale canvas content(=bild) and center in canvas
				bild.scale(canvasScale, canvasScaleH);
				
				//var left = (windowWidth - (width * canvasScale*0)) / 2;
				var left = ((windowWidth*(1/canvasScale)) - (width))/2;
				var top  = (windowHeight - (height * canvasScale)) / 2;
				//bild.translate(left,top);
				
				
				//(windowWidth - width * ((windowWidth / width) * 0.6) ) / 2
				//(windowWidth - windowWidth * 0.6) / 2
				
				//a * b/a * c = bac/a  = bc
				
			}
		}
		
		function makeText(bild, width, height) {
			
			console.log("makeText");
			
			bild.font = "30px Comic Sans MS";
			bild.fillStyle = "red";
			bild.textAlign = "center";
			bild.fillText("Hello World", width/2, height/2); 
						
		}
		
		function colorCode(temp) {
			//var color = "rgba(0,0,250,0.5)";
			var colorHSL = "hsl(260, 100%, 50%)";
			var HValue = 260;
			
			if (temp > 40) {
				HValue = 260 - temp/1.5;
				if (HValue < 0) {
					HValue = 0;
				}
			}
			
			return colorHSL = "hsla(" + HValue + ", 100%, 50%, 0.5)";
			
		}