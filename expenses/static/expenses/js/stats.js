const chartData = (labels, data) => {
  const ctx = document.getElementById("myChart").getContext("2d");
  const myChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          label: "# of Votes",
          data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
    title: {
      display: true,
      text: "Expenses per category",
    },
  });
};

const getChartData = () => {
  $.ajax({
    type: "GET",
    url: `${window.location.origin}/expenses-summary`,
    success: (res) => {
      const [labels, data] = [Object.keys(res), Object.values(res)];
      chartData(labels, data);
    },
    error: (err) => {
      console.log(err);
    },
  });
};

window.onload = getChartData();
