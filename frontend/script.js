async function predict() {
    const values = document.querySelectorAll("input");

    const data = {
        Pregnancies: values[0].value,
        Glucose: values[1].value,
        BloodPressure: values[2].value,
        SkinThickness: values[3].value,
        Insulin: values[4].value,
        BMI: values[5].value,
        DiabetesPedigreeFunction: values[6].value,
        Age: values[7].value
    };

    console.log("Sending:", data);

    const res = await fetch("https://diamodel.onrender.com/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    console.log("Received:", result);

    document.getElementById("output").innerHTML =
        result.prediction === 1
            ? `⚠ High Risk (${(result.probability_diabetes*100).toFixed(2)}%)`
            : `✅ Low Risk (${(result.probability_no_diabetes*100).toFixed(2)}%)`;
}
