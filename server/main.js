x = [];
y = [];
//Get the context of the canvas element we want to select
function resize_chart() {
    $('#placeholder').css('width', $('.charts').css('width'));
    $('#placeholder').css('height', '600px');
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
xhr.open('GET', 'JSON/frontpage.json', true);
xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
        data = JSON.parse(xhr.responseText);
        console.log('resize')
        
        // SECTION 1 //
        current_delay = Math.round(data.delay[data.delay.length - 1][1] / 60);
        if (current_delay==1) {
            $('#delay').text(current_delay + " minute");
        }
        else {
            $('#delay').text(current_delay + " minutes");
        }
        console.log(current_delay);
        
        // SECTION 2 //
        //convert all delays to ms
        for (i=0; i < data.delay.length; i++) {
            data.delay[i][0] = data.delay[i][0]*1000;
            data.delay[i][1] = data.delay[i][1]*1000;
        }
        //Display graph
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
            data: data.delay,
            label: 'Delay', 
            lines: { show: true, show: true, lineWidth: 4 },
            points: {show: false}
        }], options);
        
        // SECTION 3 //
        // Get the 7 biggest subs
        hundred_percent = 0;
        trending_subs = [];
        for (sub in data.hourly.subs) {
            if (data.hourly.subs[sub] > hundred_percent && sub!='dogecoin') {
                hundred_percent = data.hourly.subs[sub]
            }
            trending_subs.push([sub, data.hourly.subs[sub]]);
        }
        trending_subs.sort(function(a, b) {return b[1] - a[1]});
        trending_subs = trending_subs.slice(0,7);
        $('.bars').html('');
        for (i=0; i<trending_subs.length; i++) {
            this_sub = trending_subs[i][0];
            this_tips = trending_subs[i][1];
            if (this_sub != 'dogecoin') {
                if (this_tips != 1) {
                    title = this_tips + ' tips in the previous hour';
                }
                else {
                    title = this_tips + ' tip in the previous hour';
                }
                $('.bars').append('<div class="bar" style="height: ' + 200*this_tips/hundred_percent + 'px" title="' + title + '"><p>' + this_tips + '</p><span id="' + this_sub + '"><a href="http://www.reddit.com/r/' + this_sub + '">/r/' + this_sub + '</a></span></div>');
            }
        }
        //show the rest.
        adjust_spans();
        $('.bar').each(function () {
            $(this).css('font-size', $(this).height() + 'px');
        })
        $('#hourly_tips').text('Ð' + numberWithCommas(Math.round(data.hourly.amount_tipped)));
        $('#hourly_comments').text(data.hourly.many_comments);
        $('#average_tip').text('Ð' + Math.round(data.hourly.amount_tipped/data.hourly.many_comments));
        $('#data_size a').text(data.data_size)
        if (typeof(data.hourly.subs.dogecoin) == 'undefined') {
            data.hourly.subs.dogecoin = 0;
            percent_outside = 100;
        }
        else {
            other_subs = 0;
            for (sub in data.hourly.subs) {
                if (sub != 'dogecoin') {
                    other_subs += data.hourly.subs[sub];
                }
            }
            percent_outside = Math.round((other_subs / (data.hourly.subs.dogecoin + other_subs))*1000)/10;
        }
        $('#percent_outside').text(percent_outside + '%');
        
        
    }
}
xhr.send();
$(window).on('resize', function () { //Not beautiful, but it'll do for now
    xhr.onreadystatechange()
});
