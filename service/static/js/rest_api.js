$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_quantity").val(res.quantity);
        $("#product_restock_level").val(res.restock_level);
        $("#product_restock_count").val(res.restock_count);
        $("#product_condition").val(res.condition);
        $("#product_first_entry_date").val(res.first_entry_date);
        $("#product_last_restock_date").val(res.last_restock_date);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_quantity").val("");
        $("#product_restock_level").val("");
        $("#product_restock_count").val("");
        $("#product_condition").val("Unknown");
        $("#product_first_entry_date").val("");
        $("#product_last_restock_date").val("");
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
    // Search for a Product
    // ****************************************

})