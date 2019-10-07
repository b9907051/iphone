( function ( $ ) {
    "use strict";

    const Cellphone = Object.keys(Data)
      .filter(k => k !== 'Max_info' && k !== 'X_axis')
      .map(k => ({ [k]: Data[k] }));
    const MaxPrice = Data.MaxPrice;
    const X_axis = Data.X_axis;

    var borderColorArr = [brandSuccess,brandDanger,brandPrimary,brandyellow,brandblack]

    var data,time,dealnumber;

    data = Object.values(Cellphone).map((d, i) => ({
        // 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
        label: Object.keys(d)[0],
        backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
        // 這裡的i總共有幾個阿??
        borderColor: borderColorArr[i],
        pointHoverBackgroundColor: '#fff',
        borderWidth: 2,
        data: d[Object.keys(d)[0]].Price
    }))

    var myChart = new Chart( ctx, {
        type: 'line',
        data: {
          // 取出第一個Data的key
          labels: X_axis,
          datasets:data

        },
        options: {
            title: {
                display: true,
                text: '中關村銷售資訊',
                fontSize:20
            },

            maintainAspectRatio: true,
            legend: {
                display: true
            },
            responsive: true,
            scales: {
                xAxes: [{
                  ticks: {
                        autoSkip: false,
                        // maxRotation: 90,
                        minRotation: 60
                  },
                  gridLines: {
                    drawOnChartArea: false
                  },
                  type:'time',
                  time:{
                    unit:'week'
                  },
                  distribution: 'series'
                }],
                yAxes: [ {
                  scaleLabel: {
                        display: true,
                        labelString: '價格',
                        fontStyle:'bold'
                      },
                      ticks: {
                        beginAtZero: true,
                        maxTicksLimit: 5,
                        stepSize: 500,
                        max: MaxPrice
                      },
                      gridLines: {
                        display: true
                      }
                } ]
            },
            elements: {
                point: {
                  radius: 2,
                  hitRadius: 10,
                  hoverRadius: 4,
                  hoverBorderWidth: 3
              }
          }


        }
    } );
    // console.log(myChart)

})
( jQuery );