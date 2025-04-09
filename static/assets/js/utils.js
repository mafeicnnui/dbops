//引入外部js
document.write("<script src='./static/plugins/morris/morris.min.js'></script>");
document.write("<script src='./static/plugins/toastr/toastr.min.js'></script>");
document.write("<script src='./static/plugins/echarts/echarts.min.js'></script>");
// document.write("<script src='./static/assets/js/jquery.min.js'></script>");

//获取当前日期
function GetDate(format) {
     /**
     * format=1 表示获取年月日
     * format=2 表示获取年月日时分秒
     * **/
     var _time;
     var now   = new Date();
     var year  = now.getFullYear();
     var month = now.getMonth()+1;
     var date  = now.getDate();
     var day   = now.getDay();//得到周几
     var hour  = now.getHours();//得到小时
     var minu  = now.getMinutes();//得到分钟
     var sec   = now.getSeconds();//得到秒

     if (month <10) {
         month="0"+month
     }
     if (date <10) {
         date="0"+date
     }

     if (format==1){
         _time = year+"-"+month+"-"+date
     } else if (format==2){
         _time = year+"-"+month+"-"+date+" "+hour+":"+minu+":"+sec
     } else if (format==3){
        _time = year+"-"+month+"-"+date+" 0:0:0"
     } else if (format==4) {
        _time = year+"-"+month
     }  else if (format==5) {
         _time = year.toString() + month.toString() + date.toString()
     }
    return _time
 }

 //日期比较
function GetDateDiff(startTime, endTime, diffType) {
    /*
      * 获得时间差,时间格式为 年-月-日 小时:分钟:秒 或者 年/月/日 小时：分钟：秒
      * 其中，年月日为全格式，例如 ： 2010-10-12 01:00:00
      * 返回精度为：秒，分，小时，天
    */
    startTime = startTime.replace(/\-/g, "/");
    endTime   = endTime.replace(/\-/g, "/");

    //将计算间隔类性字符转换为小写
    diffType = diffType.toLowerCase();
    var sTime = new Date(startTime);      //开始时间
    var eTime = new Date(endTime);        //结束时间

    //作为除数的数字
    var divNum = 1;
    switch (diffType) {
        case "second":
            divNum = 1000;
            break;
        case "minute":
            divNum = 1000 * 60;
            break;
        case "hour":
            divNum = 1000 * 3600;
            break;
        case "day":
            divNum = 1000 * 3600 * 24;
            break;
        default:
            break;
    }
    return parseInt((eTime.getTime() - sTime.getTime()) / parseInt(divNum));

}

//左上角显示提示
function showtips(flag,title,content){
    //警告提醒
    toastr.options = {
          "closeButton": false,
          "debug": false,
          "newestOnTop": false,
          "progressBar": true,
          "positionClass": "toast-top-right",
          "preventDuplicates": false,
          "onclick": null,
          "showDuration": "3000",
          "hideDuration": "1000",
          "timeOut": "5000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
        }
        toastr[flag](content,title)
  }

//开始显示遮照
function start_Loader(p_id) {
    var light = $('#'+p_id).parent();
    $(light).block({
        message: '<i class="icon-spinner spinner"></i>',
        overlayCSS: {
            // backgroundColor: 'rgba(233,231,228,0.53)',
            backgroundColor: 'rgba(248,247,244,0.53)',

            opacity: 0.1,
            cursor: 'wait'
        },
        css: {
            border: 0,
            padding: 0,
            backgroundColor: 'none'
        }
    });
}

//结束显示遮照
function end_Loader(p_id) {
    var light = $('#'+p_id).parent();
    $(light).unblock();
}

//返回dataTable语言对象
function get_languages() {
    return {
         "search"       : "在表格中搜索:",
         "sProcessing"  : "处理中...",
         "sLengthMenu"  : "显示 _MENU_ 项结果",
         "sZeroRecords" : "没有匹配结果",
         "sInfo"        : "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
         "sInfoEmpty"   : "显示第 0 至 0 项结果，共 0 项",
         "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
         "sInfoPostFix" : "",
         "sSearch"      : "搜索:",
         "sUrl"         : "",
         "sEmptyTable"  : "表中数据为空",
         "sLoadingRecords": "载入中...",
         "sInfoThousands": ",",
         "oPaginate": {
             "sFirst"   : "首页",
             "sPrevious": "上页",
             "sNext"    : "下页",
             "sLast"    : "末页"
         },
         "oAria": {
             "sSortAscending" : ": 以升序排列此列",
             "sSortDescending": ": 以降序排列此列"
         }
     }
}

