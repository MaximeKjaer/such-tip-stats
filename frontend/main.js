x = [];
y = [];
//Get the context of the canvas element we want to select
function resize_chart() {
    $('#placeholder').css('width', $('.charts').css('width'));
    
}

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function adjust_spans () {
    $('.bar span').each(function () {
        $(this).css('left', ($(this).parent().width() - $(this).width())/2 + 'px');

    });
}


$(window).resize(function () {
    adjust_spans();
    resize_chart();
});
resize_chart();

xhr = new XMLHttpRequest();
xhr.open('GET', 'dogetipdata2.json', true);
xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
        dogetipdata = JSON.parse(xhr.responseText);
        for (i=0; i<dogetipdata.length; i++) {
            dogetipdata[i][0] = dogetipdata[i][0]*1000;
            dogetipdata[i][1] = dogetipdata[i][1]*1000;
        }
        current_delay = Math.round(dogetipdata[dogetipdata.length-1][1] / 1000 / 60);
        if (current_delay==1) document.getElementById('delay').innerText =  current_delay + " minute";
        else document.getElementById('delay').innerText = current_delay + " minutes";

        var options = {xaxis: {mode: "time",
                               tickLength: 5,
                               timeformat: "%m/%d %h:%M",
                               timezone: null
                              },
                       yaxis: {mode: "time",
                               timeformat: "%h:%M:%S"},
                       legend: {show: false},
                       grid: {hoverable: true,
                              clickable: true,
                              color: 'rgba(255,255,255,1)',
                              borderColor: 'rgba(0,0,0,0)'}
        }

        $.plot($("#placeholder"), [{
            color: '#ffffff',
            data: dogetipdata,
            label: 'Delay', 
            lines: { show: true, show: true, lineWidth: 4 },
            points: {show: false}
        }], options);
    }
}
xhr.send();

hourlyxhr = new XMLHttpRequest();
hourlyxhr.open('GET', 'hourly.json', true);
hourlyxhr.onreadystatechange = function () {
    if (hourlyxhr.readyState == 4) {
        hourlydata = JSON.parse(hourlyxhr.responseText);
        subs_data = hourlydata[hourlydata.length-1]['subs'];
        hourly_tips = hourlydata[hourlydata.length-1]['amount_tipped'];
        hourly_comments = hourlydata[hourlydata.length-1]['many_comments'];
        hundred_percent = 0;
        sortable = [];
        for (sub in subs_data) {
            if (subs_data[sub] > hundred_percent && sub!='dogecoin') {
                hundred_percent = subs_data[sub]
            }
            sortable.push([sub, subs_data[sub]]);
        }
        sortable.sort(function(a, b) {return b[1] - a[1]});
        trending_subs = sortable.slice(0,7);
        for (i=0; i<trending_subs.length; i++) {
            this_sub = trending_subs[i][0];
            this_tips = trending_subs[i][1];
            if (this_sub != 'dogecoin') {
                if (this_tips != 1) title = this_tips + ' tips in the previous hour';
                else title = this_tips + ' tip in the previous hour';
                $('.bars').append('<div class="bar" style="height: ' + 200*this_tips/hundred_percent + 'px" title="' + title + '"><p>' + this_tips + '</p><span id="' + this_sub + '">/r/' + this_sub + '</span></div>');
            }
        }
        adjust_spans();
        $('.bar').each(function () {
            $(this).css('font-size', $(this).height() + 'px');
        })
        $('.bar').hide();
        $('.bar').fadeIn(1000);
        $('#hourly_tips').text('Ð' + numberWithCommas(Math.round(hourly_tips)));
        $('#hourly_comments').text(hourly_comments);
        $('#average_tip').text('Ð' + Math.round(hourly_tips/hourly_comments));
        
        
    }
}
hourlyxhr.send();