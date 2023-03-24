$(document).on('submit', 'form[id^="product_list_add_to_cart"]', function(e){
    e.preventDefault();
    let id = e.target.name;
    $.ajax({
        type: 'POST',
        url: "{% url 'add_to_cart' %}",
        data:{
            form_type: $(`#product_list_form_type${id}`).val(),
            product_id: $(`#product_list_product_id${id}`).val(),
            product_name: $(`#product_list_product_name${id}`).val(),
            count: $(`#product_list_count${id}`).val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(data){
            console.log("adadas");
        },
    });
    $(`#product_list_count${id}`).val("1")
});
