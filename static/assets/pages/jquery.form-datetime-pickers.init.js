/**
 * Theme: Zircos Admin Template
 * Author: Coderthemes
 * Form Pickers
 */
var date = new Date();
$(function () {
    $('.datetimepicker').datetimepicker({
        language: 'zh-CN',
        CustomFormat: 'yyyy-mm-dd HH:ii:ss',
        weekStart: 1,
        todayBtn: 1,            //显示当天按钮，点击则选择当天当天时间
        autoclose: 1,           //选完时间自动关闭
        todayHighlight: 1,      //当天时间高亮
        startView: 2,           //从月视图开始，选天
        minView: 0,             //提供选择分钟的视图
        forceParse: 0,
// 　　　　 startDate: new Date(),  //只能选当前时间之后的时间
        minuteStep: 1           //用于构建小时视图。就是最小的视图是每1分钟可选一次。是以分钟为单位的
    });

})