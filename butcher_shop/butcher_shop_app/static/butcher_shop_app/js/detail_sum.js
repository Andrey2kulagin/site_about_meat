$(document).on('change', '[id="detail_input"]', function(page){
    let goods_count = $(this).val();
    let cost = $("#product_cost").text();
    $("#product_sum").text(cost*(+goods_count));
});