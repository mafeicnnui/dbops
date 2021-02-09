
/**
* Theme: Zircos  Admin Template
* Author: Coderthemes
* Dashboard
*/

!function($) {
    "use strict";

    var Dashboard1 = function() {
    	this.$realData = []
    };

    //creates Bar chart
    Dashboard1.prototype.createBarChart  = function(element, data, xkey, ykeys, labels, lineColors,postUnits) {
        Morris.Bar({
            element: element,
            data: data,
            xkey: xkey,
            ykeys: ykeys,
            labels: labels,
            hideHover: 'auto',
            resize: true, //defaulted to true
            gridLineColor: '#eeeeee',
            barSizeRatio: 0.4,
            barColors: lineColors,
            postUnits: postUnits
        });
    },

    //creates line chart
    Dashboard1.prototype.createLineChart = function(element, data, xkey, ykeys, labels, opacity, Pfillcolor, Pstockcolor, lineColors) {
        Morris.Line({
          element: element,
          data: data,
          xkey: xkey,
          ykeys: ykeys,
          labels: labels,
          fillOpacity: opacity,
          pointFillColors: Pfillcolor,
          pointStrokeColors: Pstockcolor,
          behaveLikeLine: true,
          gridLineColor: '#eef0f2',
          hideHover: 'auto',
          resize: true, //defaulted to true
          pointSize: 0,
          lineColors: lineColors,
          postUnits: 's'
        });
    },

    //creates Donut chart
    Dashboard1.prototype.createDonutChart = function(element, data, colors) {
        Morris.Donut({
            element: element,
            data: data,
            resize: true, //defaulted to true
            colors: colors
        });
    },
    
    Dashboard1.prototype.init = function() {

        //add by mafei 2019.09.23 backup timing
        /*
         var $barData_db_backup_time_biz  = [
            { y: '2019/01/16', a: 42 },
            { y: '2019/01/17', a: 75 },
            { y: '2019/01/18', a: 38 },
            { y: '2019/01/19', a: 19 },
            { y: '2019/01/20', a: 93 },
            { y: '2019/01/21', a: 19 },
            { y: '2019/01/22', a: 93 }
        ];
        console.log('$barData_db_backup_time_biz=',$barData_db_backup_time_biz)
        this.createBarChart('db-backup-size', $barData_db_backup_time_biz, 'y', ['a'], ['大小'], ['#3bafda'],'');

        //create line chart

        var $data  = [
            { y: '2008', a: 50 },
            { y: '2009', a: 75 },
            { y: '2010', a: 30 },
            { y: '2011', a: 50 },
            { y: '2012', a: 75 },
            { y: '2013', a: 50 },
            { y: '2014', a: 75 },
            { y: '2015', a: 100 }
          ];
        console.log('$barData_db_backup_time=',$barData_db_backup_time)
        this.createLineChart('db-backup-time', $barData_db_backup_time, 'y', ['a'], ['时长'],['0.9'],['#ffffff'],['#999999'], ['#10c469']);
        */

    },
    //init
    $.Dashboard1 = new Dashboard1, $.Dashboard1.Constructor = Dashboard1
}(window.jQuery),

//initializing 
function($) {
    "use strict";
    $.Dashboard1.init();
}(window.jQuery);