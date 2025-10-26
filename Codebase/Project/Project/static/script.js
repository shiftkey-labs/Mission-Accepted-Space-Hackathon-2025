var coordinates = [];
var markersList = [];



var data = [
  {
    name: "Iqaluit, NU",
    coordinates: [-68.5197, 63.7467],
    groundTemp: 267.787,
    isPermaFrost: false,
    population: 7429,
    iceChange: -16.70370370370371,
    slope: 0.28632187843322754,
    ndviChange: -0.02043234233701987,
    ndwiChange: -0.0287051720505746,
    iceChangeIndex: 5.0,
    slopeIndex: 1.7974931627902522,
    ndviChangeIndex: 3.1925426217051784,
    ndwiChangeIndex: 1.6067131581465683,
    groundTempIndex: 1.851094470046071,
    riskdex: 2.455511998224778
  },
  {
    name: "Belcher Islands, NU",
    coordinates: [-79.0, 56.0],
    groundTemp: 275.668,
    isPermaFrost: false,
    population: 1010,
    iceChange: 30.220394736842106,
    slope: 0.009224984828120635,
    ndviChange: 0.17409829977106994,
    ndwiChange: -0.03274363935719028,
    iceChangeIndex: 0.3476771642577505,
    slopeIndex: 0.05791330807875258,
    ndviChangeIndex: 0.48036015323098,
    ndwiChangeIndex: 1.500024941077089,
    groundTempIndex: 4.120967741935479,
    riskdex: 1.7441891516850383
  },
  {
    name: "Sanikiluaq, NU",
    coordinates: [-79.2333, 56.5333],
    groundTemp: 274.69,
    isPermaFrost: false,
    population: 1010,
    iceChange: 32.125,
    slope: 0,
    ndviChange: 0.20855201744580018,
    ndwiChange: -0.004447306941692125,
    iceChangeIndex: 0.15884373211219138,
    slopeIndex: 0.0,
    ndviChangeIndex: 0.0,
    ndwiChangeIndex: 2.2475573650908665,
    groundTempIndex: 3.839285714285707,
    riskdex: 1.7375016153752574
  },
  {
    name: "Grise Fiord, NU",
    coordinates: [-82.3, 76.4],
    groundTemp: 265.06,
    isPermaFrost: true,
    population: 144,
    iceChange: 0,
    slope: 0.2789935767650604,
    ndviChange: 0,
    ndwiChange: 0.015612942568174956,
    iceChangeIndex: 3.3438995150716586,
    slopeIndex: 1.7514869958306192,
    ndviChangeIndex: 2.907671096706373,
    ndwiChangeIndex: 2.777508975859295,
    groundTempIndex: 1.0656682027649729,
    riskdex: 2.2145363459356133
  },
  {
    name: "Southampton Island, NU",
    coordinates: [-85.0, 63.0],
    groundTemp: 266.24,
    isPermaFrost: true,
    population: 1035,
    iceChange: 29.588235294117645,
    slope: 0,
    ndviChange: -0.008174020530276695,
    ndwiChange: -0.08952405850790934,
    iceChangeIndex: 0.41035305807259803,
    slopeIndex: 0.0,
    ndviChangeIndex: 3.0216348143958784,
    ndwiChangeIndex: 0.0,
    groundTempIndex: 1.4055299539170483,
    riskdex: 0.9364571670453858
  },
  {
    name: "Coats Island, NU",
    coordinates: [-86.0, 64.0],
    groundTemp: 267.79,
    isPermaFrost: false,
    population: 0,
    iceChange: 9.648148148148152,
    slope: 0.09379480328949531,
    ndviChange: -0.028500035790811354,
    ndwiChange: -0.08051054471324443,
    iceChangeIndex: 2.387327062025466,
    slopeIndex: 0.5888321162905553,
    ndviChangeIndex: 3.3050239074773153,
    ndwiChangeIndex: 0.23811898011620344,
    groundTempIndex: 1.8519585253456226,
    riskdex: 1.5572947655017382
  },
  {
    name: "Rankin Inlet, NU",
    coordinates: [-92.0831, 62.8083],
    groundTemp: 276.45,
    isPermaFrost: false,
    population: 2975,
    iceChange: 4.028985507246382,
    slope: 0.02334270253777504,
    ndviChange: -0.053853155436627526,
    ndwiChange: -0.01186165270848212,
    iceChangeIndex: 2.944442905287535,
    slopeIndex: 0.14654258501758996,
    ndviChangeIndex: 3.6585018268392635,
    ndwiChangeIndex: 2.051685201089529,
    groundTempIndex: 4.346198156682017,
    riskdex: 2.8292038448486454
  },
  {
    name: "Arviat, NU",
    coordinates: [-94.0586, 61.1083],
    groundTemp: 277.4,
    isPermaFrost: false,
    population: 2061,
    iceChange: -11.122807017543863,
    slope: 0.059699688106775284,
    ndviChange: -0.05049738744714019,
    ndwiChange: 0.011718983304550665,
    iceChangeIndex: 4.446678061810031,
    slopeIndex: 0.37478722122055563,
    ndviChangeIndex: 3.6117150840890018,
    ndwiChangeIndex: 2.6746383718316973,
    groundTempIndex: 4.619815668202751,
    riskdex: 3.319581348486688
  },
  {
    name: "Baker Lake, NU",
    coordinates: [-96.0208, 64.3167],
    groundTemp: 266.4,
    isPermaFrost: false,
    population: 2060,
    iceChange: 20.307692307692307,
    slope: 0.03652359839542629,
    ndviChange: -0.01568144621974052,
    ndwiChange: -0.03401851915115728,
    iceChangeIndex: 1.3304790380856084,
    slopeIndex: 0.2292906108171754,
    ndviChangeIndex: 3.1263047425762567,
    ndwiChangeIndex: 1.466345170542998,
    groundTempIndex: 1.451612903225795,
    riskdex: 1.5049813223253439
  },
  {
    name: "Bathurst Inlet, NU",
    coordinates: [-108.03, 66.84],
    groundTemp: 266.28,
    isPermaFrost: true,
    population: 0,
    iceChange: 0,
    slope: 0.18842238356498633,
    ndviChange: 0,
    ndwiChange: 0.0031588557113318635,
    iceChangeIndex: 3.3438995150716586,
    slopeIndex: 1.1828923029844187,
    ndviChangeIndex: 2.907671096706373,
    ndwiChangeIndex: 2.448496947011522,
    groundTempIndex: 1.417050691244227,
    riskdex: 2.1524088813405164
  },
  {
    name: "Kugluktuk, NU",
    coordinates: [-115.09, 67.825],
    groundTemp: 265.03,
    isPermaFrost: true,
    population: 1382,
    iceChange: 0,
    slope: 0.12311131317633346,
    ndviChange: 0,
    ndwiChange: 0.0350748360336037,
    iceChangeIndex: 3.3438995150716586,
    slopeIndex: 0.7728775212970524,
    ndviChangeIndex: 2.907671096706373,
    ndwiChangeIndex: 3.29165321845879,
    groundTempIndex: 1.0570276497695728,
    riskdex: 2.193688819506832
  },
  {
    name: "Paulatuk, NW",
    coordinates: [-124.07, 69.35],
    groundTemp: 273.21,
    isPermaFrost: false,
    population: 298,
    iceChange: 0,
    slope: 0.0793926939368248,
    ndviChange: 0,
    ndwiChange: 0.0997408583472332,
    iceChangeIndex: 3.3438995150716586,
    slopeIndex: 0.4984174639669467,
    ndviChangeIndex: 2.907671096706373,
    ndwiChangeIndex: 5.0,
    groundTempIndex: 3.413018433179711,
    riskdex: 3.28640374131566
  },
  {
    name: "Sachs Harbour, NW",
    coordinates: [-125.247, 71.985],
    groundTemp: 261.36,
    isPermaFrost: true,
    population: 104,
    iceChange: 0,
    slope: 0,
    ndviChange: 0,
    ndwiChange: 0.06781457363062171,
    iceChangeIndex: 3.3438995150716586,
    slopeIndex: 0.0,
    ndviChangeIndex: 2.907671096706373,
    ndwiChangeIndex: 4.15657150709429,
    groundTempIndex: 0.0,
    riskdex: 1.976878468540277
  },
  {
    name: "Atlin area, YT",
    coordinates: [-132.7333, 59.5667],
    groundTemp: 276.8,
    isPermaFrost: false,
    population: 547,
    iceChange: 24.024211423699917,
    slope: 0.10097496956586838,
    ndviChange: -0.0348944443275712,
    ndwiChange: 0.039432316208386275,
    iceChangeIndex: 0.9620021290453149,
    slopeIndex: 0.63390830767384,
    ndviChangeIndex: 3.3941759430729483,
    ndwiChangeIndex: 3.406769116512882,
    groundTempIndex: 4.447004608294927,
    riskdex: 2.934306618585514
  },
  {
    name: "Tagish, YT",
    coordinates: [-134.2533, 60.0875],
    groundTemp: 269.49,
    isPermaFrost: false,
    population: 249,
    iceChange: 27.537015276145713,
    slope: 0.22832240164279938,
    ndviChange: -0.07183536974993554,
    ndwiChange: 0.043799863861118685,
    iceChangeIndex: 0.6137227134924812,
    slopeIndex: 1.4333796568762454,
    ndviChangeIndex: 3.90921321028188,
    ndwiChangeIndex: 3.5221509771689483,
    groundTempIndex: 2.3415898617511486,
    riskdex: 2.476462039915172
  },
  {
    name: "Whitehorse, YT",
    coordinates: [-135.0568, 60.7212],
    groundTemp: 275.14,
    isPermaFrost: false,
    population: 30970,
    iceChange: 23.208333333333332,
    slope: 0.37468741284680335,
    ndviChange: -0.15007179265781645,
    ndwiChange: -0.007663581624417437,
    iceChangeIndex: 1.0428929377585296,
    slopeIndex: 2.3522410039397754,
    ndviChangeIndex: 5.0,
    ndwiChangeIndex: 2.162589830268051,
    groundTempIndex: 3.9688940092165788,
    riskdex: 2.990585751586732
  },
  {
    name: "Carcross, YT",
    coordinates: [-136.2569, 60.7169],
    groundTemp: 276.15,
    isPermaFrost: false,
    population: 317,
    iceChange: 4.569686411149831,
    slope: 0.2271263748407364,
    ndviChange: -0.11099808001794327,
    ndwiChange: -0.00962707210388103,
    iceChangeIndex: 2.8908347328103647,
    slopeIndex: 1.425871149279878,
    ndviChangeIndex: 4.45522701590026,
    ndwiChangeIndex: 2.1107183447310254,
    groundTempIndex: 4.259792626728097,
    riskdex: 3.121407308899761
  },
  {
    name: "Destruction Bay, YT",
    coordinates: [-136.5, 59.75],
    groundTemp: 272.41,
    isPermaFrost: false,
    population: 40,
    iceChange: -10.49898989898989,
    slope: 0.3218936324119568,
    ndviChange: -0.02211341120118724,
    ndwiChange: 0.012626028864338612,
    iceChangeIndex: 4.384829273608959,
    slopeIndex: 2.0208082126743427,
    ndviChangeIndex: 3.2159803971234036,
    ndwiChangeIndex: 2.6986006986817963,
    groundTempIndex: 3.1826036866359453,
    riskdex: 3.072673963172239
  },
  {
    name: "Haines border area, YT",
    coordinates: [-137.0103, 60.1722],
    groundTemp: 278.72,
    isPermaFrost: false,
    population: 688,
    iceChange: 5.725894588401189,
    slope: 0.2614071149667605,
    ndviChange: -0.04155130300759326,
    ndwiChange: -0.01394612600589562,
    iceChangeIndex: 2.776201657596063,
    slopeIndex: 1.6410813746706276,
    ndviChangeIndex: 3.486987107480837,
    ndwiChangeIndex: 1.9966175918344844,
    groundTempIndex: 5.0,
    riskdex: 3.1847949189207503
  },
  {
    name: "Kluane Lake, YT",
    coordinates: [-137.5833, 59.25],
    groundTemp: 274.12,
    isPermaFrost: false,
    population: 64,
    iceChange: -8.870001132887737,
    slope: 0.45220625400543213,
    ndviChange: -0.03244462496088378,
    ndwiChange: 0.007657915550804223,
    iceChangeIndex: 4.223322033457997,
    slopeIndex: 2.8388946530864434,
    ndviChangeIndex: 3.3600201048705216,
    ndwiChangeIndex: 2.5673530962183975,
    groundTempIndex: 3.675115207373266,
    riskdex: 3.307708354978823
  },
  {
    name: "Dalton Post, YT",
    coordinates: [-138.8, 59.5167],
    groundTemp: 273.01,
    isPermaFrost: false,
    population: 100,
    iceChange: 15.11315099288123,
    slope: 0.79644775390625,
    ndviChange: 0.009964352243146402,
    ndwiChange: 0.06335567703600531,
    iceChangeIndex: 1.845495500484391,
    slopeIndex: 5.0,
    ndviChangeIndex: 2.7687462405978587,
    ndwiChangeIndex: 4.038776390368322,
    groundTempIndex: 3.3554147465437696,
    riskdex: 3.4584547827175487
  },
  {
  name: "Burwash Landing, YT",
  coordinates: [-139.0394, 61.3714],
  groundTemp: 267.71,
  isPermaFrost: false,
  population: 64,
  iceChange: -13.459909031838848,
  slope: 0.23637180253406584,
  ndviChange: -0.09231735393550526,
  ndwiChange: -0.04889485126483106,
  iceChangeIndex: 4.678391689389688,
  slopeIndex: 1.4839127951253486,
  ndviChangeIndex: 4.194776851185309,
  ndwiChangeIndex: 1.0733422738397578,
  groundTempIndex: 1.8289170506912331,
  riskdex: 2.370572884022361
},
{
  name: "Haines Junction area, YT",
  coordinates: [-139.4333, 59.55],
  groundTemp: 273.93,
  isPermaFrost: false,
  population: 688,
  iceChange: 33.72712418300653,
  slope: 0,
  ndviChange: 0.05195489717296653,
  ndwiChange: -0.05880532167551589,
  iceChangeIndex: 0.0,
  slopeIndex: 0.0,
  ndviChangeIndex: 2.1833062370787415,
  ndwiChangeIndex: 0.8115274965593495,
  groundTempIndex: 3.6203917050691197,
  riskdex: 1.6164953212223843
}
];

