function add_cart_count(id) {
  let input = document.getElementById(id);
  input.value = +input.value + 1;
    let goods_count = input.value
  let cost = $("#product_cost").text();
  $("#product_sum").text(cost*(+goods_count));
}
function sub_cart_count(id) {
  let input = document.getElementById(id);
  cure_value = +input.value;
  if (cure_value > 1) {
    input.value = cure_value -1;
  }
    let goods_count = input.value
  let cost = $("#product_cost").text();
  $("#product_sum").text(cost*(+goods_count));
}
