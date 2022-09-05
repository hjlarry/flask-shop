  $(".variant-picker__option").click(function(){
    var variant_id = $(this).children().attr("value");
    $.ajax({
    url:"api/variant_price/"+variant_id,
    success:function(result){
        $(".text-info").text('$ ' + result.price)
        $(".stock").text('Stock: ' + result.stock)
    }
    });
});