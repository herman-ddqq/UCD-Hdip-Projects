// Retrieve first Json file using xhttp Request
function loadLaureateJson() {
    var xhttp1 = new XMLHttpRequest();
    xhttp1.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            var laureateData = JSON.parse(this.responseText); 
            
            // Store laureate data globally
            window.laureatesData = laureateData.laureates; 

            laureate(laureateData);

            // Load the second JSON file
            loadPrizeJson();
        }
    };
    xhttp1.open("GET", "laureate.json", true);
    xhttp1.send();
}

// Retrieve second Json file using xhttp Request
function loadPrizeJson() {
    var xhttp2 = new XMLHttpRequest();
    xhttp2.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            var prizeData = JSON.parse(this.responseText);
            
            // Store prize data globally
            window.prizesData = prizeData.prizes; 
        }
    };
    xhttp2.open("GET", "prize.json", true);
    xhttp2.send();
}

// Ensure both Json files have been loaded and ready to manipulate
document.addEventListener("DOMContentLoaded", function() {
    loadLaureateJson();
    loadPrizeJson();
});

// Change countries where their names have since changed
function normaliseCountry(country) {
    const normalisedCountries = {
        "Austria-Hungary (now Poland)": "Poland",
        "Austria-Hungary (now Austria)": "Austria",
        "Austria-Hungary (now Bosnia and Herzegovina)": "Bosnia and Herzegovina",
        "Austria-Hungary (now Croatia)": "Croatia",
        "Austria-Hungary (now Czech Republic)": "Czech Republic",
        "Austria-Hungary (now Hungary)": "Hungary",
        "Austria-Hungary (now Slovenia)": "Slovenia",
        "Austria-Hungary (now Ukraine)": "Ukraine",
        "Austrian Empire (now Austria)": "Austria",
        "Austrian Empire (now Czech Republic)": "Czech Republic",
        "Austrian Empire (now Italy)": "Italy",
        "Bavaria (now Germany)": "Germany",
        "Belgian Congo (now Democratic Republic of the Congo)": "Democratic Republic of the Congo",
        "Bosnia (now Bosnia and Herzegovina)": "Bosnia and Herzegovina",
        "British India (now Bangladesh)": "Bangladesh",
        "British India (now India)": "India",
        "British Mandate of Palestine (now Israel)": "Israel",
        "British Protectorate of Palestine (now Israel)": "Israel",
        "British West Indies (now Saint Lucia)": "Saint Lucia",
        "Burma (now Myanmar)": "Myanmar",
        "Crete (now Greece)": "Greece",
        "Czechoslovakia (now Czech Republic)": "Czech Republic",
        "East Friesland (now Germany)": "Germany",
        "East Timor": "Timor-Leste",
        "Free City of Danzig (now Poland)": "Poland",
        "French Algeria (now Algeria)": "Algeria",
        "French protectorate of Tunisia (now Tunisia)": "Tunisia",
        "German-occupied Poland (now Poland)": "Poland",
        "Germany (now France)": "France",
        "Germany (now Poland)": "Poland",
        "Germany (now Russia)": "Russia",
        "Gold Coast (now Ghana)": "Ghana",
        "Hesse-Kassel (now Germany)": "Germany",
        "Hungary (now Slovakia)": "Slovakia",
        "Java, Dutch East Indies (now Indonesia)": "Indonesia",
        "Korea (now South Korea)": "South Korea",
        "Ottoman Empire (now North Macedonia)": "North Macedonia",
        "Ottoman Empire (now Turkey)": "Turkey",
        "Persia (now Iran)": "Iran",
        "Poland (now Belarus)": "Belarus",
        "Poland (now Lithuania)": "Lithuania",
        "Poland (now Ukraine)": "Ukraine",
        "Prussia (now Germany)": "Germany",
        "Prussia (now Poland)": "Poland",
        "Prussia (now Russia)": "Russia",
        "Romania": "Romania",
        "Russian Empire (now Azerbaijan)": "Azerbaijan",
        "Russian Empire (now Belarus)": "Belarus",
        "Russian Empire (now Finland)": "Finland",
        "Russian Empire (now Latvia)": "Latvia",
        "Russian Empire (now Lithuania)": "Lithuania",
        "Russian Empire (now Poland)": "Poland",
        "Russian Empire (now Russia)": "Russia",
        "Russian Empire (now Ukraine)": "Ukraine",
        "Schleswig (now Germany)": "Germany",
        "Southern Rhodesia (now Zimbabwe)": "Zimbabwe",
        "Tibet (now China)": "China",
        "USSR (now Belarus)": "Belarus",
        "USSR (now Russia)": "Russia",
        "West Germany (now Germany)": "Germany",
        "East Germany (now Germany)": "Germany",
        "Württemberg (now Germany)": "Germany"
    };
    
    // Return all modern country names 
    return normalisedCountries[country] || country; 
}

