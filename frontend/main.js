x = [];
y = [];
//Get the context of the canvas element we want to select



xhr = new XMLHttpRequest();
xhr.open('GET', 'dogetipdata.json', true);
xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
        dogetipdata = JSON.parse(xhr.responseText);
        for (i=0; i<dogetipdata.length; i++) {
            dogetipdata[i][0] = dogetipdata[i][0]*1000;
            dogetipdata[i][1] = dogetipdata[i][1]*1000;
        }
        current_delay = Math.round(dogetipdata[dogetipdata.length-1][1] / 1000 / 60);
        document.getElementById('delay').innerText =  current_delay + " minutes"

        var options = {xaxis: {mode: "time",
                               tickLength: 5,
                               timeformat: "%m/%d %h:%M",
                               timezone: null
                              },
                       yaxis: {mode: "time",
                               timeformat: "%h:%M:%S"},
                       legend: {show: false},
                       grid: {hoverable: true,
                              clickable: true},
        }

        $.plot($("#placeholder"), [{
            color: 'rgb(192, 57, 43)',
            data: dogetipdata,
            label: 'Delay', 
            lines: { show: true, fill: true, fillColor: "rgba(192, 57, 43, 0.5)" },
            points: {show: true}
        }], options);
    }
}
xhr.send();