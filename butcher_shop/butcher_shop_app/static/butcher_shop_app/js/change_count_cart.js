$(document).on('click', '[id^="change_btn_"]', function(page){
    page.preventDefault();
    let  type = page.target.name;
    id =
    if (type=='+'){
        $.ajax({
            type:"POST",
            url: $("#change_url").val(),
            data: formData,
            success:function(data){
                $("#application_form")[0].reset();
            },
        });
       }
     if (type=='-'){
     $.ajax({
            type:"POST",
            url: $("#change_url").val(),
            data: formData,
            success:function(data){
                $("#application_form")[0].reset();
            },
        });
     }
});