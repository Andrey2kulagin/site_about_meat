$(document).on('change', '[id^="input_"]', function(page){
    let product_id = $(this).attr('id').substring(6);
    let url_id = `#change_url`;
    let url = $(url_id).val();
  $.ajax({
            type:"post",
            url: url,
            data:{
                product_id: product_id,
                goods_count:$(this).val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
        });
});