// Organise laureates in categories
function laureate(laureateData) {
    var categories = {};
    const displayLimit = 6;

    laureateData.laureates.forEach(function(laureate) {
        if (!laureate.bornCountry) return;
        
        const country = normaliseCountry(laureate.bornCountry);

        laureate.prizes.forEach(function(prize) {
            var category = prize.category;
            categories[category] = categories[category] || {};
            categories[category][country] = (categories[category][country] || 0) + 1;
        });
    });

    // Structure categories section
    var sortCategories = Object.entries(categories)
        .slice(0, displayLimit)
        .map(function([category, countryData]) {
            var topCountries = Object.entries(countryData)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([country, count]) => {
                    return `
                        <li>${country} (${count} prizes)</li>
                        <div>
                            <button onclick="showLaureates('${category}', '${country}')">Show Laureates</button>
                        </div>
                    `;
                })
                .join("");

            return `<div class="category-item">
                        <h3>Top 5 in ${capitalise(category)}</h3>
                        <ol>${topCountries}</ol>
                    </div>`;
        })
        .join(""); 
    
    document.getElementById("categories").innerHTML = `<div class="category-group">${sortCategories}</div>`;
}

// Organise show Laureates section
function showLaureates(category, country) {
    if (!window.laureatesData) {
        console.error("Laureate data is not loaded yet.");
        return;
    }
    document.getElementById("tableTitle").innerText = `Laureates for ${category} in ${country}`;
    document.getElementById("laureatesSection").style.display = "block";

    var laureatesBody = document.getElementById("laureatesBody");
    laureatesBody.innerHTML = ""; 

            const laureates = window.laureatesData
                .filter(laureate => 
                    laureate.bornCountry === country &&
                    laureate.prizes.some(prize => prize.category === category)
                )
                .map(laureate => {
                    const prize = laureate.prizes.find(prize => prize.category === category);
                    return `
                        <tr>
                            <td>${laureate.id}</td>
                            <td>${laureate.firstname}, ${laureate.surname || ""}</td>
                            <td>${prize.year}</td>
                            <td>${category}</td>
                            <td><button onclick="showDetails('${laureate.id}')">Show Details</button></td>
                        </tr>
                    `;
                })
                .join("");

            laureatesBody.innerHTML = laureates;

            // Automatically scroll to the laureates section
            document.getElementById("laureatesSection").scrollIntoView({
                behavior: "smooth", 
                block: "start"     
            });
    }

// Defined the function formatPrizeDescription outside of the loop to avoid mistake of re-declaring it within the loop
function formatPrizeDescription(prize, laureateData) {
    const year = prize.year;
    const ageAtPrize = parseInt(year) - parseInt(laureateData.born.split("-")[0]);

    // Remove quotes around motivation and any extra "for"
    const motivation = decodeHtmlEntities(prize.motivation.replace(/^"|"$/g, '').replace(/^for\s+/i, ''));

    return `in ${year}, at the age of ${ageAtPrize}, for ${motivation}`;
}

function showDetails(id) {
    if (!window.prizesData || !window.laureatesData) {
        console.error("Data not loaded yet.");
        return;
    }

    // Find laureate by ID
    const laureateData = window.laureatesData.find(laureate => laureate.id === String(id));
    if (!laureateData) {
        console.error("Laureate not found for ID:", id);
        return;
    }

    // Create biography text
    let biographyText = `${laureateData.firstname} ${laureateData.surname} received`;

    // Group prizes by category and check if there are multiple prizes in the same category
    const prizesByCategory = {};
    laureateData.prizes.forEach(prize => {
        if (!prizesByCategory[prize.category]) {
            prizesByCategory[prize.category] = [];
        }
        prizesByCategory[prize.category].push(prize);
    });

    // Iterate over each category and format text accordingly
    const categoryTexts = [];
    for (const [category, prizes] of Object.entries(prizesByCategory)) {
        if (prizes.length > 1) {
            // Multiple prizes in the same category
            const prizeDescriptions = prizes.map(prize => formatPrizeDescription(prize, laureateData)).join(" and ");
            categoryTexts.push(`"${laureateData.firstname} ${laureateData.surname} received two Nobel Prizes in ${category}: ${prizeDescriptions}."`);
            
        } else {
            // Single prize in this category
            const prize = prizes[0];
            const year = prize.year;
            const ageAtPrize = parseInt(year) - parseInt(laureateData.born.split("-")[0]);
            
            // Remove quotes around motivation and any extra "for"
            const motivation = decodeHtmlEntities(prize.motivation.replace(/^"|"$/g, '').replace(/^for\s+/i, ''));

            categoryTexts.push(`"In ${year}, at the age of ${ageAtPrize}, ${laureateData.surname} received the Nobel Prize in ${category} for ${motivation}."`);
        }
    }

    // Join all category descriptions into the biography text
    biographyText = categoryTexts.join(" ");

    // Display the biography text in the modal and show the modal
    const modal = document.getElementById("detailsModal");
    document.getElementById("modalbiographyText").innerText = biographyText;
    modal.style.display = "flex";

    // Close modal when clicking outside the content
    modal.addEventListener("click", function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });
}

