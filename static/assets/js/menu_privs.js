
$.ajax({
      url: "/tree",
      type: "post",
      datatype: "json",
      data:{},
      success: function (dataSet) {
       console.log(dataSet.code, 'abc',dataSet.message,'ABC');
       $("#ul-menu").append(dataSet.message);
     }
});