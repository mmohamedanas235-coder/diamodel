document.getElementById("predictForm").addEventListener("submit", async function(e) {
    e.preventDefault(); // stop page reload

    const data = {
        Pregnancies: document.getElementById("Pregnancies").value,
        Glucose: document.getElementById("Glucose").value,
        BloodPressure: document.getElementById("BloodPressure").value,
        SkinThickness: document.getElementById("SkinThickness").value,
        Insulin: document.getElementById("Insulin").value,
        BMI: document.getElementById("BMI").value,
        DiabetesPedigreeFunction: document.getElementById("DiabetesPedigreeFunction").value,
        Age: document.getElementById("Age").value
    };

    console.log("Sending:", data);

    try {
        const res = await fetch("https://diamodel.onrender.com/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        // Log the raw response first
        const text = await res.text();
        console.log("Raw response:", text);

        // Try parsing JSON
        let result;
        try {
            result = JSON.parse(text);
        } catch (parseError) {
            console.error("Failed to parse JSON:", parseError);
            document.getElementById("result").innerHTML = "Invalid response from API";
            return;
        }

        console.log("Parsed result:", result);

        // Display result
        document.getElementById("result").innerHTML =
            result.prediction === 1
            ? `⚠ High Risk of Diabetes (${(result.probability_diabetes * 100).toFixed(2)}%)`
            : `✅ Low Risk of Diabetes (${(result.probability_no_diabetes * 100).toFixed(2)}%)`;

    } catch (error) {
        // Show detailed error in the console
        document.getElementById("result").innerHTML = "Error connecting to model API";
        console.error("Fetch error:", error);
    }
});
