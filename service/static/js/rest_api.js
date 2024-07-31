$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_description").val(res.description);
        $("#product_quantity").val(res.quantity);
        $("#product_price").val(res.price);
        $("#product_product_id").val(res.product_id);
        $("#product_restock_level").val(res.restock_level);
        $("#product_condition").val(res.condition);
    }

    // Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_description").val("");
        $("#product_quantity").val("");
        $("#product_price").val("");
        $("#product_product_id").val("");
        $("#product_restock_level").val("");
        $("#product_condition").val("Unknown");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {
        let name = $("#product_name").val();
        let description = $("#product_description").val();
        let quantity = parseInt($("#product_quantity").val(), 10);
        let price = parseFloat($("#product_price").val());
        let product_id = parseInt($("#product_product_id").val(), 10);
        let restock_level = parseInt($("#product_restock_level").val(), 10);
        let condition = $("#product_condition").val();

        let data = {
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price,
            "product_id": product_id,
            "restock_level": restock_level,
            "condition": condition
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: `/inventory`,
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json"
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Update a Product
    // ****************************************


    // ****************************************
    // Retrieve a Product
    // ****************************************


    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let product_id= $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/inventory/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Inventory item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for Products
    // ****************************************


})
