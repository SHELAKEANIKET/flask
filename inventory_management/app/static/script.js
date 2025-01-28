document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebarCollapse");
  const sidebarClose = document.getElementById("sidebarClose");
  
  // Toggle sidebar
  sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("active");
  });
  
  // Close sidebar when clicking the close button
  sidebarClose.addEventListener("click", () => {
    sidebar.classList.remove("active");
  });

  //! products alter
  const allProductsTable = document.querySelector("#allProductsTable tbody");
  const lowStockTable = document.querySelector("#lowStockTable tbody");

  // Get all rows from the all-products table
  const rows = allProductsTable?.querySelectorAll("tr");
  let lowStockCounter = 1;

  rows?.forEach((row) => {
    // Get available stock and threshold stock
    const availableStock = parseInt(row.dataset.stock, 10);
    const minStockAlert = parseInt(row.dataset.threshold, 10);

    // If available stock is less than the minimum stock alert
    if (availableStock < minStockAlert) {
      // Clone the row to avoid removing it from the original table
      const clonedRow = row.cloneNode(true);

      // Update Sr. No for low stock table
      clonedRow.cells[0].innerText = lowStockCounter++;

      // Append the cloned row to the low-stock table
      lowStockTable.appendChild(clonedRow);

      // Optionally: Remove the original row from the all-products table
      row.remove();
    }
  });

  //* Fetch the types for product dropdown (in Add Product form)
  const typesDropdown = document.getElementById("typeDropdown");
  if (typesDropdown) {
    fetch("/types/get_types")
      .then((response) => response.json())
      .then((types) => {
        // console.log(types);

        typesDropdown.innerHTML = '<option value="">Select Type</option>';
        types.forEach((type) => {
          typesDropdown.innerHTML += `
            <option value="${type.type_id}">${type.type_name}</option>
          `;
        });
      })
      .catch((error) => {
        console.error("Error fetching types:", error);
        typesDropdown.innerHTML =
          '<option value="">Failed to load types</option>';
      });
  }

  //* Fetch and populate customers in Add Sale form
  const customerDropdown = document.getElementById("customerDropdown");
  if (customerDropdown) {
    fetch("/customers/get_customers")
      .then((response) => response.json())
      .then((customers) => {
        // console.log("customers",customers);

        customerDropdown.innerHTML =
          '<option value="">Select Customer</option>';
        customers.forEach((customer) => {
          customerDropdown.innerHTML += `
                        <option value="${customer.customer_id}">${customer.name}</option>
                    `;
        });
      })
      .catch((error) => {
        console.error("Error fetching customers:", error);
        customerDropdown.innerHTML =
          '<option value="">Failed to load customers</option>';
      });
  }

  //* Fetch and populate suppliers in Add Purchase form
  const supplierDropdown = document.getElementById("supplierDropdown");
  if (supplierDropdown) {
    fetch("/suppliers/get_suppliers")
      .then((response) => response.json())
      .then((suppliers) => {
        // console.log("suppliers", suppliers);

        supplierDropdown.innerHTML =
          '<option value="">Select Supplier</option>';
        suppliers.forEach((supplier) => {
          supplierDropdown.innerHTML += `
                        <option value="${supplier.supplier_id}">${supplier.name}</option>
                    `;
        });
      })
      .catch((error) => {
        console.error("Error fetching suppliers:", error);
        supplierDropdown.innerHTML =
          '<option value="">Failed to load suppliers</option>';
      });
  }

  //! Add rows for the purchase form
  const addRowButton = document.getElementById("addRow");
  const productsContainer = document.getElementById("productsContainer");

  if (addRowButton && productsContainer) {
    addRowButton.addEventListener("click", async function () {
      const newRow = document.createElement("div");
      newRow.classList.add("row", "mb-3");

      try {
        // Fetch the products data dynamically
        const response = await fetch("/products/get_products");
        const products = await response.json();

        // Generate options for the dropdown
        const productOptions = products
          .map(
            (product) =>
              `<option value="${product.name}" data-product-id="${product.product_id}" data-type-id="${product.type_id}">${product.name}</option>`
          )
          .join("");

        // Add the new row with fetched data
        newRow.innerHTML = `
            <div class="col">
              <select class="form-control product-name-dropdown" name="product_names[]" required>
                <option value="">Select Product</option>
                ${productOptions}
              </select>
            </div>
            <div class="col">
              <select class="form-control product-type-dropdown" name="product_types[]" required disabled>
                <option value="">Product Type</option>
              </select>
            </div>
            <div class="col">
              <input type="hidden" class="product-id" name="product_ids[]" />
              <input type="hidden" class="type-id" name="type_ids[]" />
              <input type="number" class="form-control" name="purchase_price[]" placeholder="Purchase Price" required>
            </div>
            <div class="col">
              <input type="number" class="form-control" name="quantity[]" placeholder="Quantity" required>
            </div>
            <div class="col">
              <input type="number" class="form-control" name="weight[]" placeholder="Weight">
            </div>
            <div class="col">
              <button type="button" class="btn btn-danger remove-row">Remove</button>
            </div>
          `;

        productsContainer.appendChild(newRow);

        newRow
          .querySelector(".product-name-dropdown")
          .addEventListener("change", function () {
            const selectedOption = this.options[this.selectedIndex];
            const productId = selectedOption.getAttribute("data-product-id");
            const typeId = selectedOption.getAttribute("data-type-id");

            const row = this.closest(".row");

            // Debugging outputs
            // console.log("Product ID:", productId);
            // console.log("Type ID in new row:", typeId);
            // console.log("Row:", row);

            // Update hidden fields for the current row
            row.querySelector(".product-id").value = productId || "";
            row.querySelector(".type-id").value = typeId || "";
          });

        // Attach the remove-row event
        newRow
          .querySelector(".remove-row")
          .addEventListener("click", function () {
            newRow.remove();
          });
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    });
  }

  //! Add rows for the sale form
  const addSaleRowButton = document.getElementById("addSaleRow");
  const saleProductsContainer = document.getElementById(
    "saleProductsContainer"
  );

  if (addSaleRowButton && saleProductsContainer) {
    addSaleRowButton.addEventListener("click", async function () {
      const newRow = document.createElement("div");
      newRow.classList.add("row", "mb-3");

      try {
        // Fetch the products data dynamically
        const response = await fetch("/products/get_products");
        const products = await response.json();

        // Generate options for the dropdown
        const productOptions = products
          .map(
            (product) =>
              `<option value="${product.name}" data-product-id="${product.product_id}" data-type-id="${product.type_id}">${product.name}</option>`
          )
          .join("");

        newRow.innerHTML = `
        <div class="col">
          <select class="form-control product-name-dropdown" name="product_names[]" required>
            <option value="">Select Product</option>
            ${productOptions}
          </select>
        </div>
        <div class="col">
          <select class="form-control product-type-dropdown" name="product_types[]" required disabled>
            <option value="">Product Type</option>
          </select>
        </div>
        <div class="col">
          <input type="hidden" class="product-id" name="product_ids[]" />
          <input type="hidden" class="type-id" name="type_ids[]" />
          <input type="number" class="form-control" name="sale_price[]" placeholder="Sale Price" required>
        </div>
        <div class="col">
          <input type="number" class="form-control" name="quantity[]" placeholder="Quantity" required>
        </div>
        <div class="col">
          <input type="number" class="form-control" name="weight[]" placeholder="Weight">
        </div>
        <div class="col">
          <button type="button" class="btn btn-danger remove-row">Remove</button>
        </div>
      `;

        saleProductsContainer.appendChild(newRow);

        newRow
          .querySelector(".product-name-dropdown")
          .addEventListener("change", function () {
            const selectedOption = this.options[this.selectedIndex];
            const productId = selectedOption.getAttribute("data-product-id");
            const typeId = selectedOption.getAttribute("data-type-id");

            const row = this.closest(".row");

            // Debugging outputs
            // console.log("Product ID:", productId);
            // console.log("Type ID in new row:", typeId);
            // console.log("Row:", row);

            // Update hidden fields for the current row
            row.querySelector(".product-id").value = productId || "";
            row.querySelector(".type-id").value = typeId || "";
          });

        // Attach remove-row event
        newRow
          .querySelector(".remove-row")
          .addEventListener("click", function () {
            newRow.remove();
          });
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    });
  }

  //* Fetch product details when product name is selected
  document.body.addEventListener("change", function (e) {
    if (e.target.classList.contains("product-name-dropdown")) {
      const productName = e.target.value;
      const productTypeDropdown = e.target
        .closest(".row")
        .querySelector(".product-type-dropdown");

      if (productName) {
        fetch("/products/get_product_details", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ product_name: productName }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.type_name) {
              // Populate the product type dropdown
              productTypeDropdown.innerHTML = `
              <option value="${data.type_id}">${data.type_name}</option>
              `;
              productTypeDropdown.disabled = false; // Enable the dropdown
            } else {
              productTypeDropdown.innerHTML =
                '<option value="">Product type not found</option>';
              productTypeDropdown.disabled = true;
            }
          })
          .catch((error) => {
            console.error("Error fetching product details:", error);
            productTypeDropdown.innerHTML =
              '<option value="">Error fetching product type</option>';
            productTypeDropdown.disabled = true;
          });
      } else {
        // Reset product type dropdown if no product is selected
        productTypeDropdown.innerHTML =
          '<option value="">Select Product Type</option>';
        productTypeDropdown.disabled = true;
      }
    }
  });

  //* update hidden fields in the purchase and sale form
  document
    .querySelectorAll(".product-name-dropdown")
    .forEach(function (dropdown) {
      dropdown.addEventListener("change", function () {
        const selectedOption = this.options[this.selectedIndex];
        const productId = selectedOption.getAttribute("data-product-id");
        const typeId = selectedOption.getAttribute("data-type-id");

        const row = this.closest(".row");
        const productIdField = row.querySelector(".product-id");
        const typeIdField = row.querySelector(".type-id");

        // console.log("Product ID:", productId);
        // console.log("Type ID in separate func:", typeId);
        // console.log("Row:", row);

        if (productIdField) productIdField.value = productId;
        if (typeIdField) typeIdField.value = typeId;
      });
    });

  //* validation for purchase form
  document
    .getElementById("purchaseForm")
    ?.addEventListener("submit", function (event) {
      const rows = document.querySelectorAll("#productsContainer .row");
      let valid = true;

      rows.forEach((row) => {
        const productId = row.querySelector(".product-id").value.trim();
        const typeId = row.querySelector(".type-id").value.trim();
        const purchasePrice = row
          .querySelector('input[name="purchase_price[]"]')
          .value.trim();
        const quantity = row
          .querySelector('input[name="quantity[]"]')
          .value.trim();
        const weight = row.querySelector('input[name="weight[]"]').value.trim();

        if (!productId || !typeId || !purchasePrice || !quantity || !weight) {
          valid = false;
          alert("Please fill out all fields in each row.");
        }
      });

      if (!valid) {
        event.preventDefault(); // Prevent form submission if validation fails
      }
    });

  //* validation for sale form
  document
    .getElementById("saleForm")
    ?.addEventListener("submit", function (event) {
      const rows = document.querySelectorAll("#productsContainer .row");
      let valid = true;

      rows.forEach((row) => {
        const productId = row.querySelector(".product-id").value.trim();
        const typeId = row.querySelector(".type-id").value.trim();
        const salePrice = row
          .querySelector('input[name="sale_price[]"]')
          .value.trim();
        const quantity = row
          .querySelector('input[name="quantity[]"]')
          .value.trim();
        const weight = row.querySelector('input[name="weight[]"]').value.trim();

        if (!productId || !typeId || !salePrice || !quantity || !weight) {
          valid = false;
          alert("Please fill out all fields in each row.");
        }
      });

      if (!valid) {
        event.preventDefault(); // Prevent form submission if validation fails
      }
    });

  //* modal for add new product
  document.addEventListener("DOMContentLoaded", () => {
    // Initialize the modal
    const addProductModal = new bootstrap.Modal(
      document.getElementById("addProductModal")
    );

    // Add event listener for the form submission
    document
      .getElementById("addProductForm")
      .addEventListener("submit", (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const jsonData = Object.fromEntries(formData);

        fetch("/products/add", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(jsonData),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              alert("Product added successfully!");
              addProductModal.hide();
              location.reload(); // Optional: Reload to show updated data
            } else {
              alert("Error adding product: " + data.error);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      });
  });
});

//* chart js
// const ctx = document.getElementById("myChart");
// const labels = [
//   "January",
//   "February",
//   "March",
//   "April",
//   "May",
//   "June",
//   "July",
//   "August",
//   "September",
//   "October",
//   "November",
//   "December",
// ];

// new Chart(ctx, {
//   type: "bar",
//   data: {
//     labels: labels,
//     datasets: [
//       {
//         label: "Sales",
//         data: [12, 19, 3, 5, 2, 3, 23, 23, 2, 2, 2, 4],
//         borderWidth: 1,
//       },
//     ],
//   },
//   options: {
//     scales: {
//       y: {
//         beginAtZero: true,
//       },
//     },
//   },
// });
