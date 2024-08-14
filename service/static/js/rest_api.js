$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#system_product_id").val(res.id);
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
        $("#system_product_id").val("");
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
            url: `/api/inventory`,
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

    $("#update-btn").click(function () {

        let system_product_id = $("#system_product_id").val();  // Use the system_product_id displayed in the form
        let name = $("#product_name").val();
        let description = $("#product_description").val();
        let quantity = parseInt($("#product_quantity").val(), 10);
        let price = parseFloat($("#product_price").val());
        let product_internal_id = parseInt($("#product_product_id").val(), 10);
        let restock_level = parseInt($("#product_restock_level").val(), 10);
        let condition = $("#product_condition").val();

        let data = {
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price,
            "product_id": product_internal_id,
            "restock_level": restock_level,
            "condition": condition
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/api/inventory/${system_product_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });




    // ****************************************
    // Retrieve a Product
    // ****************************************
    $("#retrieve-btn").click(function () {

        let system_product_id = $("#system_product_id").val();  // Use the system-generated ID instead of product_id

        // Ensure ID is provided
        if (!system_product_id) {
            flash_message("Please enter an Inventory ID");
            return;
        }
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/inventory/${system_product_id}`,  // Use the system-generated ID in the URL
            contentType: "application/json",
            data: ''
        });

        ajax.done(function (res) {
            update_form_data(res);  // Populate the form with the retrieved data
            flash_message("Success");
        });

        ajax.fail(function (res) {
            clear_form_data();  // Clear the form if the retrieve operation fails
            flash_message(res.responseJSON.message);
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let product_id = $("#system_product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/inventory/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Inventory item has been Deleted!")
        });

        ajax.fail(function (res) {
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

    $("#search-btn").click(function () {
        let name = $("#product_name").val();
        let condition = $("#product_condition").val();

        let queryString = "";

        if (name) {
            queryString += `name=${name}`;
        }
        if (condition) {
            if (queryString.length > 0) {
                queryString += `&condition=${condition}`;
            } else {
                queryString += `condition=${condition}`;
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/inventory?${queryString}`,
            dataType: "json"
        });

        ajax.done(function (res) {
            $("#search_results").empty();
            if (res.length === 0) {
                flash_message("No items found");
                return;
            }

            let table = '<table class="table table-bordered"><thead><tr>';
            table += '<th>ID</th><th>Name</th><th>Description</th><th>Quantity</th><th>Price</th><th>Product ID</th><th>Restock Level</th><th>Condition</th>';
            table += '</tr></thead><tbody>';

            let matchedItem = null;
            for (let i = 0; i < res.length; i++) {
                let item = res[i];
                table += `<tr id="row_${item.id}"><td>${item.id}</td><td>${item.name}</td><td>${item.description}</td><td>${item.quantity}</td><td>${item.price}</td><td>${item.product_id}</td><td>${item.restock_level}</td><td>${item.condition}</td></tr>`;
                if (item.name === name) {
                    matchedItem = item;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // Automatically fill in the form with the matched item
            if (matchedItem) {
                update_form_data(matchedItem);
            } else {
                flash_message("No exact match found for the search criteria");
            }

            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Decrement a Product's Quantity
    // ****************************************

    $("#decrement-btn").click(function () {

        let product_id = $("#system_product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/api/inventory/${product_id}/decrement`,
            contentType: "application/json",
            data: ''
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
    // Archive an Inventory Item
    // ****************************************
    $("#archive-btn").click(function () {

        let inventory_id = $("#system_product_id").val();
        console.log("Archiving item with ID:", inventory_id);


        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/api/inventory/${inventory_id}/archive`,
            contentType: "application/json",
            data: ''
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
    // List All Inventory Items
    // ****************************************
    $("#list-all-btn").click(function () {
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/inventory`,
            dataType: "json"
        });

        ajax.done(function (res) {
            $("#search_results").empty();
            if (res.length === 0) {
                flash_message("No items found");
                return;
            }
            let table = '<table class="table table-bordered"><thead><tr>';
            table += '<th>ID</th><th>Name</th><th>Description</th><th>Quantity</th><th>Price</th><th>Product ID</th><th>Restock Level</th><th>Condition</th>';
            table += '</tr></thead><tbody>';
            for (let i = 0; i < res.length; i++) {
                let item = res[i];
                table += `<tr id="row_${item.id}"><td>${item.id}</td><td>${item.name}</td><td>${item.description}</td><td>${item.quantity}</td><td>${item.price}</td><td>${item.product_id}</td><td>${item.restock_level}</td><td>${item.condition}</td></tr>`;
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });

})
