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

function transl(id) {
  let review = document.getElementById(id);
  let reviewText = document.getElementById(id + "-text");
  if (id.includes("2")) {
    if (review.innerHTML == review_2_ING) {
      review.innerHTML = review_2_IT;
      reviewText.innerHTML = "Tradotto dall'inglese";
    } else {
      review.innerHTML = review_2_ING;
      reviewText.innerHTML = "Traduci";
    }
  } else {
    if (review.innerHTML == review_1_ING) {
      review.innerHTML = review_1_IT;
      reviewText.innerHTML = "Tradotto dall'inglese";
    } else {
      review.innerHTML = review_1_ING;
      reviewText.innerHTML = "Traduci";
    }
  }
  
}

const blue = "#55bbe7";
const red = "#3ca660";
const textColor = "white";
chart();

var review_1_ING = "“This app is very useful, I'd like to buy your company... Tell me how much”";
var review_1_IT = "“Questa app è molto utile, vorrei acquistare la vostra azienda... Ditemi quanto”";
var review_2_ING = "“Work for me. Together we'll make billions”";
var review_2_IT = "“Lavorate per me. Insieme faremo miliardi”";

const vh = window.innerHeight / 100;
const reviewsSection = document.querySelector("section:has(#container-reviews)");
let opened = false;
// console.log(reviewsSection, reviewsSection.offsetTop);
window.onscroll = () => {
  const scroll = document.documentElement.scrollTop || document.body.scrollTop;
  if (scroll > reviewsSection.offsetTop - 25 * vh && !opened) {
    opened = true;
    openReviews();
  }
}