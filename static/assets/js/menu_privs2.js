$(document).bind("keydown", function(e) {//文档绑定键盘按下事件
                e = window.event || e;//解决浏览器兼容的问题
                if(e.keyCode == 116) {//F5按下
                　　e.keyCode = 0;
                　　return false;
                }else{
                　　//让其刷新
                }
});

$('#sys_set').css('display','none');
$('#msg_mgr').css('display','none');

$("#ul-menu").append('<li class="has_sub">' +
                     '<a href="javascript:void(0);" class="waves-effect"><i class="fa fa-user"></i><span>用户管理2</span> <span class="menu-arrow"></span></a>' +
                     '<ul class="list-unstyled">' +
                         '<li><a href="#">用户查询2</a></li>' +
                         '<li><a id="user_add2" href="#">用户新增2</a></li>' +
                         '<li><a href="#">用户变更2</a></li>' +
                         '<li><a href="#">用户注销2</a></li>' +
                         '<li><a href="#">项目授权2</a></li>' +
                     '</ul>' +
                    '</li>');

$('#user_add').click(function(){
   $('#main-container-div').load("/user/add");
});

$('#user_add2').click(function(){
   $('#main-container-div').load("/user/add");
});
