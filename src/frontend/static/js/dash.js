const ctx = document.getElementById("skillsChart").getContext("2d");

new Chart(ctx, {
  type: "bar",
  data: {
    labels: [
      "SQL",
      "Typescript",
      "Python",
      "AWS",
      "Docker",
      "Machine Learning",
      "JavaScript",
      "HTML",
      "CSS",
      "GraphQL",
      "Kubernetes",
    ],
    datasets: [
      {
        label: "Market Demand",
        data: [90, 80, 85, 70, 75, 70, 65, 60, 60, 50, 45],
        backgroundColor: "rgba(150, 150, 255, 0.5)",
        borderRadius: 4,
      },
      {
        label: "In Your Resume",
        data: [90, 0, 85, 0, 0, 0, 0, 0, 0, 0, 0], // Show only the skills you have
        backgroundColor: "#8000ff",
        borderRadius: 4,
      },
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
