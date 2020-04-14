try {

  Apex.tooltip = {
    theme: 'dark'
  }



var options = {
          
          chart: {
          fontFamily: 'Nunito, sans-serif',
          height: 365,
          type: 'area',
          zoom: {
              enabled: true
          },
          dropShadow: {
            enabled: true,
            opacity: 0.3,
            blur: 5,
            left: -7,
            top: 22
          },
          toolbar: {
            show: true
          },
        },

        colors: ['#f2ef41', '#e7515a'],

        dataLabels: {
          enabled: false
        },

        markers: {
          discrete: [{
          seriesIndex: 0,
          dataPointIndex: 7,
          fillColor: '#000',
          strokeColor: '#000',
          size: 5
        }, {
          seriesIndex: 2,
          dataPointIndex: 11,
          fillColor: '#000',
          strokeColor: '#000',
          size: 4
        }]
        },
  
        stroke: {
            show: true,
            curve: 'smooth',
            width: 2,
            lineCap: 'square'
        },

        series: [{
                name: 'Sales',
                data: Object.values(totalSales)
              }],

        xaxis: {
          axisBorder: {
              show: false
            },
            axisTicks: {
              show: false
            },
            crosshairs: {
              show: true
            },
            
          type: 'datetime',
          categories: Object.values(date)
        },

        yaxis: {
            labels: {
              formatter: function(value, index) {
                return (value / 1000) + 'K'
              },
              offsetX: -22,
              offsetY: 0,
              style: {
                  fontSize: '12px',
                  fontFamily: 'Nunito, sans-serif',
                  cssClass: 'apexcharts-yaxis-title',
              },
            }
          },

        grid: {
            borderColor: '#191e3a',
            strokeDashArray: 5,
            xaxis: {
                lines: {
                    show: true
                }
            },   
            yaxis: {
                lines: {
                    show: false,
                }
            },
            padding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: -10
            }, 
          }, 

        legend: {
          position: 'top',
          horizontalAlign: 'right',
          offsetY: -50,
          fontSize: '16px',
          fontFamily: 'Nunito, sans-serif',
          markers: {
            width: 10,
            height: 10,
            strokeWidth: 0,
            strokeColor: '#fff',
            fillColors: undefined,
            radius: 12,
            onClick: undefined,
            offsetX: 0,
            offsetY: 0
          },    
          itemMargin: {
            horizontal: 0,
            vertical: 20
          }
        },

        fill: {
              type:"gradient",
              gradient: {
                  type: "vertical",
                  shadeIntensity: 1,
                  inverseColors: !1,
                  opacityFrom: .28,
                  opacityTo: .05,
                  stops: [45, 100]
              }
          },
    
        tooltip: {
                theme: 'dark',
          marker: {
            show: true,
          },
          x: {
            format: 'yyyy/MM/dd'
          },
        },
          responsive: [{
    breakpoint: 575,
    options: {
      legend: {
          offsetY: -30,
      },
    },
  }]
        };

        var chart = new ApexCharts(document.querySelector("#retailsales"), options);
        chart.render();



} catch(e) {
    console.log(e);
}