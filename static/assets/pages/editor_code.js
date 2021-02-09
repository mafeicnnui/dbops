/* ------------------------------------------------------------------------------
*
*  # Ace code editor
*
*  Specific JS code additions for editor_code.html page
*
*  Version: 1.0
*  Latest update: Aug 1, 2015
*
* ---------------------------------------------------------------------------- */

$(function() {

    // Javascript editor
    var js_editor = ace.edit("javascript_editor");
        //js_editor.setTheme("ace/theme/monokai");
        //js_editor.setTheme("ace/theme/twilight");
        js_editor.setTheme("ace/theme/xcode");
        js_editor.getSession().setMode("ace/mode/sql");
        //js_editor.setShowPrintMargin(false);

   /*
    //自动换行,设置为off关闭
    js_editor.setOption("wrap", "free");

    //设置只读（true时只读，用于展示代码）
    js_editor.setReadOnly(true);

    //跳转到行
    //editor.gotoLine(lineNumber);

    //获取总行数
    editor.session.getLength();

    /以下部分是设置输入代码提示的
    js_editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true
    });

   //支持代码折叠
    js_editor.getSession().setUseWrapMode(true);

   //获取光标所在行或列
    js_editor.selection.getCursor();
    console.log(' js_editor.selection.getCursor()=', js_editor.selection.getCursor())
 */
});
