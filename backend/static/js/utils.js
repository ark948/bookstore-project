function clearFilters() {
    $('#price_range').val("");
    $('#price_range_value').html("0 تومان");
    document.getElementById('filter_only_available').checked = false;
    $('#genre_select').prop('selectedIndex', 0);
}

function calc() {
    // JQuery only detects checked event, for some reason
    if (document.getElementById('filter_only_available').checked) {
        console.log("checked");
    } else {
        console.log("unchecked");
    }
}

function update_cart() {
    $.ajax({
        url: '{% url "shop:cart_count" %}',
        type: 'GET',
        success: function (data) {
            console.log('cart count update requested');
            $('#cart_count_badge').html(data);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(thrownError);
        }
    })
}