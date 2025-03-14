async function fetchTransactions() {
        const phone = document.getElementById("phoneNumber").value.trim();

        if (!phone) {
            alert("Please enter your phone number");
            return;
        }

        const apiUrl = `http://127.0.0.1:5000/transactions?user_id=${phone}`;

        try {
            const response = await fetch(apiUrl);
            const data = await response.json();

            const transactionsDiv = document.getElementById("transactions");
            transactionsDiv.innerHTML = ""; // Clear previous data

            if (response.status === 404 || data.length === 0) {
                transactionsDiv.innerHTML = "<p>No transactions found.</p>";
                return;
            }

            if (response.ok) {
                let table = `<table>
                                <tr>
                                    <th>Date</th>
                                    <th>Item</th>
                                    <th>Quantity</th>
                                    <th>Amount</th>
                                </tr>`;

                data.forEach(record => {
                    const fields = record.fields;
                    if (fields.user_id === phone) {  // Ensure it matches the entered phone
                        table += `<tr>
                                    <td>${fields.Date || "N/A"}</td>
                                    <td>${fields.Item || "N/A"}</td>
                                    <td>${fields.Quantity || "N/A"}</td>
                                    <td>${fields.Amount || "N/A"}</td>
                                  </tr>`;
                    }
                });

                table += `</table>`;
                transactionsDiv.innerHTML = table;
            } else {
                transactionsDiv.innerHTML = `<p>Error fetching transactions</p>`;
            }

        } catch (error) {
            console.error("Error fetching transactions:", error);
            document.getElementById("transactions").innerHTML = "<p>Failed to fetch transactions.</p>";
        }
    }

