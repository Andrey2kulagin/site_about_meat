$(document).on('change', '[id^="input_"]', function(page){
    let product_id = $(this).attr('id').substring(6);
    let url_id = `#change_url`;
    let url = $(url_id).val();
    let goods_count = $(this).val()
  $.ajax({
            type:"post",
            url: url,
            data:{
                product_id: product_id,
                goods_count: goods_count,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(page){
                let cost = $(`#product_cost${product_id}`).text();
               $(`#cart_sum${product_id}`).text(cost*(+goods_count));
            },
        });
});