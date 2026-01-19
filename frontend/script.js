document.getElementById("predictForm").addEventListener("submit", async function(e) {
    e.preventDefault();  // stop page reload

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

        const result = await res.json();
        console.log("Received:", result);

        document.getElementById("result").innerHTML =
            result.prediction === 1
            ? `⚠ High Risk of Diabetes (${(result.probability_diabetes * 100).toFixed(2)}%)`
            : `✅ Low Risk of Diabetes (${(result.probability_no_diabetes * 100).toFixed(2)}%)`;

    } catch (error) {
        document.getElementById("result").innerHTML = "Error connecting to model API";
        console.error(error);
    }
});
