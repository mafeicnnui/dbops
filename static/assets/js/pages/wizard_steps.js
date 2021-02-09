/* ------------------------------------------------------------------------------
*
*  # Steps wizard
*
*  Specific JS code additions for wizard_steps.html page
*
*  Version: 1.0
*  Latest update: Aug 1, 2015
*
* ---------------------------------------------------------------------------- */

$(function() {


    // Wizard examples
    // ------------------------------

    // Basic wizard setup
    $(".steps-basic").steps({
        headerTag: "h6",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        titleTemplate: '<span class="number">#index#</span> #title#',
        labels: {
            finish: '更新密码',
            next: '下一步',
            previous : '上一步'
        },
        onFinished: function (event, currentIndex) {
            alert("Form submitted steps-basic.");
        }
    });


    // Async content loading
    $(".steps-async").steps({
        headerTag: "h6",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        titleTemplate: '<span class="number">#index#</span> #title#',
        labels: {
            finish: '更新密码'
        },
        onContentLoaded: function (event, currentIndex) {
            alert('xxxxxxxxx');
        },
        onFinished: function (event, currentIndex) {
            alert("Form submitted steps-async.");
        }
    });


    // Saving wizard state
    $(".steps-state-saving").steps({
        headerTag: "h6",
        bodyTag: "fieldset",
        saveState: true,
        titleTemplate: '<span class="number">#index#</span> #title#',
        autoFocus: true,
        onFinished: function (event, currentIndex) {
            alert("Form submitted. steps-state-saving");
        }
    });


    // Specify custom starting step
    $(".steps-starting-step").steps({
        headerTag: "h6",
        bodyTag: "fieldset",
        startIndex: 2,
        titleTemplate: '<span class="number">#index#</span> #title#',
        autoFocus: true,
        onFinished: function (event, currentIndex) {
            alert("Form submitted. steps-starting-step");
        }
    });


    //
    // Wizard with validation
    //

    // Show form
    var form = $(".steps-validation").show();


    // Initialize wizard
    $(".steps-validation").steps({
        headerTag: "h6",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        titleTemplate: '<span class="number">#index#</span> #title#',
        labels: {
            finish   : '修改密码',
            next     : '下一步',
            previous : '上一步'
        },
        autoFocus: true,
        onStepChanging: function (event, currentIndex, newIndex) {
            console.log('steps-validation=',event, currentIndex, newIndex);

            // Allways allow previous action even if the current form is not valid!
            if (currentIndex > newIndex) {
                return true;
            }

            // Forbid next action on "Warning" step if the user is to young
            if (newIndex === 3 && Number($("#age-2").val()) < 18) {
                return false;
            }

            // Needed in some cases if the user went back (clean up)
            if (currentIndex < newIndex) {

                // To remove error styles
                form.find(".body:eq(" + newIndex + ") label.error").remove();
                form.find(".body:eq(" + newIndex + ") .error").removeClass("error");
            }

            form.validate().settings.ignore = ":disabled,:hidden";
            flag = form.valid();
            console.log('flag=',flag,'newIndex=',newIndex);
            if (newIndex == 1 ) {
                 if (flag) {
                      var ret = true;
                      $.ajax({
                            url: "/forget_password/check_user",
                            type: "post",
                            datatype: "json",
                            async:false,
                            data: {
                                 user  : $('#user').val(),
                                 email : $('#email').val(),
                            },
                            beforeSend: function () {
                                swal({
                                    title: "发送邮件中...",
                                    text: "用户["+user+"]验证邮件发送中...",
                                    type: "info",
                                    showConfirmButton: false
                                 });
                            },
                            success: function (dataSet) {
                                console.log('forget_password/check_user=',dataSet.code, dataSet.message);
                                if (dataSet.code==-1) {
                                   swal(dataSet.message, "", "error")
                                   ret = false;
                                } else {
                                   swal({title:dataSet.message,timer: 2000,showConfirmButton: false});
                                }
                            },
                       });
                      return ret;
                }
            }

            if (newIndex == 2 ) {
                 if (flag) {
                      var ret = true;
                      $.ajax({
                            url: "/forget_password/check_auth",
                            type: "post",
                            datatype: "json",
                            async:false,
                            data: {
                                 user     : $('#user').val(),
                                 auth     : $('#authcode').val(),
                            },
                            success: function (dataSet) {
                                console.log('forget_password/check_auth=',dataSet.code, dataSet.message);
                                if (dataSet.code==-1) {
                                   swal(dataSet.message, "", "error")
                                   ret = false;
                                } else {
                                   swal({title:dataSet.message,timer: 2000,showConfirmButton: false});
                                }
                            },
                       });
                      return ret;
                }
            }



            return flag;
        },

        onStepChanged: function (event, currentIndex, priorIndex) {

            // Used to skip the "Warning" step if the user is old enough.
            if (currentIndex === 2 && Number($("#age-2").val()) >= 18) {
                form.steps("next");
            }

            // Used to skip the "Warning" step if the user is old enough and wants to the previous step.
            if (currentIndex === 2 && priorIndex === 3) {
                form.steps("previous");
            }

            console.log('onStepChanged...',currentIndex)

        },

        onFinishing: function (event, currentIndex) {
            form.validate().settings.ignore = ":disabled";
            return form.valid();
            console.log('onFinishing...')
        },

        onFinished: function (event, currentIndex) {
            console.log('onFinished=>currentIndex=',currentIndex)
            if (currentIndex == 2 ) {
                 if (flag) {
                      var ret = true;
                      $.ajax({
                            url: "/forget_password/check_pass",
                            type: "post",
                            datatype: "json",
                            async:false,
                            data: {
                                 user     : $('#user').val(),
                                 auth     : $('#authcode').val(),
                                 newpass  : $('#new_password').val(),
                                 reppass  : $('#rep_password').val(),
                            },
                            success: function (dataSet) {
                                console.log('forget_password/check_pass=',dataSet.code, dataSet.message);
                                if (dataSet.code==-1) {
                                   swal(dataSet.message, "", "error")
                                   ret = false;
                                } else {
                                   swal({title:dataSet.message,timer: 2000,showConfirmButton: false});
                                   window.location.href='/'
                                }
                            },
                       });
                      return ret;
                }
            }

        }
    });


    // Initialize validation
    $(".steps-validation").validate({
        ignore: 'input[type=hidden], .select2-input',
        errorClass: 'validation-error-label',
        successClass: 'validation-valid-label',
        highlight: function(element, errorClass) {
            $(element).removeClass(errorClass);
        },
        unhighlight: function(element, errorClass) {
            $(element).removeClass(errorClass);
        },
        errorPlacement: function(error, element) {
            if (element.parents('div').hasClass("checker") || element.parents('div').hasClass("choice") || element.parent().hasClass('bootstrap-switch-container') ) {
                if(element.parents('label').hasClass('checkbox-inline') || element.parents('label').hasClass('radio-inline')) {
                    error.appendTo( element.parent().parent().parent().parent() );
                }
                 else {
                    error.appendTo( element.parent().parent().parent().parent().parent() );
                }
            }
            else if (element.parents('div').hasClass('checkbox') || element.parents('div').hasClass('radio')) {
                error.appendTo( element.parent().parent().parent() );
            }
            else if (element.parents('label').hasClass('checkbox-inline') || element.parents('label').hasClass('radio-inline')) {
                error.appendTo( element.parent().parent() );
            }
            else if (element.parent().hasClass('uploader') || element.parents().hasClass('input-group')) {
                error.appendTo( element.parent().parent() );
            }
            else {
                error.insertAfter(element);
            }
        },
        rules: {
            email: {
                email: true
            }
        }
    });



    // Initialize plugins
    // ------------------------------

    // Select2 selects
    // $('.select').select2();
    //
    //
    // // Simple select without search
    // $('.select-simple').select2({
    //     minimumResultsForSearch: '-1'
    // });
    //
    //
    // // Styled checkboxes and radios
    // $('.styled').uniform({
    //     radioClass: 'choice'
    // });
    //
    //
    // // Styled file input
    // $('.file-styled').uniform({
    //     wrapperClass: 'bg-warning',
    //     fileButtonHtml: '<i class="icon-googleplus5"></i>'
    // });
    
});
