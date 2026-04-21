async function compareFiles() {
    const text1 = document.getElementById("text1").value;
    const text2 = document.getElementById("text2").value;

    const response = await fetch("/compare", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text1, text2})
    });

    const data = await response.json();

    document.getElementById("results").innerHTML = `
        <p><b>Similarity:</b> ${data.similarity}%</p>
        <p><b>Rabin-Karp Time:</b> ${data.rabin_karp.time} ms</p>
        <p><b>KMP Time:</b> ${data.kmp.time} ms</p>
        <p><b>Better Algorithm:</b> ${data.better}</p>
        <p><b>Matches Found:</b> RK=${data.rabin_karp.matches.length}, KMP=${data.kmp.matches.length}</p>
    `;

    const ctx = document.getElementById("chart").getContext("2d");
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Rabin-Karp', 'KMP'],
            datasets: [{
                label: 'Execution Time (ms)',
                data: [data.rabin_karp.time, data.kmp.time],
                backgroundColor: ['#0078d7', '#ff5733']
            }]
        }
    });
}
