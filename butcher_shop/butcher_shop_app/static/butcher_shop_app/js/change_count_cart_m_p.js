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
                let input_val = +$(`#${product_id}`).val();
                $(`#${product_id}`).val(input_val + 1);
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
                let input_val = +$(`#${product_id}`).val();
                if (input_val>1){
                    $(`#${product_id}`).val(input_val - 1);
                   }
            },
        });
     }
});