function getCoordinates(){
    var coordinateList = []
    for (var i = 0; i < data.length; i++) {

        // Create [lat, lon] array
        var coords = [data[i]['coordinates'][1], data[i]['coordinates'][0]]; 
        var name = data[i]['name'];
        var groundTemp = data[i]['groundTemp'];
        var iceChange = data[i]['iceChange'];
        var slopeIndex = data[i]['slopeIndex'];
        var risk = data[i]['riskdex'];
        var pop = data[i]['population'];

        var radius;
        if (pop > 100) {
            radius = 50000;
        } else if (pop > 50) {
            radius = 25000;
        } else {
            radius = 10000;
        }

        // Push all values into coordinateList
        coordinateList.push([coords, name, groundTemp, iceChange, slopeIndex, risk, radius, pop]);
    }
    return coordinateList
}

window.onload = loadMetrics;

function loadMetrics() {
    sendToFlask();

}

async function sendToFlask() {


    coordinates = getCoordinates();

    if (coordinates != undefined) {
        coordinates.forEach(element => {
            var colour = 0;
            var opacity = 0;

            var coordinates = element[0];
            var city = element[1];
            var groundTemp = element[2].toFixed(1);
            var iceChange = element[3].toFixed(1)
            var slope = element[4].toFixed(1)
            var risk = element[5].toFixed(1)
            var radius = element[6].toFixed(1)
            var pop = element[7].toFixed(1)
            

            if(risk > 3){
                colour = "#e60404";
                    opacity = 0.8;
            }else if(risk > 2){
                 colour = "#eb3333";
                    opacity = 0.6;
            }else if(risk > 1){
                Colour = "#f06666";
                    opacity = 0.4;
            }else{
                color = '#facccc';
                    opacity = 0.2;
            }
            
            var circle = L.circle(coordinates, {
                color: 'red',
                fillColor: colour,
                fillOpacity: opacity,
                riseOnHover: true,
                radius: radius
            }).addTo(map);
            
            var marker = L.marker(coordinates, { riseOnHover: true, }).addTo(map);

           


            var slopeColour = 'green'
            var riskColour = 'red'

            

            var slopeString = ``;
            if(slope < 1){
                slopeString += `<div class = "groundTempBox"></div>`
            }
            for(var i = 1; i < slope + 1; i++){
                slopeString += `<div class = "groundTempBox" style="background-color: ${slopeColour}"></div>`
            }

            var riskString = ``;
            for(var i = 1; i < risk + 1; i++){
                riskString += `<div class = "groundTempBox" style="background-color: ${riskColour}"></div>`
            }

            circle.bindPopup(`<div class=popups><h2>${city}</h2>
                
                <h3>${coordinates[0]}, ${coordinates[1]}</h3>
                <br> Ground Temp: 
                <div id="groundTempBoxes"><p class="severityMarker"> ${(groundTemp - 273.15).toFixed(2)} C</p></div>

                <br> Ice Change: 
                <div id="groundTempBoxes"><p class="severityMarker"> ${iceChange}%</p></div>

                <br> Slope Index: 
                <div id="groundTempBoxes">${slopeString}<p class="severityMarker">\t${slope}/5</p></div>

                <br> Risk Index: 
                <div id="groundTempBoxes">${riskString}<p class="severityMarker">\t${risk}/5</p></div>

                <br> Population: 
                <p class="severityMarker">${pop}</p>


                </div>
                `);
            markersList.push(marker);

            
            
           




        });
    }
}





var map = L.map('map').setView([67.288194, -102.294416], 4);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);




map.on('zoomend', function () {
    var zoomLevel = map.getZoom();
    markersList.forEach((element) => {
        if (zoomLevel > 6) {
            map.removeLayer(element);
        } else {
            map.addLayer(element);
        }
    });

});
