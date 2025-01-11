async function performSearch() {
  const input = document.getElementById("searchInput").value;
  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = ""; // Clear previous results

  if (input) {
    try {
      const response = await fetch(`/api/search?query=${encodeURIComponent(input)}`);
      if (!response.ok) {
        if (response.status === 428) {
          resultsContainer.textContent = "Required data not generated. Fetch the data before searching.";
          return;
        } else if (response.status === 400) {
          resultsContainer.textContent = "No query provided.";
          return;
        } else {
          throw new Error(`Unexpected error: ${response.status}`);
        }
      }

      const data = await response.json();

      if (data && Array.isArray(data)) {

        data.forEach(item => {
          const link = document.createElement("a");
          link.href = item.url;
          link.textContent = item.title;
          link.target = "_blank";

          const description = document.createElement("p");
          description.textContent = item.description;

          const resultDiv = document.createElement("div");
          resultDiv.appendChild(link);
          resultDiv.appendChild(description);

          resultsContainer.appendChild(resultDiv);
        });
        console.log("done/n")
      } else {
        resultsContainer.textContent = "No results found.";
      }
    } catch (error) {
      console.error("Error fetching search results:", error);
      resultsContainer.textContent = "An unexpected error occurred while searching. Please try again.";
    }
  } else {
    alert("Please enter something to search.");
  }
}
