$(document).on('click', '[id^="change_btn_"]', function(page){
    page.preventDefault();
    let  type = page.target.name;
    if (type=='+'){
        let full_id = page.target.id
        let product_id = full_id.substring(15);
        let url_id = `#plus_url${product_id}`;
        let url = $(url_id).val();
        $.ajax({
            type:"get",
            url: url,
            success:function(data){
                let input_val = +$(`#input_${product_id}`).val();
                $(`#input_${product_id}`).val(input_val + 1);
                let goods_count = $(`#input_${product_id}`).val()
                let cost = $(`#product_cost${product_id}`).text();
               $(`#cart_sum${product_id}`).text(+cost*(+goods_count));
            },
        });
       }
     if (type=='-'){
     let product_id = page.target.id.substring(16);
     let url = $(`#minus_url${product_id}`).val();
     $.ajax({
            type:"get",
            url: url,
            success:function(data){
                let input_val = +$(`#input_${product_id}`).val();
                if (input_val>1){
                    $(`#input_${product_id}`).val(input_val - 1);
                   }
                let goods_count = $(`#input_${product_id}`).val()
                let cost = $(`#product_cost${product_id}`).text();
               $(`#cart_sum${product_id}`).text(+cost*(+goods_count));
            },
        });
     }
});