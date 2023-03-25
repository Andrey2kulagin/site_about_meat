$(document).on('submit', 'form[id="application_form"]', function(page){
    page.preventDefault();
    let  formData = $(this).serialize();


    $.ajax({
        type:"POST",
        url: $("#application_url").val(),
        data: formData,
        success:function(data){
            $("#application_form")[0].reset();
        },
    });
});