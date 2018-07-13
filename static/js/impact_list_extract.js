$(document).ready(function(){
        $("button").click(function(){
            var selectItem = [];
            $('.selectpicker').children().each(
                function(e,item){
                    if(item.selected)
                        selectItem.push(item.value)
                });
        // $('#output').append(selectItem.join(','))
            var edz_list = JSON.stringify(selectItem);
            $.ajax({
                url:"/impact_list_extract/",
                type: 'POST',
                dataType: 'json',
                data: edz_list
            });
        });
    });