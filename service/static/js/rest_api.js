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



    // ****************************************
    // Update a Product
    // ****************************************


    // ****************************************
    // Retrieve a Product
    // ****************************************


    // ****************************************
    // Delete a Product
    // ****************************************


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