//设置页面上标签为必选项
function set_selected(){
    $("label:contains('*')").each(function(){
        $(this).children().css('color','red')
    })
}

//检测当前表格是否选中记录
function isSelectTable(table_id) {
       var rec=0;
       $("#"+table_id+" tbody tr td input:checked").each( function() {
          rec=rec+1;
       });
       if ( rec==1 ){
          return true
       } else {
          return false
       }
}

//窗口居中
function centerModals() {
      $('.modal').each(function(i) {
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 50 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 50);
      });
 }

 //窗口居中
function topModals() {
      $('.modal').each(function(i) {
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 50 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", 50);
      });
 }

 //画柱状图
function createBarChart (element, data, xkey, ykeys, labels, lineColors,postUnits) {
        Morris.Bar({
            element: element,
            data: data,
            xkey: xkey,
            ykeys: ykeys,
            labels: labels,
            hideHover: 'auto',
            resize: true, //defaulted to true
            gridLineColor: '#65d9b2',
            barSizeRatio: 0.6,
            barColors: lineColors,
            postUnits: postUnits
        });
}

//画曲线图
function createLineChart(element, data, xkey, ykeys, labels, opacity, Pfillcolor, Pstockcolor, lineColors,postUnits) {
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
          gridLineColor: '#8b9285',
          hideHover: 'auto',
          resize: true, //defaulted to true
          pointSize: 0,
          lineColors: lineColors,
          postUnits: postUnits,
          lineWidth:2
    });
}

 // 显示图表
function get_charts_large(p_title,p_x_data,p_y_data,p_color) {
      var myChart = echarts.init($('#monitor_review')[0])
      var option = {
          title:{
                 text:p_title,
                 left:'center',
                 textStyle:{
                    color:'#9ea7c4',
                    fontWeight:'bold',
                    fontFamily:'宋体',
            　　　　 fontSize:12
                }
           },
           grid: {
               top: '25px',
               bottom: '60px',
               right: '15px',
               left:'30px'
           },
           xAxis: {
                type: 'category',
                splitLine:{
                   show:false
                },
                axisLine: { show: true,lineStyle:{ color:'#329ba3' }},
                axisLabel:{
                    textStyle:
                        {  color:'#9ea7c4',
                           fontSize:8,
                           fontStyle: 'italic',
                           fontWeight: 'bold'
                        }
                },
                axisTick : {show: false},
                data: p_x_data
            },
            yAxis: {
                type: 'value',
                splitLine:{
                   show:false
                },
                margin: 5,
                rotate: 60,
                axisTick : {show:false},
                splitLine: {show:false},
                axisLabel: {textStyle:{color:'#9ea7c4',fontSize:8} },
                axisLine : {show: true,lineStyle:{ color:'#6173A3'}},
            },
           tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#83d5a5'
                }
              }
            },
          toolbox: {
                show: true,
                feature: {
                    saveAsImage: {
                　　　　show:true,
                　　　　excludeComponents :['toolbox'],
                　　　　pixelRatio: 1
                    }
                }
            },
            series: [{
                data: p_y_data,
                type: 'line',
                itemStyle : {
                    normal : {
                      lineStyle:{
                        color:p_color
                      }
                    }
                },
                showAllSymbol: false,
                symbolSize:1,
                smooth: true
            }]
      };
      myChart.setOption(option);
}

 // 显示图表
