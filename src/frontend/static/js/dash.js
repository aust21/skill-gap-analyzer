const ctx = document.getElementById("skillsChart").getContext("2d");

new Chart(ctx, {
  type: "bar",
  data: {
    labels: skills,
    datasets: [
      {
        label: "Market Demand",
        data: demands,
        backgroundColor: "rgba(150, 150, 255, 0.5)",
        borderRadius: 4,
      },
      // {
      //   label: "In Your Resume",
      //   data: [90, 0, 85, 0, 0, 0, 0, 0, 0, 0, 0],
      //   backgroundColor: "#8000ff",
      //   borderRadius: 4,
      // },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: "Market Demand",
        },
      },
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 45,
        },
      },
    },
  },
});
