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
         _time = year + month + date
     }
    return _time
 }

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

function start_Loader(p_id) {
    var light = $('#'+p_id).parent();
    $(light).block({
        message: '<i class="icon-spinner spinner"></i>',
        overlayCSS: {
            backgroundColor: '#a3edaa',
            opacity: 0.8,
            cursor: 'wait'
        },
        css: {
            border: 0,
            padding: 0,
            backgroundColor: 'none'
        }
    });
}

function end_Loader(p_id) {
    var light = $('#'+p_id).parent();
    $(light).unblock();
}