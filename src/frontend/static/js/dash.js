document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("skillsChart").getContext("2d");
  const barCtx = document.getElementById("barChart").getContext("2d");

  const matchedSkills = window.chartData.matchedSkills;
  const missingSkills = window.chartData.missingSkills;
  const totalSkills = matchedSkills + missingSkills;

  const matchedPercentage = ((matchedSkills / totalSkills) * 100).toFixed(1);
  const missingPercentage = ((missingSkills / totalSkills) * 100).toFixed(1);

  // Doughnut chart (Pie chart)
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Matched Skills", "Missing Skills"],
      datasets: [
        {
          data: [matchedSkills, missingSkills],
          backgroundColor: [
            "rgba(34, 197, 94, 0.8)", // green
            "rgba(239, 68, 68, 0.8)", // red
          ],
          borderColor: ["rgba(34, 197, 94, 1)", "rgba(239, 68, 68, 1)"],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.label || "";
              const value = context.parsed || 0;
              const percentage = ((value / totalSkills) * 100).toFixed(1);
              return `${label}: ${value} (${percentage}%)`;
            },
          },
        },
      },
    },
  });

  // Bar chart
  new Chart(barCtx, {
    type: "bar",
    data: {
      labels: ["Matched Skills", "Missing Skills"],
      datasets: [
        {
          label: "Skills",
          data: [matchedSkills, missingSkills],
          backgroundColor: [
            "rgba(34, 197, 94, 0.8)", // green
            "rgba(239, 68, 68, 0.8)", // red
          ],
          borderColor: ["rgba(34, 197, 94, 1)", "rgba(239, 68, 68, 1)"],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const value = context.raw;
              const percentage = ((value / totalSkills) * 100).toFixed(1);
              return `${value} (${percentage}%)`;
            },
          },
        },
      },
    },
  });
});
