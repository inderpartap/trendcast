try {
  Apex.tooltip = {theme : "dark"};

  /*
      ==============================
      |    @Options Charts Script   |
      ==============================
  */
  function sum(obj) {
    var sum = 0;
    for (var el in obj) {
      if (obj.hasOwnProperty(el)) {
        sum += parseFloat(obj[el]);
      }
    }
    return sum;
  }

  var weekday = new Array(7);
  weekday[0] = "Sunday";
  weekday[1] = "Monday";
  weekday[2] = "Tuesday";
  weekday[3] = "Wednesday";
  weekday[4] = "Thursday";
  weekday[5] = "Friday";
  weekday[6] = "Saturday";

  var x;
  var day_name = {...date};
  for (x in date) {
    var d = new Date(date[x]);
    day_name[x] = d.toDateString();
  }
  /*
      =================================
          Retail Sales | Predictions
      =================================
  */
  var options1 = {
    chart : {
      fontFamily : "Nunito, sans-serif",
      height : 365,
      type : "area",
      zoom : {enabled : true},
      dropShadow :
          {enabled : true, opacity : 0.3, blur : 5, left : -7, top : 22},
      toolbar : {show : true},
      events : {
        mounted : function(ctx, config) {
          const highest1 = ctx.getHighestValueInSeries(0);
          const highest2 = ctx.getHighestValueInSeries(1);

          ctx.addPointAnnotation({
            x : new Date(
                    ctx.w.globals
                        .seriesX[0][ctx.w.globals.series[0].indexOf(highest1)])
                    .getTime(),
            y : highest1,
            label : {style : {cssClass : "d-none"}},
            customSVG : {
              SVG :
                  '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="#f2ef41" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="feather feather-circle"><circle cx="12" cy="12" r="10"></circle></svg>',
              cssClass : undefined,
              offsetX : -8,
              offsetY : 5
            }
          });

          ctx.addPointAnnotation({
            x : new Date(
                    ctx.w.globals
                        .seriesX[1][ctx.w.globals.series[1].indexOf(highest2)])
                    .getTime(),
            y : highest2,
            label : {style : {cssClass : "d-none"}},
            customSVG : {
              SVG :
                  '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="#e7515a" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="feather feather-circle"><circle cx="12" cy="12" r="10"></circle></svg>',
              cssClass : undefined,
              offsetX : -8,
              offsetY : 5
            }
          });
        }
      }
    },
    colors : [ "#f2ef41", "#e7515a" ],
    dataLabels : {enabled : false},
    markers : {
      discrete : [
        {
          seriesIndex : 0,
          dataPointIndex : 7,
          fillColor : "#000",
          strokeColor : "#000",
          size : 5
        },
        {
          seriesIndex : 2,
          dataPointIndex : 11,
          fillColor : "#000",
          strokeColor : "#000",
          size : 4
        }
      ]
    },
    subtitle : {
      text : "Sales for the whole week:",
      align : "left",
      margin : 0,
      offsetX : -10,
      offsetY : 35,
      floating : false,
      style : {fontSize : "14px", color : "#888ea8"}
    },
    title : {
      text : "$ " + parseInt(sum(totalSales_weather)),
      align : "left",
      margin : 0,
      offsetX : -10,
      offsetY : 0,
      floating : false,
      style : {fontSize : "25px", color : "#bfc9d4"}
    },
    stroke : {show : true, curve : "smooth", width : 2, lineCap : "square"},
    series : [
      {name : "Sales with weather", data : Object.values(totalSales_weather)},
      {name : "Sales without weather", data : Object.values(totalSales_base)}
    ],
    // labels: Object.values(date),
    xaxis : {
      axisBorder : {show : false},
      axisTicks : {show : false},
      crosshairs : {show : true},
      labels : {
        offsetX : 0,
        offsetY : 5,
        style : {
          fontSize : "12px",
          fontFamily : "Nunito, sans-serif",
          cssClass : "apexcharts-xaxis-title"
        }
      },
      type : "datetime",
      categories : Object.values(date)
    },
    yaxis : {
      labels : {
        formatter : function(value, index) { return "$" + value / 1; },
        offsetX : -22,
        offsetY : 0,
        style : {
          fontSize : "12px",
          fontFamily : "Nunito, sans-serif",
          cssClass : "apexcharts-yaxis-title"
        }
      }
    },
    grid : {
      borderColor : "#191e3a",
      strokeDashArray : 5,
      xaxis : {lines : {show : true}},
      yaxis : {lines : {show : false}},
      padding : {top : 0, right : 0, bottom : 0, left : -10}
    },
    legend : {
      position : "top",
      horizontalAlign : "right",
      offsetY : -50,
      fontSize : "16px",
      fontFamily : "Nunito, sans-serif",
      markers : {
        width : 10,
        height : 10,
        strokeWidth : 0,
        strokeColor : "#fff",
        fillColors : undefined,
        radius : 12,
        onClick : undefined,
        offsetX : 0,
        offsetY : 0
      },
      itemMargin : {horizontal : 0, vertical : 20}
    },
    tooltip : {theme : "dark", marker : {show : true}, x : {show : false}},
    fill : {
      type : "gradient",
      gradient : {
        type : "vertical",
        shadeIntensity : 1,
        inverseColors : !1,
        opacityFrom : 0.28,
        opacityTo : 0.05,
        stops : [ 45, 100 ]
      }
    },
    responsive : [ {breakpoint : 575, options : {legend : {offsetY : -30}}} ]
  };

  /*
      ==================================
          Sales By Date | Donut Chart
      ==================================
  */
  var options = {
    chart : {type : "donut", width : 450},
    colors : [
      "#5c1ac3", "#e2a03f", "#e7515a", "#8dbf42", "#2196f3", "#ffe1e2",
      "#25d5e4"
    ],
    dataLabels : {enabled : false},
    legend : {
      position : "bottom",
      horizontalAlign : "center",
      fontSize : "14px",
      markers : {width : 10, height : 10},
      itemMargin : {horizontal : 0, vertical : 8}
    },
    plotOptions : {
      pie : {
        donut : {
          size : "75%",
          background : "transparent",
          labels : {
            show : true,
            name : {
              show : true,
              fontSize : "16px",
              fontFamily : "Nunito, sans-serif",
              color : undefined,
              offsetY : -10
            },
            value : {
              show : true,
              fontSize : "26px",
              fontFamily : "Nunito, sans-serif",
              color : "#bfc9d4",
              offsetY : 16,
              formatter : function(
                  val) { return "$" + Math.round(val / 1000) + "k"; }
            },
            total : {
              show : true,
              showAlways : true,
              label : "Total",
              color : "#888ea8",
              formatter : function(w) {
                return ("$" + w.globals.seriesTotals.reduce(function(a, b) {
                  return Math.round((a + b) / 1000);
                }, 0) + "k");
              }
            }
          }
        }
      }
    },
    stroke : {show : true, width : 25, colors : "#0e1726"},
    series : Object.values(totalSales_weather),
    labels : Object.values(day_name),
    responsive : [ {
      // breakpoint: 1599,
      // options: {
      //     chart: {
      //         width: '350px',
      //         height: '400px'
      //     },
      //     legend: {
      //         position: 'bottom'
      //     }
      // },

      breakpoint : 1400,
      options : {
        chart : {width : "250px", height : "390px"},
        legend : {position : "bottom"},
        plotOptions : {pie : {donut : {size : "70%"}}}
      }
    } ]
  };

  /*
      ==============================
      |    @Render Charts Script    |
      ==============================
  */

  /*
      ================================
          Retail Sales | Predictions
      ================================
  */
  var chart1 = new ApexCharts(document.querySelector("#retailsales"), options1);

  chart1.render();

  /*
    =================================
        Sales By Date | Render
    =================================
*/
  var chart = new ApexCharts(document.querySelector("#chart-2"), options);

  chart.render();

  /*
      =============================================
          Perfect Scrollbar | Recent Activities
      =============================================
  */
  const ps = new PerfectScrollbar(document.querySelector(".mt-container"));
} catch (e) {
  console.log(e);
}
