
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
            postUnits: 'k'
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

        //creating bar chart
        var $barData  = [
            { y: '2019/01/16', a: 42 },
            { y: '2019/02/16', a: 75 },
            { y: '2019/03/16', a: 38 },
            { y: '2019/04/16', a: 19 },
            { y: '2019/05/16', a: 93 }
        ];
        this.createBarChart('morris-bar-example', $barData, 'y', ['a'], ['Statistics'], ['#3bafda'],'k');

        //add by mafei 2019.09.23 slow query
         var $barData_db_slow_master  = [
            { y: '2019/01/16', a: 42 },
            { y: '2019/01/17', a: 75 },
            { y: '2019/01/18', a: 38 },
            { y: '2019/01/19', a: 19 },
            { y: '2019/01/20', a: 93 },
            { y: '2019/01/21', a: 19 },
            { y: '2019/01/22', a: 93 }
        ];
        this.createBarChart('morris-bar-db-slow-master', $barData_db_slow_master, 'y', ['a'], ['master'], ['#3bafda'],'');

        var $barData_db_slow_slave  = [
            { y: '2019/01/16', a: 42 },
            { y: '2019/01/17', a: 45 },
            { y: '2019/01/18', a: 38 },
            { y: '2019/01/19', a: 29 },
            { y: '2019/01/20', a: 93 },
            { y: '2019/01/21', a: 19 },
            { y: '2019/01/22', a: 43 }
        ];
        this.createBarChart('morris-bar-db-slow-slave', $barData_db_slow_slave, 'y', ['a'], ['slave'], ['#c5da22'],'');

        var $barData_db_slow_bi  = [
            { y: '2019/01/16', a: 72 },
            { y: '2019/01/17', a: 75 },
            { y: '2019/01/18', a: 28 },
            { y: '2019/01/19', a: 19 },
            { y: '2019/01/20', a: 93 },
            { y: '2019/01/21', a: 19 },
            { y: '2019/01/22', a: 63 }
        ];
        this.createBarChart('morris-bar-db-slow-bi', $barData_db_slow_bi, 'y', ['a'], ['bi'], ['#2ddad4'],'');

        //add by mafei 2019.09.23 backup timing
         var $barData_db_backup_time_biz  = [
            { y: '2019/01/16', a: 42 },
            { y: '2019/01/17', a: 75 },
            { y: '2019/01/18', a: 38 },
            { y: '2019/01/19', a: 19 },
            { y: '2019/01/20', a: 93 },
            { y: '2019/01/21', a: 19 },
            { y: '2019/01/22', a: 93 }
        ];
        this.createBarChart('morris-bar-db-backup-time-biz', $barData_db_backup_time_biz, 'y', ['a'], ['Statistics'], ['#3bafda'],'');

        var $barData_db_backup_time_bi  = [
            { y: '2019/01/16', a: 42 },
            { y: '2019/01/17', a: 45 },
            { y: '2019/01/18', a: 38 },
            { y: '2019/01/19', a: 29 },
            { y: '2019/01/20', a: 93 },
            { y: '2019/01/21', a: 19 },
            { y: '2019/01/22', a: 43 }
        ];
        this.createBarChart('morris-bar-db-backup-time-bi', $barData_db_backup_time_bi, 'y', ['a'], ['Statistics'], ['#c5da22'],'');

        //add by mafei 2019.09.23 backup space
        var $barData_db_backup_space_biz  = [
            { y: '2019/01/16', a: 9.6 },
            { y: '2019/01/17', a: 9.2 },
            { y: '2019/01/18', a: 8.6 },
            { y: '2019/01/19', a: 9.0 },
            { y: '2019/01/20', a: 7.5 },
            { y: '2019/01/21', a: 8.2 },
            { y: '2019/01/22', a: 9.2 }
        ];
        this.createBarChart('morris-bar-db-backup-space-biz', $barData_db_backup_space_biz, 'y', ['a'], ['Statistics'], ['#3bafda'],'G');

         var $barData_db_backup_space_bi  = [
            { y: '2019/01/16', a: 9.6 },
            { y: '2019/01/17', a: 9.2 },
            { y: '2019/01/18', a: 8.6 },
            { y: '2019/01/19', a: 9.0 },
            { y: '2019/01/20', a: 7.5 },
            { y: '2019/01/21', a: 8.2 },
            { y: '2019/01/22', a: 9.2 }
        ];
        this.createBarChart('morris-bar-db-backup-space-bi', $barData_db_backup_space_bi, 'y', ['a'], ['Statistics'], ['#3bafda'],'G');

        //create line chart
        var $data  = [
            { y: '2008', a: 50, b: 0 },
            { y: '2009', a: 75, b: 50 },
            { y: '2010', a: 30, b: 80 },
            { y: '2011', a: 50, b: 50 },
            { y: '2012', a: 75, b: 10 },
            { y: '2013', a: 50, b: 40 },
            { y: '2014', a: 75, b: 50 },
            { y: '2015', a: 100, b: 70 }
          ];
        this.createLineChart('morris-line-example', $data, 'y', ['a','b'], ['Series A','Series B'],['0.9'],['#ffffff'],['#999999'], ['#10c469','#188ae2']);

        //creating donut chart
        var $donutData = [
                {label: "生产主库", value: 32},
                {label: "生产从库", value: 30},
                {label: "生产BI库", value: 38}
            ];
        this.createDonutChart('morris-donut-example', $donutData, ['#3ac9d6', '#f5707a', "#3ed359"]);
    },
    //init
    $.Dashboard1 = new Dashboard1, $.Dashboard1.Constructor = Dashboard1
}(window.jQuery),

//initializing 
function($) {
    "use strict";
    $.Dashboard1.init();
}(window.jQuery);