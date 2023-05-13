function openReviews() {

    let r = document.getElementById("container-reviews");
    let b = document.getElementById("showRates");
    r.classList.toggle("open");
    r.classList.toggle("close");
    b.classList.toggle("ruotate");
}

function chart() {
    const data = {
        labels: ['2023', '2024', '2025', '2026', '2027'],
        datasets: [{
          label: 'con WBMaster',
          data: [50, 65, 75, 80, 110],
          fill: false,
          tension: 0.3,
          backgroundColor: blue,
          borderColor: blue,
        }, {
            label: 'Senza WBMaster',
            data: [50, 60, 50, 60, 20],
            fill: false,
            tension: 0.3,
            backgroundColor: red,
            borderColor: red,
          },]
      };
      
      const config = {
        type: 'line',
        data: data,
        options: {
            scales: {
              y: {
                min: 0
              }
            },
            
            plugins: {
                title: {
                  display: true,
                  text: 'Stima entrate economiche annuali in migliaia di €',
                  color: textColor,
                  font: {
                    size: 18,
                    weight: 'normal'
                  }
                },

                legend: {
                    labels: {
                      color: textColor,
                      font: {
                        size: 13
                      }
                    }
                  }
              },
              scales: {
                x: {
                  ticks: {
                    color: textColor,
                    font: {
                        size: 13
                      }
                  },

                },
                y: {
                  min: 0,
                  ticks: {
                    color: textColor,
                    font: {
                        size: 13
                      }
                  },
                }
              },
          }
      };
      
      const myChart = new Chart(
        document.getElementById('myChart'),
        config
      );
}

const blue = "#55bbe7";
const red = "#3ca660";
const textColor = "white";
chart();