function get_charts_large_label(p_title,p_x_data,p_y_data,p_color,p_x_label,p_y_label) {
      var myChart = echarts.init($('#monitor_review')[0])
      var option = {
          title:{
                 text:p_title,
                 left:'center',
                 textStyle:{
                    color:'#9ea7c4',
                    fontWeight:'bold',
                    fontFamily:'宋体',
            　　　　 fontSize:12
                }
           },
           grid: {
                 left: '5%',
                 right: '10%',
                 bottom: '10%',
                 containLabel: true,
                 borderWidth: 1,
                 borderColor: '#ccc'
           },
           xAxis: {
                type: 'category',
                name:p_x_label,
                splitLine:{
                   show:false
                },
                axisLine: { show: true,lineStyle:{ color:'#329ba3' }},
                axisLabel:{
                    textStyle:
                        {  color:'#9ea7c4',
                           fontSize:8,
                           fontStyle: 'italic',
                           fontWeight: 'bold'
                        }
                },
                axisTick : {show: false},
                data: p_x_data
            },
           yAxis: {
                name:p_y_label,
                type: 'value',
                splitLine:{
                   show:false
                },
                margin: 5,
                rotate: 60,
                axisTick : {show:false},
                splitLine: {show:false},
                axisLabel: {textStyle:{color:'#9ea7c4',fontSize:8} },
                axisLine : {show: true,lineStyle:{ color:'#6173A3'}},
            },
           tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#83d5a5'
                }
              },
              formatter: function (params, ticket, callback) {
                  var htmlStr = '';
                  for(var i=0;i<params.length;i++){
                        var param = params[i];
                        var valx = param.name;
                        var valy = param.value;
                        var valz = valx.split(':')[0]+'时'+valx.split(':')[1]+'分'
                        //console.log(i,param)
                        htmlStr=htmlStr+'<span>请求时间&nbsp;&nbsp;:&nbsp;'+valz+'</span><br>'+'<span>响应时长&nbsp;&nbsp;: '+valy+'毫秒</span>'
                  }
                  return htmlStr;
                 }
            },
            toolbox: {
                show: true,
                feature: {
                    saveAsImage: {
                　　　　show:true,
                　　　　excludeComponents :['toolbox'],
                　　　　pixelRatio: 1
                    }
                }
            },
            series: [{
                data: p_y_data,
                type: 'line',
                itemStyle : {
                    normal : {
                      lineStyle:{
                        color:p_color
                      }
                    }
                },
                showAllSymbol: false,
                symbolSize:1,
                smooth: true
            }]
      };
      myChart.setOption(option);
}

//返回备份任务数组
function get_backup_tasks(){
    $.ajax({
              url: "/get/backup/task",
              type: "post",
              datatype: "json",
              data:{
                  db_env    : $('#db_env').val(),
                  db_type   : $('#db_type').val(),
              },
              success: function (dataSet) {
                 $("#tagname").empty();
                 $("#tagname").append("<option value=''>请选择任务...</option>");
                 for(i=0;i<dataSet['data'].length;i++){
                      var val  = dataSet['data'][i][0];
                      var text = dataSet['data'][i][1];
                      $("#tagname").append("<option value='"+val+"'>"+text+"</option>");
                 }
              },
         });
}

//格式化SQL
function format_sql(sql) {
   var res='';
   $.ajax({
        type: 'post',
        url: '/sql/_format',
        async:false,
        data: {
            "sql":sql
        },
        success: function (dataSet) {
          res=dataSet.message
        },
    })
    return res
}

//获取当前时间前一小时
function get_hour(n_hours) {
    var now = new Date;
    now.setMinutes(now.getMinutes() - n_hours*30);
    var stime = now.format("yyyy-MM-dd hh:mm");//一个小时前的时间
    //console.log('get_hour_minus_one_hours=',stime)
    return stime
}

//获取当前时间H:M:S
function get_curr_time() {
    var date    = new Date();
    this.hour   = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
    this.minute = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
    this.second = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
    var currentTime = this.hour + "时" + this.minute + "分" + this.second + '秒';
    return currentTime
}

String.prototype.format = function () {
    var values = arguments;
    return this.replace(/\{(\d+)\}/g, function (match, index) {
        if (values.length > index) {
            return values[index];
        } else {
            return "";
        }
    });
};

Date.prototype.format = function(fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
                "h+": this.getHours(), //小时
                "m+": this.getMinutes(), //分
                "s+": this.getSeconds(), //秒
                "q+": Math.floor((this.getMonth() + 3) / 3), //季度
                "S": this.getMilliseconds() //毫秒
        };
        if(/(y+)/.test(fmt)) {
                fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 -RegExp.$1.length));
        }
        for(var k in o) {
                if(new RegExp("(" + k + ")").test(fmt)) {
                    fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
                }
        }
        return fmt;
}

$.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        //console.log('this.name=',this.name)
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    //console.log('o=',o)
    return o;
};


function dict2str(item) {
      var tmp='';
      arr = $('#'+item).val()
      if (arr.length>0) {
         for (let i = 0, len = arr.length; i < len; i++) {
           tmp=tmp+','+arr[i];
         }
      } else {
          return ''
      }
      return tmp.substr(1);
}