// Function to decode text obtained from JSON so it displays in a readable format; used textarea method for that.
function decodeHtmlEntities(text) {
    var textarea = document.createElement("textarea");
    textarea.innerHTML = text;
    let decodedText = textarea.value;
    
    // This is to replace where are <I> and </I> tags with single quotes
    decodedText = decodedText.replace(/<I>/gi, "'").replace(/<\/I>/gi, "'");

    // If there are any comma before single quote, move it so it comes after the quote
    decodedText = decodedText.replace(/,(\s*)'/g, "'$1,");
    
    // Add single quotes around titles if not already quoted; Matches capitalized words following phrases like 'novel', 'work', etc.
    decodedText = decodedText.replace(/(novel|work|play|poem|book|opera)\s([A-Z][\w\s]*\b)(?!')/g, "$1 '$2'");
    
    // If there's a quote-comma (' ,), it's corrected to comma-quote (, ')
    decodedText = decodedText.replace(/' ,/g, ", '");
    
    return decodedText;
}

// Ensure modal closes
function closeModal() {
    const modal = document.getElementById("detailsModal");
    modal.style.display = "none";

    // prevent multiple triggers on reopen
    modal.removeEventListener("click", closeModal);
}

// Global variables for sorting
let currentSortColumn = '';
let isAscending = true;

// Sort laureates
function sortLaureates(column, buttonElement) {
    // for the same colum
    if (currentSortColumn === column) {
        isAscending = !isAscending;
    } else {
        currentSortColumn = column;
        isAscending = true;
    }

    // Update button icons for sorting direction
    updateButtonIcons(buttonElement);

    // Get all table rows in the laureatesBody
    const rows = Array.from(document.querySelectorAll('#laureatesBody tr'));

    // Sort laureates by surname
    rows.sort((a, b) => {
        let aText, bText;

        // Get the correct text to compare based on the column
        if (column === 'name') {
            // Split laureate's name into first and last name
            const aFullName = a.querySelector('td:nth-child(2)').innerText.trim(); 
            const bFullName = b.querySelector('td:nth-child(2)').innerText.trim(); 

            const aParts = aFullName.split(' ');
            const bParts = bFullName.split(' ');

            // Use the last part (assumed to be the surname) for sorting
            const aSurname = aParts[aParts.length - 1] || "UNKNOWN"; // If no surname is found
            const bSurname = bParts[bParts.length - 1] || "UNKNOWN"; // If no surname is found

            aText = aSurname;
            bText = bSurname;
        } else {
            // For other columns, get the text content
            aText = a.querySelector(`td:nth-child(${sortcolumn(column)})`).innerText.trim();
            bText = b.querySelector(`td:nth-child(${sortcolumn(column)})`).innerText.trim();
        }

        // Compare the text 
        let compareResult;
        if (column === 'id' || column === 'year') {
            // Parse as numbers if sorting by id or year
            compareResult = parseInt(aText) - parseInt(bText);
        } else {
            // Otherwise, use localeCompare for string columns
            compareResult = aText.localeCompare(bText);
        }

        // Return the comparison result based on the sorting direction
        return isAscending ? compareResult : -compareResult;
    });

    // Update sorted rows in the table
    const laureatesBody = document.getElementById("laureatesBody");
    laureatesBody.innerHTML = ''; // Clear current rows
    rows.forEach(row => laureatesBody.appendChild(row)); // Append sorted rows back into the body
}

// Capitalise  the category names when displaying the laureates’ data
function capitalise(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Return sorted columns
function sortcolumn(column) {
    switch (column) {
        case 'id': return 1;
        case 'name': return 2;
        case 'year': return 3;
        case 'category': return 4;
        default: return 1;
    }
}

// Function to update button icons based on sort order
function updateButtonIcons(buttonElement) {
    // Reset all arrow icons
    document.querySelectorAll('th button').forEach(button => {
        button.textContent = '▲▼'; // Default icon for both directions
    });

    // Set the icon of the current button based on sort order
    buttonElement.textContent = isAscending ? '▲' : '▼'; // ▲ for ascending, ▼ for descending
}